import pickle
from src.generate_data.generate_files import get_gen_region
from src.anki.print import get_pokemon_in_colour
from data.Knowledge.generations import GENERATIONS
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

def get_de_pokemon(name):
    if name[0].lower() in ('a', 'e', 'i', 'o', 'u'):
        return "d'" + name
    return "de " + name

def get_starters():
    for i in range(1, len(GENERATIONS) + 1):
        first_pokemon_id = GENERATIONS[i]['pokemon_range'][0]
        print(get_gen_region(GENERATIONS[i]['name']) + ":")
        for j in range(first_pokemon_id, first_pokemon_id + 9):
            print(get_pokemon_in_colour(POKEMON[j]['french_name'], POKEMON[j]['types']), end='', flush=True)
            if (j - first_pokemon_id +1) % 3 == 0:
                print("")
            elif j + 1 < first_pokemon_id + 9:
                print(" → ", end='', flush=True)
        print("")