import pickle
from src.pokedle.utils import *
from pokedle.try_evolutions import try_evolutions
from pokedle.try_height_weight import try_height, try_weight
from src.pokedle.try_generation import try_generation
from src.pokedle.try_pokemon import try_pokemon
from pokedle.try_others import *
from data.Knowledge.colours import COLOURS
from data.Knowledge.habitats import HABITATS
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

DATA = [
    {'id': 'pokemon', 'max_len': 12},
    {'id': 'first_type', 'max_len': 8},
    {'id': 'second_type', 'max_len': 8},
    {'id': 'evolution_stage', 'max_len': 1},
    {'id': 'height', 'max_len': 6},
    {'id': 'weight', 'max_len': 9},
    {'id': 'colours', 'max_len': 14},
    {'id': 'habitats', 'max_len': 32},
    {'id': 'generation', 'max_len': 3},
]
CATEGORIES = ["POKÉMON", "TYPE 1", "TYPE 2", "ÉV.", "TAILLE", "POIDS", "COULEURS", "HABITATS", "GÉN"]


def get_centered_value(value, max_len, value_colour, lines_colour, line = '│'):
    if isinstance(value, list):
        list_to_string = ""
        for values in value:
            list_to_string += values + ", "
        number_of_spaces = max_len + 2 - len(list_to_string[:-2])
    else:
        number_of_spaces = max_len + 2 - len(value)
    left_spaces = number_of_spaces // 2
    right_spaces = number_of_spaces - left_spaces
    line = lines_colour + line + RESET
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

def get_lines(lines, max_len, colour):
    return colour + lines[0] + lines[1] * (max_len + 2) + lines[2] + RESET

def display_caption(cols, lines):
    number_of_spaces = calculate_number_of_spaces(cols)
    top_caption = ""
    for row in DATA:
        top_caption += get_lines("╔═╗", row['max_len'], WHITE)
    print(" " * number_of_spaces + top_caption)
    mid_caption = ""
    for i in range(len(CATEGORIES)):
        mid_caption += get_centered_value(CATEGORIES[i], DATA[i]['max_len'], WHITE, WHITE, '║')
    print(" " * number_of_spaces + mid_caption)
    bottom_caption = ""
    for row in DATA:
        bottom_caption += get_lines("╚═╝", row['max_len'], WHITE)
    print(" " * number_of_spaces + bottom_caption)

def display_row(result, cols, lines):
    number_of_spaces = calculate_number_of_spaces(cols)
    top_lines = ""
    for row in DATA:
        if 'colour' in result[row['id']]:
            top_lines += get_lines("╭─╮", row['max_len'], result[row['id']]['colour'])
        else:
            top_lines += get_lines("╭─╮", row['max_len'], result[row['id']]['line_colour'])
    print(" " * number_of_spaces + top_lines)
    mid_rows = ""
    for row in DATA:
        if 'colour' in result[row['id']]:
            mid_rows += get_centered_value(result[row['id']]['value'], row['max_len'], result[row['id']]['colour'], result[row['id']]['colour'])
        else:
            mid_rows += get_centered_value(result[row['id']]['value'], row['max_len'], result[row['id']]['text_colours'], result[row['id']]['line_colour'])
    print(" " * number_of_spaces + mid_rows)
    bottom_lines = ""
    for row in DATA:
        if 'colour' in result[row['id']]:
            bottom_lines += get_lines("╰─╯", row['max_len'], result[row['id']]['colour'])
        else:
            bottom_lines += get_lines("╰─╯", row['max_len'], result[row['id']]['line_colour'])
    print(" " * number_of_spaces + bottom_lines)

def display_table(pokemon_id_tried, mystery_pokemon, cols, lines):
    row = {}
    tried_types = try_types(POKEMON[pokemon_id_tried]['types'], mystery_pokemon['types'])
    row['first_type'] = tried_types[0]
    row['second_type'] = tried_types[1]
    row['evolution_stage'] = try_evolutions(pokemon_id_tried, mystery_pokemon)
    row['height'] = try_height(POKEMON[pokemon_id_tried]['height'], mystery_pokemon['height'])
    row['weight'] = try_weight(POKEMON[pokemon_id_tried]['weight'], mystery_pokemon['weight'])
    row['colours'] = try_colours(COLOURS[pokemon_id_tried], COLOURS[int(mystery_pokemon['number'])])
    row['habitats'] = try_habitats(HABITATS[pokemon_id_tried], HABITATS[int(mystery_pokemon['number'])])
    row['generation'] = try_generation(pokemon_id_tried, int(mystery_pokemon['number']))
    row['pokemon'] = try_pokemon(row, pokemon_id_tried)
    display_row(row, cols, lines)