def pick_unique_letters(name, number_of_letters):
    unique_letters = [c for c in dict.fromkeys(name.upper()) if c.isalpha()]
    letters_array = []
    for i in range(number_of_letters):
        index = (i * 1357 + 42) % len(unique_letters)
        letters_array.append(unique_letters[index])
        unique_letters.remove(unique_letters[index])
    return letters_array

def get_description_lines(description, pokemon_name):
    lines = ['', '', '']
    description = description.replace(pokemon_name, '***')
    max_len = len(description) / 3 + 5
    if (len(description) <= max_len):
        lines[1] = description
    else:
        words = description.split(' ')
        line_number = 0
        for i in range(len(words)):
            if (len(lines[line_number]) + len(words[i]) > max_len):
                line_number += 1
            if (len(lines[line_number]) + len(words[i]) < max_len and i < len(words) - 1
                    and len(lines[line_number]) + len(words[i]) + len(words[i + 1]) <= max_len):
                lines[line_number] += words[i] + " "
            else:
                lines[line_number] += words[i]
    return lines