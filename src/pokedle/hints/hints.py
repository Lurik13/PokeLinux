import pickle
from src.pokedle.display import get_centered_value, get_lines
from src.pokedle.hints.letters_and_description import pick_unique_letters, get_description_lines
from src.pokedle.hints.unlock_hints import unlock_hints_by_counter
from src.pokedle.hints.weaknesses import get_weaknesses_list
from src.pokedle.utils import BLUE, calculate_number_of_spaces
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

DATA = [
    {'id': 'weaknesses', 'max_len': 18}, #ramoloss noeunoeuf
    {'id': 'letters', 'max_len': 7},
    {'id': 'description', 'max_len': 65}, #hélionceau cerbyllin
]
CATEGORIES = ["Faiblesses", "Lettres", "Description"]

def center_in_cell(max_len, value):
    number_of_spaces = max((max_len + 2 - len(value)) // 2, 0)
    return " " * number_of_spaces + value + " " * (max_len + 2 - len(value) - number_of_spaces)

def display_hints(counter, mystery_pokemon, cols):
    top_lines = BLUE + "┌"
    title = ""
    mid_lines = BLUE + "├"
    mid_bottom_lines = "├"
    bottom_lines = BLUE + "└"
    lines_len = 0
    max_category_len = 0

    # DISPLAY CAPTION
    for i in range(len(CATEGORIES)):
        max_category_len = DATA[i]['max_len']
        if i == len(CATEGORIES) - 1:
            max_category_len = int(len(mystery_pokemon['description']) / 3 + 6)
        lines_len += max_category_len + 2
        top_lines += get_lines("─┬", max_category_len, BLUE)
        title += get_centered_value(CATEGORIES[i], max_category_len, BLUE, BLUE, '│', '')
        mid_lines += get_lines("─┼", max_category_len, BLUE)
        mid_bottom_lines += get_lines("─┴", max_category_len, BLUE)
    bottom_lines += get_lines("─┘", lines_len, BLUE)
    number_of_spaces = calculate_number_of_spaces(cols, lines_len)
    print(" " * number_of_spaces + top_lines[:-5] + '┐')
    print(" " * number_of_spaces + title + BLUE + '│')
    print(" " * number_of_spaces + mid_lines[:-5] + '┤')

    weaknesses_list = get_weaknesses_list(mystery_pokemon)
    letters_list = pick_unique_letters(mystery_pokemon['french_name'], 3)
    description_lines = get_description_lines(mystery_pokemon['description'], mystery_pokemon['french_name'])
    hint_footer = f"Prochain indice dans {3 - counter % 3} essai{'s' if 3 - counter % 3 > 1 else ''}"
    if (counter >= 9 * 3 - weaknesses_list.count('') * 3):
        hint_footer = f"Tu disposes de tous les indices !"

    # DISPLAY HINTS
    weaknesses_list, letters_list, description_lines = \
        unlock_hints_by_counter(counter, weaknesses_list, letters_list, description_lines)
    for i in range(3):
        line_to_print = " "  * number_of_spaces + '│'
        if i < len(weaknesses_list):
            line_to_print += center_in_cell(DATA[0]['max_len'], weaknesses_list[i]) + '│'
        else:
            line_to_print += center_in_cell(DATA[0]['max_len'], "") + '│'
        line_to_print += center_in_cell(DATA[1]['max_len'], letters_list[i]) + '│'
        line_to_print += center_in_cell(max_category_len, description_lines[i]) + '│'
        print(BLUE + line_to_print)

    # DISPLAY NEXT HINT
    print(" " * number_of_spaces + mid_bottom_lines[:-5] + '┤')
    footer = get_centered_value(hint_footer, lines_len, BLUE, BLUE)
    print(" " * number_of_spaces + footer)
    print(" " * number_of_spaces + bottom_lines[:-5] + '┘')
    return 9
