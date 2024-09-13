#!/usr/bin/env python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_pdf import PdfPages

# Dictionnaire pour stocker les informations par client
clients = defaultdict(lambda: {'totalPoint': 0, 'objets': []})

# Fonction pour afficher les 10 meilleurs clients
def get_top_clients(clients):
    # Trier les clients par fidélité décroissante et sélectionner les 10 premiers
    return sorted(clients.items(), key=lambda x: x[1]['totalPoint'], reverse=True)[:10]

# Parcourir les données ligne par ligne depuis le mapper
for line in sys.stdin:
    line = line.strip()

    # Séparer la clé (client) et la valeur (Objet, Quantité, Fidélité)
    client, value = line.split('\t')
    dpt, villecli, lbobj, qte, points = value.split(',')

    quantite = int(qte)
    fidelite = int(points)

    # Accumuler les quantités et fidélités totales pour chaque client
    totalPoint = quantite * fidelite
    clients[client]['totalPoint'] += totalPoint
    clients[client]['Objets'].append((dpt,villecli, lbobj, qte, points))
    #clients[client]['fidelite_totale'] += fidelite
    #clients[client]['objets'][lbobj] += quantite  # Stocker tous les objets et leurs quantités


# Obtenir les 10 clients les plus fidèles
top_clients = get_top_clients(clients)
#nomcli, prenomcli, villecli, cpcli, codobj, qty, points, lbobj
# Exporter les résultats dans un fichier Excel
data = []
for client, info in top_clients:
    nomcli, prenomcli = client.split(' ')
    for objet in info['objets']:
        villecli,dpt, lbobj, qte, points = objet
        data.append([nomcli, prenomcli, villecli, dpt, lbobj, qte, info['totalPoint']])

# Créer un DataFrame Pandas
df = pd.DataFrame(data, columns=['Nom', 'Prénom', 'Ville', 'Département', 'Objet', 'Quantité', 'Fidélité totale'])

# Exporter le DataFrame dans un fichier Excel
df.to_excel('/datavolume1/top_clients_fideles.xlsx', index=False)

# Générer des graphiques en PDF pour les 10 clients
for client, info in top_clients:
    nomcli, prenomcli, villecli, dpt = client.split(',')
    objets = info['objets']
    output_pdf_file="/datavolume1/%s-%s.pdf"%(nomcli,prenomcli)

    # Créer un graphique en camembert (% des objets commandés par client)
    plt.figure(figsize=(6, 6))
    plt.pie(objets.values(), labels=objets.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Répartition des objets commandés pour %s-%s"%(nomcli,prenomcli))

    # Sauvegarder chaque graphique dans un fichier PDF distinct
    #plt.savefig(f"/datavolume1/{nomcli}_{prenomcli}_repartition.pdf")
    with PdfPages(output_pdf_file) as pdf:
        pdf.savefig()
    plt.close()

print("OK")
