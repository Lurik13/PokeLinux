def get_de_pokemon(name):
	if name[0].lower() in ('a', 'e', 'i', 'o', 'u'):
		return "d'" + name
	return "de " + name
