import tkinter as tk
from modele import Modele
from vue import Vue
from controleur import Controleur


def main():
    root = tk.Tk()
    modele = Modele()
    vue = Vue(root)
    controleur = Controleur(modele, vue)

    root.mainloop()


if __name__ == "__main__":
    main()
