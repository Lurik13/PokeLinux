import shutil
import sys
import os
import pickle
from genericpath import exists

sys.path.append(os.path.abspath('../..'))
from data.Knowledge.generations import *
from src.generate_data.get_data import get_pokemon_data

def get_gen_region(gen_name):
	words = gen_name.strip().split()
	if not words:
		return None
	return words[-1]

def clear_and_print(message, should_flush = False):
	new_message = message + " " * (80 - len(message))
	if should_flush:
		print(new_message, end='\r', flush=True)
	else:
		print(new_message)


def generate_folder(path, suffix):
	folder_path = path + suffix
	if not exists(path):
		os.mkdir(path)
	if not exists(folder_path):
		os.mkdir(folder_path)
		clear_and_print("📂 Création du dossier " + suffix + ".")
	return folder_path

def get_good_constant_name(pokemon_name):
	return pokemon_name.replace(".", "").replace(" ", "").replace("♀", "Femelle").replace("♂", "Male").replace("-", "").replace(":", "")

def write_file(file, pokemon):
	text = str(pokemon)
	new_text = get_good_constant_name(pokemon['french_name']).upper() + " = "
	number_of_brackets = 0
	for letter in text:
		match letter:
			case '{' | '[':
				number_of_brackets += 1
				new_text += letter + '\n' + number_of_brackets * '    '
			case '}' | ']':
				number_of_brackets -= 1
				new_text += '\n' + number_of_brackets * '    ' + letter
			case ',':
				new_text += ',\n' + (number_of_brackets - 1) * '    ' + '   '
			case _:
				new_text += letter
	file.writelines(new_text)

def generate_file(folder_name, gen_name, pokemon):
	file_name = get_good_constant_name(pokemon['french_name']) + ".py"
	file_path = folder_name + '/' + file_name
	file = open(file_path, 'w')
	write_file(file, pokemon)
	file.close()
	clear_and_print("Données enregistrées dans le Pokédex de " + gen_name + " : " + file_name, True)

def generate_pokedex():
	pokedex_path = "data/Pokédex/"
	if os.path.exists(pokedex_path):
		shutil.rmtree(pokedex_path)
	generate_folder(pokedex_path, "")
	poke_file = open(pokedex_path + "pokemon_relations.py", 'w')
	poke_imports = ""
	poke_dict = ""
	poke_dict += "\nPOKEMON = {\n"
	for gen_number in GENERATIONS:
		first_pokemon = GENERATIONS[gen_number]['pokemon_range'][0]
		last_pokemon = GENERATIONS[gen_number]['pokemon_range'][1] + 1
		folder_path = generate_folder(pokedex_path, get_gen_region(GENERATIONS[gen_number]['name']))
		for i in range(first_pokemon, last_pokemon):
			pokemon = get_pokemon_data(i)
			generate_file(folder_path, get_gen_region(GENERATIONS[gen_number]['name']), pokemon)
			poke_name = get_good_constant_name(pokemon['french_name'])
			poke_imports += "from data.Pokédex." + get_gen_region(GENERATIONS[gen_number]['name']) \
				+ "." + poke_name + " import " + poke_name.upper() + "\n"
			poke_dict += "    " + str(pokemon['number']).lstrip("0") + ": " + poke_name.upper() + ",\n"
	poke_dict += "}"
	poke_file.writelines(poke_imports + poke_dict)
	poke_file.close()
	clear_and_print("En train de mettre tous ces pokémons dans leurs pokéballs ...")
	from data.Pokédex.pokemon_relations import POKEMON
	with open(pokedex_path + "pokemon_relations.pkl", "wb") as executable: # wb = write binary
		pickle.dump(POKEMON, executable)
	clear_and_print("Toutes les données ont bien été téléchargées !")
