import pickle
from generate_data.generate_files import generate_pokedex
from anki.anki_utils import *
import sys
from anki.print import *
from anki.generate_deck import get_anki_deck
from utils import get_starters
from pokedle.main import pokedle
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

RED = "\033[38;2;210;30;30m"
BLUE = "\033[38;2;0;100;200m"
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
              "name": "pokedle",
              "description": "Lance un jeu pour deviner un pokémon.",
    },
    {
        "name": "get_starters",
        "description": "Affiche les starters de toutes les générations.",
    },
    {
        "name": "reset_data",
        "description": "Met à jour la base de données. À faire s'il n'y a aucune autre solution.",
    },
    {
        "name": "exit",
        "description": "Quitter le menu.",
    }
]

def parsing_gen(function, cols = None, lines = None):
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
            if (cols):
                function(gen_number, cols, lines)
            else:
                function(gen_number)

if __name__ == "__main__":
    try:
        print("Que souhaitez-vous faire ? Voici l'inventaire des commandes disponibles :")
        display_commands()
        # input_command = input()
        invalid_command = True
        while invalid_command:
            invalid_command = False
            print("\nCommande : ", end='', flush=True)
            match input():
                case "help":
                    display_commands()
                    invalid_command = True
                case "get_anki_deck":
                    parsing_gen(get_anki_deck)
                case "pokedle":
                    parsing_gen(pokedle, sys.argv[1], sys.argv[2])
                case "get_starters":
                    get_starters()
                case "reset_data":
                    print("Êtes-vous vraiment sûr de vouloir lancer cette commande ? Écrivez \"Oui\" pour confirmer. Autre chose pour annuler.")
                    print("Confirmation : ", end='', flush=True)
                    confirmation = input()
                    if (confirmation == "Oui"):
                        generate_pokedex()
                case "exit":
                    break
                case _:
                    print("Commande introuvable. Pour rappel, voici les commandes disponibles :")
                    display_commands()
                    invalid_command = True
        
    except ValueError as ve:
        print("Error:", ve)
