from datetime import datetime

class CompteBancaire:
    def __init__(self, nom, solde_initial, taux_interet, pin):
        self.nom = nom
        self.solde = solde_initial
        self.taux_interet = taux_interet
        self.pin = pin
        self.historique = []  # Stockage des transactions
        self.date_creation = datetime.now()

    def client_solde(self):
        return f"Solde actuel de {self.nom}: {self.solde} €"

    def deposer(self, montant):
        self.solde += montant
        self.historique.append(f"Déposé: {montant} € le {datetime.now()}")
        return f"{montant} € ont été déposés."

    def retirer(self, montant):
        if montant <= self.solde:
            self.solde -= montant
            self.historique.append(f"Retiré: {montant} € le {datetime.now()}")
            return f"{montant} € ont été retirés."
        else:
            return "Fonds insuffisants pour ce retrait."

    def afficher_historique(self):
        if self.historique:
            return "\n".join(self.historique)
        else:
            return "Aucune transaction effectuée."

    def appliquer_interets(self):
        interets = self.solde * self.taux_interet / 100
        self.solde += interets
        self.historique.append(f"Intérêts de {interets} € appliqués le {datetime.now()}")

    def transferer(self, montant, compte_destinataire):
        if montant <= self.solde:
            self.solde -= montant
            compte_destinataire.solde += montant
            self.historique.append(f"Transféré: {montant} € à {compte_destinataire.nom} le {datetime.now()}")
            compte_destinataire.historique.append(f"Reçu: {montant} € de {self.nom} le {datetime.now()}")
            return f"{montant} € ont été transférés à {compte_destinataire.nom}."
        else:
            return "Fonds insuffisants pour ce transfert."
         # End of CompteBancaire class
        # Path: pythonProject/final_project/banque_gui.py