import pickle
from random import randint
from data.Knowledge.generations import GENERATIONS
from src.pokedle.display import display_caption, display_table
from src.pokedle.utils import *
from src.generate_data.generate_files import get_gen_region
from src.utils import get_de_pokemon
from src.pokedle.input import *
from prompt_toolkit import prompt # type: ignore
from prompt_toolkit.shortcuts import clear # type: ignore
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

# penser à faire une fonction qui regarde le nom de pokémon le plus proche #####################

def find_pokemon_by_name(name):
    new_mystery_name = normalize(name)
    for key, data in POKEMON.items():
        new_data_name = normalize(data["french_name"])
        if new_data_name == new_mystery_name:
            return key
    return 0

def is_correct_generation(try_id, first_pokemon_id, last_pokemon_id):
    if try_id < first_pokemon_id or try_id > last_pokemon_id:
        return False
    return True

def pokedle(gen_number, cols, lines):
    gen_number = int(gen_number)
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    mystery_pokemon = POKEMON[randint(first_pokemon_id, last_pokemon_id)]
    clear()
    print(mystery_pokemon['french_name'])
    display_caption()
    counter = 0
    remaining_pokemon_names = get_completer_array(first_pokemon_id, last_pokemon_id)
    number_of_lines_to_clear = 1
    while True:
        completer = AccentInsensitiveCompleter(remaining_pokemon_names)
        new_try = prompt("Pokémon : ", completer=completer, complete_while_typing=True)
        clear_lines(number_of_lines_to_clear)
        number_of_lines_to_clear = 1
        pokemon_id_tried = find_pokemon_by_name(new_try)
        if not pokemon_id_tried:
            console_print(f"Ce pokémon n'existe pas ou est mal ortographié.", False, RED)
            number_of_lines_to_clear += 1
        else:
            counter += 1
            if is_correct_generation(pokemon_id_tried, first_pokemon_id, last_pokemon_id):
                if normalize(new_try) in normalize(remaining_pokemon_names):
                    remaining_pokemon_names.remove(POKEMON[pokemon_id_tried]['french_name'])
                    display_table(pokemon_id_tried, mystery_pokemon)
                    if normalize(new_try) == normalize(mystery_pokemon['french_name']):
                        console_print(f"Bien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coup", True, GREEN)
                        if counter != 1:
                            console_print("s", True, GREEN)
                        console_print(" !", False, GREEN)
                        break
                else:
                    console_print(f"Tu as déjà tenté avec {POKEMON[pokemon_id_tried]['french_name']} et ça n'a pas marché...", False, RED)
                    number_of_lines_to_clear += 1
            else:
                console_print(f"Les {POKEMON[pokemon_id_tried]['french_name']} ne proviennent pas de la région " + \
                    f"{get_de_pokemon(get_gen_region(GENERATIONS[gen_number]['name']))} !", False, RED)
                number_of_lines_to_clear += 1

