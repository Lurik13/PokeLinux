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
