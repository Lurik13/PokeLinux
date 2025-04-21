import sys
import unicodedata

GRAY = "\033[38;2;150;150;150;1m"
GREEN = "\033[38;2;50;200;50m"
BLUE = "\033[38;2;0;100;200m"
RED = "\033[38;2;200;50;50m"
ORANGE = "\033[38;2;200;150;0m"
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
