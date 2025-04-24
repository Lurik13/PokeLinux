import pickle
import unicodedata
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
        if i == 5:
            first_pokemon_id += 1
        print(get_gen_region(GENERATIONS[i]['name']) + ":")
        for j in range(first_pokemon_id, first_pokemon_id + 9):
            print(get_pokemon_in_colour(POKEMON[j]['french_name'], POKEMON[j]['types']), end='', flush=True)
            if (j - first_pokemon_id +1) % 3 == 0:
                print("")
            elif j + 1 < first_pokemon_id + 9:
                print(" → ", end='', flush=True)
        print("")

def remove_accents(value):
    return ''.join(
            c for c in unicodedata.normalize('NFD', value)
            if unicodedata.category(c) != 'Mn')

def normalize(value):
    if isinstance(value, str):
        return remove_accents(value).lower()
    else:
        new_array = []
        for i in range(len(value)):
            new_value = remove_accents(value[i])
            new_array.append(new_value.lower())
        return new_array