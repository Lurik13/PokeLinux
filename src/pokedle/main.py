import pickle
from random import randint
from data.Knowledge.generations import GENERATIONS
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)


# penser à faire une fonction qui regarde le nom de pokémon le plus proche #####################

def find_pokemon_by_name(name):
    for key, data in POKEMON.items():
        if data["french_name"].lower() == name.lower():
            return key
    return 0

GRAY = "\033[38;2;150;150;150;1m"
GREEN = "\033[38;2;50;200;50m"
RED = "\033[38;2;200;50;50m"
RESET = "\033[0m"

def console_print(message, should_flush = False, color = GRAY):
    if should_flush:
        print(color + message + RESET, end='', flush=should_flush)
    else:
        print(color + message + RESET)

def pokedle(gen_number):
    gen_number = int(gen_number)
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    mystery_pokemon = POKEMON[randint(first_pokemon_id, last_pokemon_id)]
    print(mystery_pokemon['french_name'])
    console_print("Entrez le nom d'un pokémon")
    counter = 0
    while True:
        console_print("Pokémon : ", True)
        new_try = input()
        counter += 1
        if new_try.lower() == mystery_pokemon['french_name'].lower():
            console_print(f"Bien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coup", True, GREEN)
            if counter != 1:
                console_print("s", True, GREEN)
            console_print(" !", False, GREEN)
            break
        else:
            pokemon_id_tried = find_pokemon_by_name(new_try)
            if pokemon_id_tried:
                console_print("On a trouvé " + POKEMON[pokemon_id_tried]['french_name'])
                types_tried = POKEMON[pokemon_id_tried]['types']
                for i in range(2):
                    console_print("Type " + str(i + 1) + " : ", True)
                    if i == 1 and len(types_tried) == 1:
                        if len(mystery_pokemon['types']) == 1:
                            console_print("Aucun", False, GREEN)
                        else:
                            console_print("Aucun", False, RED)
                    else:
                        if types_tried[i] in mystery_pokemon['types']:
                            console_print(types_tried[i], False, GREEN)
                        else:
                            console_print(types_tried[i], False, RED)
#             else:
            console_print("Incorrect !")
