"""
Ce module permet de nettoyer le fichier dope.par.

  - Il n'est pris en compte que les interactions atoms atoms.
    "atoms" est renseigné par l'utilisateur, par défaut il vaut CA
  - Si le fichier dope-CA.par existe déja, pas de nettoyage
  - Les données présentes dans le fichier dope-CA.par sont stockées

Instruction python if __name__ == "__main__":
  - Si le programme read_file.py est exécuté en tant que script dans un shell,
    renvoie true et execute le bloc d'instruction correspondant.
  - Si le programme read_file.py est importé en tant que module, renvoie false
    et non execution du bloc d'instruction.
"""

import os
import sys


def nettoyage_dope_file(atoms):
    """Lit le fichier dope.par et sélectionne les interactions atoms atoms.

    Parameter
    ---------
    atoms: str
        les atomes à prendre en compte dans le fichier DOPE
    """
    path = f"../data/dope-{atoms}.par"
    if os.path.exists(path):
        return None

    dope_atoms = []
    with open("../data/dope.par", "r") as filin:
        line = filin.readline()
        while line != "":
            tmp = line.split()
            if tmp[1] == tmp[3] == atoms:
                dope_atoms.append(line)
            line = filin.readline()

    with open(f"../data/dope-{atoms}.par", "w") as filout:
        for line in dope_atoms:
            filout.write("{}".format(line))


def save_dope(atoms):
    """Le main du programme.

    Parameter
    ---------
    atoms: str
        les atomes à prendre en compte dans le fichier DOPE
    """
    nettoyage_dope_file(atoms)
    data_dope = {}

    with open(f"../data/dope-{atoms}.par", "r") as filin:
        lines = filin.readlines()
        for line in lines:
            tmp = line.split()
            if tmp[0] not in data_dope.keys():
                data_dope[tmp[0]] = {}
            data_dope[tmp[0]][tmp[2]] = tmp[4:34]

    return data_dope


if __name__ == "__main__":
    sys.exit()
