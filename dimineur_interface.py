import random
import tkinter as tk
from PIL import Image, ImageTk
from demineur import Demineur



class DemineurUI(tk.Tk):
    def __init__(self, hauteur, largeur, mines):
        super().__init__()
        self.frame_menu = None
        self.info_label = None
        self.bouton_reset_niveau = None
        self.bouton_niveau_facile = None
        self.bouton_niveau_moyen = None
        self.bouton_niveau_difficile = None
        self.frame_grille = None
        self.grille_cases = None
        self.message_label = None
        self.title("Démineur")
        self.demineur = Demineur(hauteur, largeur, mines)
        self.interface()
        self.afficher_victoire = False
        self.etat_clique = True
        self.niveau_facile()
        self.timer_actif = False
        self.temps_ecoule = 0

    def interface(self):
        # Fond de l'application
        image_ecran = Image.open("assets/plateau.png")  # Charger l'image de fond
        plateau = ImageTk.PhotoImage(image_ecran)

        # Créer un label pour afficher l'image de l'application en arrière-plan
        background_label = tk.Label(self, image=plateau)
        background_label.image = plateau
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Créer un cadre pour contenir l'image et le texte du titre
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, pady=10)

        # Charger l'image du titre et la redimensionner
        nouvelle_largeur = 200
        nouvelle_hauteur = 50
        image_titre = Image.open("assets/banniere.png")
        image_titre_resized = image_titre.resize((nouvelle_largeur, nouvelle_hauteur))
        banniere = ImageTk.PhotoImage(image_titre_resized)

        # Créer un label pour l'image du titre avec la nouvelle taille
        image_titre_label = tk.Label(title_frame, image=banniere, borderwidth=0)
        image_titre_label.image = banniere
        image_titre_label.grid(row=0, column=0)

        # Ajouter le texte du titre au centre de l'image
        titre = "Demineur"
        titre_label = tk.Label(title_frame, text=titre, fg="white", bg="#692000", font=("Verdana", 16))
        # Calculer les coordonnées x et y pour placer le texte au centre de l'image
        x = (nouvelle_largeur - titre_label.winfo_reqwidth()) / 2
        y = (nouvelle_hauteur - titre_label.winfo_reqheight()) / 2
        titre_label.place(x=x, y=y)

        # Ajouter le label pour les messages
        self.message_label = tk.Label(self, text="", font=("Verdana", 12),
                                      bg='#7e5835',
                                      fg="white", borderwidth=2, relief="groove", padx=10, pady=5)
        self.message_label.grid(row=0, column=2, sticky="ew", padx=5, pady=(10, 0))

        # Frames grille
        self.frame_grille = tk.Frame(self, bg="#764929")  # Cadre de la grille de jeu
        self.frame_grille.grid(row=1, column=0, padx=15)

        # Boîte menu
        self.frame_menu = tk.Frame(self, bg="#764929", width=400, height=400, relief="groove")
        self.frame_menu.grid(row=1, column=2, padx=10)
        self.texte_timer = "Temps écoulé : 0 secondes"  # Initialisez le texte du timer
        self.label_timer = tk.Label(self.frame_menu, text=self.texte_timer, font=("Verdana", 15,),
                                    bg='#7e5835', fg="white", borderwidth=2, relief="groove", padx=10, pady=5)
        self.label_timer.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 0))

        # Contours des frames
        self.frame_grille.config(borderwidth=2, relief="raised")
        self.frame_menu.config(borderwidth=2, relief="raised")

        # Création de la grille de jeu
        self.creation_grille()

        # Boutons pour les niveaux de difficulté
        self.bouton_niveau_facile = tk.Button(self.frame_menu, text="Facile", font="Verdana, 11",
                                              command=self.niveau_facile, width=10,
                                              height=1, relief="groove")
        self.bouton_niveau_facile.grid(row=1, column=0, padx=5, pady=6)

        self.bouton_niveau_moyen = tk.Button(self.frame_menu, text="Moyen", font="Verdana, 11",
                                             command=self.niveau_moyen, width=10,
                                             height=1, relief="groove")
        self.bouton_niveau_moyen.grid(row=2, column=0, padx=5, pady=6)

        self.bouton_niveau_difficile = tk.Button(self.frame_menu, text="Difficile", font="Verdana, 11",
                                                 command=self.niveau_difficile,
                                                 width=10, height=1, relief="groove")
        self.bouton_niveau_difficile.grid(row=3, column=0, padx=5, pady=6)

        # Bouton pour réinitialiser le jeu
        self.bouton_reset_niveau = tk.Button(self.frame_menu, text="Réinitialiser", font="Verdana, 15",
                                             command=self.reset_partie, width=10,
                                             height=2)
        self.bouton_reset_niveau.grid(row=4, column=0, padx=5, pady=5)

    def gestion_clic_droit(self, event, ligne, colonne):
        # Vérifions si le clic est désactivé ou si la case est déjà révélée
        if not self.etat_clique or self.grille_cases[ligne][colonne].cget("relief") == "sunken":
            return

        # Récupérons la case correspondante dans la grille
        case = self.grille_cases[ligne][colonne]

        texte_actuel = case.cget("text")

        # Si la case n'a pas de texte, plaçons un drapeau
        if texte_actuel == "":
            case.config(text="🚩")
        # Si le texte actuel est un drapeau, changez-le en point d'interrogation
        elif texte_actuel == "🚩":
            case.config(text="❓")
        # Sinon, placez un drapeau
        else:
            case.config(text="", fg="red")

    def creation_grille(self):
        # Initialisation de la grille de cases
        self.grille_cases = []

        # Parcours des lignes de la grille
        for ligne_index in range(self.demineur.hauteur):
            row = []  # Initialisation d'une liste pour stocker les étiquettes de chaque ligne

            # Parcours des colonnes de la grille
            for colonne_index in range(self.demineur.largeur):
                # Création d'une étiquette (label) pour représenter une case dans la grille
                case_label = tk.Label(self.frame_grille, text=" ", width=4, height=2, relief="raised", bg="#43302f")

                # Positionnement de l'étiquette dans la grille graphique
                case_label.grid(row=ligne_index, column=colonne_index, padx=2, pady=2)

                # Liaison d'un clic de souris sur la case à la méthode reveler_cases
                case_label.bind("<Button-1>",
                                lambda e, ligne=ligne_index, colonne=colonne_index: self.reveler_cases(ligne, colonne))
                case_label.bind("<Button-3>",
                                lambda event, ligne=ligne_index, colonne=colonne_index: self.gestion_clic_droit(event,
                                                                                                                ligne,
                                                                                                                colonne))

                # Ajout d'un effet de survol à l'étiquette
                self.effet_clique(case_label)

                # Ajout de l'étiquette à la liste représentant la ligne actuelle de la grille
                row.append(case_label)

            # Ajout de la ligne complète de la grille à la liste représentant l'ensemble de la grille
            self.grille_cases.append(row)

    def reveler_cases(self, row, col):
        # Vérifie si le clic est désactivé
        if not self.etat_clique:
            return

        # Place les mines si elles ne sont pas encore placées
        if not self.demineur.mines_placees:
            self.demineur.placer_mines((row, col))

        # Vérifie si le chronomètre est déjà actif
        if not self.timer_actif:
            # Démarrer le chronomètre lorsque la première case est révélée
            self.demarrer_timer()

        # Récupère la case correspondante dans la grille
        case = self.grille_cases[row][col]

        # Change l'apparence de la case révélée
        case.config(bg="#cab2a3")  # Change la couleur de fond pour indiquer que la cellule a été révélée
        case.unbind("<Enter>")  # Désactive l'effet de survol lorsque la case est révélée
        case.unbind("<Leave>")  # Désactive l'effet de survol lorsque la case est révélée
        case.config(relief="sunken")  # Modifie le relief pour indiquer que la case est révélée

        # Vérifie si la case contient une bombe
        if self.demineur.grille[row][col] == -1:
            # Code pour gérer la révélation d'une case contenant une bombe
            case.config(text="💣")  # Affiche le symbole de bombe
            self.message_label.config(text="Vous avez perdu !", fg="white")  # Affiche un message de défaite
            self.etat_clique = False  # Désactive les clics sur la grille
            self.arreter_timer()  # Arrête le timer lorsque le joueur perd

            # Affiche toutes les bombes après la défaite
            for bombe_sur_la_ligne in range(self.demineur.hauteur):
                for bombe_dans_la_colonne in range(self.demineur.largeur):
                    if self.demineur.grille[bombe_sur_la_ligne][bombe_dans_la_colonne] == -1:
                        self.grille_cases[bombe_sur_la_ligne][bombe_dans_la_colonne].config(text="💣")
        else:
            # Si la case ne contient pas de bombe, affiche le nombre de bombes adjacentes
            nombre_bombes_adjacentes = self.demineur.compter_bombes_adjacentes(row, col)
            if nombre_bombes_adjacentes > 0:
                case.config(text=str(nombre_bombes_adjacentes))
            else:
                self.reveler_cases_vides(row, col)

        # Vérifie si le joueur a gagné après avoir révélé toutes les cases sans bombe
        cases_revelees = sum(1 for row in self.grille_cases for case in row if case.cget("relief") == "sunken")
        bombes_non_revelees = sum(row.count(-1) for row in self.demineur.grille)
        cases_totales = self.demineur.hauteur * self.demineur.largeur
        if cases_revelees == (cases_totales - bombes_non_revelees):
            self.message_label.config(text="Vous avez gagné !", fg="white")
            self.etat_clique = False
            # Arrête le timer lorsque le joueur gagne
            self.arreter_timer()

    def reveler_cases_vides(self, ligne, colonne):
        # Parcours des cases adjacentes à la case vide
        for ligne_adjacente in range(max(0, ligne - 1), min(self.demineur.hauteur, ligne + 2)):
            for colonne_adjacente in range(max(0, colonne - 1), min(self.demineur.largeur, colonne + 2)):
                # Vérifie si la case adjacente n'est pas déjà révélée et n'est pas une bombe
                if self.grille_cases[ligne_adjacente][colonne_adjacente]['bg'] == '#43302f' and \
                        self.demineur.grille[ligne_adjacente][colonne_adjacente] != -1:
                    # Révéler la case adjacente
                    self.reveler_cases(ligne_adjacente, colonne_adjacente)

    def effet_clique(self, case_label):
        # Associer un événement de survol de la souris à la fonction de gestion du survol à l'entrée de la case
        case_label.bind("<Enter>", lambda event, case=case_label: self.gestion_survol_entree(case))
        # Associer un événement de sortie de survol de la souris à la fonction de sortie de survol de la case
        case_label.bind("<Leave>", lambda event, case=case_label: self.sortir_survole_case(case))

    @staticmethod
    def gestion_survol_entree(case_label):
        case_label.config(bg="#a3a3a3")  # Changer la couleur de fond lorsque la souris survole la case

    @staticmethod
    def sortir_survole_case(case_label):
        # Vérifier si la case n'est pas révélée avant de restaurer sa couleur de fond par défaut
        if case_label.cget('relief') != 'sunken':
            case_label.config(bg="#43302f")

    def niveau_facile(self):
        # Réinitialiser le jeu avec les paramètres du niveau facile
        self.reset_partie(10, 10, random.randint(10, 15))

    def niveau_moyen(self):
        # Réinitialiser le jeu avec les paramètres du niveau moyen
        self.reset_partie(13, 13, random.randint(20, 35))

    def niveau_difficile(self):
        # Réinitialiser le jeu avec les paramètres du niveau difficile
        self.reset_partie(14, 14, random.randint(45, 55))

    def reset_partie(self, hauteur=None, largeur=None, mines=None):
        # Utiliser les paramètres donnés ou les valeurs par défaut pour réinitialiser le jeu
        hauteur = hauteur or self.demineur.hauteur
        largeur = largeur or self.demineur.largeur
        mines = mines or self.demineur.mines
        self.etat_clique = True
        self.temps_ecoule = 0  # Réinitialiser le temps écoulé
        self.arreter_timer()  # Arrêter le timer s'il est en cours

        # Supprimer les widgets existants de la grille de jeu
        for row in self.grille_cases:
            for case in row:
                case.destroy()

        # Réinitialiser la grille de jeu avec les nouvelles dimensions et le nombre de mines
        self.demineur = Demineur(hauteur, largeur, mines)
        self.creation_grille()  # Recréer la grille de jeu avec les nouvelles dimensions
        self.message_label.config(text="")  # Effacer tout message affiché précédemment

    def demarrer_timer(self):
        # Démarre le chronomètre en mettant à jour l'attribut timer_actif et en appelant la méthode d'actualisation du chronomètre
        self.timer_actif = True
        self.actualiser_timer()

    def actualiser_timer(self):
        # Méthode pour mettre à jour le chronomètre
        if self.timer_actif:
            self.temps_ecoule += 1
            self.texte_timer = "Temps écoulé : " + str(self.temps_ecoule) + " secondes"
            self.label_timer.config(text=self.texte_timer)
            self.after(1000, self.actualiser_timer)  # Appel récursif pour mettre à jour le chronomètre chaque seconde

    def arreter_timer(self):
        # Arrête le chronomètre en mettant à jour l'attribut timer_actif
        self.timer_actif = False


if __name__ == "__main__":
    app = DemineurUI(10, 10, random.randint(5, 10))  # Niveau facile par défaut

    app.mainloop()
