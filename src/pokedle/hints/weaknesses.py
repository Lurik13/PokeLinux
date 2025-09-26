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

#1voltali 2otaria 3osselait 4rafflesia, 5tartard, 6rhinoferos, 7noeunoeuf
def get_weaknesses_list(mystery_pokemon):
    from src.pokedle.hints.hints import DATA
    remaining_weakness = mystery_pokemon['weaknesses'].copy()
    max_len = DATA[0]['max_len']
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