# def add_card_to_anki(pokemon):
#     note = {
#         "deckName": "Pokedex Gen 1",
#         "modelName": "Basic",
#         "fields": {
#             "Front": f"<img src='{pokemon['sprite']}'><br>{pokemon['name']}<br>Types: {', '.join(pokemon['types'])}",
#             "Back": f"N° {pokemon['number']}<br>Évolutions: {', '.join(pokemon['evolutions']) if pokemon['evolutions'] else 'N/A'}<br>Faiblesses: {', '.join(pokemon['weaknesses'])}"
#         },
#         "options": {
#             "allowDuplicate": False
#         },
#         "tags": ["pokemon", "gen1"]
#     }
    
#     res = requests.post("http://localhost:8765", json={
#         "action": "addNote",
#         "version": 6,
#         "params": {
#             "note": note
#         }
#     }).json()
#     print(res)

# for i in range(1, 152):
#     pkmn = get_pokemon_data(i)
    # add_card_to_anki(pkmn)
