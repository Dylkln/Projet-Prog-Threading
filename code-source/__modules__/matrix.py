"""
Module
"""

import numpy as np
import pandas as pd
import sys


class Matrice:
    """Classe Matrice"""
    col_names = ""
    row_names = ""
    nb_cols = 0
    nb_rows = 0
    score_opti = 0
    matrice = 0

    def __init__(self, template, sequence):
        self.col_names = ['__'] + template
        self.row_names = ['__'] + sequence
        self.nb_cols = len(self.col_names)
        self.nb_rows = len(self.row_names)
        self.create_zero_matrix()


    def create_zero_matrix(self):
        self.matrice = np.zeros((self.nb_rows, self.nb_cols), dtype = float)


    def remplissage_matrice(self, dope, distance, aa_fixed):
        """
        Parameter
        ---------
        aa_fixed: dictionary
            - Name: le code à 3 lettres de l'acide aminé fixé
            - Pos: tupple (row, col) de l'acide aminé fixé
        """

        self.parcourir_matrice(
            n=1, o=aa_fixed['Pos'][0] + 1,
            k=1, l=aa_fixed['Pos'][1] + 1,
            dope=dope, distance=distance, aa_fixed=aa_fixed
        )

        self.parcourir_matrice(
            n=aa_fixed['Pos'][0], o=self.nb_rows,
            k=aa_fixed['Pos'][1], l=self.nb_cols,
            dope=dope, distance=distance, aa_fixed=aa_fixed
        )


    def parcourir_matrice(self, n, o, k, l, dope, distance, aa_fixed):
        gap = 1

        for row in range(n, o):
            for col in range(k, l):
                position = {
                    'AA-fixed': self.col_names[aa_fixed['Pos'][1]],
                    'AA-test': self.col_names[col]
                }
                aa_test = self.row_names[row]

                a = self.score_dope(
                    list_score=dope[aa_fixed['Name']][aa_test],
                    dist=distance[position['AA-fixed']][position['AA-test']]
                ) + self.matrice[row - 1][col - 1]

                b = self.matrice[row - 1][col] + gap
                c = self.matrice[row][col - 1] + gap

                self.matrice[row][col] = min(a, b, c)

                if row == self.nb_rows - 1 and col == self.nb_cols - 1:
                    self.score_opti = self.matrice[row][col]


    def score_dope(self, list_score, dist):
        l = []
        for i in range(0,29):
            l.append(0.25 + 0.5 * i)

        tmp = 0
        for angstrom in l:
            if dist > (angstrom + 0.5):
                tmp += 1
            else:
                break

        return float(list_score[tmp])


    def show_matrix(self):
        print(pd.DataFrame(self.matrice, columns = self.col_names,
                           index = self.row_names))
