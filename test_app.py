import pytest
from starlette.testclient import TestClient
from app import app

client = TestClient(app)


class TestHome:
    def test_home(self):

        response = client.get("/")
        assert response.status_code == 200
        assert response.text == "Uplight HMAC API"


class TestHMACToken:
    def test_generate_hmac_token(self):

        data = {
            "message": "Apiary: a place where bees and beehives are kept, especially a place where bees are raised "
            "for "
            "their honey.",
            "key": "supersecretkey",
            "hash_func": "sha256",
        }
        response = client.post("/generate-token", json=data)
        assert response.json() == {
            "message": "Apiary: a place where bees and beehives are kept, especially a place where bees are raised "
            "for "
            "their honey.",
            "signature": "eca6d60230fa860ce475bcb4382bd7c9ab675bb8bf085a51b7ec7e8ae43c3295",
        }

        data = {
            "message": "Hello World!",
            "key": "anothersupersecretkey",
            "hash_func": "md5",
        }
        response = client.post("/generate-token", json=data)
        assert response.json() == {
            "message": "Hello World!",
            "signature": "973eaabafa612fe31aee662ba88c853b",
        }

    def test_generate_hmac_token_with_no_payload(self):

        response = client.post("/generate-token")
        assert response.json() == {"message": "Unable to process payload"}

    def test_generate_hmac_token_with_non_json_payload(self):

        response = client.post("/generate-token", data="non-json-payload")
        assert response.json() == {"message": "Unable to process payload"}

    def test_generate_hmac_token_with_invalid_payload(self):

        response = client.post("/generate-token", json={"id": 4})
        assert response.json() == {"message": "Invalid request payload"}

        response = client.post(
            "/generate-token", json={"message": "msg", "key": 12, "hash_func": "sha256"}
        )
        assert response.json() == {"message": "Invalid request payload"}

    def test_generate_hmac_token_with_invalid_hash(self):

        response = client.post(
            "/generate-token",
            json={"message": "msg", "key": "secretkey", "hash_func": "sha-256"},
        )
        assert response.json() == {
            "message": "Invalid hash function or hash function not supported"
        }
