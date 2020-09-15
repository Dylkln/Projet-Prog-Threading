"""
Ce programme permet de sauvegarder les données présentes dans le fichier dope-CA.par.

Usage:
------
    python save_dope.py
"""


def save_dope():

	data_dope = {}
	with open("../data/dope-CA.par", "r") as filin:
		lines = filin.readlines()
		for line in lines:
			tmp = line.split()
			if tmp[0] not in data_dope.keys():
				data_dope[tmp[0]] = {}
			data_dope[tmp[0]][tmp[2]] = tmp[4:34]

	return data_dope

def main():
	data_dope = save_dope()


if __name__ == "__main__":
    main()