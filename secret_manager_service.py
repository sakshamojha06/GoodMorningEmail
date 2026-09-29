import os
import base64
import subprocess
import requests

from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key():

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    secret_id = os.getenv("GOOGLE_SECRET_ID")
    secret_version = os.getenv("GOOGLE_SECRET_VERSION")
    gcloud_path = os.getenv("GOOGLE_CLOUD_SDK_PATH")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID is missing")

    if not secret_id:
        raise ValueError("GOOGLE_SECRET_ID is missing")

    if not secret_version:
        raise ValueError("GOOGLE_SECRET_VERSION is missing")

    access_token = subprocess.check_output(
        [gcloud_path, "auth", "print-access-token"],
        text=True
    ).strip()

    url = (
        "https://secretmanager.googleapis.com/v1/"
        f"projects/{project_id}/secrets/{secret_id}/"
        f"versions/{secret_version}:access"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    encoded_secret = data["payload"]["data"]

    decoded_secret = base64.b64decode(
        encoded_secret
    ).decode("UTF-8")

    return decoded_secret

# if __name__ == "__main__":

#     api_key = get_openai_api_key()

#     print("Secret retrieved successfully")
#     print("Key length:", len(api_key))