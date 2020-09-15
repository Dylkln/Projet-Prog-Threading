"""
Ce module permet de lire un fichier pdb passé en paramètre.

Le fichier pdb correspond à la structure modèle utilisé pour déterminer la
conformation 3D de la protéine cible.

Le module permet de:
  - Lire un fichier pdb stocké dans data/PDB-file/
  - Vérifier que le fichier pdb existe
  - Créer la matrice de distance euclidienne 3D des atomes de la potéine modèle
    Il n'est pris en compte que les Calpha

Instruction python if __name__ == "__main__":
  - Si le programme read_file.py est exécuté en tant que script dans un shell,
    renvoie true et execute le bloc d'instruction correspondant.
  - Si le programme read_file.py est importé en tant que module, renvoie false
    et non execution du bloc d'instruction.
"""

import os
import pandas as pd
import numpy as np
import sys


def valide_pdb_file(pdb, path):
    """Vérifie que le fichier pdb passer en paramètre est valide.

    I.E:
      - fichier au format pdb
      - fichier présent dans le répertoire data/PDB-file/

    Parameter
    ---------
    pdb: str
        le nom du fichier fasta
    path: str
        le path des fichiers fasta

    Return
    ------
    Boolean
      - True: fichier valide
      - False: fichier non valide
    """
    if pdb.endswith('pdb') and os.path.exists(path + pdb):
        return True
    return False


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
    with open(f"../data/PDB-file/{fichier}", "r") as filin:
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


def read_pdb_file(pdb):
    """Le main du programme."""
    path = "../data/PDB-file/"
    if valide_pdb_file(pdb, path):
        coord_dict = save_coord(pdb)
        matrix = create_euclidian_matrix(coord_dict)
        matrix = matrix.round(4)
    else:
        raise Exception("Veuillez renseigner un fichier pdb valide!")

    return matrix


if __name__ == "__main__":
    sys.exit()
