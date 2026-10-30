#  Gestion de Bibliothèque de Livres

Application de bureau développée en Python permettant de gérer une bibliothèque de livres de manière simple et intuitive grâce à une architecture **Modèle-Vue-Contrôleur (MVC)** et une base de données **SQLite**.

---

##  Fonctionnalités

* **Ajouter un livre** : Enregistrer de nouveaux ouvrages (titre, auteur, année, etc.).
* **Modifier les informations** : Mettre à jour les détails d'un livre existant.
* **Supprimer un livre** : Retirer un ouvrage de la base de données.
* **Rechercher et Afficher** : Consulter la liste complète des livres enregistrés.

---

##  Structure du Projet

Le projet est organisé selon les principes de l'architecture **MVC** :

```text
📦 Biblioth-que_de_livres
 ┣ 📜 main.py            # Point d'entrée de l'application
 ┣ 📜 modèle.py          # Gestion des données et des requêtes SQLite
 ┣ 📜 vue.py             # Interface utilisateur
 ┣ 📜 contrôleur.py      # Logique de liaison entre le modèle et la vue
 ┣ 📜 bibliothèque.db    # Base de données SQLite
 ┗ 📂 images             # Ressources graphiques du projet
```
## Prérequis
* Assurez vous d'avoir installé Python 3.x sur votre machine.
* Exécutez le fichier principal **main.py** depuis votre terminal en tapant la commande : python main.py
