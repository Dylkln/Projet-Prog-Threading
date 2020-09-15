"""
Programme principal

Usage:
------
    python prog_threading.py file.fasta file.pdb

      - file.fasta: fichier fasta de la protéine cible (data/FASTA-file/)
      - file.pdb: fichier pdb de la protéine modèle (data/PDB-file/)

   exemple
     python prog_threading.py Q14493.fasta 2kjm.pdb
"""

import sys
from __modules__.fasta_file import read_fasta_file
from __modules__.pdb_file import read_pdb_file
from __modules__.dope_file import save_dope


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
    protein_cible = read_fasta_file(sys.argv[1])
    matrix = read_pdb_file(sys.argv[2])

    dope = save_dope()
