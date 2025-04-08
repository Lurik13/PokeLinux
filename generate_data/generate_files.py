import shutil
import sys
import os
from genericpath import exists

sys.path.append(os.path.abspath('..'))
from data.Knowledge.generations import *
from get_data import get_pokemon_data

def get_generation_number(pokemon_id): ###
	for i in range(1, len(GENERATIONS) + 1):
		if pokemon_id >= GENERATIONS[i]['pokemon_range'][0] and pokemon_id <= GENERATIONS[i]['pokemon_range'][1]:
			return i
	return 0

def get_gen_region(gen_name): ###
	words = gen_name.strip().split()
	if not words:
		return None
	return words[-1]

def generate_folder(path, suffix):
	folder_path = path + suffix
	if not exists(path):
		os.mkdir(path)
	if not exists(folder_path):
		os.mkdir(folder_path)
		print("📂 Création du dossier " + suffix + ".")
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

def generate_file(folder_name, pokemon):
	file_name = get_good_constant_name(pokemon['french_name']) + ".py"
	file_path = folder_name + '/' + file_name
	file = open(file_path, 'w')
	write_file(file, pokemon)
	file.close()
	print("Généré " + file_name + " avec succès.")

def generate_pokemon_data_files():
	if os.path.exists("../data/Pokemons/"):
		shutil.rmtree("../data/Pokemons/")
	generate_folder("../data/Pokemons/", "")
	file = open("../data/Pokemons/pokemon_relations.py", 'w')
	poke_imports = ""
	poke_dict = ""
	poke_dict += "\nPOKEMON = {\n"
	for i in range(1, 1026):
		pokemon = get_pokemon_data(i)
		gen_number = get_generation_number(i)
		folder_path = generate_folder("../data/Pokemons/", get_gen_region(GENERATIONS[gen_number]['name']))
		generate_file(folder_path, pokemon)
		poke_name = get_good_constant_name(pokemon['french_name'])
		poke_imports += "from data.Pokemons." + get_gen_region(GENERATIONS[gen_number]['name']) \
			+ "." + poke_name + " import " + poke_name.upper() + "\n"
		poke_dict += "    " + str(pokemon['number']).lstrip("0") + ": " + poke_name.upper() + ",\n"
	poke_dict += "}"
	file.writelines(poke_imports + poke_dict)
	file.close()
	print("Toutes les données ont bien été téléchargées !")



generate_pokemon_data_files()
