import pickle
from src.pokedle.display import get_centered_value, get_lines
from src.pokedle.utils import BLUE, calculate_number_of_spaces, display_message
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

DATA = [
    {'id': 'clue', 'max_len': 6},
    {'id': 'weaknesses', 'max_len': 18}, #ramoloss noeunoeuf
    {'id': 'letters', 'max_len': 7},
    {'id': 'description', 'max_len': 82}, #hélionceau cerbyllin
]
CATEGORIES = ["Indice", "Faiblesses", "Lettres", "Description"]

def pick_unique_letters(name, number_of_letters):
    unique_letters = list(dict.fromkeys(name.upper()))
    letters_array = []
    for i in range(number_of_letters):
        index = (i * 1357 + 42) % len(unique_letters)
        letters_array.append(unique_letters[index])
    return letters_array

def center_in_cell(max_len, value):
    number_of_spaces = max((max_len + 2 - len(value)) // 2, 0)
    return " " * number_of_spaces + value + " " * (max_len + 2 - len(value) - number_of_spaces)

def get_weaknesses_line(number_of_weaknesses_by_line, remaining_weakness, max_len):
    line = ""
    i = 0
    if (len(remaining_weakness)):
        longest_weakness = min(remaining_weakness, key=len)
        remaining_weakness.remove(longest_weakness)
        line = longest_weakness
        while len(remaining_weakness) and i + 1 < number_of_weaknesses_by_line:
            longest_weakness = min(remaining_weakness, key=len)
            remaining_weakness.remove(longest_weakness)
            if len(line + ', ' + longest_weakness) <= max_len:
                line += ', ' + longest_weakness
            else:
                remaining_weakness.append(longest_weakness)
                break
            i += 1
    return line

def get_weaknesses_list(mystery_pokemon, max_len):
    remaining_weakness = mystery_pokemon['weaknesses']
    max_len = DATA[1]['max_len']
    lines = ['', '', '']
    match len(remaining_weakness):
        case 0:
            return ['', '', '']
        case 1:
            return ['', remaining_weakness[0], '']
        case 2 | 3:
            for i in range(3):
                lines[i] = get_weaknesses_line(1, remaining_weakness, max_len)
            return [lines[0], lines[1], lines[2]]
        case 4:
            lines[0] = get_weaknesses_line(2, remaining_weakness, max_len)
            for i in range(2):
                lines[i + 1] = get_weaknesses_line(1, remaining_weakness, max_len)
            return [lines[0], lines[1], lines[2]]
        case 5:
            for i in range(2):
                lines[i] = get_weaknesses_line(2, remaining_weakness, max_len)
            lines[2] = get_weaknesses_line(1, remaining_weakness, max_len)
            return [lines[0], lines[1], lines[2]]
        case 6:
            for i in range(3):
                lines[i] = get_weaknesses_line(2, remaining_weakness, max_len)
            return [lines[0], lines[1], lines[2]]
        case _:
            for i in range(3):
                lines[i] = get_weaknesses_line(5, remaining_weakness, max_len)
            return [lines[0], lines[1], lines[2]]
    #     if len(line + ', ' + weakness) < max_len:
    #         line += ', ' + weakness
    #     else:
    #         lines.append(line)
    #         line = weakness

    # lines.append(line)

    # for l in lines:
    #     print(" " * (number_of_spaces + DATA[0]['max_len'] + 4) + '│' + center_in_cell(max_len, l) + '│')

# Insecte*, Ténèbres
# Spectre, Poison
# Glace, Vol, Feu

# │   Insecte*, Vol    │
# │    Poison, Feu     │
# │   Glace, Spectre   │
# │      Ténèbres      │

def display_clue(counter, mystery_pokemon, cols):
    # faiblesses, lettres, description
    top_lines = ""
    titre = ""
    mid_lines = ""
    lines_len = 0
    for i in range(len(CATEGORIES)):
        lines_len += DATA[i]['max_len'] + 4
        top_lines += get_lines("┌─┐", DATA[i]['max_len'], BLUE)
        titre += get_centered_value(CATEGORIES[i], DATA[i]['max_len'], BLUE, BLUE, '│')
        mid_lines += get_lines("├─┤", DATA[i]['max_len'], BLUE)
    number_of_spaces = calculate_number_of_spaces(cols, lines_len)
    print(" " * number_of_spaces + top_lines)
    print(" " * number_of_spaces + titre)
    print(" " * number_of_spaces + mid_lines)
    # weaknesses = POKEMON[102]['weaknesses'][0]
    # for weakness in POKEMON[102]['weaknesses'][1:]:
    #     if len(weaknesses + ', ' + weakness) < DATA[1]['max_len']:
    #         weaknesses += ', ' + weakness
    # print(" " * (number_of_spaces + DATA[0]['max_len'] + 4) + '│' + center_in_cell(DATA[1]['max_len'], weaknesses) + '│')
    weaknesses_list = get_weaknesses_list(POKEMON[102], DATA[1]['max_len']) #1voltali 2otaria 3osselait 4rafflesia, 5tartard, 6rhinoferos, 7noeunoeuf
    # weaknesses_list = get_weaknesses_list(mystery_pokemon, DATA[1]['max_len'])
    for i in range(3):
        if i < len(weaknesses_list):
            print(" " * (number_of_spaces + DATA[0]['max_len'] + 4) + '│' + center_in_cell(DATA[1]['max_len'], weaknesses_list[i]) + '│')
        else:
            print(" " * (number_of_spaces + DATA[0]['max_len'] + 4) + '│' + center_in_cell(DATA[1]['max_len'], "") + '│')
    print(weaknesses_list)
    # display_message(get_lines("┌─┐", 5, BLUE), BLUE, cols)
    # display_message(get_centered_value('Lett.', 5, BLUE, BLUE, '│'), BLUE, cols)
    # display_message(get_lines("├─┤", 5, BLUE), BLUE, cols)
    # display_message(get_centered_value('L', 5, BLUE, BLUE, '│'), BLUE, cols)
    # display_message(get_lines("└─┘", 5, BLUE), BLUE, cols)
    return 0
    # description = mystery_pokemon['description'].replace(mystery_pokemon['french_name'], '***').replace(mystery_pokemon['english_name'], '***')
    # if counter < 4:
    #     display_message(f"Persévère ! Il te reste {4 - counter} essai{'s' if counter != 3 else ''} pour obtenir le premier indice.", BLUE, cols)
    # elif counter < 8:
    #     display_message(description[:len(description)//2] + " [...]", BLUE, cols)
    # else:
    #     display_message(description, BLUE, cols)
    # number_of_lines_to_clear = 1
    # letters = []
    # if counter >= 12:
    #     letter_count = 0
    #     if counter < 16:
    #         letter_count = 1
    #     elif counter < 20:
    #         letter_count = 2
    #     else:
    #         letter_count = 3
    #     letters = pick_unique_letters(mystery_pokemon['french_name'], letter_count)
    #     if letter_count == 1:
    #         display_message(f"Le pokémon mystère contient la lettre {letters[0]} dans son nom.", BLUE, cols)
    #     elif letter_count == 2:
    #         display_message(f"Le pokémon mystère contient les lettres {letters[0]} et {letters[1]} dans son nom.", BLUE, cols)
    #     elif letter_count == 3:
    #         display_message(f"Le pokémon mystère contient les lettres {letters[0]}, {letters[1]} et {letters[2]} dans son nom.", BLUE, cols)
    #     number_of_lines_to_clear += 1
    # return number_of_lines_to_clear
