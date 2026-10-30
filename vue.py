import tkinter as tk
from tkinter import ttk


class Vue:
    def __init__(self, root):
        self.root = root
        self.root.title("Bibliothèque personnelle")

        self.largeur = 1240
        self.hauteur = 740

        self.root.geometry(f"{self.largeur}x{self.hauteur}")
        self.root.after(0,lambda: self.centrer_fenetre(self.largeur,self.hauteur))
        self.root.resizable(False,False)
        self.root.state("normal")

        self.root.configure(bg="#F3F4F6")

        try:
            self.root.iconbitmap("images/iconefenetre.ico")
        except Exception:
            pass

        self.couleur_fond = "#F3F4F6"
        self.couleur_carte = "#FFFFFF"
        self.couleur_bordure ="#E5E7EB"
        self.couleur_separteur="#DEDEDE"
        self.couleur_texte = "#0D0E11"
        self.couleur_texte_muet = "#6B7280"

        self.couleur_bleu = "#2563EB"
        self.couleur_vert = "#16A34A"
        self.couleur_rouge = "#D64242"
        self.couleur_noir = "#000000"

        self.police_titre = ("Calibri", 18, "bold")
        self.police_h2 = ("Segoe UI", 12, "bold")
        self.police_label = ("Segoe UI", 11)
        self.police_saisie = ("Segoe UI", 11)
        self.police_bouton = ("Segoe UI", 11)

        self.placeholder_annee = "ex: 2026"

        self._styler_treeview()
        self._construire_interface()

        self.ent_titre.focus_set()

     
    def centrer_fenetre(self, w: int, h: int):
        # 1) fixe la taille
        self.root.geometry(f"{w}x{h}")
        self.root.update_idletasks()

        # 2) calcule l'épaisseur des bordures + hauteur de la barre de titre
        border_x = self.root.winfo_rootx() - self.root.winfo_x()
        border_y = self.root.winfo_rooty() - self.root.winfo_y()

        # dimensions externes (fenêtre complète)
        outer_w = w + 2 * border_x
        outer_h = h + border_y + border_x  # bordure bas ~ border_x

        # 3) centre avec les dimensions externes
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = (sw - outer_w) // 2
        y = (sh - outer_h) // 2

        self.root.geometry(f"{w}x{h}+{x}+{y}")



    def _styler_treeview(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
        )
        style.map(
            "Treeview",
            background=[("selected", "#CFE8FF")],
            foreground=[("selected", "#111827")],
        )
        style.configure(
            "Treeview.Heading",
            background="#E6E6E6",
            foreground="#111827",
            font=("Segoe UI", 11, "bold"),
            relief="flat"
        )
        style.map("Treeview.Heading", background=[("active", "#E5E7EB")])


    def _carte(self, parent, x, y, w, h):
        cadre = tk.Frame(
            parent,
            bg=self.couleur_carte,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.couleur_bordure,
            highlightcolor=self.couleur_bordure
        )
        cadre.place(x=x, y=y, width=w, height=h)
        cadre.bind("<Button-1>", lambda e: self.root.focus_set())
        return cadre

    def _champ_saisie(self, parent, x, y, w, h=34, placeholder=None):
        entree = tk.Entry(
            parent,
            font=self.police_saisie,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.couleur_bordure,
            highlightcolor=self.couleur_bleu,
            fg=self.couleur_texte,
            bg="#FFFFFF",
        )
        entree.place(x=x, y=y, width=w, height=h)

        entree._placeholder = placeholder
        if placeholder:
            entree.insert(0, placeholder)
            entree.config(fg=self.couleur_texte_muet)
            entree.bind("<FocusIn>", self._placeholder_focus_in)
            entree.bind("<FocusOut>", self._placeholder_focus_out)
            entree.bind("<Button-1>", self._placeholder_click, add=True)

        return entree

    def _placeholder_click(self, event):
        entree = event.widget
        ph = getattr(entree, "_placeholder", None)
        if ph and entree.get() == ph:
            entree.delete(0, "end")
            entree.config(fg=self.couleur_texte)

    def _placeholder_focus_in(self, event):
        entree = event.widget
        ph = getattr(entree, "_placeholder", None)
        if ph and entree.get() == ph:
            entree.delete(0, "end")
            entree.config(fg=self.couleur_texte)

    def _placeholder_focus_out(self, event):
        entree = event.widget
        ph = getattr(entree, "_placeholder", None)
        if ph and entree.get().strip() == "":
            entree.insert(0, ph)
            entree.config(fg=self.couleur_texte_muet)

    def _bouton_plein(self, parent, texte, x, y, w, h, fond, fg="white", etat="normal"):
        btn = tk.Button(
            parent,
            text=texte,
            font=("Segoe UI", 10, "bold"),
            bg=fond,
            fg=fg,
            activebackground=fond,
            activeforeground=fg,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            state=etat,
        )
        btn.place(x=x, y=y, width=w, height=h)
        return btn

    def _bouton_doux(self, parent, texte, x, y, w, h, etat="normal"):
        btn = tk.Button(
            parent,
            text=texte,
            font=("Segoe UI", 10),
            bg="#EEF2F7",
            fg=self.couleur_texte,
            activebackground="#E5EAF2",
            activeforeground=self.couleur_texte,
            disabledforeground="#BDC4CE",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.couleur_bordure,
            cursor="hand2",
            state=etat,
        )
        btn.place(x=x, y=y, width=w, height=h)
        return btn

    def _valider_annee(self, nouvelle_valeur):
        if nouvelle_valeur == "":
            return True
        if nouvelle_valeur == self.placeholder_annee:
            return True
        if len(nouvelle_valeur) > 4:
            return False
        return nouvelle_valeur.isdigit()


    def _construire_interface(self):

        self.carte_gauche = self._carte(self.root, 18, 18, 360, 704)

        tk.Label(
            self.carte_gauche,
            text="DÉTAILS DU LIVRE",
            bg=self.couleur_carte,
            fg=self.couleur_texte,
            font=self.police_titre
        ).place(relx=0.5, y=30, anchor="center")

        dy = -20

        tk.Label(self.carte_gauche, text="Titre", bg=self.couleur_carte, fg=self.couleur_texte, font=self.police_label)\
            .place(x=22, y=84 + dy)
        self.ent_titre = self._champ_saisie(self.carte_gauche, 22, 112 + dy, 316)

        tk.Label(self.carte_gauche, text="Auteur", bg=self.couleur_carte, fg=self.couleur_texte, font=self.police_label)\
            .place(x=22, y=168 + dy)
        self.ent_auteur = self._champ_saisie(self.carte_gauche, 22, 196 + dy, 316)

        tk.Label(self.carte_gauche, text="Genre", bg=self.couleur_carte, fg=self.couleur_texte, font=self.police_label)\
            .place(x=22, y=252 + dy)
        self.ent_genre = self._champ_saisie(self.carte_gauche, 22, 280 + dy, 316)

        tk.Label(self.carte_gauche, text="Année", bg=self.couleur_carte, fg=self.couleur_texte, font=self.police_label)\
            .place(x=22, y=336 + dy)

        vcmd = (self.root.register(self._valider_annee), "%P")

        self.ent_annee = tk.Entry(
            self.carte_gauche,
            font=self.police_saisie,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.couleur_bordure,
            highlightcolor=self.couleur_bleu,
            fg=self.couleur_texte,
            bg="#FFFFFF",
            validate="key",
            validatecommand=vcmd
        )
        self.ent_annee.place(x=22, y=364 + dy, width=120, height=34)

        self.ent_annee._placeholder = self.placeholder_annee
        self.ent_annee.insert(0, self.placeholder_annee)
        self.ent_annee.config(fg=self.couleur_texte_muet)
        self.ent_annee.bind("<FocusIn>", self._placeholder_focus_in)
        self.ent_annee.bind("<FocusOut>", self._placeholder_focus_out)
        self.ent_annee.bind("<Button-1>", self._placeholder_click, add=True)


        self.btn_reinitialiser = self._bouton_doux(self.carte_gauche, "Réinitialiser", 110, 410, 140, 34)
        tk.Frame(self.carte_gauche, bg=self.couleur_separteur).place(x=22, y=460, width=316, height=2)

        btn_x = 70
        btn_w = 220
        btn_h = 42
        ecart = 12
        y = 475

        self.btn_ajouter = self._bouton_plein(self.carte_gauche, "Ajouter", btn_x, y, btn_w, btn_h, fond=self.couleur_bleu)
        y += btn_h + ecart

        self.btn_modifier = self._bouton_doux(self.carte_gauche, "Modifier", btn_x, y, btn_w, btn_h, etat="disabled")
        y += btn_h + ecart

        self.btn_supprimer = self._bouton_doux(self.carte_gauche, "Supprimer", btn_x, y, btn_w, btn_h, etat="disabled")


        separateur2_y = 640
        tk.Frame(self.carte_gauche, bg=self.couleur_separteur).place(x=22, y=separateur2_y, width=316, height=2)

        quitter_y = 655
        self.btn_quitter = self._bouton_plein(self.carte_gauche, "Quitter", 110, quitter_y, 140, 34,fond=self.couleur_rouge)


        self.carte_droite = self._carte(self.root, 396, 18, 826, 704)

        tk.Label(
            self.carte_droite,
            text="LISTE DES LIVRES",
            bg=self.couleur_carte,
            fg=self.couleur_texte,
            font=self.police_titre
        ).place(relx=0.5, y=30, anchor="center")


        y_ligne = 96
        h_ligne = 34
        ecart = 10

        larg_rechercher = 120
        larg_annuler = 95
        larg_tout = 120

        largeur_interne = 826 - 18 - 18
        largeur_saisie = largeur_interne - (larg_rechercher + larg_annuler + larg_tout + ecart * 3)

        self.ent_recherche = self._champ_saisie(
            self.carte_droite, 18, y_ligne, largeur_saisie, h=h_ligne,
            placeholder="  Titre, auteur ou ..."
        )

        x_btn = 18 + largeur_saisie + ecart
        self.btn_rechercher = self._bouton_plein(self.carte_droite, "Rechercher", x_btn, y_ligne, larg_rechercher, h_ligne, fond=self.couleur_bleu)
        x_btn += larg_rechercher + ecart

        self.btn_annuler = self._bouton_doux(self.carte_droite, "Annuler", x_btn, y_ligne, larg_annuler, h_ligne)
        x_btn += larg_annuler + ecart

        self.btn_afficher_tout = self._bouton_doux(self.carte_droite, "Afficher tout", x_btn, y_ligne, larg_tout, h_ligne)


        cadre_tableau = tk.Frame(self.carte_droite, bg=self.couleur_carte)
        cadre_tableau.place(x=18, y=170, width=790, height=510)

        self.scrollbar = tk.Scrollbar(cadre_tableau)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        cols = ("Titre", "Auteur", "Genre", "Année")
        self.tree = ttk.Treeview(cadre_tableau, columns=cols, show="headings", yscrollcommand=self.scrollbar.set)

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.column("Titre", width=260, anchor="w")
        self.tree.column("Auteur", width=220, anchor="w")
        self.tree.column("Genre", width=180, anchor="w")
        self.tree.column("Année", width=90, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)

        self.tree.tag_configure("pair", background="#FFFFFF")
        self.tree.tag_configure("impair", background="#F6F6F6")


    def boite_confirmation(self, message):
        fen = tk.Toplevel(self.root)
        fen.title("Confirmation")
        fen.configure(bg="white")
        fen.resizable(False, False)
        fen.transient(self.root)
        fen.grab_set()

        w, h = 360, 130
        fen.update_idletasks()

        px = self.root.winfo_rootx()
        py = self.root.winfo_rooty()
        pw = self.root.winfo_width()
        ph = self.root.winfo_height()

        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)

        fen.geometry(f"{w}x{h}+{x}+{y}")

        resultat = {"choix": False}

        centre = tk.Frame(fen, bg="white")
        centre.pack(expand=True, fill="both")

        lbl = tk.Label(
            centre,
            text=message,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 10),
            wraplength=320,
            justify="center"
        )
        lbl.pack(pady=(20, 15))

        zone_btn = tk.Frame(centre, bg="white")
        zone_btn.pack()

        def oui():
            resultat["choix"] = True
            fen.destroy()

        def non():
            resultat["choix"] = False
            fen.destroy()

        btn_oui = tk.Button(zone_btn, text="Oui", width=10, command=oui)
        btn_non = tk.Button(zone_btn, text="Non", width=10, command=non)

        btn_oui.grid(row=0, column=0, padx=10)
        btn_non.grid(row=0, column=1, padx=10)

        fen.bind("<Return>", lambda e: oui())
        fen.bind("<Escape>", lambda e: non())

        btn_non.focus_set()

        fen.wait_window()
        return resultat["choix"]    


    def get_inputs(self):
        titre = self.ent_titre.get().strip()
        auteur = self.ent_auteur.get().strip()
        genre = self.ent_genre.get().strip()
        annee = self.ent_annee.get().strip()

        if annee == self.placeholder_annee:
            annee = ""
        return titre, auteur, genre, annee

    def set_inputs(self, titre, auteur, genre, annee):
        self.ent_titre.delete(0,"end")
        self.ent_titre.insert(0, titre)

        self.ent_auteur.delete(0, "end")
        self.ent_auteur.insert(0, auteur)

        self.ent_genre.delete(0, "end")
        self.ent_genre.insert(0, genre)

        self.ent_annee.delete(0, "end")
        self.ent_annee.config(fg=self.couleur_texte)
        self.ent_annee.insert(0, str(annee))

    def vider_saisies(self):
        for ent in (self.ent_titre, self.ent_auteur, self.ent_genre):
            ent.delete(0, "end")

        self.ent_annee.delete(0, "end")
        self.ent_annee.insert(0, self.placeholder_annee)
        self.ent_annee.config(fg=self.couleur_texte_muet)

    def obtenir_recherche(self):
        texte = self.ent_recherche.get().strip()
        ph = getattr(self.ent_recherche, "_placeholder", None)

        if not texte:
            return ""
        if ph and texte == ph.strip():
            return ""
        return texte

    def vider_recherche(self):
        ph = getattr(self.ent_recherche, "_placeholder", None)
        self.ent_recherche.delete(0, "end")
        if ph:
            self.ent_recherche.insert(0, ph)
            self.ent_recherche.config(fg=self.couleur_texte_muet)

    def remplir_tableau(self, liste):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, (id_livre, titre, auteur, genre, annee) in enumerate(liste):
            tag = "pair" if i % 2 == 0 else "impair"
            self.tree.insert("", "end", iid=str(id_livre), values=(titre, auteur, genre, annee), tags=(tag,))

    def obtenir_id_selectionne(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(sel[0])

    def effacer_selection(self):
        self.tree.selection_remove(self.tree.selection())
