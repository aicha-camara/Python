import random

class Demineur:
    def __init__(self, hauteur, largeur, mines):
        self.hauteur = hauteur
        self.largeur = largeur
        self.mines = mines
        self.grille = [[0 for _ in range(largeur)] for _ in range(hauteur)]
        self.placer_mines()

    def placer_mines(self):
        mines_placees = 0
        while mines_placees < self.mines:
            x = random.randint(0, self.largeur - 1)
            y = random.randint(0, self.hauteur - 1)
            if self.grille[y][x] != -1:
                self.grille[y][x] = -1
                mines_placees += 1

    def afficher_grille(self):
        for ligne in self.grille:
            print(' '.join([str(cellule) for cellule in ligne]))

# Exemple d'utilisation
if __name__ == "__main__":
    hauteur = 5
    largeur = 5
    mines = 5
    jeu = Demineur(hauteur, largeur, mines)
    jeu.afficher_grille()
