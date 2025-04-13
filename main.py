import asyncio
import pickle
from src.generate_data.generate_files import generate_folder
from src.anki.anki_utils import *
import genanki # type: ignore
import sys
from src.anki.print import *
from src.generate_data.generate_evolutions_file import generate_evolutions_file
from data.Knowledge.evolutions import EVOLUTIONS
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

def get_de_pokemon(name):
	if name[0].lower() in ('a', 'e', 'i', 'o', 'u'):
		return "d'" + name
	return "de " + name

def get_tags(pokemon_id, pokemon_name, types):
	tags = [pokemon_id + "-" + pokemon_name.replace(' ', '-')]
	for type in types:
		tags.append(type)
	return tags

def add_sprite(sprite, pokemon_name, tags):
	add_card_to_anki('<img src="' + sprite + '" />', pokemon_name, tags, model, deck)

def add_types_or_weaknesses(question_start, types_or_weaknesses, pokemon_name, tags):
	result_string = ""
	for type_or_weakness in types_or_weaknesses:
		result_string += type_or_weakness + ", "
	result_string = result_string[:-2]
	add_card_to_anki(f"{question_start} " + get_de_pokemon(pokemon_name), result_string, tags, model, deck)

def create_pokemon_cards(pokemon):
	tags = get_tags(pokemon['number'], pokemon['french_name'], pokemon['types'])
	add_card_to_anki("Numéro " + get_de_pokemon(pokemon['french_name']), pokemon['number'], tags, model, deck)
	add_card_to_anki("Nom anglais " + get_de_pokemon(pokemon['french_name']), pokemon['english_name'], tags, model, deck)
	add_sprite(pokemon['sprite'], pokemon['french_name'], tags)
	add_types_or_weaknesses("Types", pokemon['types'], pokemon['french_name'], tags)
	add_types_or_weaknesses("Faiblesses", pokemon['weaknesses'], pokemon['french_name'], tags)
	if pokemon['forms']:
		for form in pokemon['forms']:
			if (form['types'] is None):
				tags = get_tags(pokemon['number'], form['french_name'], pokemon['types'])
				add_sprite(form['sprite'], form['french_name'], tags)
			else:
				tags = get_tags(pokemon['number'], form['french_name'], form['types'])
				add_sprite(form['sprite'], form['french_name'], tags)
				add_types_or_weaknesses("Types", form['types'], form['french_name'], tags)
				add_types_or_weaknesses("Faiblesses", form['weaknesses'], form['french_name'], tags)

def parsing(argv): ###################
	if len(argv) != 2:
		raise ValueError("Vous devez indiquer le numéro d'une génération.")
	if argv[1].isnumeric() == False:
		raise ValueError(f"'{argv[1]}' n'est pas un numéro.")

def add_gen_pokemons(gen_number):
	first_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][0]
	last_pokemon_id = GENERATIONS[gen_number]['pokemon_range'][1] + 1
	for pokemon_id in range(first_pokemon_id, last_pokemon_id):
		asyncio.run(print_pokemon(POKEMON[pokemon_id], gen_number))
		create_pokemon_cards(POKEMON[pokemon_id])

RED = "\033[38;2;170;0;0m"
GREEN = "\033[38;2;0;170;0m"
RESET = "\033[0m"
def ou(chain, colour):
	print(colour + str(chain) + RESET)

def add_evolutions(gen_number):
	for i in range (GENERATIONS[gen_number]['pokemon_range'][0], GENERATIONS[gen_number]['pokemon_range'][1] + 1):
		if i in EVOLUTIONS:
			print(str(i) + ": ", end='', flush=True)
			for j in range(len(EVOLUTIONS[i])):
				if j == 0 and isinstance(EVOLUTIONS[i][j], list): # on veut 2 questions différentes (on a forcément que des listes)
					while j < len(EVOLUTIONS[i]):
						ou(EVOLUTIONS[i][j], RED)
						j += 1
					continue
					# for form in line:
					# 	print(form)
					# 	for j in range(len(form)):
					# 		print("\033[38;2;170;0;0m" + form[j] + "\033[0m", end='', flush=True)
					# 		if j < len(form):
					# 			print(' → ', end='', flush=True)
				else:
					ou(EVOLUTIONS[i][j], GREEN)
					# print(str(EVOLUTIONS[i][j]) + ', ', end='', flush=True)
			print("")

if __name__ == "__main__":
	# generate_evolutions_file(POKEMON)
	add_evolutions(1)
	# try:
	# 	parsing(sys.argv)
	# 	gen_number = sys.argv[1]
	# 	gen_id = int(str((gen_number * (10 // len(gen_number) + 1)))[:10])
	# 	gen_number = int(gen_number)
	# 	if gen_number not in GENERATIONS:
	# 		raise ValueError("Cette génération n'existe pas.")
		
	# 	model = add_model_to_anki(gen_id, GENERATIONS[gen_number]['name'], 
	# 		GENERATIONS[gen_number]['text_color'], GENERATIONS[gen_number]['background_image'])
	# 	deck = genanki.Deck(gen_id, GENERATIONS[gen_number]['name'])

	# 	asyncio.run(print_download(gen_number))
	# 	add_gen_pokemons(gen_number)
	# 	print("Fini ! Tu peux dès maintenant importer le paquet dans Anki, depuis le dossier anki_decks !")
		
	# 	generate_folder("./anki_decks", "")
	# 	my_package = genanki.Package(deck)
	# 	my_package.write_to_file("./anki_decks/" + GENERATIONS[gen_number]['name'] + '.apkg')
		
	# except ValueError as ve:
	# 	print("Error:", ve)
