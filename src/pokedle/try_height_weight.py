from src.pokedle.utils import GREEN, RED

def get_higher_or_lower(message, value, mystery_value):
    if value == mystery_value:
        return {'value': message, 'colour': GREEN}
    elif value > mystery_value:
        return {'value': message + ' ↓', 'colour': RED}
    else:
        return {'value': message + ' ↑', 'colour': RED}

def try_height(height, mystery_height):
    meters = height // 10
    centimeters = (height % 10) * 10
    result = ""
    if (meters):
        result += str(meters) + 'm'
        if (centimeters):
            result += str(centimeters)
    else:
        result += str(centimeters) + 'cm'
    return get_higher_or_lower(result, height, mystery_height)

def try_weight(weight, mystery_weight):
    result = ""
    if (weight):
        real_weight = weight / 10
        if real_weight.is_integer():
            result += str(int(real_weight)) + 'kg'
        else:
            result += str(real_weight) + 'kg'
    return get_higher_or_lower(result, weight, mystery_weight)
