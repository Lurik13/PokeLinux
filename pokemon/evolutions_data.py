from utils import get_data


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