from src.pokedle.utils import GREEN, RED, ORANGE

def try_types(types, mystery_types):
    result = [None, None]
    for i in range(2):
        if i == 1 and len(types) == 1:
            if len(mystery_types) == 1:
                result[1] = {'value': "Aucun", 'colour': GREEN}
            else:
                result[1] = {'value': "Aucun", 'colour': RED}
        else:
            if types[i] in mystery_types:
                result[i] = {'value': types[i], 'colour': GREEN}
            else:
                result[i] = {'value': types[i], 'colour': RED}
    return result

def try_colours(try_colours, mystery_colours):
    correct_colours = 0
    for colour in try_colours:
        if colour in mystery_colours:
            correct_colours += 1
    if correct_colours == len(mystery_colours) == len(try_colours):
        return {'value': try_colours, 'colour': GREEN}
    elif correct_colours:
        return {'value': try_colours, 'colour': ORANGE}
    return {'value': try_colours, 'colour': RED}

def try_habitats(try_habitats, mystery_habitats):
    correct_habitats = 0
    text_colours = []
    for colour in try_habitats:
        if colour in mystery_habitats:
            correct_habitats += 1
            text_colours.append(GREEN)
        else:
            text_colours.append(RED)
    if correct_habitats == len(mystery_habitats) == len(try_habitats):
        return {'value': try_habitats, 'text_colours': text_colours, 'line_colour': GREEN}
    elif correct_habitats:
        return {'value': try_habitats, 'text_colours': text_colours, 'line_colour': ORANGE}
    return {'value': try_habitats, 'text_colours': text_colours, 'line_colour': RED}
