import tkinter as tk  # Importation du module tkinter pour créer des interfaces graphiques
from banque_gui import BanqueGUI  # Importation de la classe BanqueGUI depuis le fichier banque_gui.py

# Lancer l'interface graphique
root = tk.Tk()  # Création de la fenêtre principale
app = BanqueGUI(root)  # Création d'une instance de l'application BanqueGUI
root.mainloop()  # Lancement de la boucle principale de l'interface graphique

# pythonProject/final_project/main.py