import pickle
import sys
import unicodedata
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

GRAY = "\033[38;2;150;150;150;1m"
BLUE = "\033[38;2;0;100;200m"
GREEN = "\033[38;2;50;200;50m"
GREENYELLOW = "\033[38;2;100;200;50m"
YELLOWGREEN = "\033[38;2;150;200;50m"
YELLOW = "\033[38;2;200;200;50m"
YELLOWORANGE = "\033[38;2;200;175;25m"
ORANGE = "\033[38;2;200;150;0m"
REDORANGE = "\033[38;2;200;100;25m"
RED = "\033[38;2;200;50;50m"
WHITE = "\033[38;2;255;255;255m"
RESET = "\033[0m"

def console_print(message, should_flush = False, color = GRAY):
    if should_flush:
        print(color + message + RESET, end='', flush=should_flush)
    else:
        print(color + message + RESET)

def remove_accents(value):
    return ''.join(
            c for c in unicodedata.normalize('NFD', value)
            if unicodedata.category(c) != 'Mn')

def normalize(value):
    if isinstance(value, str):
        return remove_accents(value).lower()
    else:
        new_array = []
        for i in range(len(value)):
            new_value = remove_accents(value[i])
            new_array.append(new_value.lower())
        return new_array

def clear_lines(n):
    for _ in range(n):
        sys.stdout.write('\033[F\033[K')
    sys.stdout.flush()

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

def calculate_number_of_spaces(cols, custom_len = 0):
    if custom_len:
        return max((cols - custom_len) // 2, 0)
    from src.pokedle.display import DATA
    number_of_spaces = 0
    for row in DATA:
        number_of_spaces += 4 + row['max_len']
    return max((cols - number_of_spaces) // 2, 0)

def display_message(message, colour, cols):
    number_of_spaces = calculate_number_of_spaces(cols)
    console_print(" " * number_of_spaces + message, False, colour)