import requests # type: ignore

def get_weaknesses(types_api_names):
    damage_relations = {}

    for type_name in types_api_names:
        res = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}").json()
        for category, multiplier in {
            "double_damage_from": 2,
            "half_damage_from": 0.5,
            "no_damage_from": 0
        }.items():
            for t in res["damage_relations"][category]:
                # t_name = TYPE_TRADUCTION[t["name"]]
                t_name = t["name"]
                if t_name not in damage_relations:
                    damage_relations[t_name] = 1
                damage_relations[t_name] *= multiplier
    weaknesses = []
    for name, damage in damage_relations.items():
        if damage == 4:
            weaknesses.append(name + '*')
    for name, damage in damage_relations.items():
        if damage == 2:
            weaknesses.append(name)

    return weaknesses
