#!/usr/bin/env python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_pdf import PdfPages

# Dictionnaire pour stocker les informations par client
clients = defaultdict(lambda: {'totalPoint': 0, 'objets': defaultdict(int)})


# Fonction pour afficher les 10 meilleurs clients
def get_top_clients(clients):
    # Trier les clients par fidélité décroissante et sélectionner les 10 premiers
    return sorted(clients.items(), key=lambda x: x[1]['totalPoint'], reverse=True)[:10]


# Parcourir les données ligne par ligne depuis le mapper
for line in sys.stdin:
    line = line.strip()

    # Séparer la clé (client) et la valeur (Objet, Quantité, Fidélité)
    try:
        client, value = line.split('\t')
        dpt, villecli, lbobj, qte, points = value.split(',')

        quantite = int(qte)
        fidelite = int(points)

        # Accumuler les quantités et fidélités totales pour chaque client
        totalPoint = quantite * fidelite
        clients[client]['totalPoint'] += totalPoint
        clients[client]['objets'][(dpt, villecli, lbobj)] += quantite
    except ValueError as e:
        sys.stderr.write("Ignored line due to error: {}\n".format(str(e)))
        continue

# Obtenir les 10 clients les plus fidèles
top_clients = get_top_clients(clients)

# Préparer les données pour l'exportation Excel
data = []
for client, info in top_clients:
    nomcli, prenomcli = client.split(' ')
    for (dpt, villecli, lbobj), qte in info['objets'].items():
        data.append([nomcli, prenomcli, villecli, dpt, lbobj, qte, info['totalPoint']])

# Créer un DataFrame Pandas
df = pd.DataFrame(data, columns=['Nom', 'Prénom', 'Ville', 'Département', 'Objet', 'Quantité', 'Fidélité totale'])

# Exporter le DataFrame dans un fichier Excel
df.to_excel('/datavolume1/top_clients_fideles.xlsx', index=False)

# Générer des graphiques en PDF pour les 10 clients
for client, info in top_clients:
    nomcli, prenomcli = client.split(' ')
    objets = info['objets']
    output_pdf_file = "/datavolume1/{}-{}.pdf".format(nomcli, prenomcli)

    # Préparer les données pour le graphique
    objets_labels = [lbobj for (_, _, lbobj) in objets.keys()]
    objets_values = list(objets.values())

    # Créer un graphique en camembert (% des objets commandés par client)
    plt.figure(figsize=(6, 6))
    plt.pie(objets_values, labels=objets_labels, autopct='%1.1f%%', startangle=140)
    plt.title("Répartition des objets commandés pour {}-{}".format(nomcli, prenomcli))

    # Sauvegarder chaque graphique dans un fichier PDF distinct
    with PdfPages(output_pdf_file) as pdf:
        pdf.savefig()
    plt.close()

print("OK")
