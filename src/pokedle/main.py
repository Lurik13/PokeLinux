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

def pick_unique_letters(name, number_of_letters):
    unique_letters = list(dict.fromkeys(name.upper()))
    letters_array = []
    for i in range(number_of_letters):
        index = (i * 1357 + 42) % len(unique_letters)
        letters_array.append(unique_letters[index])
    return letters_array

def print_clue(counter, mystery_pokemon, cols):
    description = mystery_pokemon['description'].replace(mystery_pokemon['french_name'], '***').replace(mystery_pokemon['english_name'], '***')
    if counter < 4:
        display_message(f"Persévère ! Il te reste {4 - counter} essai{'s' if counter != 2 else ''} pour obtenir le premier indice.", BLUE, cols)
    elif counter < 8:
        display_message(description[:len(description)//2] + " [...]", BLUE, cols)
    else:
        display_message(description, BLUE, cols)
    number_of_lines_to_clear = 1
    letters = []
    if counter >= 12:
        letter_count = 0
        if counter < 16:
            letter_count = 1
        elif counter < 20:
            letter_count = 2
        else:
            letter_count = 3
        letters = pick_unique_letters(mystery_pokemon['french_name'], letter_count)
        if letter_count == 1:
            display_message(f"Le pokémon mystère contient la lettre {letters[0]} dans son nom.", BLUE, cols)
        elif letter_count == 2:
            display_message(f"Le pokémon mystère contient les lettres {letters[0]} et {letters[1]} dans son nom.", BLUE, cols)
        elif letter_count == 3:
            display_message(f"Le pokémon mystère contient les lettres {letters[0]}, {letters[1]} et {letters[2]} dans son nom.", BLUE, cols)
        number_of_lines_to_clear += 1
    return number_of_lines_to_clear


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
            number_of_lines_to_clear += print_clue(counter, mystery_pokemon, cols)
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
    display_message('Si tu as besoin d\'aide, écris "Indice". Tu as le droit à un indice supplémentaire tous les 4 essais', BLUE, cols)
    display_caption(cols, lines)
    input_loop(gen_number, mystery_pokemon, first_pokemon_id, last_pokemon_id, cols, lines)
    number_of_spaces = calculate_number_of_spaces(cols)
    want_to_continue = prompt(" " * number_of_spaces + 'Entre "Continuer" pour commencer une nouvelle partie.\n' + " " * number_of_spaces + 'Réponse : ')
    if want_to_continue.lower() == 'continuer':
        from src.main import parsing_gen
        print('')
        parsing_gen(pokedle, cols, lines)
