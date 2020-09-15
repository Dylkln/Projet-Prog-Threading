"""
Module
"""

import numpy as np
import pandas as pd
import sys


class Matrix:
    """Classe Matrix"""
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
        gap = 1

        for row in range(1, aa_fixed['Pos'][0] + 1):
            for col in range(1, aa_fixed['Pos'][1] + 1):
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

        for row in range(aa_fixed['Pos'][0], self.nb_rows):
            for col in range(aa_fixed['Pos'][1], self.nb_cols):
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

        self.score_opti = self.matrice[row][col]

        self.show_matrix()


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
