![Protein threading](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)

# Programme de threading par double programmation dynamique

## Threading de protéine

Méthode qui consiste à prédire la structure 3D d'une protéine cible à partir de sa séquence en acide aminé (1D) en utilisant comme modèles des structures 3D déja résolu dans la Protein Data Bank.

## Double programmation dynamique

Méthode qui consiste, pout tout couple (a,p), à déterminer le score minimal de l'alignement de la séquence cible avec la struture modèle (avec a n’importe quel acide aminé de la séquence cible et p n’importe quelle position de la structure modèle). Le score minimal de chaque couple (a,p) est stocké dans une matrice de haut niveau. Ensuite, l'alignement optimal entre la séquence et la structure est déterminé en trouvant le meilleur chemin dans cette matrice.  

## Prérequis

L'utilisation de [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) est fortement recommandée pour l'utilisation du programme de threading.

## Quick start

1. Clone du répertoire github

> Lien HTTPS
```
git clone https://github.com/Dylkln/Projet-Prog-Threading.git
```
> Lien SSH
```
git@github.com:Dylkln/Projet-Prog-Threading.git
```

2. Initialiser l'environnement conda à partir du fichier *environment.yml*

```
conda env create --file environment.yml
```

3. Activer l'environnement conda

```
conda activate prog-threading
```

## Exécuter le programme

Pour lancer le programme il faut exécuter le programme *prog_threading.py*.
```
python prog_threading.py FILE.fasta FILE.pdb
```

Fichier fasta et pdb de test
```
python prog_threading.py 2KJM.fasta 2kjm.pdb

python prog_threading.py 3CHY.fasta 4FXN.pdb
```

## Auteurs

Pierre IMBERT : pierre.damase.mbert@gmail.com

Dylan KLEIN : klein.dylan@outlook.com

Université de Paris M2-BI

## Date

16 septembre 2020
