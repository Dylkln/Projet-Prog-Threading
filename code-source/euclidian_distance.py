"""
Ce programme permet de créer une matrice de distance euclidienne 3D.
Il ne prend en compte que les carbones alphas d'un fichier pdb.

Usage:
------
    python euclidian_distance.py
"""

######################## Modules #########################



import sys
import numpy as np
import pandas as pd




##########################################################

def save_coord(fichier):
    """Lit un fichier pdb.

    Sauvegarde dans un dictionnaire les coordonnées x, y et z des atomes.

    Parameters
    ----------
    fichier: string
        fichier pdb à lire
    arg1: string

    Returns
    -------
    coor: dictionary
        coordonnées x, y et z des atomes
    """
    coord = {}
    with open(f"../data/pdb-files/{fichier}", "r") as filin:
        lines = filin.readlines()
        for line in lines:
            if line.startswith("ATOM"):
                num_atom = int(line[7:11])
                if line[12:16].strip() == "CA":
                    coord[num_atom] = np.array(extract_coord(line))
                else:
                    continue
    return coord


def extract_coord(line):
    """Extrait les coordonnées x, y et z d'une ligne ATOM d'un fichier pdb.

     Parameters
    ----------
    line: string
        une ligne ATOM du fichier pdb

    Returns
    -------
    coord: list
        liste des coordonnées x, y et z d'un atome
    """
    coord_x = float(line[30:38])
    coord_y = float(line[38:46])
    coord_z = float(line[46:54])
    coord = [coord_x, coord_y, coord_z]
    return coord


def create_euclidian_matrix(coord_dict):
	"""créé une matrice de distance euclidienne à partir des coordonnées des
	atomes.

     Parameters
    ----------
    coord_dict: dictionnaire
        dictionnaire contenant en clé le numéro de l'atome et en valeur
        la liste représentant les coordonnées x, y et z de l'atome

    Returns
    -------
    matrix: DataFrame
        Dataframe contenant les distances euclidiennes entre chaque atome
    """
	cles = []
	valeurs = []
	rows_cols = len(coord_dict.keys())

	matrix = pd.DataFrame(np.zeros((rows_cols, rows_cols)))
	matrix.columns = coord_dict.keys()
	matrix.index = coord_dict.keys()

	for cle, valeur in coord_dict.items():
		cles.append(cle)
		valeurs.append(valeur)

	for i in range(len(cles)):
		for j in range(len(cles)):
			a = valeurs[i]
			b = valeurs[j]
			distance = np.linalg.norm(a - b)
			matrix[cles[i]][cles[j]] = distance

	return matrix



def main():
	
	fichier_pdb = input("Quel est le nom du fichier .pdb à analyser (sans l'extension) ? (fichier test = 2kjm) ") + ".pdb"
	coord_dict = save_coord(fichier_pdb)
	matrix = create_euclidian_matrix(coord_dict)
	matrix = matrix.round(4)

if __name__ == "__main__":
    main()