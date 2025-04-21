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

def input_loop(gen_number, mystery_pokemon, first_pokemon_id, last_pokemon_id, cols, lines):
    counter = 0
    remaining_pokemon_names = get_completer_array(first_pokemon_id, last_pokemon_id)
    number_of_lines_to_clear = 1
    while True:
        completer = AccentInsensitiveCompleter(remaining_pokemon_names)
        number_of_spaces = calculate_number_of_spaces(cols)
        new_try = prompt(" " * number_of_spaces + "Pokémon : ", completer=completer, complete_while_typing=True)
        clear_lines(number_of_lines_to_clear)
        number_of_lines_to_clear = 1
        if normalize(new_try) == "indice":
            display_message(mystery_pokemon['description'][:counter*5], ORANGE, cols)
            number_of_lines_to_clear += 1
        else:
            pokemon_id_tried = find_pokemon_by_name(new_try)
            if not pokemon_id_tried:
                display_message("Ce pokémon n'existe pas ou est mal ortographié.", RED, cols)
                number_of_lines_to_clear += 1
            else:
                counter += 1
                if is_correct_generation(pokemon_id_tried, first_pokemon_id, last_pokemon_id):
                    if normalize(new_try) in normalize(remaining_pokemon_names):
                        remaining_pokemon_names.remove(POKEMON[pokemon_id_tried]['french_name'])
                        display_table(pokemon_id_tried, mystery_pokemon, cols, lines)
                        if normalize(new_try) == normalize(mystery_pokemon['french_name']):
                            message = f"Bien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coup{'s' if counter != 1 else ''} !"
                            display_message(message, GREEN, cols)
                            break
                    else:
                        display_message(f"Tu as déjà tenté avec {POKEMON[pokemon_id_tried]['french_name']} et ça n'a pas marché...", RED, cols)
                        number_of_lines_to_clear += 1
                else:
                    display_message(f"Les {POKEMON[pokemon_id_tried]['french_name']} ne proviennent pas de la région " + \
                        f"{get_de_pokemon(get_gen_region(GENERATIONS[gen_number]['name']))} !", RED, cols)
                    number_of_lines_to_clear += 1

def pokedle(gen_number, cols, lines):
    gen_number = int(gen_number)
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    mystery_pokemon = POKEMON[randint(first_pokemon_id, last_pokemon_id)]
    clear()
    # print(mystery_pokemon['french_name']) ################
    display_message('Si tu as besoin d\'aide, écris "Indice".', ORANGE, cols)
    display_caption(cols, lines)
    input_loop(gen_number, mystery_pokemon, first_pokemon_id, last_pokemon_id, cols, lines)
    number_of_spaces = calculate_number_of_spaces(cols)
    want_to_continue = prompt(" " * number_of_spaces + 'Entre "Continuer" pour commencer une nouvelle partie.\n' + " " * number_of_spaces + 'Réponse : ')
    if want_to_continue.lower() == 'continuer':
        from src.main import parsing_gen
        print('')
        parsing_gen(pokedle, cols, lines)
