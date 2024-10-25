from datetime import datetime  # Importation du module datetime pour gérer les dates et heures

# Définition de la classe CompteBancaire pour représenter un compte bancaire
class CompteBancaire:
    # Initialisation d'un compte bancaire avec nom, solde initial, taux d'intérêt, et code PIN
    def __init__(self, nom, solde, taux_interet, pin, historique=None, date_creation=None):
        # Vérification que le PIN est composé de 4 chiffres
        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("Le code PIN doit être composé de 4 chiffres.")
        # Vérification que le taux d'intérêt est entre 0% et 5%
        if not (0 <= taux_interet <= 5):
            raise ValueError("Le taux d'intérêt doit être compris entre 0% et 5%.")

        # Initialisation des attributs du compte
        self.nom = nom  # Nom du titulaire du compte
        self.solde = solde  # Solde initial du compte
        self.taux_interet = taux_interet  # Taux d'intérêt annuel
        self.pin = pin  # Code PIN du compte pour la sécurité
        self.historique = historique if historique is not None else []  # Liste pour enregistrer l'historique des transactions
        self.date_creation = date_creation if date_creation is not None else datetime.now()  # Date de création du compte

    # Méthode pour afficher le solde actuel du compte
    def client_solde(self):
        return f"Solde actuel de {self.nom}: {self.solde} €"

    # Méthode pour déposer de l'argent sur le compte
    def deposer(self, montant):
        self.solde += montant  # Augmentation du solde
        # Enregistrement de la transaction dans l'historique
        self.historique.append(f"Déposé: {montant} € le {datetime.now()}")
        return f"{montant} € ont été déposés."

    # Méthode pour retirer de l'argent du compte
    def retirer(self, montant):
        # Vérification que le solde est suffisant pour le retrait
        if montant <= self.solde:
            self.solde -= montant  # Réduction du solde
            # Enregistrement de la transaction dans l'historique
            self.historique.append(f"Retiré: {montant} € le {datetime.now()}")
            return f"{montant} € ont été retirés."
        else:
            return "Fonds insuffisants pour ce retrait."

    # Méthode pour afficher l'historique des transactions du compte
    def afficher_historique(self):
        if self.historique:
            return "\n".join(self.historique)  # Retourne les transactions sous forme de texte
        else:
            return "Aucune transaction effectuée."

    # Méthode pour appliquer les intérêts annuels au solde du compte
    def appliquer_interets(self):
        interets = self.solde * self.taux_interet / 100  # Calcul des intérêts
        self.solde += interets  # Ajout des intérêts au solde
        # Enregistrement de la transaction dans l'historique
        self.historique.append(f"Intérêts de {interets} € appliqués le {datetime.now()}")

    # Méthode pour transférer un montant vers un autre compte
    def transferer(self, montant, compte_destinataire):
        # Vérification que le montant de transfert est positif
        if montant <= 0:
            return "Le montant du transfert doit être supérieur à 0."
        # Vérification que le solde est suffisant pour le transfert
        if montant <= self.solde:
            self.solde -= montant  # Réduction du solde du compte de l'expéditeur
            compte_destinataire.solde += montant  # Augmentation du solde du compte destinataire
            # Enregistrement de la transaction dans l'historique des deux comptes
            self.historique.append(f"Transféré: {montant} € à {compte_destinataire.nom} le {datetime.now()}")
            compte_destinataire.historique.append(f"Reçu: {montant} € de {self.nom} le {datetime.now()}")
            return f"{montant} € ont été transférés à {compte_destinataire.nom}."
        else:
            return "Fonds insuffisants pour ce transfert."
# pythonProject/final_project/compte_bancaire.py