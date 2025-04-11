import requests # type: ignore
import sys
import os
sys.path.append(os.path.abspath('..'))
from data.Knowledge.damages import *
from data.Knowledge.others import *


###############################################################################
############################    UTILS FUNCTIONS    ############################
###############################################################################
def get_data(type, value):
	url = f"https://pokeapi.co/api/v2/{type}/{value}/"
	return requests.get(url).json()

import time

def get_data(type, value, retries=3, delay=1):
	url = f"https://pokeapi.co/api/v2/{type}/{value}/"
	
	for attempt in range(retries):
		try:
			# Effectuer la requête
			response = requests.get(url)
			
			# Vérifier si la requête a été réussie (statut 200)
			if response.status_code == 200:
				try:
					return response.json()  # Essayer de convertir la réponse en JSON
				except requests.exceptions.JSONDecodeError as json_err:
					print(f"[ERROR] JSON Decode Error for {url}: {json_err}")
					break  # Sortir de la boucle en cas d'erreur de décodage
			elif response.status_code == 429:
				# Gérer le rate-limiting (trop de requêtes)
				print(f"[RATE LIMIT] Too many requests. Retrying in {delay}s...")
				time.sleep(delay)
			else:
				print(f"[ERROR] HTTP Error {response.status_code} for {url}")
				break  # Sortir de la boucle si le code HTTP est différent de 200 ou 429
		except requests.exceptions.RequestException as e:
			print(f"[NETWORK ERROR] Error occurred while making request to {url}: {e}")
			time.sleep(delay)  # Attendre un peu avant de réessayer
	
	# Si toutes les tentatives échouent, lever une exception
	raise Exception(f"Failed to retrieve data from {url} after {retries} attempts.")


def get_french_name(pokemon_data):
	for name_entry in pokemon_data['names']:
		if name_entry["language"]["name"] == "fr":
			return name_entry["name"]
		
pokemon_species_cache = {}

def get_pokemon_species(id):
	if id in pokemon_species_cache:
		return pokemon_species_cache[id]
	pokemon_data = get_data("pokemon-species", id)
	pokemon_species_cache[id] = pokemon_data
	return pokemon_data



###############################################################################
##########################    EVOLUTION FUNCTIONS    ##########################
###############################################################################
evolution_chain_cache = {}

def add_evolution(evolution_list, chain):
	poke_url = chain["species"]["url"]
	id = poke_url.strip("/").split("/")[-1]
	name = get_french_name(get_pokemon_species(id))
	evolution_list.append({
		"id": f"{int(id):04}",
		"name": name
	})
	for evolves_to in chain["evolves_to"]:
		add_evolution(evolution_list, evolves_to)

def get_evolution_chain(species_data):
	evo_chain_url = species_data["evolution_chain"]["url"]
	evo_chain_id = evo_chain_url.strip("/").split("/")[-1]
	if evo_chain_id in evolution_chain_cache:
		return evolution_chain_cache[evo_chain_id]
	evolution_chain = get_data("evolution-chain", evo_chain_id)
	evolution_list = []
	add_evolution(evolution_list, evolution_chain["chain"])
	evolution_chain_cache[evo_chain_id] = evolution_list
	return evolution_list



###############################################################################
#########################    WEAKNESSES FUNCTIONS    ##########################
###############################################################################
def calculate_damages(pokemon_types):
	damage_relations = {}

	for pokemon_type in pokemon_types:
		type_relations = DAMAGE_RELATIONS[pokemon_type]
		for category, multiplier in DAMAGE_MULTIPLIER.items():
			for type_name in type_relations[category]:
				if type_name not in damage_relations:
					damage_relations[type_name] = 1
				damage_relations[type_name] *= multiplier

	return damage_relations


def get_weaknesses(types):
	damage_relations = calculate_damages(types)
	critical_weaknesses = []
	normal_weaknesses = []

	for name, damage in damage_relations.items():
		if damage == 4:
			critical_weaknesses.append(TYPE_TRANSLATIONS[name] + '*')
		elif damage == 2:
			normal_weaknesses.append(TYPE_TRANSLATIONS[name])

	return critical_weaknesses + normal_weaknesses



###############################################################################
############################    FORM FUNCTIONS    #############################
###############################################################################
def get_sprite(form_data):
	form_url = form_data["pokemon"]["url"]
	form_id = form_url.strip("/").split("/")[-1]
	return SPRITE_URL.format(form_id)

def get_forms(species):
	forms = []
	for form in species['varieties']:
		if form['is_default'] is False:
			form_dict = {
				'french_name': "",
				'sprite': "",
				'types': None,
				'weaknesses': None
			}
			form_data = get_data('pokemon-form', form['pokemon']['name'])

			if form['pokemon']['name'].endswith('gmax') == False \
			 and form['pokemon']['name'].startswith('pikachu') == False:
				types = [t["type"]["name"] for t in form_data["types"]]
				form_dict['types'] = [TYPE_TRANSLATIONS[t] for t in types]
				form_dict['weaknesses'] = get_weaknesses(types)
			form_dict['french_name'] = get_french_name(form_data)
			form_dict['sprite'] = get_sprite(form_data)
			forms.append(form_dict)
	return forms



###############################################################################
###########################    MAIN FUNCTION    ############################
###############################################################################
def get_pokemon_data(pokemon_id):
	pokemon = get_data('pokemon', pokemon_id)
	species = get_pokemon_species(pokemon_id)
	number = pokemon["id"]
	french_name = get_french_name(species)
	types = [t["type"]["name"] for t in pokemon["types"]]
	weaknesses = get_weaknesses(types)

	return {
		"number": f"{number:04}" ,
		"french_name": french_name,
		"english_name": pokemon["name"].capitalize(),
		"evolution_chain": get_evolution_chain(species),
		"sprite": SPRITE_URL.format(number),
		"types": [TYPE_TRANSLATIONS[t] for t in types],
		"weaknesses": list(weaknesses),
		"forms": get_forms(species)
	}
