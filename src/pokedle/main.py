import pickle
from random import randint
from data.Knowledge.generations import GENERATIONS
from src.pokedle.utils import console_print
from src.pokedle.evolutions import try_evolutions
from src.generate_data.generate_files import get_gen_region
from src.utils import get_de_pokemon
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)


# penser à faire une fonction qui regarde le nom de pokémon le plus proche #####################

def find_pokemon_by_name(name, first_pokemon_id, last_pokemon_id):
    new_mystery_name = name.lower().replace("é", "e").replace("è", "e") #######
    for key, data in POKEMON.items():
        new_data_name = data["french_name"].lower().replace("é", "e").replace("è", "e") #######
        if new_data_name == new_mystery_name:
            if key < first_pokemon_id or key > last_pokemon_id:
                return -1
            return key
    return 0

GRAY = "\033[38;2;150;150;150;1m"
GREEN = "\033[38;2;50;200;50m"
BLUE = "\033[38;2;0;100;200m"
RED = "\033[38;2;200;50;50m"
RESET = "\033[0m"

def try_types(types, mystery_types):
    for i in range(2):
        console_print("Type " + str(i + 1) + " : ", True)
        if i == 1 and len(types) == 1:
            if len(mystery_types) == 1:
                console_print("Aucun", True, GREEN)
            else:
                console_print("Aucun", True, RED)
        else:
            if types[i] in mystery_types:
                console_print(types[i], True, GREEN)
            else:
                console_print(types[i], True, RED)
        console_print("  |  ", True, GRAY)



def pokedle(gen_number):
    gen_number = int(gen_number)
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    mystery_pokemon = POKEMON[randint(first_pokemon_id, last_pokemon_id)]
    print(mystery_pokemon['french_name'] + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    console_print("Entrez le nom d'un pokémon")
    counter = 0
    while True:
        console_print("Pokémon : ", True)
        new_try = input().lower().replace("é", "e").replace("è", "e") #######
        counter += 1
        if new_try.lower() == mystery_pokemon['french_name'].lower().replace("é", "e").replace("è", "e"): #######
            console_print(f"Bien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coup", True, GREEN)
            if counter != 1:
                console_print("s", True, GREEN)
            console_print(" !", False, GREEN)
            break
        else:
            pokemon_id_tried = find_pokemon_by_name(new_try, first_pokemon_id, last_pokemon_id)
            if pokemon_id_tried > 0:
                try_types(POKEMON[pokemon_id_tried]['types'], mystery_pokemon['types'])
                try_evolutions(pokemon_id_tried, mystery_pokemon)
            elif pokemon_id_tried < 0:
                console_print(f"Les {new_try} ne vivent pas dans la région " + \
                    f"{get_de_pokemon(get_gen_region(GENERATIONS[gen_number]['name']))} !", False, RED)
            else:
                console_print(f"Ce pokémon n'existe pas ou est mal ortographié.", False, RED)
