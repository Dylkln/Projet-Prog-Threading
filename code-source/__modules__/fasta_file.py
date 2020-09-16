"""
Ce module permet de lire un fichier fasta passé en paramètre.

Le fichier fasta correspond à la protéine cible dont on souhaite déterminer la
structure 3D à partir de sa séquence en acides aminés.

Le module permet de:
  - Lire un fichier fasta stocké dans data/FASTA-file/
  - Vérifier que le fichier fasta existe
  - Convertir la séquence code 1 lettre en code à 3 lettres

Instruction python if __name__ == "__main__":
  - Si le programme read_file.py est exécuté en tant que script dans un shell,
    renvoie true et execute le bloc d'instruction correspondant.
  - Si le programme read_file.py est importé en tant que module, renvoie false
    et non execution du bloc d'instruction.
"""

import os
import sys


def valide_fasta_file(fasta, path):
    """Vérifie que le fichier fasta passé en paramètre est valide.

    I.E:
      - fichier au format fasta
      - fichier présent dans le répertoire data/FASTA-file/

    Parameter
    ---------
    fasta: str
        le nom du fichier fasta
    path: str
        le path des fichiers fasta

    Return
    ------
    Boolean
      - True: fichier valide
      - False: fichier non valide
    """
    if fasta.endswith('fasta') and os.path.exists(path + fasta):
        return True
    return False


def convertir_sequence(seq_1_lettre):
    """Convertit la séquence code 1 lettre en code à 3 lettres.

    Parameter
    --------
    seq_1_lettre: str
        la séquence en acides aminés de la protéine cible (code 1 lettre)

    Return
    ------
    seq_3_lettres: list
        la séquence en acides aminés de la protéine cible (code 3 lettres)
    """
    dico_aa = {
        "D": 'ASP', "E": 'GLU', "H": 'HIS', "R": 'ARG', "Y": 'TYR', "C": 'CYS',
        "K": 'LYS', "A": 'ALA', "V": 'VAL', "I": 'ILE', "L": 'LEU', "M": 'MET',
        "F": 'PHE', "W": 'TRP', "N": 'ASN', "Q": 'GLN', "S": 'SER', "T": 'THR',
        "P": 'PRO', "G": 'GLY'
    }
    seq_3_lettres = []

    for aa in seq_1_lettre:
        seq_3_lettres.append(dico_aa[aa])

    return seq_3_lettres


def read_fasta_file(fasta):
    """Lit le fichier fasta passé en paramètre.

    Parameter
    ---------
    fasta: str
        le nom du fichier fasta

    Return
    ------
    seq_3_lettres: list
        la séquence en acides aminés de la protéines cible (code 3 lettres)
    """
    path = "../data/FASTA-file/"

    if valide_fasta_file(fasta, path):
        with open(path + fasta, "r") as filin:
            seq_1_lettre = ""
            for line in filin:
                if not line.startswith(">"):
                    seq_1_lettre += line.strip()
        seq_3_lettres = convertir_sequence(seq_1_lettre)

    else:
        raise Exception("Veuillez renseigner un fichier fasta valide!")

    return seq_3_lettres


if __name__ == "__main__":
    sys.exit()
