import genanki # type: ignore

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

def add_card_to_anki(question, answer, tags, model, deck):
  note = genanki.Note(
    model=model,
    fields=[question, answer],
    tags=tags
  )
  deck.add_note(note)

