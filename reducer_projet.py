#!/usr/bin/env python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Dictionnaire pour stocker les informations par client
clients = defaultdict(lambda: {'quantite_totale': 0, 'fidelite_totale': 0, 'objets': defaultdict(int)})

# Fonction pour afficher les 10 meilleurs clients
def get_top_clients(clients):
    # Trier les clients par fidélité décroissante et sélectionner les 10 premiers
    return sorted(clients.items(), key=lambda x: x[1]['fidelite_totale'], reverse=True)[:10]

# Parcourir les données ligne par ligne depuis le mapper
for line in sys.stdin:
    line = line.strip()

    # Séparer la clé (client) et la valeur (Objet, Quantité, Fidélité)
    client, value = line.split('\t')
    objet, quantite, fidelite = value.split(',')

    quantite = int(quantite)
    fidelite = int(fidelite)

    # Accumuler les quantités et fidélités totales pour chaque client
    clients[client]['quantite_totale'] += quantite
    clients[client]['fidelite_totale'] += fidelite
    clients[client]['objets'][objet] += quantite  # Stocker tous les objets et leurs quantités

# Obtenir les 10 clients les plus fidèles
top_clients = get_top_clients(clients)

# Exporter les résultats dans un fichier Excel
data = []
for client, info in top_clients:
    nom, prenom, ville, departement = client.split(',')
    for objet, quantite in info['objets'].items():
        data.append([nom, prenom, ville, departement, objet, quantite, info['fidelite_totale']])

# Créer un DataFrame Pandas
df = pd.DataFrame(data, columns=['Nom', 'Prénom', 'Ville', 'Département', 'Objet', 'Quantité', 'Fidélité totale'])

# Exporter le DataFrame dans un fichier Excel
df.to_excel('top_clients_fideles.xlsx', index=False)

# Générer des graphiques en PDF pour les 10 clients
for client, info in top_clients:
    nom, prenom, ville, departement = client.split(',')
    objets = info['objets']

    # Créer un graphique en camembert (% des objets commandés par client)
    plt.figure(figsize=(6, 6))
    plt.pie(objets.values(), labels=objets.keys(), autopct='%1.1f%%', startangle=140)
    plt.title(f"Répartition des objets commandés pour {nom} {prenom}")

    # Sauvegarder chaque graphique dans un fichier PDF distinct
    plt.savefig(f"{nom}_{prenom}_repartition_objets.pdf")
    plt.close()

print("Exportation Excel et graphiques PDF terminés.")
