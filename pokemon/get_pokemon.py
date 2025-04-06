from pokemon.utils import *
from pokemon.weaknesses import *
from pokemon.forms import *

def get_pokemon(pokemon_id):
    pokemon = get_data('pokemon', pokemon_id)
    species = get_data('pokemon-species', pokemon_id)
    number = pokemon["id"]
    french_name = get_french_name(species)
    types = [t["type"]["name"] for t in pokemon["types"]]
    weaknesses = get_weaknesses(types)

    return {
        "number": f"{number:04}" ,
        "english_name": pokemon["name"].capitalize(),
        "french_name": french_name,
        "sprite": SPRITE_URL.format(number),
        "types": [TYPE_TRANSLATION[t] for t in types],
        "weaknesses": list(weaknesses),
        "forms": get_forms(species),
    }
