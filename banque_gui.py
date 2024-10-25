import tkinter as tk
from tkinter import messagebox, simpledialog
from compte_bancaire import CompteBancaire
import json  # Importation du module json pour sauvegarder et charger les comptes
import os  # Importation du module os pour vérifier l'existence du fichier
from datetime import datetime  # Importation du module datetime pour gérer les dates et heures

class BanqueGUI:
    def __init__(self, root):
        # Initialise l'interface graphique de la banque
        self.root = root
        self.root.title("brerootBank - Gestionnaire de Banque Simplifié")
        self.root.geometry("600x400")
        self.root.configure(bg="#a4dff4")  # Couleur de fond
        self.comptes = {}  # Dictionnaire pour stocker les comptes par nom de titulaire

        # Charger les comptes depuis le fichier JSON
        self.charger_comptes()

        # Titre principal
        self.titre = tk.Label(self.root, text="brerootBank", font=("Arial", 24), bg="#115e8e", fg="white")
        self.titre.pack(fill=tk.X)

        # Menu principal avec des boutons pour les options de gestion de compte
        self.menu_frame = tk.Frame(self.root, bg="#000")
        self.menu_frame.pack(pady=80)

        self.btn_creer = tk.Button(self.menu_frame, text="Créer un compte", command=self.creer_compte, width=20, bg="#333", fg="white")
        self.btn_acceder = tk.Button(self.menu_frame, text="Accéder à un compte", command=self.acceder_compte, width=20, bg="#333", fg="white")
        self.btn_quitter = tk.Button(self.menu_frame, text="Quitter", command=self.root.quit, width=20, bg="#333", fg="white", background="#960303")

        # Disposition des boutons dans le menu principal
        self.btn_creer.grid(row=0, column=0, padx=12, pady=12)
        self.btn_acceder.grid(row=1, column=0, padx=12, pady=12)
        self.btn_quitter.grid(row=2, column=0, padx=12, pady=12)

        # Pied de page
        self.footer_frame = tk.Frame(self.root, bg="#115e8e")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer_label = tk.Label(self.footer_frame, text="© 2024 breroot", bg="#115e8e", fg="white")
        self.footer_label.pack(pady=6)

    def creer_compte(self):
        # Ouvre une fenêtre pour la création d'un nouveau compte
        self.creer_window = tk.Toplevel(self.root)
        self.creer_window.title("Créer un compte")
        self.creer_window.geometry("400x400")

        # Champs pour entrer les informations du nouveau compte
        tk.Label(self.creer_window, text="Nom du compte:").pack(pady=6)
        self.nom_entry = tk.Entry(self.creer_window)
        self.nom_entry.pack(pady=6)

        tk.Label(self.creer_window, text="Solde initial (€):").pack(pady=6)
        self.solde_entry = tk.Entry(self.creer_window)
        self.solde_entry.pack(pady=6)

        tk.Label(self.creer_window, text="Taux d'intérêt (%):").pack(pady=6)
        self.taux_entry = tk.Entry(self.creer_window)
        self.taux_entry.pack(pady=6)

        tk.Label(self.creer_window, text="Code PIN:").pack(pady=6)
        self.pin_entry = tk.Entry(self.creer_window, show="*")
        self.pin_entry.pack(pady=6)

        tk.Label(self.creer_window, text="Type de compte:").pack(pady=6)
        self.type_compte = tk.StringVar(value="courant")
        tk.Radiobutton(self.creer_window, text="Courant", variable=self.type_compte, value="courant").pack(pady=2)
        tk.Radiobutton(self.creer_window, text="Épargne", variable=self.type_compte, value="epargne").pack(pady=2)
        tk.Radiobutton(self.creer_window, text="Pro", variable=self.type_compte, value="pro").pack(pady=2)

        # Bouton pour confirmer la création du compte
        self.btn_confirmer = tk.Button(self.creer_window, text="Créer le compte", command=self.confirmer_creation)
        self.btn_confirmer.pack(pady=12)

    def confirmer_creation(self):
        # Récupère et valide les informations du compte avant de l'enregistrer
        nom = self.nom_entry.get().lower()  # Normaliser le nom en minuscules
        solde_initial = float(self.solde_entry.get())
        taux_interet = float(self.taux_entry.get())
        pin = self.pin_entry.get()
        type_compte = self.type_compte.get()

        # Validation du code PIN
        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Erreur", "Le code PIN doit être composé de 4 chiffres.")
            return

        # Validation du taux d'intérêt
        if not (0 <= taux_interet <= 5):
            messagebox.showerror("Erreur", "Le taux d'intérêt doit être compris entre 0% et 5%.")
            return

        # Limite des types de comptes par titulaire
        if nom in self.comptes:
            comptes_utilisateur = [compte[0] for compte in self.comptes[nom]]
            if type_compte == "courant" and "courant" in comptes_utilisateur:
                messagebox.showerror("Erreur", "Vous ne pouvez pas avoir plus d'un compte courant.")
                return
            if type_compte == "epargne" and comptes_utilisateur.count("epargne") >= 2:
                messagebox.showerror("Erreur", "Vous ne pouvez pas avoir plus de deux comptes épargne.")
                return
            if type_compte == "pro" and comptes_utilisateur.count("pro") >= 2:
                messagebox.showerror("Erreur", "Vous ne pouvez pas avoir plus de deux comptes pro.")
        else:
            self.comptes[nom] = []

        # Création d'une instance de CompteBancaire et ajout au dictionnaire
        compte = CompteBancaire(nom, solde_initial, taux_interet, pin)
        self.comptes[nom].append((type_compte, compte))

        # Sauvegarder les comptes dans le fichier JSON
        self.sauvegarder_comptes()

        # Fermeture de la fenêtre et message de succès
        messagebox.showinfo("Succès", f"Compte {nom} ({type_compte}) créé avec succès !")
        self.creer_window.destroy()

    def acceder_compte(self):
        # Ouvre une fenêtre pour accéder à un compte existant
        self.acceder_window = tk.Toplevel(self.root)
        self.acceder_window.title("Accéder à un compte")
        self.acceder_window.geometry("300x200")

        # Champs pour entrer le nom du compte et le PIN
        tk.Label(self.acceder_window, text="Nom du compte:").pack(pady=6)
        self.nom_acces_entry = tk.Entry(self.acceder_window)
        self.nom_acces_entry.pack(pady=6)

        tk.Label(self.acceder_window, text="Code PIN:").pack(pady=6)
        self.pin_acces_entry = tk.Entry(self.acceder_window, show="*")
        self.pin_acces_entry.pack(pady=6)

        # Bouton pour confirmer l'accès au compte
        self.btn_confirmer_acces = tk.Button(self.acceder_window, text="Accéder", command=self.confirmer_acces)
        self.btn_confirmer_acces.pack(pady=10)

    def confirmer_acces(self):
        # Vérifie si le compte existe et si le PIN est correct
        nom = self.nom_acces_entry.get().lower()  # Normaliser le nom en minuscules
        pin = self.pin_acces_entry.get()

        if nom in self.comptes:
            for type_compte, compte in self.comptes[nom]:
                if compte.pin == pin:
                    self.ouvrir_menu_compte(compte)
                    self.acceder_window.destroy()
                    return
        messagebox.showerror("Erreur", "Compte introuvable ou PIN incorrect.")

    def ouvrir_menu_compte(self, compte):
        # Ouvre un menu pour gérer un compte spécifique
        self.menu_compte_window = tk.Toplevel(self.root)
        self.menu_compte_window.title(f"Gestion du compte - {compte.nom}")
        self.menu_compte_window.geometry("400x400")

        tk.Label(self.menu_compte_window, text=f"Compte: {compte.nom}").pack(pady=6)
        self.solde_label = tk.Label(self.menu_compte_window, text=compte.client_solde())
        self.solde_label.pack(pady=6)

        # Boutons pour effectuer des opérations sur le compte
        tk.Button(self.menu_compte_window, text="Déposer", command=lambda: self.operation_depot(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Retirer", command=lambda: self.operation_retrait(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Historique", command=lambda: self.afficher_historique(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Appliquer les intérêts", command=lambda: self.appliquer_interets(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Transférer", command=lambda: self.operation_transfert(compte)).pack(pady=6)

    def operation_depot(self, compte):
        # Demande le montant à déposer et met à jour le solde
        montant = float(tk.simpledialog.askstring("Dépôt", "Montant à déposer (€):"))
        resultat = compte.deposer(montant)
        self.solde_label.config(text=compte.client_solde())
        messagebox.showinfo("Dépôt", resultat)
        self.sauvegarder_comptes()  # Sauvegarder les comptes après l'opération

    def operation_retrait(self, compte):
        # Demande le montant à retirer et met à jour le solde
        montant = float(tk.simpledialog.askstring("Retrait", "Montant à retirer (€):"))
        resultat = compte.retirer(montant)
        self.solde_label.config(text=compte.client_solde())
        messagebox.showinfo("Retrait", resultat)
        self.sauvegarder_comptes()  # Sauvegarder les comptes après l'opération

    def afficher_historique(self, compte):
        # Affiche l'historique des transactions
        historique = compte.afficher_historique()
        messagebox.showinfo("Historique", historique)

    def appliquer_interets(self, compte):
        # Applique les intérêts au solde du compte
        compte.appliquer_interets()
        self.solde_label.config(text=compte.client_solde())
        messagebox.showinfo("Intérêts", "Les intérêts ont été appliqués.")
        self.sauvegarder_comptes()  # Sauvegarder les comptes après l'opération

    def operation_transfert(self, compte_source):
        # Demande les informations du compte destinataire et le montant à transférer
        nom_destinataire = tk.simpledialog.askstring("Transfert", "Nom du compte destinataire:").lower()  # Normaliser le nom en minuscules
        montant = float(tk.simpledialog.askstring("Transfert", "Montant à transférer (€):"))

        if nom_destinataire in self.comptes:
            compte_destinataire = self.comptes[nom_destinataire][0][1]  # Supposons qu'il n'y ait qu'un seul compte destinataire
            resultat = compte_source.transferer(montant, compte_destinataire)
            self.solde_label.config(text=compte_source.client_solde())
            messagebox.showinfo("Transfert", resultat)
            self.sauvegarder_comptes()  # Sauvegarder les comptes après l'opération
        else:
            messagebox.showerror("Erreur", "Compte destinataire introuvable.")

    def sauvegarder_comptes(self):
        # Sauvegarde les comptes dans un fichier JSON
        comptes_a_sauvegarder = {}
        for nom, comptes in self.comptes.items():
            comptes_a_sauvegarder[nom] = [
                (type_compte, {**compte.__dict__, "date_creation": compte.date_creation.isoformat()})
                for type_compte, compte in comptes
            ]
        with open("comptes.json", "w") as f:
            json.dump(comptes_a_sauvegarder, f)

    def charger_comptes(self):
        # Charge les comptes depuis le fichier JSON s'il existe
        if os.path.exists("comptes.json"):
            with open("comptes.json", "r") as f:
                comptes_charges = json.load(f)
                for nom, comptes in comptes_charges.items():
                    self.comptes[nom] = []
                    for type_compte, compte_data in comptes:
                        compte = CompteBancaire(
                            nom=compte_data["nom"],
                            solde=compte_data["solde"],
                            taux_interet=compte_data.get("taux_interet", 0),  # Utiliser 0 si la clé est manquante
                            pin=compte_data["pin"],
                            historique=compte_data["historique"],
                            date_creation=datetime.fromisoformat(compte_data["date_creation"])
                        )
                        self.comptes[nom].append((type_compte, compte))