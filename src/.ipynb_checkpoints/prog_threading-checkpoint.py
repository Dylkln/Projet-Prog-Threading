"""
Programme principal.

Usage:
------
    python prog_threading.py file.fasta file.pdb

      - file.fasta: fichier fasta de la protéine cible (data/FASTA-file/)
      - file.pdb: fichier pdb de la protéine modèle (data/PDB-file/)

   exemple
     python prog_threading.py ../data/FASTA-file/2KJM.fasta ../data/PDB-file/2kjm.pdb

"""

import argparse
import sys
from __modules__.fasta_file import read_fasta_file
from __modules__.pdb_file import read_pdb_file
from __modules__.dope_file import save_dope
import __modules__.matrix as matrix


def arguments():
    """
    Détermine les arguments requis & optionnels pour le programme.

    Return
    ------
    args.fichier_fasta: str
        la protéine cible (.fasta)
    args.fichier_pdb: str
        la protéine modèle (.pdb)
    args.gap: int
        la pénalité du gap - par défaut 1
    args.atoms: str
        les atomes du fichier DOPE à prendre en compte
    """
    parser = argparse.ArgumentParser()

    # Argument nécessaire
    group = parser.add_argument_group('fichiers', "les fichiers pour l'analyse")
    group.add_argument('fichier_fasta',
                       help="la séquence en acide aminés de la protéine cible")
    group.add_argument('fichier_pdb',
                       help="la structure 3D de la protéine modèle")

    # Argument optionnel
    parser.add_argument('-g', '--gap', type=int, default=1, choices=range(6),
                        help="La pénalité du gap - par défaut vaut 1 et >= 0")
    parser.add_argument('-a', '--atoms', default='CA', choices=['CA', 'C'],
                        help="Les atomes du fichier DOPE à prendre en compte")
    parser.add_argument('-m', '--model', default=1,
                        help="le modèle de la strucutre à prendre en compte")

    args = parser.parse_args()

    return args.fichier_fasta, args.fichier_pdb, args.gap, args.atoms


if __name__ == "__main__":
    fasta, pdb, gap, atoms = arguments()

    distance = read_pdb_file(pdb)  # Matrice de distance
    sequence = read_fasta_file(fasta)  # Protéine cible
    dope = save_dope(atoms)

    sys.exit()

    fasta, pdb = fasta.split('/')[-1], pdb.split('/')[-1]

    print("Alignement de la séquence cible {} avec la structure modèle {}"
          .format(fasta, pdb))

    # Initilaliser la matrice de haut niveau
    high_level = matrix.Matrice(template=list(distance.columns),
                                sequence=sequence, gap_score=gap)
    high_level.create_zero_matrix()

    aa_fixed = {'Name': high_level.row_names[2], 'Pos': (2, 4)}
    high_level.remplissage_matrice(dope, distance, aa_fixed)

    # Générer les matrices de bas niveau
    for row in range(1, high_level.nb_rows):
        for col in range(1, high_level.nb_cols):
            low_level = matrix.Matrice(template=list(distance.columns),
                                       sequence=sequence, gap_score=gap)
            low_level.create_zero_matrix()

            aa_fixed = {'Name': high_level.row_names[row], 'Pos': (row, col)}
            low_level.remplissage_matrice(dope, distance, aa_fixed)

            high_level.matrice[row][col] = low_level.score_opti

    print(high_level)

    # Alignement
    align = high_level.chemin_opti()
    high_level.show_align(align, fasta, pdb)
