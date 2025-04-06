from utils import *
from weaknesses import *
from forms import *

def get_pokemon(pokemon_id):
    pokemon = get_data('pokemon', pokemon_id)
    species = get_data('pokemon-species', pokemon_id)
    number = pokemon["id"]
    french_name = get_french_name(species)
    types = [t["type"]["name"] for t in pokemon["types"]]
    weaknesses = get_weaknesses(types)

    return {
        "number": number,
        "english_name": pokemon["name"].capitalize(),
        "french_name": french_name,
        "sprite": SPRITE_URL.format(number),
        "types": [TYPE_TRANSLATION[t] for t in types],
        "weaknesses": list(weaknesses),
        "forms": get_forms(species),
    }

pokemon = get_pokemon(6)
for key, value in pokemon.items():
    if key == 'forms':
        if value:
            print("forms :")
            for form in value:
                print("   ", form['form_french_name'])
                print("      ", form['sprite'])
                if form['types'] is not None:
                    print("      ", form['types'])
                    print("      ", form['weaknesses'])
    else:
        print(key, ":", value)
