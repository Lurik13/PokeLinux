import pickle
from random import randint
from data.Knowledge.generations import GENERATIONS
from src.pokedle.utils import console_print
from src.pokedle.evolutions import try_evolutions
from src.generate_data.generate_files import get_gen_region
from src.utils import get_de_pokemon
from src.pokedle.colours import *
from src.pokedle.height_weight import try_height, try_weight
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

def try_types(types, mystery_types):
    result = [None, None]
    for i in range(2):
        if i == 1 and len(types) == 1:
            if len(mystery_types) == 1:
                result[1] = {'value': "Aucun", 'colour': GREEN}
            else:
                result[1] = {'value': "Aucun", 'colour': RED}
        else:
            if types[i] in mystery_types:
                result[i] = {'value': types[i], 'colour': GREEN}
            else:
                result[i] = {'value': types[i], 'colour': RED}
    return result

def get_centered_value(value, max_len, value_colour, lines_colour):
    number_of_spaces = max_len + 2 - len(value)
    left_spaces = number_of_spaces // 2
    right_spaces = number_of_spaces - left_spaces
    line = lines_colour + '│' + RESET
    return line + ' ' * left_spaces + value_colour + value + RESET + ' ' * right_spaces + line

def get_lines(is_top, max_len, colour):
    if is_top:
        return colour + '╭' + '─' * (max_len + 2) + '╮' + RESET
    return colour + '╰' + '─' * (max_len + 2) + '╯' + RESET

def display_result(result):
    static_data = [
        {'id': 'pokemon', 'max_len': 12, 'colour': result['pokemon']['colour']},
        {'id': 'first_type', 'max_len': 8, 'colour': result['first_type']['colour']},
        {'id': 'second_type', 'max_len': 8, 'colour': result['second_type']['colour']},
        {'id': 'evolution_stage', 'max_len': 1, 'colour': result['evolution_stage']['colour']},
        {'id': 'height', 'max_len': 6, 'colour': result['height']['colour']},
        {'id': 'weight', 'max_len': 9, 'colour': result['weight']['colour']},
    ]
    top_lines = ""
    for row in static_data:
        top_lines += get_lines(True, row['max_len'], row['colour'])
    print(top_lines)

    mid_rows = ""
    for row in static_data:
        mid_rows += get_centered_value(result[row['id']]['value'], row['max_len'], row['colour'], row['colour'])
    print(mid_rows)

    bottom_lines = ""
    for row in static_data:
        bottom_lines += get_lines(False, row['max_len'], row['colour'])
    print(bottom_lines)

    # ╔═╗║╚╝
    # print('╭─────────────╮╭───────────╮╭─────────────────╮')
    # print('│             ││   Jungle  ││  Terres arides  │')
    # print('│   Ville     ││   Forêt   ││     Grotte      │')
    # print('│             ││           ││      Ciel       │')
    # print('╰─────────────╯╰───────────╯╰─────────────────╯')


def pokedle(gen_number, cols, lines):
    gen_number = int(gen_number)
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    mystery_pokemon = POKEMON[randint(first_pokemon_id, last_pokemon_id)]
    print("Height:", mystery_pokemon['height'], "Weight:", mystery_pokemon['weight'])
    print(mystery_pokemon['french_name'] + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    console_print("Entrez le nom d'un pokémon")
    counter = 0
    while True:
        console_print("Pokémon : ", True)
        new_try = input().lower().replace("é", "e").replace("è", "e") #######
        counter += 1
        # else:
        pokemon_id_tried = find_pokemon_by_name(new_try, first_pokemon_id, last_pokemon_id)
        if pokemon_id_tried > 0:
            result = {}
            result['pokemon'] = {'value': POKEMON[pokemon_id_tried]['french_name'], 'colour': WHITE}
            tried_types = try_types(POKEMON[pokemon_id_tried]['types'], mystery_pokemon['types'])
            result['first_type'] = tried_types[0]
            result['second_type'] = tried_types[1]
            result['evolution_stage'] = try_evolutions(pokemon_id_tried, mystery_pokemon)
            result['height'] = try_height(POKEMON[pokemon_id_tried]['height'], mystery_pokemon['height'])
            result['weight'] = try_weight(POKEMON[pokemon_id_tried]['weight'], mystery_pokemon['weight'])
            display_result(result)
        elif pokemon_id_tried < 0:
            console_print(f"Les {new_try} ne vivent pas dans la région " + \
                f"{get_de_pokemon(get_gen_region(GENERATIONS[gen_number]['name']))} !", False, RED)
        else:
            console_print(f"Ce pokémon n'existe pas ou est mal ortographié.", False, RED)
        if new_try.lower() == mystery_pokemon['french_name'].lower().replace("é", "e").replace("è", "e"): #######
            console_print(f"\nBien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coup", True, GREEN)
            if counter != 1:
                console_print("s", True, GREEN)
            console_print(" !", False, GREEN)
            break
