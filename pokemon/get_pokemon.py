from evolution_chain import *
from utils import *
from weaknesses import *

def get_pokemon(pokemon_id):
    pokemon = get_data('pokemon', pokemon_id)
    species = get_data('pokemon-species', pokemon_id)
    
    evolutions = get_evolution_chain(species)
    number = pokemon["id"]
    french_name = get_french_name(species)
    types = [t["type"]["name"] for t in pokemon["types"]]
    weaknesses = get_weaknesses(types)

    return {
        "evolutions": evolutions if french_name == evolutions[0] else None,
        "number": number,
        "english_name": pokemon["name"].capitalize(),
        "french_name": french_name,
        "sprite": SPRITE_URL.format(number),
        "types": [TYPE_TRANSLATION[t] for t in types],
        "weaknesses": list(weaknesses)
    }

pokemon = get_pokemon(103)
for key, value in pokemon.items():
    print(key, ":", value)
    