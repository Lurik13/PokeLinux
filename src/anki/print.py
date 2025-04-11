import os
import sys
import asyncio

sys.path.append(os.path.abspath('../..'))
from data.Knowledge.generations import *
from data.Knowledge.others import TYPE_COLOURS

async def print_text_slowly(text, delay = 0.015):
	for char in text:
		print(char, end='', flush=True)
		if char.isdigit() == False and char != ";" and char != "\\":
			await asyncio.sleep(delay)

async def print_download(gen_number):
	await print_text_slowly("Téléchargement du deck de la génération " + str(gen_number) + " : " \
		+ GENERATIONS[gen_number]['name'] + " ...\n", 0.05)
	
def get_pokemon_in_colour(name, types):
	reset_colour = "\033[0m"
	if (len(types) == 1):
		return TYPE_COLOURS[types[0]] + name + reset_colour
	first_mid_name = name[:len(name) // 2]
	second_mid_name = name[len(name) // 2:]
	return TYPE_COLOURS[types[0]] + first_mid_name + TYPE_COLOURS[types[1]] + second_mid_name + reset_colour

	
async def print_pokemon(pokemon, gen_number):
	for i in range(len(pokemon['evolution_chain'])):
		if pokemon['number'] == pokemon['evolution_chain'][i]['id']:
			pokemon_in_colour = get_pokemon_in_colour(pokemon['french_name'], pokemon['types'])
			await print_text_slowly(pokemon_in_colour)
			if i == len(pokemon['evolution_chain']) - 1 \
					or int(pokemon['evolution_chain'][i + 1]['id']) < GENERATIONS[gen_number]['pokemon_range'][0] \
					or int(pokemon['evolution_chain'][i + 1]['id']) > GENERATIONS[gen_number]['pokemon_range'][1]:
				await print_text_slowly("\n")
			else:
				await print_text_slowly(', ')
