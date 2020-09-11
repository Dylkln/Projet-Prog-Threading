"""
Ce programme permet de nettoyer le fichier dope.par.

Il n'est pris en compte que les interactions CA CA.

Usage:
------
    python nettoyage-dope-file.py
"""

def nettoyage_fichier():
    """Lit le fichier dope.par et sélectionne que les interractions CA CA."""
    dope_ca = []

    with open("../data/dope.par", "r") as filin:
        ligne = filin.readline()
        while ligne != "":
            tmp = ligne.split()
            if tmp[1] == tmp[3] == 'CA':
                dope_ca.append(ligne)
            ligne = filin.readline()

    with open("../data/dope-CA.par", "w") as filout:
        for ligne in dope_ca:
            filout.write("{}".format(ligne))


if __name__ == "__main__":
    nettoyage_fichier()
