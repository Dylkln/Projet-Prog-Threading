"""
Ce module permet de mettre en place les arguments requis et optionnels.

Requis
  - fichier fasta de la protéine cible
  - fichier pdb de la strucutre modèle

Optionnels
  - le scrore de gap à appliquer
  - les atomes du fichier DOPE à prendre en compte
  - le modèle de la strucutre à prendre en compte
"""

import argparse
import os

import sys


def valide_file(parser, fichier, extension):
    """
    Test la validité des fichiers passés en paramètre.

      - format du fichier
      - fichier présent

    Parameter
    ---------
    parser
    fichier: str
        le nom du fichier
    extension: str
        l'extension souhaitée du fichier
    """
    if not fichier.endswith(extension) and not os.path.exists(fichier):
        parser.error('Fichier {} non valide - format ou path (voir aide -h)'
                     .format(fichier))
    return fichier


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
    args.models: int
        le modèle de la structure à prendre à compte
    """
    parser = argparse.ArgumentParser()

    # Argument nécessaire
    group = parser.add_argument_group('fichiers', "les fichiers pour l'analyse")
    group.add_argument(
        'fichier_fasta', type=lambda x: valide_file(parser, x, '.fasta'),
        help="la séquence en acide aminés de la protéine cible (.fasta)"
    )
    group.add_argument(
        'fichier_pdb', type=lambda x: valide_file(parser, x, '.pdb'),
        help="la structure 3D de la protéine modèle (.pdb)"
    )

    # Argument optionnel
    parser.add_argument('-g', '--gap', type=int, default=1, choices=range(6),
                        help="La pénalité du gap - par défaut vaut 1 et >= 0")
    parser.add_argument('-a', '--atoms', default='CA', choices=['CA', 'C'],
                        help="Les atomes du fichier DOPE à prendre en compte")
    parser.add_argument('-m', '--model', default=1,
                        help="le modèle de la strucutre à prendre en compte")

    args = parser.parse_args()

    return args.fichier_fasta, args.fichier_pdb, args.gap, args.atoms
