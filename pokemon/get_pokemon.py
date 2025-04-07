from pokemon.utils import *
from pokemon.weaknesses import *
from pokemon.forms import *

def add_evolution(evolution_list, chain):
	name = chain["species"]["name"]
	pokemon_data = get_data("pokemon", name)
	evolution_list.append({
		"id": pokemon_data["id"],
		"name": name
	})
	for evolves_to in chain["evolves_to"]:
		add_evolution(evolution_list, evolves_to)

def get_evolution_chain(species_data):
	evo_chain_url = species_data["evolution_chain"]["url"]
	evo_chain_id = evo_chain_url.strip("/").split("/")[-1]
	evolution_chain = get_data("evolution-chain", evo_chain_id)
	evolution_list = []
	add_evolution(evolution_list, evolution_chain["chain"])
	return evolution_list

def get_pokemon(pokemon_id):
	pokemon = get_data('pokemon', pokemon_id)
	species = get_data('pokemon-species', pokemon_id)
	number = pokemon["id"]
	french_name = get_french_name(species)
	types = [t["type"]["name"] for t in pokemon["types"]]
	weaknesses = get_weaknesses(types)

	return {
		"pokemon_data": pokemon,
		"species_data": species,
		"evolution_chain": get_evolution_chain(species),
		"number": f"{number:04}" ,
		"english_name": pokemon["name"].capitalize(),
		"french_name": french_name,
		"sprite": SPRITE_URL.format(number),
		"types": [TYPE_TRANSLATION[t] for t in types],
		"weaknesses": list(weaknesses),
		"forms": get_forms(species)
	}
