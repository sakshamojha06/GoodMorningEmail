from secret_manager_service import get_openai_api_key
from openai_service import generate_fact

try:
    api_key = get_openai_api_key()
except Exception as error:
    print(f"Failed to retrive the API key: {error}")
    raise SystemExit(1)

fact = generate_fact(
    "Space",
    api_key
)

print("Generated fact:")
print(fact)