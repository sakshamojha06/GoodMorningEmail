from openai import OpenAI

def generate_fact(topic, api_key):

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
    Generate exactly one interesting and accurate fact about {topic}.

    Requirements:
    - 2 to 4 sentences maximum.
    - Suitable for a daily morning email.
    - Easy to understand.
    - Do not mention that you are an AI.
    - Return only the fact.
"""
    )

    return response.output_text