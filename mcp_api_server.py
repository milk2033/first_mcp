import json
import requests
import time
from flask import Flask, request, jsonify
from pokemon import get_all

app = Flask(__name__)
pokemon_list = get_all()

MODEL_SERVER_URL = "http://localhost:5005/generate"


@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    user_query = data.get("query", "How many Pokémon names are there?")

    # Build prompt dynamically (this is hot-reloadable!)
    preview = pokemon_list[:10]
    preview_json = json.dumps(preview, indent=2)

    prompt = f"""You are a Python code assistant. You are given:

- A user query about Pokémon.
- A list of Pokémon dictionaries, each with a 'name' and 'url' field.
- A preview of the list:

{preview_json}

You must write a complete Python function named `analyze_pokemon_list`, which accepts `pokemon_list`.

Output format:

1. Output **only** the function definition, including the `def analyze_pokemon_list(pokemon_list):` header.
2. Do **not** include comments, explanations, usage examples, or return values after the function.
3. Do not include any markdown formatting (no triple backticks).
4. Do not include `print()` statements.
5. Do not define any decorators.
6. Do not use additional arguments beyond `pokemon_list`.



User query: "{user_query}"

"""

    # Now return only the complete python function, strictly adhering to rules 1-7 stated above.
    # Do not make any extra comments, only the full function and its contents.

    # === Measure full round-trip time ===
    start = time.time()
    response = requests.post(MODEL_SERVER_URL, json={"prompt": prompt})
    duration = time.time() - start
    print(f"⏱️ Total round-trip time: {duration:.2f} seconds")

    if response.status_code == 200:
        result = response.json().get("result", "")
        return jsonify({"response": result})
    else:
        return jsonify({"error": "Model server error"}), 500


if __name__ == "__main__":
    app.run(port=8000, debug=True, use_reloader=True)
