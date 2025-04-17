import pickle
from data.Knowledge.evolutions import EVOLUTIONS
from src.pokedle.utils import console_print
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)
GRAY = "\033[38;2;150;150;150;1m"
GREEN = "\033[38;2;50;200;50m"
BLUE = "\033[38;2;0;100;200m"
RED = "\033[38;2;200;50;50m"
RESET = "\033[0m"

def get_evolution_index(evolution_chain, pokemon_name, evolution_number = 0):
    for i in range(len(evolution_chain)):
        if isinstance(evolution_chain[i], str):
            if evolution_chain[i] == pokemon_name:
                return i + evolution_number + 1
        else:
            found = 0
            original_index = i
            while found == 0:
                found = get_evolution_index(evolution_chain[i], pokemon_name, original_index)
                i += 1
            if found:
                return found
    return 0

def get_evolution_stage(pokemon_id):
    first_evolution_id = int(POKEMON[pokemon_id]['evolution_chain'][0]['id'])
    if isinstance(EVOLUTIONS[first_evolution_id][0], list):
        return get_evolution_index(EVOLUTIONS[first_evolution_id][0], POKEMON[pokemon_id]['french_name'])
    else:
        return get_evolution_index(EVOLUTIONS[first_evolution_id], POKEMON[pokemon_id]['french_name'])
    
def try_evolutions(pokemon_id_tried, mystery_pokemon):
    console_print("Stade d'évolution : ", True, GRAY)
    try_evolution_stage = get_evolution_stage(pokemon_id_tried)
    if (try_evolution_stage == get_evolution_stage(int(mystery_pokemon['number']))):
        console_print(str(try_evolution_stage), False, GREEN)
    else:
        console_print(str(try_evolution_stage), False, RED)
