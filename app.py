import hmac
import hashlib
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse

HMAC_PAYLOAD_KEYS = ["message", "key", "hash_func"]

app = Starlette(debug=True)


@app.route("/", methods=["GET"])
async def home(request):
    """Test endpoint."""
    return PlainTextResponse("Uplight HMAC API")


@app.route("/generate-token", methods=["POST"])
async def generate_hmac_token(request):
    """Generate an HMAC token given a key, message, and hash function."""

    def _valid_request_body(payload):
        keys = payload.keys()

        if len(keys) != 3:
            return False
        for key in keys:
            if key not in HMAC_PAYLOAD_KEYS or type(payload[key]) != str:
                return False
        return True

    try:
        data = await request.json()
    except Exception as e:
        response = {"message": "Unable to process payload"}
        return JSONResponse(response)

    if not _valid_request_body(data):
        response = {"message": "Invalid request payload"}
        return JSONResponse(response)

    try:
        secret_key = data["key"]
        message = data["message"]
        hash = data["hash_func"]

        if hash not in hashlib.algorithms_guaranteed:
            response = {
                "message": "Invalid hash function or hash function not supported"
            }
            return JSONResponse(response)

        signature = hmac.new(secret_key.encode(), message.encode(), hash)
        signature = signature.hexdigest()

        response = {
            "message": message,
            "signature": signature,
        }
    except Exception as e:
        response = {"message": "Unable to generate HMAC token"}
        return JSONResponse(response)

    return JSONResponse(response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
