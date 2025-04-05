import requests # type: ignore
from utils import *

def get_evolution_chain(species):
    # evo_chain_url = get_data(species, "evolution-chain")
    evo_chain_url = species["evolution_chain"]["url"]
    evo_data = requests.get(evo_chain_url).json()["chain"]

    evo_line = []
    current = evo_data
    while current:
        name = current["species"]["name"]
        current_pokemon = get_data(name, 'pokemon-species')
        evo_line.append(get_french_name(current_pokemon))
        if current["evolves_to"]:
            current = current["evolves_to"][0]
        else:
            break
    return evo_line
