"""
Programme principal

Usage:
------
    python prog_threading.py file.fasta file.pdb

      - file.fasta: fichier fasta de la protéine cible (data/FASTA-file/)
      - file.pdb: fichier pdb de la protéine modèle (data/PDB-file/)

   exemple
     python prog_threading.py 2KJM.fasta 2kjm.pdb
"""

import sys
from __modules__.fasta_file import read_fasta_file
from __modules__.pdb_file import read_pdb_file
from __modules__.dope_file import save_dope
from __modules__.matrix import *


def arguments():
    """Vérifie que 2 arguments sont passés en paramètre.

      - Le fichier fasta de la protéine cible.
      - Le fichier pdb de la protéine modèle.
    """
    if len(sys.argv) != 3:
        sys.exit('Veuillez renseigner 2 arguments\n'
                 '  - La protéine cible (.fasta)\n'
                 '  - La protéine modèle (.pdb)')
    pass


if __name__ == "__main__":
    arguments()
    distance = read_pdb_file(sys.argv[2])  # Matrice de distance
    sequence = read_fasta_file(sys.argv[1])  # Protéine cible
    dope = save_dope()

    # Initilaliser la matrice de haut niveau
    high_level = Matrice(template=list(distance.columns), sequence=sequence)
    high_level.create_zero_matrix()

    # Générer les matrices de bas niveau
    for row in range(1, high_level.nb_rows):
        for col in range(1, high_level.nb_cols):
            low_level = Matrice(template=list(distance.columns),
                                sequence=sequence)
            low_level.create_zero_matrix()

            aa_fixed = {'Name': high_level.row_names[row], 'Pos': (row, col)}
            low_level.remplissage_matrice(dope, distance, aa_fixed)

            high_level.matrice[row][col] = low_level.score_opti



    high_level.show_matrix()
