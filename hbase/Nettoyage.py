#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import pandas as pd
import happybase
from datetime import datetime
 
# Fonction pour valider la date (années interdites et format valide)
def validate_date(date_str):
    """Valide le format de la date (YYYY-MM-DD). Renvoie False si la date est invalide ou de l'année 2004."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if date_obj.year == 2004:
            return False  # Rejeter les dates de 2004
        return True
    except ValueError:
        return False  # Date invalide
 
# Fonction pour ajouter un client sans valeurs NULL
def add_client(table, row_key, nom, prenom, ville):
    """Ajoute un client à HBase, en filtrant les valeurs NULL."""
    data = {}
    if pd.notnull(nom):
        data[b'client:nom'] = nom.encode('utf-8')
    if pd.notnull(prenom):
        data[b'client:prenom'] = prenom.encode('utf-8')
    if pd.notnull(ville):
        data[b'client:ville'] = ville.encode('utf-8')
    if data:
        table.put(row_key.encode('utf-8'), data)
 
# Fonction pour ajouter une commande sans valeurs NULL
def add_commande(table, row_key, date, nbcolis):
    """Ajoute une commande à HBase, en filtrant les valeurs NULL."""
    if not validate_date(date):
        print(f"Commande ignorée pour la clé {row_key}, date invalide ou année 2004.")
        return
    data = {}
    if pd.notnull(date):
        data[b'commande:date'] = date.encode('utf-8')
    if pd.notnull(nbcolis):
        data[b'commande:nbcolis'] = str(nbcolis).encode('utf-8')
    if data:
        table.put(row_key.encode('utf-8'), data)
 
# Fonction pour ajouter un objet sans valeurs NULL
def add_objet(table, row_key, libobj, prix):
    """Ajoute un objet à HBase, en filtrant les valeurs NULL."""
    data = {}
    if pd.notnull(libobj):
        data[b'objet:libobj'] = libobj.encode('utf-8')
    if pd.notnull(prix):
        data[b'objet:prix'] = str(prix).encode('utf-8')
    if data:
        table.put(row_key.encode('utf-8'), data)
 
# Connexion à HBase
connection = happybase.Connection('127.0.0.1', port=9090)
connection.open()
 
# Vérifiez si la table existe déjà, sinon créez-la
try:
    connection.create_table(
        'commerce_simple',
        {
            'client': dict(),
            'commande': dict(),
            'objet': dict()
        }
    )
except Exception as e:
    print("Table already exists or an error occurred:", e)
 
# Récupération de la table
table = connection.table('commerce_simple')
 
# Boucle sur les données de Power BI (dataset est fourni par Power BI)
for index, row in dataset.iterrows():
    # Ajouter un client (clé basée sur le code client)
    row_key_client = f"client_{row['codcli']}"
    add_client(table, row_key_client, row['nomcli'], row['prenomcli'], row['villecli'])
    # Ajouter une commande (clé basée sur le code commande et client)
    row_key_commande = f"commande_{row['codcde']}_client_{row['codcli']}"
    add_commande(table, row_key_commande, row['datcde'], row['Nbcolis'])
    # Ajouter un objet pour la commande (clé basée sur l'objet, commande et client)
    row_key_objet = f"objet_{row['codobj']}_commande_{row['codcde']}_client_{row['codcli']}"
    add_objet(table, row_key_objet, row['libobj'], row['puobj'])
 
# Afficher toutes les données de la table pour vérification
print('Affichage de la table après l\'import :')
for key, data in table.scan():
    print(key, data)
 
# Fermeture de la connexion à HBase
connection.close()

 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import happybase
 
def add_client(table, row_key, codcli, genrecli, nomcli, prenomcli, cpcli, villecli, timbrecli, cheqcli):
    """Ajoute un client dans la table"""
    table.put(
        row_key.encode('utf-8'),
        {
            b'client:codcli': str(codcli).encode('utf-8'),
            b'client:genrecli': genrecli.encode('utf-8'),
            b'client:nomcli': nomcli.encode('utf-8'),
            b'client:prenomcli': prenomcli.encode('utf-8'),
            b'client:cpcli': str(cpcli).encode('utf-8'),
            b'client:villecli': villecli.encode('utf-8'),
            b'client:timbrecli': str(timbrecli).encode('utf-8'),
            b'client:cheqcli': str(cheqcli).encode('utf-8')
        }
    )
 
def add_commande(table, row_key, codcde, datcde, timbrecde, Nbcolis, barchive, bstock):
    """Ajoute une commande dans la table"""
    table.put(
        row_key.encode('utf-8'),
        {
            b'commande:codcde': str(codcde).encode('utf-8'),
            b'commande:datcde': datcde.encode('utf-8'),
            b'commande:timbrecde': str(timbrecde).encode('utf-8'),
            b'commande:Nbcolis': str(Nbcolis).encode('utf-8'),
            b'commande:barchive': str(barchive).encode('utf-8'),
            b'commande:bstock': str(bstock).encode('utf-8')
        }
    )
 
def add_objet(table, row_key, codobj, qte, colis, libobj, Tailleobj, Poidsobj, points, indispobj, libcondit, prixcond, puobj):
    """Ajoute un objet dans la table"""
    table.put(
        row_key.encode('utf-8'),
        {
            b'objet:codobj': str(codobj).encode('utf-8'),
            b'objet:qte': str(qte).encode('utf-8'),
            b'objet:colis': colis.encode('utf-8'),
            b'objet:libobj': libobj.encode('utf-8'),
            b'objet:Tailleobj': Tailleobj.encode('utf-8'),
            b'objet:Poidsobj': str(Poidsobj).encode('utf-8'),
            b'objet:points': str(points).encode('utf-8'),
            b'objet:indispobj': str(indispobj).encode('utf-8'),
            b'objet:libcondit': libcondit.encode('utf-8'),
            b'objet:prixcond': str(prixcond).encode('utf-8'),
            b'objet:puobj': str(puobj).encode('utf-8')
        }
    )
 
# Connexion à HBase en localhost
connection = happybase.Connection('127.0.0.1', port=9090)
connection.open()
 
# 1. Créer la table si nécessaire
connection.create_table(
    'commerce',
    {
        'client': dict(),
        'commande': dict(),
        'objet': dict()
    }
)
 
# Récupération de la table commerce
table = connection.table('commerce')
 
# 2. Ajouter des enregistrements clients
add_client(table, 'client1', 1, 'M.', 'Dupont', 'Jean', 75001, 'Paris', 1234567890, 987654321)
add_client(table, 'client2', 2, 'Mme', 'Durand', 'Marie', 69001, 'Lyon', 1234567891, 987654322)
 
# 3. Ajouter des enregistrements commandes pour client1
add_commande(table, 'commande1_client1', 1001, '2023-09-10', 202309101234, 2, 0, 1)
add_commande(table, 'commande2_client1', 1002, '2023-09-12', 202309121234, 1, 1, 0)
 
# 4. Ajouter des objets à la commande1_client1
add_objet(table, 'objet1_commande1', 5001, 3, 'Colis A', 'Livre', 'XL', 1.5, 10, 0, 'Boîte', 15.99, 9.99)
add_objet(table, 'objet2_commande1', 5002, 1, 'Colis B', 'Chaussures', '42', 0.8, 20, 0, 'Sac', 59.99, 49.99)
 
# 5. Afficher toutes les données de la table
print('Affichage de la table :')
for key, data in table.scan():
    print(key, data)
 
# 6. Afficher la liste des commandes pour client1
print('\nAffichage des commandes de client1 :')
print(table.row(b'client1'))
 
# 7. Modifier la quantité d'un objet
table.put(b'objet1_commande1', {b'objet:qte': b'5'})
 
# 8. Supprimer un objet d'une commande
table.delete(b'objet2_commande1')
 
# 9. Afficher les commandes créées après 2023
print('\nAffichage des commandes après 2023 :')
for key, data in table.scan(filter="SingleColumnValueFilter('commande', 'datcde', >, 'binary:2023-01-01')"):
    print(key, data)
 
# Fermeture de la connexion
connection.close()

 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import happybase
 
# Fonction pour ajouter un client à la table HBase
def add_client(table, row_key, codcli, genrecli, nomcli, prenomcli, cpcli, villecli, timbrecli, cheqcli):
    """
    Ajoute un client dans la table HBase.
    table: La table HBase dans laquelle ajouter les données.
    row_key: Clé de ligne unique pour le client.
    codcli: Code client (numérique).
    genrecli: Genre du client (texte, ex: Mme).
    nomcli: Nom du client.
    prenomcli: Prénom du client.
    cpcli: Code postal du client.
    villecli: Ville du client.
    timbrecli: Timbre du client (numérique).
    cheqcli: Chèque du client (numérique).
    """
    table.put(
        row_key.encode('utf-8'),  # La clé de ligne doit être encodée en binaire
        {
            b'client:codcli': str(codcli).encode('utf-8'),  # Ajout du code client
            b'client:genrecli': genrecli.encode('utf-8'),  # Ajout du genre du client
            b'client:nomcli': nomcli.encode('utf-8'),  # Ajout du nom
            b'client:prenomcli': prenomcli.encode('utf-8'),  # Ajout du prénom
            b'client:cpcli': str(cpcli).encode('utf-8'),  # Ajout du code postal
            b'client:villecli': villecli.encode('utf-8'),  # Ajout de la ville
            b'client:timbrecli': str(timbrecli).encode('utf-8'),  # Ajout du timbre
            b'client:cheqcli': str(cheqcli).encode('utf-8')  # Ajout du chèque
        }
    )
 
# Fonction pour ajouter une commande à la table HBase
def add_commande(table, row_key, codcde, datcde, timbrecde, Nbcolis, barchive, bstock):
    """
    Ajoute une commande dans la table HBase.
    table: La table HBase dans laquelle ajouter les données.
    row_key: Clé de ligne unique pour la commande.
    codcde: Code de la commande (numérique).
    datcde: Date de la commande (format texte).
    timbrecde: Timbre de la commande (numérique).
    Nbcolis: Nombre de colis (numérique).
    barchive: Indicateur d'archivage (booléen ou numérique).
    bstock: Indicateur de stock (booléen ou numérique).
    """
    table.put(
        row_key.encode('utf-8'),  # Clé de ligne encodée en binaire
        {
            b'commande:codcde': str(codcde).encode('utf-8'),  # Ajout du code commande
            b'commande:datcde': datcde.encode('utf-8'),  # Ajout de la date de commande
            b'commande:timbrecde': str(timbrecde).encode('utf-8'),  # Ajout du timbre commande
            b'commande:Nbcolis': str(Nbcolis).encode('utf-8'),  # Ajout du nombre de colis
            b'commande:barchive': str(barchive).encode('utf-8'),  # Ajout de l'indicateur d'archivage
            b'commande:bstock': str(bstock).encode('utf-8')  # Ajout de l'indicateur de stock
        }
    )
 
# Fonction pour ajouter un objet à une commande
def add_objet(table, row_key, codobj, qte, colis, libobj, Tailleobj, Poidsobj, points, indispobj, libcondit, prixcond, puobj):
    """
    Ajoute un objet dans la table HBase.
    table: La table HBase dans laquelle ajouter les données.
    row_key: Clé de ligne unique pour l'objet.
    codobj: Code de l'objet (numérique).
    qte: Quantité de l'objet (numérique).
    colis: Colis lié à l'objet (texte).
    libobj: Libellé de l'objet (texte).
    Tailleobj: Taille de l'objet (texte).
    Poidsobj: Poids de l'objet (numérique).
    points: Points associés à l'objet (numérique).
    indispobj: Indicateur de disponibilité de l'objet (booléen ou numérique).
    libcondit: Libellé de la condition (texte).
    prixcond: Prix de la condition (numérique).
    puobj: Prix unitaire de l'objet (numérique).
    """
    table.put(
        row_key.encode('utf-8'),  # Clé de ligne encodée en binaire
        {
            b'objet:codobj': str(codobj).encode('utf-8'),  # Ajout du code objet
            b'objet:qte': str(qte).encode('utf-8'),  # Ajout de la quantité
            b'objet:colis': colis.encode('utf-8'),  # Ajout du colis
            b'objet:libobj': libobj.encode('utf-8'),  # Ajout du libellé objet
            b'objet:Tailleobj': Tailleobj.encode('utf-8'),  # Ajout de la taille de l'objet
            b'objet:Poidsobj': str(Poidsobj).encode('utf-8'),  # Ajout du poids
            b'objet:points': str(points).encode('utf-8'),  # Ajout des points
            b'objet:indispobj': str(indispobj).encode('utf-8'),  # Ajout de l'indisponibilité
            b'objet:libcondit': libcondit.encode('utf-8'),  # Ajout du libellé de la condition
            b'objet:prixcond': str(prixcond).encode('utf-8'),  # Ajout du prix de la condition
            b'objet:puobj': str(puobj).encode('utf-8')  # Ajout du prix unitaire
        }
    )
 
# Connexion à HBase sur localhost avec le port 9090
connection = happybase.Connection('node182954-env-1839015-Etudiant-L09.sh1.hidora.com', port=11526)
connection.open()  # Ouvrir la connexion à HBase
 
# Création de la table HBase "Digifromgerie" si elle n'existe pas déjà
try:
    connection.create_table(
        'Digifromgerie',
        {
            'client': dict(),  # Famille de colonnes pour les clients
            'commande': dict(),  # Famille de colonnes pour les commandes
            'objet': dict()  # Famille de colonnes pour les objets
        }
    )
except Exception as e:
    print("La table existe déjà ou une erreur s'est produite:", e)
 
# Récupération de la table "Digifromgerie"
table = connection.table('Digifromgerie')
 
# Ajout d'un exemple de client
add_client(table, 'client1', 123, 'M.', 'Dupont', 'Jean', 75000, 'Paris', 456, 1234)
 
# Ajout d'un exemple de commande
add_commande(table, 'commande1', 789, '2023-09-10', 987, 2, 0, 1)
 
# Ajout d'un exemple d'objet
add_objet(table, 'objet1', 456, 5, 'ColisA', 'Chaussures', 'L', 1.2, 100, 0, 'Neuf', 50, 49.99)
 
# Affichage de toutes les données de la table
print('Affichage de la table Digifromgerie :')
for key, data in table.scan():
    print(key, data)
 
# Fermeture de la connexion HBase
connection.close()