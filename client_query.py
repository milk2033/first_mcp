import requests
import json
from mcp_execute_pipeline import run_pipeline
from pokemon import get_all
from preprocessor import preprocess_query

pokemon_list = get_all()


def send_query():
    print("Welcome to the Pokémon MCP assistant!")

    # preprocessing below. seems to be working OK
    # didn't continue with it because it takes too long to wait for prompts
    # user_query = "Return all of the pokemon in alphabetical order"
    # built_prompt = preprocess_query(user_query)

    # Hardcoded for now – you can swap this with input() if you want interactivity
    # another note in case of issues with prompts - Yes — exactly. That's a
    # very effective strategy.
    # You're describing a common technique called query rewriting or query
    # preprocessing, and it's used all the time in production LLM systems to
    # improve reliability.
    # https://chatgpt.com/share/680a3a40-786c-8005-a7b6-dc9aeef4311e
    user_query = "Return all of the pokemon in alphabetical order"
    response = requests.post(
        "http://localhost:8000/query",
        json={"query": user_query},
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        data = response.json()
        # print("\n--- LLM Output ---\n")
        # print(data["response"])
        return data["response"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    query_result = send_query()
    print("//// QUERY RESULT ////")
    print(query_result)
    print("///////////END QUERY RESULT////////////")

    pipeline_result = run_pipeline(query_result, pokemon_list)
    print("run_pipeline finished")
