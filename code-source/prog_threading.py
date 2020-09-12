"""
Programme principal

Usage:
------
    python prog_threading.py file.fasta file.pdb

      - file.fasta: fichier fasta de la protéine cible (data/FASTA-file/)
      - file.pdb: fichier pdb de la protéine modèle (data/PDB-file/)
"""

import sys
from __modules__.fasta_file import *


def arguments():
    """Vérifie que 2 arguments sont passés en paramètre.

      - Le fichier fasta de la protéine cible.
      - Le fichier pdb de la protéine modèle.
    """
    if len(sys.argv) != 2: # != 3 quand on rajoutera le fichier pdb
        sys.exit('Veuillez renseigner 2 arguments\n'
                 '  - La protéine cible (.fasta)\n'
                 '  - La protéine modèle (.pdb)')
    pass


if __name__ == "__main__":
    arguments()
    protein = read_fasta_file(sys.argv[1])
