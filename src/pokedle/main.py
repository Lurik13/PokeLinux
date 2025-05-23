import pickle
from prompt_toolkit import prompt # type: ignore
from prompt_toolkit.shortcuts import clear # type: ignore
from random import randint
from data.Knowledge.generations import GENERATIONS
from src.pokedle.clue import display_clue
from src.pokedle.display import display_caption, display_table
from src.pokedle.input import get_completer_array, AccentInsensitiveCompleter
from src.pokedle.utils import BLUE, RED, GREEN, WHITE, RESET, \
    display_message, calculate_number_of_spaces, normalize, clear_lines, find_pokemon_by_name, is_correct_generation, get_generation_name_by_pokemon
from src.utils import get_de_pokemon
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

def get_new_mystery_pokemon(generations):
    gen_number = generations[randint(0, len(generations) - 1)]
    first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
    last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1]
    return POKEMON[randint(first_pokemon_id, last_pokemon_id)]

def input_loop(generations, mystery_pokemon, cols):
    counter = 0
    remaining_pokemon_names = get_completer_array(generations)
    number_of_lines_to_clear = 1
    while True:
        completer = AccentInsensitiveCompleter(remaining_pokemon_names)
        number_of_spaces = calculate_number_of_spaces(cols)
        new_try = prompt(" " * number_of_spaces + "Pokémon : ", completer=completer, complete_while_typing=True)
        if counter == 0 and normalize(new_try) == normalize(mystery_pokemon['french_name']):
            mystery_pokemon = get_new_mystery_pokemon(generations)
        clear_lines(number_of_lines_to_clear)
        number_of_lines_to_clear = 1
        if normalize(new_try) == "indice":
            number_of_lines_to_clear += display_clue(counter, mystery_pokemon, cols)
        elif normalize(new_try) == "abandonner":
            display_message(f"Le pokémon mystère était {mystery_pokemon['french_name']} !", WHITE, cols)
            break
        else:
            pokemon_id_tried = find_pokemon_by_name(new_try)
            if not pokemon_id_tried:
                display_message("Ce pokémon n'existe pas ou est mal ortographié.", RED, cols)
                number_of_lines_to_clear += 1
            else:
                counter += 1
                if is_correct_generation(pokemon_id_tried, generations):
                    if normalize(POKEMON[pokemon_id_tried]['french_name']) in normalize(remaining_pokemon_names):
                        remaining_pokemon_names.remove(POKEMON[pokemon_id_tried]['french_name'])
                        display_table(pokemon_id_tried, mystery_pokemon, cols)
                        if normalize(new_try) == normalize(mystery_pokemon['french_name']):
                            message = f"Bien joué ! Tu as trouvé {mystery_pokemon['french_name']} en {counter} coups !"
                            display_message(message, GREEN, cols)
#                             save_in_pokedex(mystery_pokemon)
                            break
                    else:
                        display_message(f"Tu as déjà tenté avec {POKEMON[pokemon_id_tried]['french_name']} et ça n'a pas marché...", RED, cols)
                        number_of_lines_to_clear += 1
                else:
                    display_message(f"Les {POKEMON[pokemon_id_tried]['french_name']} proviennent de la région " + \
                        f"{get_de_pokemon(get_generation_name_by_pokemon(pokemon_id_tried))} !", RED, cols)
                    number_of_lines_to_clear += 1

def are_gens_valids(gen_numbers):
    for nb in gen_numbers:
        if not len(nb):
            print(RED + "Vous devez indiquer le numéro d'une génération." + RESET)
            return False
        elif nb.isnumeric() == False:
            print(RED + f"'{nb}' n'est pas un numéro positif." + RESET)
            return False
        elif int(nb) == 0:
            exit()
        elif int(nb) not in GENERATIONS:
            print(RED + f"La génération '{nb}' n'existe pas selon mes sources." + RESET)
            return False
    return True

def parsing_gens():
    valid = False
    print("Veuillez indiquer le numéro d'une génération. 0 pour sortir.\nMettez des virgules si vous voulez plusieurs générations.")
    while not valid:
        print("Génération(s) : ", end='', flush=True)
        gen_numbers = input().replace(' ', '').split(',')
        valid = are_gens_valids(gen_numbers)
    return [int(x) for x in gen_numbers]

def pokedle(cols):
    generations = parsing_gens()
    input_choices = ['Rejouer avec les mêmes générations', 'Changer de générations', 'Quitter']
    completer = AccentInsensitiveCompleter(input_choices)
    while True:
        mystery_pokemon = get_new_mystery_pokemon(generations)
        clear()
        display_message('Si tu as besoin d\'aide, écris "Indice". Tu as le droit à un indice supplémentaire tous les 4 essais', BLUE, cols)
        display_caption(cols)
        input_loop(generations, mystery_pokemon, cols)
        number_of_spaces = calculate_number_of_spaces(cols)
        want_to_continue = prompt(
            " " * number_of_spaces + 'On rejoue ? Utilise le TAB pour voir les propositions.\n' + " " * number_of_spaces + 'Réponse : ',
            completer=completer, complete_while_typing=True)
        while True:
            if normalize(want_to_continue.lower()) == normalize(input_choices[0]):
                break
            if normalize(want_to_continue.lower()) == normalize(input_choices[1]):
                generations = parsing_gens()
                break
            if normalize(want_to_continue.lower()) == normalize(input_choices[2]):
                return
            want_to_continue = prompt(" " * number_of_spaces + 'Réponse invalide. Utilise le TAB pour voir les propositions.\n' + " " * number_of_spaces + 'Réponse : ',
                completer=completer, complete_while_typing=True)
