import random

class Demineur:
    def __init__(self, hauteur, largeur, mines):
        self.hauteur = hauteur
        self.largeur = largeur
        self.mines = mines
        self.grille = [[0 for _ in range(largeur)] for _ in range(hauteur)]
        self.mines_placees = False

    def placer_mines(self, premier_clic):
        # Vérifie si les mines n'ont pas déjà été placées
        if not self.mines_placees:
            x, y = premier_clic  # Récupère les coordonnées du premier clic
            indices = [(i, j) for i in range(self.hauteur) for j in
                       range(self.largeur)]  # Génère tous les indices possibles dans la grille
            indices.remove((x, y))  # Supprime les coordonnées du premier clic de la liste des indices
            mines_a_placer = random.sample(indices,
                                           self.mines)  # Sélectionne aléatoirement les emplacements pour les mines
            for x, y in mines_a_placer:
                self.grille[x][y] = -1  # Place les mines dans la grille
            self.mines_placees = True  # Indique que les mines ont été placées

    def compter_bombes_adjacentes(self, row, col):
        compteur = 0  # Initialise le compteur de bombes adjacentes
        # Parcourt les cases adjacentes à la case donnée
        for i in range(max(0, row - 1), min(self.hauteur, row + 2)):
            for j in range(max(0, col - 1), min(self.largeur, col + 2)):
                if self.grille[i][j] == -1:  # Vérifie si la case contient une bombe
                    compteur += 1  # Incrémente le compteur si une bombe est trouvée
        return compteur  # Retourne le nombre de bombes adjacentes à la case donnée
