def unlock_hint(table, moves, counter):
    counter = int(counter / 3)
    i = 0
    while (moves != counter and i < 3):
        if (table[i] != ''):
            moves += 1
        i += 1
    while (i < 3):
        table[i] = ""
        i += 1
    return moves

def unlock_hints_by_counter(counter, weaknesses_list, letters_list, description_lines):
    unlocked_weaknesses = weaknesses_list
    unlocked_letters = letters_list
    unlocked_description = description_lines
    moves = unlock_hint(unlocked_weaknesses, 0, counter)
    moves = unlock_hint(unlocked_letters, moves, counter)
    unlock_hint(unlocked_description, moves, counter)
    return unlocked_weaknesses, unlocked_letters, unlocked_description