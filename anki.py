import genanki # type: ignore
import sys
from pokemon.get_pokemon import *

def add_model_to_anki(gen_id, name, text_color, background_image):
  model = genanki.Model(
    gen_id,
    name,
    fields=[
      {'name': 'Recto'},
      {'name': 'Verso'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Recto}}{{type:Verso}}',
        'afmt': '{{Recto}}<hr id=answer>{{type:Verso}}',
      },
    ],
    css=f'.card {{font-family: arial;font-size: 20px;text-align: center; \
      color: {text_color} !important;font-weight: bold; \
      background-image: url("{background_image}");background-size: cover; \
      background-position: center;background-repeat: no-repeat;}}'
    )
  return model

def get_de_pokemon(name):
   if name[0].lower() in ('a', 'e', 'i', 'o', 'u'):
      return "d'" + name
   return "de " + name

def add_card_to_anki(question, answer, tags):
  note = genanki.Note(
    model=model,
    fields=[question, answer],
    tags=tags
  )
  deck.add_note(note)

def get_tags(pokemon_id, pokemon_name, types):
  tags = [pokemon_id + "-" + pokemon_name.replace(' ', '-')]
  for type in types:
    tags.append(type)
  return tags

def add_sprite(sprite, pokemon_name, tags):
  add_card_to_anki('<img src="' + sprite + '" />', pokemon_name, tags)

def add_types_or_weaknesses(question_start, types_or_weaknesses, pokemon_name, tags):
  result_string = ""
  for type_or_weakness in types_or_weaknesses:
    result_string += type_or_weakness + ", "
  result_string = result_string[:-2]
  add_card_to_anki(f"{question_start} " + get_de_pokemon(pokemon_name), result_string, tags)

def create_pokemon_cards(pokemon):
  tags = get_tags(pokemon['number'], pokemon['french_name'], pokemon['types'])
  add_card_to_anki("Numéro " + get_de_pokemon(pokemon['french_name']), pokemon['number'], tags)
  add_card_to_anki("Nom anglais " + get_de_pokemon(pokemon['french_name']), pokemon['english_name'], tags)
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

def parsing(argv):
  if len(argv) != 2:
    raise ValueError("Vous indiquer le numéro d'une génération.")
  if argv[1].isnumeric() == False:
    raise ValueError(f"'{argv[1]}' n'est pas un numéro.")

if __name__ == "__main__":
    try:
      parsing(sys.argv)
      gen_number = sys.argv[1]
      gen_id = int((gen_number * (10 // len(gen_number) + 1))[:10])
      if gen_number not in GENERATIONS:
        raise ValueError("Cette génération n'existe pas.")
      
      model = add_model_to_anki(gen_id, GENERATIONS[gen_number]['name'], 
        GENERATIONS[gen_number]['text_color'], GENERATIONS[gen_number]['background_image'])
      deck = genanki.Deck(gen_id, GENERATIONS[gen_number]['name'])
      first_pokemon = GENERATIONS[gen_number]['pokemon_range'][0]
      last_pokemon = GENERATIONS[gen_number]['pokemon_range'][1]
      for pokemon_id in range(first_pokemon, last_pokemon):
        pokemon = get_pokemon(pokemon_id)
        print("En train de créer les cartes de " + pokemon['french_name'])
        create_pokemon_cards(pokemon)

      my_package = genanki.Package(deck)
      my_package.write_to_file(GENERATIONS[gen_number]['name'] + '.apkg')
      
    except ValueError as ve:
       print("Error:", ve)
