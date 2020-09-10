"""
Ce programme permet de nettoyer le fichier dope.par.

Il n'est pris en compte que les interactions CA CA.

Usage:
------
    python nettoyage-dope-file.py
"""

def nettoyage_file():
    """Lit le fichier dope.par et sélectionne que les intercations CA CA."""
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
    nettoyage_file()
