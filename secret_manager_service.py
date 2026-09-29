import base64
import json
import os
import time

import jwt
import requests
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

    if not service_account_file:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_FILE is missing in .env")

    with open(service_account_file, "r") as file:
        service_account = json.loads(file.read())

    client_email = service_account["client_email"]
    private_key = service_account["private_key"]
    token_uri = service_account["token_uri"]

    now = int(time.time())

    payload = {
        "iss": client_email,
        "scope": "https://www.googleapis.com/auth/cloud-platform",
        "aud": token_uri,
        "iat": now,
        "exp": now + 3600,
    }

    signed_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    response = requests.post(
        token_uri,
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": signed_jwt,
        },
    )

    response.raise_for_status()
    data = response.json()

    return data["access_token"]


def get_openai_api_key():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    secret_id = os.getenv("GOOGLE_SECRET_ID")
    secret_version = os.getenv("GOOGLE_SECRET_VERSION")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID is missing")

    if not secret_id:
        raise ValueError("GOOGLE_SECRET_ID is missing")

    if not secret_version:
        raise ValueError("GOOGLE_SECRET_VERSION is missing")

    access_token = get_access_token()

    url = (
        f"https://secretmanager.googleapis.com/v1/"
        f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}:access"
    )

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    encoded_secret = data["payload"]["data"]
    decoded_secret = base64.b64decode(encoded_secret).decode("UTF-8")

    return decoded_secret


if __name__ == "__main__":
    try:
        api_key = get_openai_api_key()
        print("✅ Secret retrieved successfully")
        print("Key length:", len(api_key))
    except Exception as e:
        print("❌ Error:", e)