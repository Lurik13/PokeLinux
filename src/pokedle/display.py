import asyncio
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
    if isinstance(value, str):
        return [lines_colour, line, RESET, ' ' * left_spaces, value_colour, value, RESET, ' ' * right_spaces, lines_colour, line, RESET]
    else:
        if isinstance(value_colour, str):
            return [lines_colour, line, RESET, ' ' * left_spaces, value_colour, list_to_string[:-2],  RESET, ' ' * right_spaces, lines_colour, line, RESET]
        else:
            result = [lines_colour, line, RESET, ' ' * left_spaces]
            for i in range(len(value)):
                result.append(value_colour[i])
                result.append(value[i])
                result.append(RESET)
                if i + 1 < len(value):
                    result.append(lines_colour)
                    result.append(', ')
                    result.append(RESET)
            result.append(' ' * right_spaces)
            result.append(lines_colour)
            result.append(line)
            result.append(RESET)
            return result

def get_lines(lines, max_len, colour):
    return [colour, lines[0] + lines[1] * (max_len + 2) + lines[2], RESET]

async def display_slowly_row(number_of_spaces, number_of_chars_by_row, rows, slowly = True):
    if not slowly:
        for row in rows:
            result = " " * number_of_spaces
            for category in row:
                for case in category:
                    result += case
            print(result)
    else:
        colours = [GRAY, BLUE, GREEN, GREENYELLOW, YELLOWGREEN, YELLOW, YELLOWORANGE, ORANGE, REDORANGE, RED, WHITE, RESET]
        for i in range(sum(number_of_chars_by_row) + 1):
            for row in rows:
                j = 0
                print(" " * number_of_spaces, end='', flush=True)
                for category in row:
                    for case in category:
                        if case in colours:
                            print(case, end='', flush=True)
                        else:
                            k = 0
                            while j + k < i and k < len(case):
                                print(case[k], end='', flush=True)
                                k += 1
                            j += k
                print('')
            await asyncio.sleep(0.012)
            total_len = 0
            for category_len in number_of_chars_by_row:
                total_len += category_len
                if i == total_len:
                    await asyncio.sleep(0.37)
                    break
            if i < sum(number_of_chars_by_row):
                clear_lines(3)

async def display_caption(cols):
    number_of_spaces = calculate_number_of_spaces(cols)
    top_caption = []
    for row in DATA:
        top_caption.append(get_lines("╔═╗", row['max_len'], WHITE))
    mid_caption = []
    for i in range(len(CATEGORIES)):
        mid_caption.append(get_centered_value(CATEGORIES[i], DATA[i]['max_len'], WHITE, WHITE, '║'))
    bottom_caption = []
    for row in DATA:
        bottom_caption.append(get_lines("╚═╝", row['max_len'], WHITE))
    number_of_chars = []
    for row in DATA:
        number_of_chars.append(row['max_len'] + 4)
    await display_slowly_row(number_of_spaces, number_of_chars, [top_caption, mid_caption, bottom_caption], False)

async def display_row(result, cols):
    number_of_spaces = calculate_number_of_spaces(cols)
    top_lines = []
    for row in DATA:
        if 'colour' in result[row['id']]:
            top_lines.append(get_lines("╭─╮", row['max_len'], result[row['id']]['colour']))
        else:
            top_lines.append(get_lines("╭─╮", row['max_len'], result[row['id']]['line_colour']))
    mid_rows = []
    for row in DATA:
        if 'colour' in result[row['id']]:
            mid_rows.append(get_centered_value(result[row['id']]['value'], row['max_len'], result[row['id']]['colour'], result[row['id']]['colour']))
        else:
            mid_rows.append(get_centered_value(result[row['id']]['value'], row['max_len'], result[row['id']]['text_colours'], result[row['id']]['line_colour']))
    bottom_lines = []
    for row in DATA:
        if 'colour' in result[row['id']]:
            bottom_lines.append(get_lines("╰─╯", row['max_len'], result[row['id']]['colour']))
        else:
            bottom_lines.append(get_lines("╰─╯", row['max_len'], result[row['id']]['line_colour']))
    number_of_chars = []
    for row in DATA:
        number_of_chars.append(row['max_len'] + 4)
    await display_slowly_row(number_of_spaces, number_of_chars, [top_lines, mid_rows, bottom_lines])

def display_table(pokemon_id_tried, mystery_pokemon, cols):
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
    asyncio.run(display_row(row, cols))