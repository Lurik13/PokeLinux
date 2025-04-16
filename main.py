import asyncio
import pickle
from src.generate_data.generate_files import generate_folder, generate_pokedex
from src.anki.anki_utils import *
import genanki # type: ignore
import sys
from src.anki.print import *
from src.generate_data.generate_evolutions_file import generate_evolutions_file
from data.Knowledge.evolutions import EVOLUTIONS
from src.anki.generate_deck import add_evolutions, add_pokemons, get_anki_deck
from src.utils import get_starters
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

RED = "\033[38;2;170;0;0m"
BLUE = "\033[38;2;0;50;150m"
RESET = "\033[0m"


def display_commands():
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
		"name": "get_starters",
		"description": "Affiche les starters de toutes les générations.",
	},
	{
      		"name": "pokedle",
      		"description": "Lance un jeu pour deviner un pokémon.",
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
		elif int(gen_number) not in GENERATIONS:
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
		# input_command = input()
		while True:
			print("\nCommande : ", end='', flush=True)
			match input():
				case "help":
					display_commands()
				case "get_anki_deck":
					parsing_get_anki_deck()
					break
				case "get_starters":
					get_starters()
					break
				case "generate_data":
					print("Êtes-vous vraiment sûr de vouloir lancer cette commande ? Écrivez \"Oui\" pour confirmer. Autre chose pour annuler.")
					print("Confirmation : ", end='', flush=True)
					confirmation = input()
					if (confirmation == "Oui"):
						generate_pokedex()
						break
				case "exit":
					break
				case _:
					print("Commande introuvable. Pour rappel, voici les commandes disponibles :")
					display_commands()
		
	except ValueError as ve:
		print("Error:", ve)
