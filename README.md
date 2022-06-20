# Uplight HMAC API

## Introduction
This API generates an HMAC token when given a message and a secret key. This API was built using [starlette](https://www.starlette.io/) and makes use of Python's [HMAC](https://docs.python.org/3/library/hmac.html#module-hmac) and [hashlib](https://docs.python.org/3/library/hashlib.html) libraries to generate the tokens. The [pytest](https://docs.pytest.org/en/7.1.x/) framework was used to test this API.  
## Installation

Clone the repository:
``` 
$ git clone https://github.com/shraddhashah1/uplight-hmac-api.git
$ cd uplight-hmac-api
```
Install the requirements:
``` 
$ pip3 install -r requirements.txt
```

Start the app:
```
$ python3 app.py
```

The app will run at http://localhost:8080. To check if the app is running: 
```
$ curl http://127.0.0.1:8080/

Uplight HMAC API
``` 
## Usage

To generate an HMAC token, the following will need to be provided to the API:
1) A message
2) A secret key
3) A hash function

Note: The hash functions supported by this API include:
``` 
{'sha1', 'md5', 'sha3_384', 'sha384', 'sha3_512', 'shake_256', 'blake2s', 'shake_128', 'sha512', 'sha3_256', 'sha224', 'blake2b', 'sha3_224', 'sha256'}
```

Simply `POST` the data to the `/generate-token` endpoint as shown below:
```
$ curl --request POST --url http://127.0.0.1:8080/generate-token -H 'Content-Type: application/json' --data '{"message"
: "your-message", "key": "your-secret-key", "hash_func": "a-hash-function"}'
```
If the request is processed successfully, you will receive a response like this:
``` 
{"message":"your-message","signature":"hmac-token"}
```

Otherwise you will receive an error message:

Here is an example of a successful request and it's corresponding response:

``` 
$ curl --request POST --url http://127.0.0.1:8080/generate-token -H 'Content-Type: application/json' --data '{"message"
: "Hello World!", "key": "supersecretkey", "hash_func": "sha256"}'

{"message":"Hello World!","signature":"091ba07212a35a347c5983c0b4a628ddb59cfd540a0a770560b5d5f6d307675e"}
```

## Testing

To run the tests, run:
```
$ pytest
```