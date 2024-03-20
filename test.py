import tkinter as tk
import random
from PIL import Image, ImageTk


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


class DemineurUI(tk.Tk):
    def __init__(self, hauteur, largeur, mines):
        super().__init__()
        self.title("Démineur")
        self.demineur = Demineur(hauteur, largeur, mines)
        self.create_ui()

    def create_ui(self):
        # Charger l'image
        image = Image.open("pngwing.com (10).png")  # Remplacez "background_image.jpg" par le chemin de votre image
        photo = ImageTk.PhotoImage(image)

        # Créer un label pour afficher l'image
        background_label = tk.Label(self, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame pour le titre
        self.title_frame = tk.Frame(self, bg="blue")
        self.title_frame.grid(row=0, column=0, columnspan=self.demineur.largeur + 2, pady=10)

        # Titre
        self.title_label = tk.Label(self.title_frame, text="Démineur", font=("Helvetica", 20), fg="white", bg="blue")
        self.title_label.pack(pady=10)

        # Frames grille
        self.game_frame = tk.Frame(self, bg="#764929")  # la grille de jeu
        self.game_frame.grid(row=1, column=0, padx=15)

        #boite menu
        self.menu_frame = tk.Frame(self, bg="#764929", width=400, height=400)
        self.menu_frame.grid(row=1, column=2, padx=10)

        # Contours des frames
        self.game_frame.config(borderwidth=2, relief="raised")
        self.menu_frame.config(borderwidth=2, relief="raised")

        # Création de la grille de jeu
        self.create_game_grid()

        # Label pour les informations
        self.info_label = tk.Label(self.menu_frame, text="Informations", font=("Helvetica", 16), width=13, height=1)
        self.info_label.grid(row=0, column=0, padx=5, pady=5)

        # Boutons pour les niveaux de difficulté
        self.easy_button = tk.Button(self.menu_frame, text="Facile", command=self.set_easy, width=10, height=2)
        self.easy_button.grid(row=1, column=0, padx=5, pady=5)

        self.medium_button = tk.Button(self.menu_frame, text="Moyen", command=self.set_medium, width=10, height=2)
        self.medium_button.grid(row=2, column=0, padx=5, pady=5)

        self.hard_button = tk.Button(self.menu_frame, text="Difficile", command=self.set_hard, width=10, height=2)
        self.hard_button.grid(row=3, column=0, padx=5, pady=5)

        # Configuration dynamique de la taille des lignes et colonnes
        self.grid_rowconfigure(1, weight=1)  # Ajustement dynamique de la hauteur de la ligne 1
        self.grid_columnconfigure(0, weight=1)  # Ajustement dynamique de la largeur de la colonne 0
        self.grid_columnconfigure(2, weight=1)  # Ajustement dynamique de la largeur de la colonne 2

    def create_game_grid(self):
        self.cells = []
        for i in range(self.demineur.hauteur):
            row = []
            for j in range(self.demineur.largeur):
                cell_label = tk.Label(self.game_frame, text=" ", width=4, height=2, relief="raised", bg="#43302f") #changer la couleur de case
                cell_label.grid(row=i, column=j, padx=2, pady=2)
                cell_label.bind("<Button-1>", lambda e, i=i, j=j: self.reveal_cell(i, j))
                row.append(cell_label)
            self.cells.append(row)

    def reveal_cell(self, row, col):
        if not self.demineur.mines_placees:
            self.demineur.placer_mines((row, col))
        cell = self.cells[row][col]
        cell.config(bg="#cab2a3")  # Change la couleur de fond pour indiquer que la cellule a été révélée
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
                if self.cells[i][j]['bg'] == '#43302f':
                    self.reveal_cell(i, j)

    def set_easy(self):
        self.reset_game(10, 10, 30)

    def set_medium(self):
        self.reset_game(13, 13, 60)

    def set_hard(self):
        self.reset_game(18, 18, 90)

    def reset_game(self, hauteur, largeur, mines):
        # Supprimer les widgets existants de la grille de jeu
        for row in self.cells:
            for cell in row:
                cell.destroy()

        # Réinitialiser la grille de jeu avec les nouvelles dimensions
        self.demineur = Demineur(hauteur, largeur, mines)
        self.create_game_grid()


if __name__ == "__main__":
    hauteur = 10
    largeur = 10
    mines = 2

    app = DemineurUI(hauteur, largeur, mines)
    app.mainloop()
