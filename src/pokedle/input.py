import pickle
from src.pokedle.utils import normalize
from prompt_toolkit.completion import Completer, Completion # type: ignore
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

def get_completer_array(first_pokemon_id, last_pokemon_id):
    array = []
    for i in range(first_pokemon_id, last_pokemon_id + 1):
        array.append(POKEMON[i]['french_name'])
    return array

class AccentInsensitiveCompleter(Completer):
    def __init__(self, pokemons_names):
        self.pokemons_names = pokemons_names

    def get_completions(self, document, complete_event):
        normalized_input = normalize(document.text_before_cursor)
        for name in self.pokemons_names:
            if normalize(name).startswith(normalized_input):
                yield Completion(name, start_position=-len(document.text_before_cursor))