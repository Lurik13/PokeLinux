SPRITE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{}.png"

TYPE_TRANSLATION = {
    "normal": "Normal",
    "fire": "Feu",
    "water": "Eau",
    "electric": "Électrik",
    "grass": "Plante",
    "ice": "Glace",
    "fighting": "Combat",
    "poison": "Poison",
    "ground": "Sol",
    "flying": "Vol",
    "psychic": "Psy",
    "bug": "Insecte",
    "rock": "Roche",
    "ghost": "Spectre",
    "dragon": "Dragon",
    "dark": "Ténèbres",
    "steel": "Acier",
    "fairy": "Fée"
}

DAMAGES = {
    "double_damage_from": 2,
    "half_damage_from": 0.5,
    "no_damage_from": 0
}

TYPE_RELATIONS = {
    "normal": {
        "double_damage_from": [
            "fighting"
        ],
        "half_damage_from": [],
        "no_damage_from": [
            "ghost"
        ]
    },
    "fire": {
        "double_damage_from": [
            "ground",
            "rock",
            "water"
        ],
        "half_damage_from": [
            "bug",
            "steel",
            "fire",
            "grass",
            "ice",
            "fairy"
        ],
        "no_damage_from": []
    },
    "water": {
        "double_damage_from": [
            "grass",
            "electric"
        ],
        "half_damage_from": [
            "steel",
            "fire",
            "water",
            "ice"
        ],
        "no_damage_from": []
    },
    "electric": {
        "double_damage_from": [
            "ground"
        ],
        "half_damage_from": [
            "flying",
            "steel",
            "electric"
        ],
        "no_damage_from": []
    },
    "grass": {
        "double_damage_from": [
            "flying",
            "poison",
            "bug",
            "fire",
            "ice"
        ],
        "half_damage_from": [
            "ground",
            "water",
            "grass",
            "electric"
        ],
        "no_damage_from": []
    },
    "ice": {
        "double_damage_from": [
            "fighting",
            "rock",
            "steel",
            "fire"
        ],
        "half_damage_from": [
            "ice"
        ],
        "no_damage_from": []
    },
    "fighting": {
        "double_damage_from": [
            "flying",
            "psychic",
            "fairy"
        ],
        "half_damage_from": [
            "rock",
            "bug",
            "dark"
        ],
        "no_damage_from": []
    },
    "poison": {
        "double_damage_from": [
            "ground",
            "psychic"
        ],
        "half_damage_from": [
            "fighting",
            "poison",
            "bug",
            "grass",
            "fairy"
        ],
        "no_damage_from": []
    },
    "ground": {
        "double_damage_from": [
            "water",
            "grass",
            "ice"
        ],
        "half_damage_from": [
            "poison",
            "rock"
        ],
        "no_damage_from": [
            "electric"
        ]
    },
    "flying": {
        "double_damage_from": [
            "rock",
            "electric",
            "ice"
        ],
        "half_damage_from": [
            "fighting",
            "bug",
            "grass"
        ],
        "no_damage_from": [
            "ground"
        ]
    },
    "psychic": {
        "double_damage_from": [
            "bug",
            "ghost",
            "dark"
        ],
        "half_damage_from": [
            "fighting",
            "psychic"
        ],
        "no_damage_from": []
    },
    "bug": {
        "double_damage_from": [
            "flying",
            "rock",
            "fire"
        ],
        "half_damage_from": [
            "fighting",
            "ground",
            "grass"
        ],
        "no_damage_from": []
    },
    "rock": {
        "double_damage_from": [
            "fighting",
            "ground",
            "steel",
            "water",
            "grass"
        ],
        "half_damage_from": [
            "normal",
            "flying",
            "poison",
            "fire"
        ],
        "no_damage_from": []
    },
    "ghost": {
        "double_damage_from": [
            "ghost",
            "dark"
        ],
        "half_damage_from": [
            "poison",
            "bug"
        ],
        "no_damage_from": [
            "normal",
            "fighting"
        ]
    },
    "dragon": {
        "double_damage_from": [
            "ice",
            "dragon",
            "fairy"
        ],
        "half_damage_from": [
            "fire",
            "water",
            "grass",
            "electric"
        ],
        "no_damage_from": []
    },
    "dark": {
        "double_damage_from": [
            "fighting",
            "bug",
            "fairy"
        ],
        "half_damage_from": [
            "ghost",
            "dark"
        ],
        "no_damage_from": [
            "psychic"
        ]
    },
    "steel": {
        "double_damage_from": [
            "fighting",
            "ground",
            "fire"
        ],
        "half_damage_from": [
            "normal",
            "flying",
            "rock",
            "bug",
            "steel",
            "grass",
            "psychic",
            "ice",
            "dragon",
            "fairy"
        ],
        "no_damage_from": [
            "poison"
        ]
    },
    "fairy": {
        "double_damage_from": [
            "poison",
            "steel"
        ],
        "half_damage_from": [
            "fighting",
            "bug",
            "dark"
        ],
        "no_damage_from": [
            "dragon"
        ]
    }
}
