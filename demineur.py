import random

class Demineur:
    def __init__(self, hauteur, largeur, mines):
        self.hauteur = hauteur
        self.largeur = largeur
        self.mines = mines
        self.grille = [[0 for _ in range(largeur)] for _ in range(hauteur)]
        self.mines_placees = False

    def placer_mines(self, premier_clic):
        if not self.mines_placees:
            x, y = premier_clic
            indices = [(i, j) for i in range(self.hauteur) for j in range(self.largeur)]
            indices.remove((x, y))
            mines_a_placer = random.sample(indices, self.mines)
            for x, y in mines_a_placer:
                self.grille[x][y] = -1
            self.mines_placees = True

    def compter_bombes_adjacentes(self, row, col):
        compteur = 0
        for i in range(max(0, row - 1), min(self.hauteur, row + 2)):
            for j in range(max(0, col - 1), min(self.largeur, col + 2)):
                if self.grille[i][j] == -1:
                    compteur += 1
        return compteur
