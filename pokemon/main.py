import sys
from evolution_chain import *
from utils import *
from weaknesses import *

SPRITE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"

TYPE_TRADUCTION = {
    "normal": "Normal",
    "fire": "Feu",
    "water": "Eau",
    "electric": "Électrik",
    "grass": "Plante",
    "ice": "Glace",
    "fighting": "Combat",
    "poison": "Poison",
    "ground": "Sol",
    "flying": "Vol",
    "psychic": "Psy",
    "bug": "Insecte",
    "rock": "Roche",
    "ghost": "Spectre",
    "dragon": "Dragon",
    "dark": "Ténèbres",
    "steel": "Acier",
    "fairy": "Fée"
}

FAIBLESSES = {
    "Normal": ["Combat"],
    "Feu": ["Eau", "Roche", "Sol"],
    "Eau": ["Électrik", "Plante"],
    "Électrik": ["Sol"],
    "Plante": ["Feu", "Glace", "Poison", "Vol", "Insecte"],
    "Glace": ["Feu", "Combat", "Roche", "Acier"],
    "Combat": ["Vol", "Psy", "Fée"],
    "Poison": ["Sol", "Psy"],
    "Sol": ["Eau", "Glace", "Plante"],
    "Vol": ["Électrik", "Glace", "Roche"],
    "Psy": ["Insecte", "Spectre", "Ténèbres"],
    "Insecte": ["Feu", "Vol", "Roche"],
    "Roche": ["Eau", "Plante", "Combat", "Sol", "Acier"],
    "Spectre": ["Spectre", "Ténèbres"],
    "Dragon": ["Glace", "Dragon", "Fée"],
    "Ténèbres": ["Combat", "Insecte", "Fée"],
    "Acier": ["Feu", "Combat", "Sol"],
    "Fée": ["Poison", "Acier"]
}

def get_pokemon(pokemon_id):
    pokemon = get_data(pokemon_id)
    species = get_data(pokemon_id, 'pokemon-species')
    
    evolutions = get_evolution_chain(species)
    number = pokemon["id"]
    name = pokemon["name"].capitalize()
    sprite = SPRITE_URL.format(number)
    # types = [TYPE_TRADUCTION[t["type"]["name"]] for t in poke["types"]]
    types = [t["type"]["name"] for t in pokemon["types"]]
    weaknesses = get_weaknesses(types)
    types = [TYPE_TRADUCTION[t] for t in types]
    return {
        "evolutions": evolutions if get_french_name(species) == evolutions[0] else None,
        "number": number,
        "englishName": name,
        "sprite": sprite,
        "types": types,
        "weaknesses": list(weaknesses)
    }

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('Veuillez renseigner le numéro d\'un pokémon entre 1 et 1000.')
        arg = sys.argv[1]
        if not arg.isnumeric():
            raise ValueError(f"'{arg}' n'est pas le numéro d'un pokémon entre 1 et 1000.")
        pokemon = get_pokemon(arg)
        for key, value in pokemon.items():
            print(key, ":", value)
    except ValueError as ve:
        print(ve)

main()
