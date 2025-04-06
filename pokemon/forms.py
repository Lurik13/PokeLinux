from pokemon.weaknesses import *
from pokemon.utils import *
from pokemon.data import SPRITE_URL

def get_sprite(form_data):
    form_url = form_data["pokemon"]["url"]
    form_id = form_url.strip("/").split("/")[-1]
    return SPRITE_URL.format(form_id)

def get_forms(species):
    forms = []
    for form in species['varieties']:
        if form['is_default'] is False:
            form_dict = {
                'french_name': "",
                'sprite': "",
                'types': None,
                'weaknesses': None
            }
            form_data = get_data('pokemon-form', form['pokemon']['name'])

            if form['pokemon']['name'].endswith('gmax') == False \
             and form['pokemon']['name'].startswith('pikachu') == False:
                types = [t["type"]["name"] for t in form_data["types"]]
                form_dict['types'] = [TYPE_TRANSLATION[t] for t in types]
                form_dict['weaknesses'] = get_weaknesses(types)
            form_dict['french_name'] = get_french_name(form_data)
            form_dict['sprite'] = get_sprite(form_data)
            forms.append(form_dict)
    return forms
