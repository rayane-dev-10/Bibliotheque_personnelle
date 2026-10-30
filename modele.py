import sqlite3

class Modele:
    def __init__(self, db_name="bibliotheque.db"):
        
        self.conn = sqlite3.connect("bibliotheque.db")
        self.cur = self.conn.cursor()
        self.creer_table()

    def creer_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS livres(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                genre TEXT NOT NULL,
                annee INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def ajouter(self, titre, auteur, genre, annee):
        self.cur.execute(
            "INSERT INTO livres(titre,auteur,genre,annee) VALUES (?,?,?,?)",
            (titre, auteur, genre, int(annee))
        )
        self.conn.commit()

    def modifier(self, livre_id, titre, auteur, genre, annee):
        self.cur.execute("""
            UPDATE livres SET titre=?, auteur=?, genre=?, annee=?
            WHERE id=?
        """, (titre, auteur, genre, int(annee), int(livre_id)))
        self.conn.commit()

    def supprimer(self, livre_id):
        self.cur.execute("DELETE FROM livres WHERE id=?", (int(livre_id),))
        self.conn.commit()

    def get_list(self):
        self.cur.execute("SELECT * FROM livres ORDER BY id DESC")
        return self.cur.fetchall()

    def rechercher(self, keyword):
  
        self.cur.execute("""
            SELECT *
            FROM livres
            WHERE titre LIKE ? OR auteur LIKE ? OR genre LIKE ? OR annee LIKE ?
            ORDER BY id DESC
        """, (f"{keyword}%", f"{keyword}%", f"{keyword}%",f"{keyword}%"))
        return self.cur.fetchall()

    def existe_titre(self, titre):
        self.cur.execute("SELECT 1 FROM livres WHERE titre = ?", (titre,))
        return self.cur.fetchone() is not None

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
