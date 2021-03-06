"""
Ce module permet de lire un fichier pdb passé en paramètre.

Le fichier pdb correspond à la structure modèle utilisée pour déterminer la
conformation 3D de la protéine cible.

Un seul modèle contenu dans le fichier pdb est pris en compte.

Le module permet de:
  - Lire un fichier pdb stocké dans data/PDB-file/
  - Vérifier que le fichier pdb existe
  - Créer la matrice de distance euclidienne des atomes de la protéine modèle
    Il n'est pris en compte que les Calpha

Instruction python if __name__ == "__main__":
  - Si le programme read_file.py est exécuté en tant que script dans un shell,
    renvoie true et execute le bloc d'instruction correspondant.
  - Si le programme read_file.py est importé en tant que module, renvoie false
    et non execution du bloc d'instruction.
"""

import pandas as pd
import numpy as np
import sys


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

    with open(fichier, "r") as filin:
        lines = filin.readlines()
        for line in lines:
            if line.startswith("ENDMDL"):
                return coord
            if line.startswith("ATOM"):
                num_atom = int(line[7:11])
                if line[12:16].strip() == "CA":
                    coord[num_atom] = np.array(extract_coord(line))

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
    """Créer une matrice de distance euclidienne.

    Et ceux à partir des coordonnées des atomes.

    Parameters
    ----------
    coord_dict: dictionary
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
    coord_dict = save_coord(pdb)
    matrix = create_euclidian_matrix(coord_dict)
    matrix = matrix.round(4)

    return matrix


if __name__ == "__main__":
    sys.exit()
