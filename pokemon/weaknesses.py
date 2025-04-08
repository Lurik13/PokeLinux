from utils import *
from data import *

# def calculate_damages(pokemon_types):
#     damage_relations = {}

#     for pokemon_type in pokemon_types:
#         type_relations = TYPE_RELATIONS[pokemon_type]
#         for category, multiplier in DAMAGE_MULTIPLIER.items():
#             for type_name in type_relations[category]:
#                 if type_name not in damage_relations:
#                     damage_relations[type_name] = 1
#                 damage_relations[type_name] *= multiplier

#     return damage_relations


# def get_weaknesses(types):
#     damage_relations = calculate_damages(types)
#     critical_weaknesses = []
#     normal_weaknesses = []

#     for name, damage in damage_relations.items():
#         if damage == 4:
#             critical_weaknesses.append(TYPE_TRANSLATION[name] + '*')
#         elif damage == 2:
#             normal_weaknesses.append(TYPE_TRANSLATION[name])

#     return critical_weaknesses + normal_weaknesses
