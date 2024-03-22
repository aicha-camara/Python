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
        self.cells = None
        self.message_label = None
        self.title("Démineur")
        self.demineur = Demineur(hauteur, largeur, mines)
        self.create_ui()
        self.victoire_affichee = False
        self.click = True

        self.set_easy()

    def create_ui(self):
        # fond de l'application
        image = Image.open("assets/plateau.png")  # Remplacez "background_image.jpg" par le chemin de votre image
        photo = ImageTk.PhotoImage(image)

        # Créer un label pour afficher l'image de l'application
        background_label = tk.Label(self, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer un cadre pour contenir l'image et le texte du titre
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, pady=10)

        # Charger l'image du titre et la redimensionner
        nouvelle_largeur = 200
        nouvelle_hauteur = 50
        title_image = Image.open("assets/banniere.png")
        title_image_resized = title_image.resize((nouvelle_largeur, nouvelle_hauteur))
        title_photo = ImageTk.PhotoImage(title_image_resized)

        # Créer un label pour l'image du titre avec la nouvelle taille
        title_image_label = tk.Label(title_frame, image=title_photo, borderwidth=0)
        title_image_label.image = title_photo
        title_image_label.grid(row=0, column=0)

        # Ajouter le texte du titre au centre de l'image
        titre_texte = "Demineur"
        title_label = tk.Label(title_frame, text=titre_texte, fg="white", bg="#692000", font=("Helvetica", 16))
        # Calculer les coordonnées x et y pour placer le texte au centre de l'image
        x = (nouvelle_largeur - title_label.winfo_reqwidth()) / 2
        y = (nouvelle_hauteur - title_label.winfo_reqheight()) / 2
        title_label.place(x=x, y=y)

        # Ajouter le label pour les messages
        self.message_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#764929", fg="red")
        self.message_label.grid(row=0, column=2, sticky="ew", padx=5, pady=(10, 0))

        # Frames grille
        self.game_frame = tk.Frame(self, bg="#764929")  # la grille de jeu
        self.game_frame.grid(row=1, column=0, padx=15)

        # boite menu
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

        # Bouton pour réinitialiser le jeu
        self.reset_button = tk.Button(self.menu_frame, text="Réinitialiser", command=self.reset_game, width=10,
                                      height=2)
        self.reset_button.grid(row=4, column=0, padx=5, pady=5)

    def create_game_grid(self):
        self.cells = []
        for i in range(self.demineur.hauteur):
            row = []
            for j in range(self.demineur.largeur):
                cell_label = tk.Label(self.game_frame, text=" ", width=4, height=2, relief="raised",
                                      bg="#43302f")  # changer la couleur de case
                cell_label.grid(row=i, column=j, padx=2, pady=2)
                cell_label.bind("<Button-1>", lambda e, i=i, j=j: self.reveal_cell(i, j))
                self.add_hover_effect(cell_label)
                row.append(cell_label)
            self.cells.append(row)

    def reveal_cell(self, row, col):

        if not self.click:
            return
        if not self.demineur.mines_placees:
            self.demineur.placer_mines((row, col))
        cell = self.cells[row][col]
        cell.config(bg="#cab2a3")  # Change la couleur de fond pour indiquer que la cellule a été révélée
        cell.unbind("<Enter>")  # Désactiver l'effet de survol lorsque la case est révélée
        cell.unbind("<Leave>")  # Désactiver l'effet de survol lorsque la case est révélée
        cell.config(relief="sunken")  # Modifier le relief pour indiquer que la case est révélée
        if self.demineur.grille[row][col] == -1:
            cell.config(text="💣")  # Symbole de bombe
            self.message_label.config(text="Vous avez perdu !", fg="white")
            self.click = False
        else:
            nombre_bombes_adjacentes = self.demineur.compter_bombes_adjacentes(row, col)
            if nombre_bombes_adjacentes > 0:
                cell.config(text=str(nombre_bombes_adjacentes))  # Affiche le nombre de bombes adjacentes
            else:
                self.reveler_cases_vides(row, col)
            cases_revelees = sum(1 for row in self.cells for cell in row if cell.cget("relief") == "sunken")
            bombes_non_revelees = sum(row.count(-1) for row in self.demineur.grille)
            cases_totales = self.demineur.hauteur * self.demineur.largeur
            if cases_revelees == cases_totales - bombes_non_revelees and not self.victoire_affichee:
                self.message_label.config(text="Vous avez gagné !", fg="white")
                self.victoire_affichee = True
                self.click = False

    def reveler_cases_vides(self, row, col):
        for i in range(max(0, row - 1), min(self.demineur.hauteur, row + 2)):
            for j in range(max(0, col - 1), min(self.demineur.largeur, col + 2)):
                if self.cells[i][j]['bg'] == '#43302f':
                    self.reveal_cell(i, j)

    def add_hover_effect(self, cell_label):
        cell_label.bind("<Enter>", lambda event, cell=cell_label: self.on_enter(cell))
        cell_label.bind("<Leave>", lambda event, cell=cell_label: self.on_leave(cell))

    @staticmethod
    def on_enter(cell_label):
        cell_label.config(bg="#a3a3a3")  # Changer la couleur de fond lorsque la souris survole la cas

    @staticmethod
    def on_leave(cell_label):
        if cell_label.cget('relief') != 'sunken':  # Vérifier si la case n'est pas révélée
            cell_label.config(bg="#43302f")

    def set_easy(self):
        self.reset_game(10, 10, random.randint(5, 10))

    def set_medium(self):
        self.reset_game(13, 13, random.randint(20, 40))

    def set_hard(self):
        self.reset_game(16, 16, random.randint(60, 80))

    def reset_game(self, hauteur=None, largeur=None, mines=None):
        hauteur = hauteur or self.demineur.hauteur
        largeur = largeur or self.demineur.largeur
        mines = mines or self.demineur.mines
        self.click = True

        # Supprimer les widgets existants de la grille de jeu
        for row in self.cells:
            for cell in row:
                cell.destroy()

        # Réinitialiser la grille de jeu avec les nouvelles dimensions
        self.demineur = Demineur(hauteur, largeur, mines)
        self.create_game_grid()
        self.message_label.config(text="")


if __name__ == "__main__":
    app = DemineurUI(10, 10, random.randint(5, 10))  # Niveau facile par défaut

    app.mainloop()
