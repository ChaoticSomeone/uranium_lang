from src import errors

"""
This file contains the BuiltIns class, which contains all standard libraries and
functions, constants, ... they define for the actual Uranium program
"""
class BuiltIns:
	LIBS = {
		"io": [
			"print",
			"println",
			"read"
		],

		"random": [
			"randint",
			"randfloat",
			"randstring",
			"randbool"
		]
	}
