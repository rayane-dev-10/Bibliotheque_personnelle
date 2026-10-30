import tkinter as tk
from tkinter import messagebox

class Controleur:
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue

        self.vue.btn_ajouter.config(command=self.ajouter)
        self.vue.btn_modifier.config(command=self.modifier)
        self.vue.btn_supprimer.config(command=self.supprimer)

        self.vue.btn_reinitialiser.config(command=self.reinitialiser_formulaire)

        self.vue.btn_rechercher.config(command=self.rechercher)
        self.vue.btn_annuler.config(command=self.annuler_recherche)
        self.vue.btn_afficher_tout.config(command=self.remplir_tableau)

        self.vue.btn_quitter.config(command=self.quitter)


        self.vue.root.protocol("WM_DELETE_WINDOW", self.quitter)
        self.vue.tree.bind("<<TreeviewSelect>>", self.sur_selection)
        self.vue.tree.bind("<Button-1>", self.clic_treeview, add=True)
        self.vue.root.bind("<Escape>", lambda e: self.reinitialiser_formulaire())
        self.vue.root.bind("<Return>", lambda e: self.rechercher())


        self.remplir_tableau()

    def reinitialiser_formulaire(self):
        self.vue.vider_saisies()
        self.vue.effacer_selection()
        self.vue.btn_modifier.config(state="disabled")
        self.vue.btn_supprimer.config(state="disabled")

    def _valider_saisies(self):
        titre, auteur, genre, annee = self.vue.get_inputs()

        if not titre or not auteur or not genre or not annee:
            messagebox.showerror("Erreur", "veuillez remplir tous les champs.", parent=self.vue.root)
            return None


        annee = int(annee)
        if annee==0 or annee > 2026:
            messagebox.showerror("Erreur", "Veuillez saisir une année valide.", parent=self.vue.root)
            return None

        return titre, auteur, genre, annee

    def remplir_tableau(self):
        liste = self.modele.get_list()
        self.vue.remplir_tableau(liste)

    def ajouter(self):
        data = self._valider_saisies()
        if not data:
            return

        titre, auteur, genre, annee = data

        if self.modele.existe_titre(titre):
            messagebox.showerror("Erreur", "Un livre avec ce titre existe déjà.", parent=self.vue.root)
            return

        self.modele.ajouter(titre, auteur, genre, annee)
        messagebox.showinfo("succès","Livre ajouté.")
        self.remplir_tableau()
        self.reinitialiser_formulaire()
        

    def sur_selection(self, event=None):
        livre_id = self.vue.obtenir_id_selectionne()
        if livre_id is None:
            return

        valeurs = self.vue.tree.item(str(livre_id), "values")
        if not valeurs:
            return

        titre, auteur, genre, annee = valeurs
        self.vue.set_inputs(titre, auteur, genre, annee)

        self.vue.btn_modifier.config(state="normal")
        self.vue.btn_supprimer.config(state="normal")

    def modifier(self):
        livre_id = self.vue.obtenir_id_selectionne()

        data = self._valider_saisies()
        if not data:
            return

        titre, auteur, genre, annee = data

        ok = messagebox.askyesno("Confirmation", "Appliquer les modifications ?", parent=self.vue.root)
        if not ok:
            return

        self.modele.modifier(livre_id, titre, auteur, genre, annee)
        messagebox.showinfo("succès","Livre modifié.")
        self.remplir_tableau()
        self.reinitialiser_formulaire()
        

    def supprimer(self):
        livre_id = self.vue.obtenir_id_selectionne()
        
        ok = messagebox.askyesno("Confirmation", "Supprimer ce livre ?", parent=self.vue.root)
        if not ok:
            return

        self.modele.supprimer(livre_id)
        messagebox.showinfo("succès","Livre supprimé.")
        self.remplir_tableau()
        self.reinitialiser_formulaire()
        

    def rechercher(self):
        keyword = (self.vue.obtenir_recherche() or "")

        if not keyword:
            messagebox.showerror(
                "Erreur",
                "veuillez saisir un mot-clé avant de lancer la recherche.",
                parent=self.vue.root
            )
            return

        liste = self.modele.rechercher(keyword)

        if not liste:
            messagebox.showinfo(
                "Information",
                f"Aucun livre trouvé pour : {keyword}",
                parent=self.vue.root
            )

        self.vue.remplir_tableau(liste)

    def annuler_recherche(self):
        self.vue.vider_recherche()
        self.vue.root.focus_set()

    
    def quitter(self):
        ok = self.vue.boite_confirmation("voulez-vous vraiment quitter l'application ?")
        if not ok:
            return

        self.modele.close()
        self.vue.root.destroy()

    def clic_treeview(self, event):
        tree = self.vue.tree
        row_id = tree.identify_row(event.y)
        region = tree.identify("region", event.x, event.y)

        # clic dans une zone vide
        if region == "nothing" or row_id == "":
            self.reinitialiser_formulaire()
