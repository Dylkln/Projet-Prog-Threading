"""
Ce module contient une class "Matrice".

Elle permet la création d'une matrice par programmation dynamique.
"""

import numpy as np
import pandas as pd
import sys


class Matrice:
    """Classe Matrice.

    Elle permet de créer des objets matrice.

    Elle contient les attributs de classe:
      - col_names: nom des colonnes
      - row_names: nom des lignes
      - nb_cols: nombre de colonnes
      - nb_rows: nombre de lignes
      - score_opti: le score d'alignement optimal (d'une matrice de bas niveau)
      - matrice: la matrice de haut niveau
    """

    col_names = ""
    row_names = ""
    nb_cols = 0
    nb_rows = 0
    score_opti = 0
    matrice = 0

    def __init__(self, template, sequence):
        """Constructeur de la classe Matrice.

        Parameter
        ---------
        template: list
            position des acides aminés
        sequence: list
            séquence en acide aminés
        """
        self.col_names = ['__'] + template
        self.row_names = ['__'] + sequence
        self.nb_cols = len(self.col_names)
        self.nb_rows = len(self.row_names)
        self.create_zero_matrix()

    def create_zero_matrix(self):
        """Créé une matrice et l'initialise avec que des zéro."""
        self.matrice = np.zeros((self.nb_rows, self.nb_cols), dtype=float)

    def remplissage_matrice(self, dope, distance, aa_fixed):
        """Méthode de remplissage de la matrice.

        Parameter
        ---------
        dope: dictionary
            - Première clé: code 3 lettres acide aminé 1 (aa1)
            - Deuxième clé: code 3 lettres acide aminé 2 (aa2)
            - Valeur: liste des intercations de Van der Walls entre aa1 et aa2
        distance: pandas dataframe
            matrice de distance des atomes de la structure modèle
        aa_fixed: dictionary
            'Name' le code à 3 lettres de l'acide aminé fixé
            'Pos' tupple (row, col) de l'acide aminé fixé
        """
        self.parcourir_matrice(
            n=1, o=aa_fixed['Pos'][0] + 1,
            k=1, m=aa_fixed['Pos'][1] + 1,
            dope=dope, distance=distance, aa_fixed=aa_fixed
        )

        self.parcourir_matrice(
            n=aa_fixed['Pos'][0], o=self.nb_rows,
            k=aa_fixed['Pos'][1], m=self.nb_cols,
            dope=dope, distance=distance, aa_fixed=aa_fixed
        )

    def parcourir_matrice(self, n, o, k, m, dope, distance, aa_fixed):
        """Application de l'algorithme de Needleman & Wunsch.

        Cet algorithme est utilisé:
          - pour remplir la matrice
          - déterminer le score d'alignement minimal

        Parameter
        ---------
        n, o : int
            range sur lequel on parcours les lignes de la matrice
        k, m : int
            range sur lequel on parcours les colonnes de la matrice
        dope: dictionary
            - Première clé: code 3 lettres acide aminé 1 (aa1)
            - Deuxième clé: code 3 lettres acide aminé 2 (aa2)
            - Valeur: liste des intercations de Van der Walls entre aa1 et aa2
        distance: pandas dataframe
            matrice de distance des atomes de la structure modèle
        aa_fixed: dictionary
            - Name: le code à 3 lettres de l'acide aminé fixé
            - Pos: tupple (row, col) de l'acide aminé fixé
        """
        gap = 1

        for row in range(n, o):
            for col in range(k, m):

                position = {
                    'AA-fixed': self.col_names[aa_fixed['Pos'][1]],
                    'AA-test': self.col_names[col]
                }

                aa_test = self.row_names[row]

                align = self.score_dope(
                    list_score=dope[aa_fixed['Name']][aa_test],
                    dist=distance[position['AA-fixed']][position['AA-test']]
                ) + self.matrice[row - 1][col - 1]

                deletion = self.matrice[row - 1][col] + gap
                insertion = self.matrice[row][col - 1] + gap

                self.matrice[row][col] = min(align, deletion, insertion)

                if row == self.nb_rows - 1 and col == self.nb_cols - 1:
                    self.score_opti = self.matrice[row][col]

    def score_dope(self, list_score, dist):
        """Renvoie la valeur de l'intercation de VdW.

        Cette valeur correspondant à la distance en angström entre deux acides
        aminés dans la structure.

        list_score: list
            liste des interactions de Van der Walls entre l'acide aminé fixé et
            l'acide aminé testé
        distance: float
            distance euclidienne entre deux atomes
        """
        liste = []
        for i in range(0, 29):
            liste.append(0.25 + 0.5 * i)

        tmp = 0
        for angstrom in liste:
            if dist > (angstrom + 0.5):
                tmp += 1
            else:
                break

        return float(list_score[tmp])

    def __str__(self):
        """Convertis la matrice en une Dataframe Pandas pour la visualiser."""
        return ("\n\nMatrice de haut niveau:\n\n{}"
                .format(pd.DataFrame(self.matrice, columns=self.col_names,
                                     index=self.row_names)))

    def chemin_opti(self):
        """Détermine le chemin optimal pour l'alignement séquence/structure.

        Et ceux, dans la matrice de haut niveau.

        Return
        ------
        align: dictionary
            'Sequence' liste des acides aminés
            'Structure' liste des positions dans la strucutre modèle
        """
        row, col = self.nb_rows - 1, self.nb_cols - 1
        align = {
            'Sequence': [self.row_names[row]],
            'Structure': [self.col_names[col]]
        }

        while row > 1 and col > 1:
            minimum = min(
                self.matrice[row-1][col-1],
                self.matrice[row-1][col],
                self.matrice[row][col-1]
            )

            if minimum == self.matrice[row-1][col-1]:
                align['Sequence'].insert(0, self.row_names[row-1])
                align['Structure'].insert(0, self.col_names[col-1])
                row -= 1
                col -= 1

            elif minimum == self.matrice[row-1][col]:
                align['Sequence'].insert(0, self.row_names[row-1])
                align['Structure'].insert(0, "-")
                row -= 1

            else:
                align['Sequence'].insert(0, "-")
                align['Structure'].insert(0, self.col_names[col-1])
                col -= 1

        return align

    def show_align(self, align, sequence, structure):
        """Affiche l'alignement optimal dans le terminal."""
        print("\n\nAlignement optimal de la séquence {} avec la structure {}\n"
              .format(sequence, structure))

        for aa in align['Sequence']:
            print("{:^3s}".format(aa), end=" ")
        print()

        for pos in align['Structure']:
            if isinstance(pos, int):
                print("{:^3d}".format(pos), end=" ")
            else:
                print("{:^3s}".format(pos), end=" ")
        print()
