import pickle
from random import randint
import unicodedata
from data.Knowledge.generations import GENERATIONS
from data.Knowledge.colours import COLOURS
from data.Knowledge.habitats import HABITATS
from src.pokedle.utils import console_print
from src.pokedle.evolutions import try_evolutions
from src.generate_data.generate_files import get_gen_region
from src.utils import get_de_pokemon
from src.pokedle.colours import *
from src.pokedle.height_weight import try_height, try_weight
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)


# penser à faire une fonction qui regarde le nom de pokémon le plus proche #####################

def normalize(name):
    new_name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    return new_name.lower()

def find_pokemon_by_name(name, first_pokemon_id, last_pokemon_id):
    new_mystery_name = normalize(name)
    for key, data in POKEMON.items():
        new_data_name = normalize(data["french_name"])
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

def try_colours(try_colours, mystery_colours):
    correct_colours = 0
    for colour in try_colours:
        if colour in mystery_colours:
            correct_colours += 1
    if correct_colours == len(mystery_colours) == len(try_colours):
        return {'value': try_colours, 'colour': GREEN}
    elif correct_colours:
        return {'value': try_colours, 'colour': ORANGE}
    return {'value': try_colours, 'colour': RED}

def try_habitats(try_habitats, mystery_habitats):
    correct_habitats = 0
    text_colours = []
    for colour in try_habitats:
        if colour in mystery_habitats:
            correct_habitats += 1
            text_colours.append(GREEN)
        else:
            text_colours.append(RED)
    if correct_habitats == len(mystery_habitats) == len(try_habitats):
        return {'value': try_habitats, 'text_colours': text_colours, 'line_colour': GREEN}
    elif correct_habitats:
        return {'value': try_habitats, 'text_colours': text_colours, 'line_colour': ORANGE}
    return {'value': try_habitats, 'text_colours': text_colours, 'line_colour': RED}

def get_centered_value(value, max_len, value_colour, lines_colour):
    if isinstance(value, list):
        list_to_string = ""
        for values in value:
            list_to_string += values + ", "
        number_of_spaces = max_len + 2 - len(list_to_string[:-2])
    else:
        number_of_spaces = max_len + 2 - len(value)
    left_spaces = number_of_spaces // 2
    right_spaces = number_of_spaces - left_spaces
    line = lines_colour + '│' + RESET
    if isinstance(value, str):
        return line + ' ' * left_spaces + value_colour + value + RESET + ' ' * right_spaces + line
    else:
        if isinstance(value_colour, str):
            return line + ' ' * left_spaces + value_colour + list_to_string[:-2] + RESET + ' ' * right_spaces + line
        else:
            result = line + ' ' * left_spaces
            for i in range(len(value)):
                result += value_colour[i] + value[i] + RESET
                if i + 1 < len(value):
                    result += lines_colour + ', ' + RESET
            result += ' ' * right_spaces + line
            return result

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
    dynamic_data = [
        {'id': 'colours', 'max_len': 14},
        {'id': 'habitats', 'max_len': 32},
    ]

    top_lines = ""
    for row in static_data:
        top_lines += get_lines(True, row['max_len'], row['colour'])
    top_lines += get_lines(True, dynamic_data[0]['max_len'], result['colours']['colour'])
    top_lines += get_lines(True, dynamic_data[1]['max_len'], result['habitats']['line_colour'])
    print(top_lines)

    mid_rows = ""
    for row in static_data:
        mid_rows += get_centered_value(result[row['id']]['value'], row['max_len'], row['colour'], row['colour'])
    mid_rows += get_centered_value(result['colours']['value'], dynamic_data[0]['max_len'], result['colours']['colour'], result['colours']['colour']) ###
    mid_rows += get_centered_value(result['habitats']['value'], dynamic_data[1]['max_len'], result['habitats']['text_colours'], result['habitats']['line_colour']) ###
    print(mid_rows)

    bottom_lines = ""
    for row in static_data:
        bottom_lines += get_lines(False, row['max_len'], row['colour'])
    bottom_lines += get_lines(False, dynamic_data[0]['max_len'], result['colours']['colour'])
    bottom_lines += get_lines(False, dynamic_data[1]['max_len'], result['habitats']['line_colour'])
    print(bottom_lines)
    # ╔═╗║╚╝


def pokedle(gen_number, cols, lines):
    gen_number = int(gen_number)
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    mystery_pokemon = POKEMON[randint(first_pokemon_id, last_pokemon_id)]
    print(mystery_pokemon['french_name'] + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    console_print("Entrez le nom d'un pokémon")
    counter = 0
    while True:
        console_print("Pokémon : ", True)
        new_try = normalize(input())
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
            result['colours'] = try_colours(COLOURS[pokemon_id_tried], COLOURS[int(mystery_pokemon['number'])])
            result['habitats'] = try_habitats(HABITATS[pokemon_id_tried], HABITATS[int(mystery_pokemon['number'])])
            display_result(result)
        elif pokemon_id_tried < 0:
            console_print(f"Les {new_try} ne vivent pas dans la région " + \
                f"{get_de_pokemon(get_gen_region(GENERATIONS[gen_number]['name']))} !", False, RED)
        else:
            console_print(f"Ce pokémon n'existe pas ou est mal ortographié.", False, RED)
        if new_try == normalize(mystery_pokemon['french_name']):
            console_print(f"\nBien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coup", True, GREEN)
            if counter != 1:
                console_print("s", True, GREEN)
            console_print(" !", False, GREEN)
            break
