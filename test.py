import tkinter as tk
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

    def compter_bombes_adjacentes(self, row, col):
        compteur = 0
        for i in range(max(0, row - 1), min(self.hauteur, row + 2)):
            for j in range(max(0, col - 1), min(self.largeur, col + 2)):
                if self.grille[i][j] == -1:
                    compteur += 1
        return compteur

class DemineurUI(tk.Tk):
    def __init__(self, hauteur, largeur, mines):
        super().__init__()
        self.title("Démineur")
        self.demineur = Demineur(hauteur, largeur, mines)
        self.create_ui()

    def create_ui(self):
        self.cells = []
        for i in range(self.demineur.hauteur):
            row = []
            for j in range(self.demineur.largeur):
                cell_label = tk.Label(self, text=" ", width=4, height=2, relief="ridge", bg="gray")
                cell_label.grid(row=i, column=j, padx=2, pady=2)
                cell_label.bind("<Button-1>", lambda e, i=i, j=j: self.reveal_cell(i, j))
                row.append(cell_label)
            self.cells.append(row)

    def reveal_cell(self, row, col):
        cell = self.cells[row][col]
        cell.config(bg="white")  # Change la couleur de fond pour indiquer que la cellule a été révélée
        if self.demineur.grille[row][col] == -1:
            cell.config(text="💣")  # Symbole de bombe
        else:
            nombre_bombes_adjacentes = self.demineur.compter_bombes_adjacentes(row, col)
            if nombre_bombes_adjacentes > 0:
                cell.config(text=str(nombre_bombes_adjacentes))  # Affiche le nombre de bombes adjacentes
            else:
                self.reveler_cases_vides(row, col)

    def reveler_cases_vides(self, row, col):
        for i in range(max(0, row - 1), min(self.demineur.hauteur, row + 2)):
            for j in range(max(0, col - 1), min(self.demineur.largeur, col + 2)):
                if self.cells[i][j]['bg'] == 'gray':
                    self.reveal_cell(i, j)



if __name__ == "__main__":
    hauteur = 10
    largeur = 10
    mines = 20
    app = DemineurUI(hauteur, largeur, mines)
    app.mainloop()
