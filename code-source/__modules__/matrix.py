"""
Module contenant une class "Matrice" permettant la création d'une matrice par programmation dynamique.
"""

import numpy as np
import pandas as pd
import sys


class Matrice:
    """Classe Matrice"""
    col_names = ""  # Nom des colonnes
    row_names = ""  # Nom des lignes
    nb_cols = 0     # Nombre de colonnes
    nb_rows = 0     # Nombre de lignes
    score_opti = 0  # Le score de l'alignement optimal
    matrice = 0     # La matrice

    def __init__(self, template, sequence):
        """
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
        """
        Créé une matrice de zéro.
        """
        self.matrice = np.zeros((self.nb_rows, self.nb_cols), dtype = float)

    # Pour les trois prochaines fonctions : "remplissage_matrice", "parcourir matrice",
    # "score_dope", les paramètres "dope" et "distance / dist" correspondent à : 
    #       - dope : dictionnaire imbriqué :
    #                -  première clé = Acide aminé trois lettres,
    #                -  deuxième clé = acide aminé trois lettres,
    #                -  valeur = liste des valeurs des interactions de Van der Walls.
    
    #       - distance / dist : float:
    #                           - Distance calculé entre deux atomes.

    def remplissage_matrice(self, dope, distance, aa_fixed):
        """
        Méthode de remplissage de la matrice.

        Parameter
        ---------
        aa_fixed: dictionary
            - Name: le code à 3 lettres de l'acide aminé fixé
            - Pos: tupple (row, col) de l'acide aminé fixé
        """

        self.parcourir_matrice(
            n = 1, o = aa_fixed['Pos'][0] + 1,
            k = 1, l = aa_fixed['Pos'][1] + 1,
            dope = dope, distance = distance, aa_fixed = aa_fixed
        )

        self.parcourir_matrice(
            n = aa_fixed['Pos'][0], o = self.nb_rows,
            k = aa_fixed['Pos'][1], l = self.nb_cols,
            dope = dope, distance = distance, aa_fixed = aa_fixed
        )


    def parcourir_matrice(self, n, o, k, l, dope, distance, aa_fixed):
        """
        Parameter
        ---------
        n, o : int
            range sur lequel on parcours les lignes de la matrice
        k, l : int
            range sur lequel on parcours les colonnes de la matrice
        aa_fixed: dictionary
            - Name: le code à 3 lettres de l'acide aminé fixé
            - Pos: tupple (row, col) de l'acide aminé fixé
        """
        gap = 1

        for row in range(n, o):
            for col in range(k, l):
                
                position = {
                    'AA-fixed': self.col_names[aa_fixed['Pos'][1]],
                    'AA-test': self.col_names[col]
                }
                
                aa_test = self.row_names[row]

                a = self.score_dope(
                    list_score = dope[aa_fixed['Name']][aa_test],
                    dist = distance[position['AA-fixed']][position['AA-test']]
                ) + self.matrice[row - 1][col - 1]

                b = self.matrice[row - 1][col] + gap
                c = self.matrice[row][col - 1] + gap

                self.matrice[row][col] = min(a, b, c)

                if row == self.nb_rows - 1 and col == self.nb_cols - 1:
                    self.score_opti = self.matrice[row][col]


    def score_dope(self, list_score, dist):
        """
        Permet de retourner la valeur de l'interaction de VdW
        correspondant à la distance en angström entre deux acides
        aminés dans la structure.
        """
        l = []
        
        for i in range(0,29):
            l.append(0.25 + 0.5 * i)

        tmp = 0
        
        for angstrom in l:
            if distance > (angstrom + 0.5):
                tmp += 1
            else:
                break

        return float(list_score[tmp])


    def show_matrix(self):
        """
        transforme la matrice en une Dataframe Pandas pour la visualiser.
        """
        print(pd.DataFrame(self.matrice, columns = self.col_names,
                           index = self.row_names))
