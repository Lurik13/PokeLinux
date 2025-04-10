import time
import asyncio
from pokemon.data import *
from pokemon.get_pokemon import get_evolution_chain
from pokemon.utils import get_french_name

async def print_text_slowly(text, delay = 0.025):
	for char in text:
		print(char, end='', flush=True)
		await asyncio.sleep(delay)

async def print_download(gen_number):
	await print_text_slowly("Téléchargement du deck de la génération " + gen_number + " : " + GENERATIONS[gen_number]['name'] + " ...\n")

def print_pokemon(pokemon, gen_number):
	for i in range(len(pokemon['evolution_chain'])):
		if pokemon['evolution_chain'][i]['id'] == pokemon['species_data']['id']:
			print(pokemon['french_name'], end='', flush=True)
			if i == len(pokemon['evolution_chain']) - 1 \
					or pokemon['evolution_chain'][i + 1]['id'] < GENERATIONS[gen_number]['pokemon_range'][0] \
					or pokemon['evolution_chain'][i + 1]['id'] > GENERATIONS[gen_number]['pokemon_range'][1]:
				print("\n", end='', flush=True)
			else:
				print(', ', end='', flush=True)
