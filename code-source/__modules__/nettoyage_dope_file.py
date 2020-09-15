"""
Ce module permet de nettoyer le fichier dope.par.

Il n'est pris en compte que les interactions CA CA.

Si le fichier dope.par existe déja aucune action n'est réalisée.

Instruction python if __name__ == "__main__":
  - Si le programme read_file.py est exécuté en tant que script dans un shell,
    renvoie true et execute le bloc d'instruction correspondant.
  - Si le programme read_file.py est importé en tant que module, renvoie false
    et non execution du bloc d'instruction.
"""

import os
import sys


def nettoyage_dope_file():
    """Lit le fichier dope.par et sélectionne que les intercations CA CA."""
    path = "../data/dope-CA.par"
    if os.path.exists(path):
        return None

    dope_ca = []
    with open("../data/dope.par", "r") as filin:
        line = filin.readline()
        while line != "":
            tmp = line.split()
            if tmp[1] == tmp[3] == 'CA':
                dope_ca.append(line)
            line = filin.readline()

    with open("../data/dope-CA.par", "w") as filout:
        for line in dope_ca:
            filout.write("{}".format(line))


if __name__ == "__main__":
    sys.exit()
