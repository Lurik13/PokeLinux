from data.Knowledge.generations import GENERATIONS
from src.pokedle.utils import *

def get_generation(pokemon_id):
    for gen in GENERATIONS:
        if pokemon_id > GENERATIONS[gen]['pokemon_range'][0] and pokemon_id < GENERATIONS[gen]['pokemon_range'][1]:
            return gen

def try_generation(pokemon_id_tried, mystery_id):
    try_gen = get_generation(pokemon_id_tried)
    mystery_gen = get_generation(mystery_id)
    if try_gen == mystery_gen:
        return {'value': str(try_gen), 'colour': GREEN}
    elif try_gen > mystery_gen:
        return {'value': str(try_gen) + ' ↓', 'colour': RED}
    else:
        return {'value': str(try_gen) + ' ↑', 'colour': RED}