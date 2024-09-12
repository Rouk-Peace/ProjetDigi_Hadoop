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
    ville, dpt, lbobj, qty, points = value.split(',')

    quantite = int(qty)
    fidelite = int(points)

    # Accumuler les quantités et fidélités totales pour chaque client
    clients[client]['quantite_totale'] += quantite
    clients[client]['fidelite_totale'] += fidelite
    clients[client]['objets'][lbobj] += quantite  # Stocker tous les objets et leurs quantités

# Obtenir les 10 clients les plus fidèles
top_clients = get_top_clients(clients)
#nomcli, prenomcli, villecli, cpcli, codobj, qty, points, lbobj
# Exporter les résultats dans un fichier Excel
data = []
for client, info in top_clients:
    nomcli, prenomcli, villecli, dpt = client.split(',')
    for lbobj, qty in info['objets'].items():
        data.append([nomcli, prenomcli, villecli, dpt, lbobj, qty, info['fidelite_totale']])

# Créer un DataFrame Pandas
df = pd.DataFrame(data, columns=['Nom', 'Prénom', 'Ville', 'Département', 'Objet', 'Quantité', 'Fidélité totale'])

# Exporter le DataFrame dans un fichier Excel
df.to_excel('top_clients_fideles.xlsx', index=False)

# Générer des graphiques en PDF pour les 10 clients
for client, info in top_clients:
    nomcli, prenomcli, villecli, dpt = client.split(',')
    objets = info['objets']

    # Créer un graphique en camembert (% des objets commandés par client)
    plt.figure(figsize=(6, 6))
    plt.pie(objets.values(), labels=objets.keys(), autopct='%1.1f%%', startangle=140)
    plt.title(f"Répartition des objets commandés pour {nomcli} {prenomcli}")

    # Sauvegarder chaque graphique dans un fichier PDF distinct
    plt.savefig(f"{nomcli}_{prenomcli}_repartition_objets.pdf")
    plt.close()

print("Exportation Excel et graphiques PDF terminés.")
