from src.pokedle.utils import *
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

POKEMON_COLOURS = [GREEN, GREENYELLOW, YELLOWGREEN, YELLOW, YELLOWORANGE, ORANGE, REDORANGE, RED]

def get_colour(colours_array, colour_to_add):
    if colour_to_add == GREEN:
        colours_array[GREEN] += 1
    elif colour_to_add == ORANGE:
        colours_array[ORANGE] += 1
    else:
        colours_array[RED] += 1
    return colours_array

def try_pokemon(row, pokemon_id_tried):
    colours = {
        GREEN: 0,
        ORANGE: 0,
        RED: 0
    }
    for  category in row:
        if 'colour' in row[category]:
            colours = get_colour(colours, row[category]['colour'])
        else:
            colours = get_colour(colours, row[category]['line_colour'])
    final_colour = min(colours[RED] + colours[ORANGE] // 2, 7)
    return {'value': POKEMON[pokemon_id_tried]['french_name'], 'colour': POKEMON_COLOURS[final_colour]}