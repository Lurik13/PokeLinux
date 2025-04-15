import asyncio
import pickle
from src.generate_data.generate_files import generate_folder, generate_pokedex
from src.anki.anki_utils import *
import genanki # type: ignore
import sys
from src.anki.print import *
from src.generate_data.generate_evolutions_file import generate_evolutions_file
from data.Knowledge.evolutions import EVOLUTIONS
from src.functions.anki_deck import add_evolutions, add_pokemons, get_anki_deck
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)


def parsing(argv): ###################
	if len(argv) != 2:
		raise ValueError("Vous devez indiquer le numéro d'une génération.")
	if argv[1].isnumeric() == False:
		raise ValueError(f"'{argv[1]}' n'est pas un numéro.")

RED = "\033[38;2;170;0;0m"
BLUE = "\033[38;2;0;50;150m"
RESET = "\033[0m"


def display_commands(help = False):
	for command in COMMANDS:
		print(BLUE + command['name'] + RESET + " " * (20 - len(command['name'])) + command['description'])

COMMANDS = [
	{
		"name": "help",
		"description": "Affiche toutes les commandes disponibles.",
	},
	{
		"name": "get_anki_deck",
		"description": "Génère les cartes Anki de tous les pokémons d'une génération.",
	},
	{
		"name": "generate_data",
		"description": "Met à jour la base de données. À faire s'il n'y a aucune autre solution.",
	},
	{
		"name": "exit",
		"description": "Quitter le menu.",
	}
]

def parsing_get_anki_deck():
	valid = False
	print("Veuillez indiquer le numéro d'une génération. 0 pour sortir.")
	while not valid:
		print("Génération : ", end='', flush=True)
		gen_number = input()
		if not len(gen_number):
			print(RED + "Vous devez indiquer le numéro d'une génération." + RESET)
		elif gen_number.isnumeric() == False:
			print(RED + f"'{gen_number}' n'est pas un numéro positif." + RESET)
		elif int(gen_number) < 1 or int(gen_number) > list(GENERATIONS.keys())[-1]:
			print(RED + f"La génération '{gen_number}' n'existe pas selon mes sources." + RESET)
		elif int(gen_number) == 0:
			valid = True
		else:
			valid = True
			get_anki_deck(gen_number)

if __name__ == "__main__":
	# generate_evolutions_file(POKEMON)
	try:
		print("Que souhaitez-vous faire ? Voici l'inventaire des commandes disponibles :")
		display_commands()
		print("\nCommande : ", end='', flush=True)
		# input_command = input()
		match input():
			case "help":
				display_commands(True)
			case "get_anki_deck":
				parsing_get_anki_deck()

		# parsing(sys.argv)
		# gen_number = sys.argv[1]
		# gen_id = int(str((gen_number * (10 // len(gen_number) + 1)))[:10])
		# gen_number = int(gen_number)
		# if gen_number not in GENERATIONS:
		# 	raise ValueError("Cette génération n'existe pas.")
		
		# model = add_model_to_anki(gen_id, GENERATIONS[gen_number]['name'], 
		# 	GENERATIONS[gen_number]['text_color'], GENERATIONS[gen_number]['background_image'])
		# deck = genanki.Deck(gen_id, GENERATIONS[gen_number]['name'])

		# asyncio.run(print_download(gen_number))
		# add_pokemons(gen_number, model, deck)
		# add_evolutions(gen_number, model, deck)
		# print("Fini ! Tu peux dès maintenant importer le paquet dans Anki, depuis le dossier anki_decks !")
		
		# generate_folder("./anki_decks", "")
		# my_package = genanki.Package(deck)
		# my_package.write_to_file("./anki_decks/" + GENERATIONS[gen_number]['name'] + '.apkg')
		
	except ValueError as ve:
		print("Error:", ve)
