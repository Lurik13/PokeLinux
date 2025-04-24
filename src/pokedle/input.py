import pickle
from src.pokedle.utils import normalize
from prompt_toolkit.completion import Completer, Completion # type: ignore
from data.Knowledge.generations import GENERATIONS
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

def get_completer_array(generations):
    array = []
    for gen in generations:
        first_pokemon_id = GENERATIONS[gen]['pokemon_range'][0]
        last_pokemon_id = GENERATIONS[gen]['pokemon_range'][1]
        for i in range(first_pokemon_id, last_pokemon_id + 1):
            array.append(POKEMON[i]['french_name'])
    return array

class AccentInsensitiveCompleter(Completer):
    def __init__(self, names):
        self.names = names

    def get_completions(self, document, complete_event):
        normalized_input = normalize(document.text_before_cursor)
        for name in self.names:
            if normalize(name).startswith(normalized_input):
                yield Completion(name, start_position=-len(document.text_before_cursor))