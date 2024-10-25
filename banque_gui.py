import tkinter as tk
from tkinter import messagebox, simpledialog
from compte_bancaire import CompteBancaire

class BanqueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("brerootBank - Gestionnaire de Banque Simplifié")
        self.root.geometry("600x400")
        self.root.configure(bg="#f1f1f1")  # Couleur de fond blanche
        self.comptes = {}

        # Titre principal
        self.titre = tk.Label(self.root, text="brerootBank", font=("Arial", 24), bg="#115e8e", fg="white")
        self.titre.pack(fill=tk.X)

        # Menu principal
        self.menu_frame = tk.Frame(self.root, bg="#000")
        self.menu_frame.pack(pady=80)

        self.btn_creer = tk.Button(self.menu_frame, text="Créer un compte", command=self.creer_compte, width=20, bg="#333", fg="white")
        self.btn_acceder = tk.Button(self.menu_frame, text="Accéder à un compte", command=self.acceder_compte, width=20, bg="#333", fg="white")
        self.btn_quitter = tk.Button(self.menu_frame, text="Quitter", command=self.root.quit, width=20, bg="#333", fg="white", background="#960303")

        self.btn_creer.grid(row=0, column=0, padx=12, pady=12)
        self.btn_acceder.grid(row=1, column=0, padx=12, pady=12)
        self.btn_quitter.grid(row=2, column=0, padx=12, pady=12)

        # Footer
        self.footer_frame = tk.Frame(self.root, bg="#115e8e")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer_label = tk.Label(self.footer_frame, text="© 2024 breroot", bg="#115e8e", fg="white")
        self.footer_label.pack(pady=6)

    def creer_compte(self):
        # Fenêtre de création de compte
        self.creer_window = tk.Toplevel(self.root)
        self.creer_window.title("Créer un compte")
        self.creer_window.geometry("400x300")

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

        self.btn_confirmer = tk.Button(self.creer_window, text="Créer le compte", command=self.confirmer_creation)
        self.btn_confirmer.pack(pady=12)

    def confirmer_creation(self):
        # Récupérer les valeurs des entrées
        nom = self.nom_entry.get()
        solde_initial = float(self.solde_entry.get())
        taux_interet = float(self.taux_entry.get())
        pin = self.pin_entry.get()

        # Créer un nouveau compte
        compte = CompteBancaire(nom, solde_initial, taux_interet, pin)
        self.comptes[nom] = compte

        # Fermer la fenêtre de création et afficher un message de succès
        messagebox.showinfo("Succès", f"Compte {nom} créé avec succès !")
        self.creer_window.destroy()

    def acceder_compte(self):
        # Fenêtre d'accès à un compte
        self.acceder_window = tk.Toplevel(self.root)
        self.acceder_window.title("Accéder à un compte")
        self.acceder_window.geometry("300x200")

        tk.Label(self.acceder_window, text="Nom du compte:").pack(pady=6)
        self.nom_acces_entry = tk.Entry(self.acceder_window)
        self.nom_acces_entry.pack(pady=6)

        tk.Label(self.acceder_window, text="Code PIN:").pack(pady=6)
        self.pin_acces_entry = tk.Entry(self.acceder_window, show="*")
        self.pin_acces_entry.pack(pady=6)

        self.btn_confirmer_acces = tk.Button(self.acceder_window, text="Accéder", command=self.confirmer_acces)
        self.btn_confirmer_acces.pack(pady=10)

    def confirmer_acces(self):
        nom = self.nom_acces_entry.get()
        pin = self.pin_acces_entry.get()

        if nom in self.comptes and self.comptes[nom].pin == pin:
            self.ouvrir_menu_compte(self.comptes[nom])
            self.acceder_window.destroy()
        else:
            messagebox.showerror("Erreur", "Compte introuvable ou PIN incorrect.")

    def ouvrir_menu_compte(self, compte):
        # Menu pour gérer un compte spécifique
        self.menu_compte_window = tk.Toplevel(self.root)
        self.menu_compte_window.title(f"Gestion du compte - {compte.nom}")
        self.menu_compte_window.geometry("400x400")

        tk.Label(self.menu_compte_window, text=f"Compte: {compte.nom}").pack(pady=6)
        self.solde_label = tk.Label(self.menu_compte_window, text=compte.client_solde())
        self.solde_label.pack(pady=6)

        # Boutons pour les différentes opérations
        tk.Button(self.menu_compte_window, text="Déposer", command=lambda: self.operation_depot(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Retirer", command=lambda: self.operation_retrait(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Historique", command=lambda: self.afficher_historique(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Appliquer les intérêts", command=lambda: self.appliquer_interets(compte)).pack(pady=6)
        tk.Button(self.menu_compte_window, text="Transférer", command=lambda: self.operation_transfert(compte)).pack(pady=6)

    def operation_depot(self, compte):
        # Fenêtre de dépôt
        montant = float(tk.simpledialog.askstring("Dépôt", "Montant à déposer (€):"))
        resultat = compte.deposer(montant)
        self.solde_label.config(text=compte.client_solde())
        messagebox.showinfo("Dépôt", resultat)

    def operation_retrait(self, compte):
        # Fenêtre de retrait
        montant = float(tk.simpledialog.askstring("Retrait", "Montant à retirer (€):"))
        resultat = compte.retirer(montant)
        self.solde_label.config(text=compte.client_solde())
        messagebox.showinfo("Retrait", resultat)

    def afficher_historique(self, compte):
        # Fenêtre d'affichage de l'historique
        historique = compte.afficher_historique()
        messagebox.showinfo("Historique", historique)

    def appliquer_interets(self, compte):
        compte.appliquer_interets()
        self.solde_label.config(text=compte.client_solde())
        messagebox.showinfo("Intérêts", "Les intérêts ont été appliqués.")

    def operation_transfert(self, compte_source):
        # Fenêtre de transfert
        nom_destinataire = tk.simpledialog.askstring("Transfert", "Nom du compte destinataire:")
        montant = float(tk.simpledialog.askstring("Transfert", "Montant à transférer (€):"))

        if nom_destinataire in self.comptes:
            compte_destinataire = self.comptes[nom_destinataire]
            resultat = compte_source.transferer(montant, compte_destinataire)
            self.solde_label.config(text=compte_source.client_solde())
            messagebox.showinfo("Transfert", resultat)
        else:
            messagebox.showerror("Erreur", "Compte destinataire introuvable.")
            # End of BanqueGUI class
            # Path: pythonProject/final_project/BanqueGUI.py