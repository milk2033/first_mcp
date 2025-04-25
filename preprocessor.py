# preprocessor.py

import requests

# first use client_query prompt, then use the
# preprocessed prompt here and hit mcp_api_server

PREPROCESSOR_MODEL_URL = (
    "http://localhost:5005/generate"  # Adjust if using OpenAI or other backend
)


def build_prompt(user_query):
    return f"""
You are an AI assistant that rewrites vague natural-language questions into clear and explicit instructions suitable for generating Python functions.

Each Pokémon is a dictionary with:
{{ "name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/" }}

Rephrase the user's query into a precise instruction for working with this list.

### Examples

User: Which Pokémon have 'a' in the name?
Rephrased: Return a list of Pokémon names that contain the letter 'a'.

User: Give me the last one
Rephrased: Return the last Pokémon in the list.

User: How many have names starting with 's'?
Rephrased: Return the number of Pokémon whose names start with the letter 's'.

User: Show all URLs
Rephrased: Return a list of URLs for all Pokémon in the list.

With these examples in mind, now rephrase the following user query:

User: {user_query}
Rephrased:""".strip()


def preprocess_query(user_query):
    print("preprocessing now....")

    prompt = build_prompt(user_query)
    try:
        response = requests.post(
            PREPROCESSOR_MODEL_URL,
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        result = response.json().get("result", "").strip()
        print("/////////////RESULT//////////")
        print(result)
        print("/////////////////////////////")
        # return result
    except Exception as e:
        print("❌ Error preprocessing query:", e)
        return user_query  # Fallback to original if preprocessing fails


if __name__ == "__main__":
    # Example usage
    user_input = input("Enter your Pokémon question: ")
    refined = preprocess_query(user_input)
    print("\n🧠 Refined Query:", refined)
