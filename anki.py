import genanki # type: ignore
import requests # type: ignore

input_model = genanki.Model(
  123456789,
  'Pokémon',
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
  css='.card {font-family: arial;font-size: 20px;text-align: center;color: black;background-color: white;}'
  )

note = genanki.Note(
  model=input_model,
  fields=['<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/76.png" />', 'ouiiiiii'])

deck = genanki.Deck(
  1111111111,
  'Rouge, Bleu et Jaune - Kanto')

deck.add_note(note)

my_package = genanki.Package(deck)

my_package.write_to_file('output.apkg')
