import sys
import os
from genericpath import exists

sys.path.append(os.path.abspath('..'))
from data.Knowledge.generations import *

def get_generation_number(pokemon_id): ###
	for i in range(len(GENERATIONS)):
		if pokemon_id >= GENERATIONS[i + 1]['pokemon_range'][0] and pokemon_id <= GENERATIONS[i + 1]['pokemon_range'][1]:
			return i + 1
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
		print("Generated the " + suffix + " folder.")
	return folder_path

HEHE = {
	"number": 1024,
	"french_name": "Mouahaha",
	"english_name": "Attempt",
	"evolution_chain": ['Essai', 'Test', 'Tentative'],
	"sprite": "test.gif",
	"types": ['Ténèbres'],
	"weaknesses": ['AA', 'bb'],
	"forms": {
		'french_name': "CCCCCCC",
		'sprite': "C.png",
		'types': None,
		'weaknesses': None
	}
}

def write_file(file, pokemon):
	text = str(pokemon) #.replace('{', '{\n	').replace(', ', ',\n	')
	new_text = pokemon['french_name'].upper() + " = "
	number_of_curly_brackets = 0
	number_of_square_brackets = 0
	for letter in text:
		match letter:
			case '{':
				number_of_curly_brackets += 1
				new_text += '{\n' + number_of_curly_brackets * '    '
			case '}':
				number_of_curly_brackets -= 1
				new_text += '\n' + number_of_curly_brackets * '    ' + '}'
			case '[':
				number_of_square_brackets += 1
				new_text += '['
			case ']':
				number_of_square_brackets -= 1
				new_text += ']'
			case ',':
				if number_of_square_brackets == 0:
					new_text += ',\n' + (number_of_curly_brackets - 1) * '    ' + '   '
				else:
					new_text += ','
			case _:
				new_text += letter
	file.writelines(new_text)
	

def generate_file(folder_name, pokemon):
	file_name = pokemon['french_name'] + ".py"
	file_path = folder_name + '/' + file_name
	file = open(file_path, 'w')
	write_file(file, pokemon)
	file.close()
	print("Generated the " + file_name + " file.")

def generate_pokemon_relations_file():
	file = open("../data/Pokemons/pokemon_relations.py", 'w')
	poke_imports = ""
	poke_dict = ""
	gen_number = get_generation_number(900)
	poke_dict += "\nPOKEMON = {\n"
	poke_imports += "from data.Pokemons." + get_gen_region(GENERATIONS[gen_number]['name']) \
		+ "." + HEHE['french_name'] + " import " + HEHE['french_name'].upper() + "\n"
	poke_dict += "    " + str(HEHE['number']) + ": " + HEHE['french_name'].upper() + "\n"
	poke_dict += "}"
	file.writelines(poke_imports + poke_dict)
	file.close()

gen_number = get_generation_number(900)
folder_path = generate_folder("../data/Pokemons/", get_gen_region(GENERATIONS[gen_number]['name']))
generate_file(folder_path, HEHE)
generate_pokemon_relations_file()

# print(POKEMON[3]['name'])

# fichier = open("../data/" + GENERATIONS ".py", "w")
# print(fichier)