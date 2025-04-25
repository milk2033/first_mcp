import requests
import time
from dataclasses import dataclass
from typing import Optional, List


def get_all():
    # returns all pokemon
    url = f"https://pokeapi.co/api/v2/pokemon?limit=1000000&offset=0"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"didn't work")

    data = response.json()
    pokemon_list = data["results"][0:80]
    return pokemon_list
    # def get_pokemon_names_starting(pokemon_list):
    #     list = [
    #         pokemon["name"]
    #         for pokemon in pokemon_list
    #         if pokemon["name"].startswith("w")
    #     ]
    #     count = len(list)

    # get_pokemon_names_starting(test)
    # # for i in data["results"]:
    # #     count += 1
    # #     print(i["name"])
    # return data["results"][0:50]


def testing():
    url = f"https://pokeapi.co/api/v2/pokemon?limit=1000000&offset=0"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"didn't work")

    data = response.json()
    pokemon_list = data["results"][0:80]
    # count = 0
    # for name in sorted(p["name"] for p in pokemon_list):
    #     count += 1
    # print(count)

    # count = 0
    # for pokemon in pokemon_list:
    #     name = pokemon["name"].lower()
    #     if name.startswith("c") or name.startswith("c"):
    #         count += 1
    count = 0
    for pokemon in pokemon_list:
        if len(pokemon["name"]) > 8:
            count += 1

    return count


if __name__ == "__main__":

    # get list of all pokemons
    data = get_all()
    test = testing()
    print(data)
    print(test)

    # "What is the name of the first Pokémon in the list?"
    # Simple list indexing.

    # "What is the URL of the last Pokémon?"
    # Accessing dictionary fields and using negative indexing.

    # "How many Pokémon have names that start with the letter 'c'?"
    # String filtering and counting.

    # "How many Pokémon names are longer than 8 characters?"
    # String length logic.

    # "Find all Pokémon whose name contains the word 'saur'."
    # Substring match.

    # "Which Pokémon names contain both the letters 'a' and 'r'?"
    # Multiple condition checks.

    # "Return a list of all Pokémon names sorted alphabetically."
    # Extracting and sorting.

    # "Return all Pokémon names in uppercase."
    # Transformation logic.

    # "Show me the names of the first 5 Pokémon."
    # List slicing and formatting.

    # "Return a list of Pokémon whose names start with a vowel."
    # Set-based matching against vowels.
