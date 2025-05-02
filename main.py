import pickle
from prompt_toolkit import prompt # type: ignore
import sys
from data.Knowledge.generations import GENERATIONS
from src.anki.generate_deck import get_anki_deck
from src.generate_data.generate_files import generate_pokedex
from src.pokedle.input import AccentInsensitiveCompleter
from src.pokedle.main import pokedle
from src.pokedle.utils import BLUE, RED, RESET
from src.utils import get_starters, normalize
with open("data/Pokédex/pokemon_relations.pkl", "rb") as executable:
    POKEMON = pickle.load(executable)

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

def parsing_gen(function):
    valid = False
    print("Veuillez indiquer le numéro d'une génération. 0 pour sortir.")
    while not valid:
        print("Génération : ", end='', flush=True)
        gen_number = input()
        if not len(gen_number):
            print(RED + "Vous devez indiquer le numéro d'une génération." + RESET)
        elif gen_number.isnumeric() == False:
            print(RED + f"'{gen_number}' n'est pas un numéro positif." + RESET)
        elif int(gen_number) == 0:
            valid = True
        elif int(gen_number) not in GENERATIONS:
            print(RED + f"La génération '{gen_number}' n'existe pas selon mes sources." + RESET)
        else:
            valid = True
            function(gen_number)

if __name__ == "__main__":
    try:
        input_choices = ['help', 'get_anki_deck', 'pokedle', 'get_starters', 'reset_data', 'exit']
        completer = AccentInsensitiveCompleter(input_choices)
        print("Que souhaitez-vous faire ? Voici l'inventaire des commandes disponibles :")
        display_commands()
        invalid_command = True
        while invalid_command:
            invalid_command = False
            new_input = normalize(prompt('Commande : ', completer=completer, complete_while_typing=True))
            match new_input:
                case "help":
                    display_commands()
                    invalid_command = True
                case "get_anki_deck":
                    parsing_gen(get_anki_deck)
                case "pokedle":
                    pokedle(int(sys.argv[1]))
                case "get_starters":
                    get_starters()
                case "reset_data":
                    confirmation = prompt("Êtes-vous vraiment sûr de vouloir lancer cette commande ? Écrivez \"Oui\" pour confirmer. Autre chose pour annuler.\nConfirmation : ",
                        completer=AccentInsensitiveCompleter(['Oui']), complete_while_typing=True)
                    if (normalize(confirmation) == normalize("Oui")):
                        generate_pokedex()
                case "exit":
                    break
                case _:
                    print("Commande introuvable. Pour rappel, voici les commandes disponibles :")
                    display_commands()
                    invalid_command = True
        
    except ValueError as ve:
        print("Error:", ve)
