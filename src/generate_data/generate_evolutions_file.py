
def generate_evolutions_file(pokemon):
    evolution_chains_cache = {}
    for i in range(1, len(pokemon) + 1):
        chain = pokemon[i]['evolution_chain']
        chain_id = int(chain[0]['id'])
        if chain_id not in evolution_chains_cache:
            new_chain = []
            for poke in chain:
                new_chain.append(poke['name'])
            evolution_chains_cache[chain_id] = new_chain
        for form in pokemon[i]['forms']:
            name = form['french_name']
            if all(x not in name for x in ["Méga-", "Gigamax", "Dominant", "Forme"]):
                evolution_chains_cache[chain_id].append(name)

    print('EVOLUTIONS = {')
    for i in range(1, len(pokemon) + 1):
        if (i in evolution_chains_cache):
            print("    " + str(i) + ": ", end='', flush=True)
            print(str(evolution_chains_cache[i]) + ",")
    print('}')
