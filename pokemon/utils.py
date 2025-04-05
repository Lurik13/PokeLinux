import requests # type: ignore

def get_data(type, value):
    url = f"https://pokeapi.co/api/v2/{type}/{value}/"
    return requests.get(url).json()

def get_french_name(pokemon_data):
    for name_entry in pokemon_data['names']:
        if name_entry["language"]["name"] == "fr":
            return name_entry["name"]
