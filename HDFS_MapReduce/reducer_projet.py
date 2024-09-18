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
    client, value = line.split('\t')
    dpt, villecli, lbobj, qte, points = value.split(',')

    quantite = int(qte)
    fidelite = int(points)

    # Accumuler les quantités et fidélités totales pour chaque client
    totalPoint = quantite * fidelite
    clients[client]['totalPoint'] += totalPoint
    clients[client]['objets'][lbobj] += quantite

# Obtenir les 10 clients les plus fidèles
top_clients = get_top_clients(clients)

# Exporter les résultats dans un fichier Excel
data = []
for client, info in top_clients:
    nomcli, prenomcli = client.split(' ')

    # Filtrer les objets pour exclure "points bonus fidelite", "carte publicitaire", et "flyer"
    objets_filtres = {lbobj: qte for lbobj, qte in info['objets'].items() if
                      lbobj not in ["points bonus fidelite", "carte publicitaire", "flyer", "points flyer"]}

    for lbobj, qte in objets_filtres.items():
        data.append([nomcli, prenomcli, dpt, villecli, lbobj, qte, info['totalPoint']])

# Créer un DataFrame Pandas
df = pd.DataFrame(data, columns=['Nom', 'Prénom', 'Département', 'Ville', 'Objet', 'Quantité', 'Fidélité totale'])

# Exporter le DataFrame dans un fichier Excel
df.to_excel('/datavolume1/top_clients_fideles.xlsx', index=False)

# Générer des graphiques en PDF pour les 10 clients
for client, info in top_clients:
    nomcli, prenomcli = client.split(' ')
    objets = info['objets']

    # Filtrer les objets pour exclure "points bonus fidelite", "carte publicitaire", et "flyer"
    objets_filtres = {k: v for k, v in objets.items() if
                      k not in ["points bonus fidelite", "carte publicitaire", "flyer", "points flyer"]}

    output_pdf_file = "/datavolume1/%s-%s.pdf" % (nomcli, prenomcli)

    # Créer un graphique en camembert (% des objets commandés par client)
    plt.figure(figsize=(8, 8))
    plt.pie(
        objets_filtres.values(),
        labels=objets_filtres.keys(),
        autopct=lambda p: '%.1f%%\n(%d)' % (p, int(p * sum(objets_filtres.values()) / 100)),  # Affiche % et quantité
        startangle=140,
        colors=plt.cm.Paired.colors  # Palette de couleurs distinctes
    )
    plt.title("Répartition des objets commandés pour %s %s" % (nomcli.capitalize(), prenomcli.capitalize()))

    # Sauvegarder chaque graphique dans un fichier PDF distinct
    with PdfPages(output_pdf_file) as pdf:
        pdf.savefig()
    plt.close()

print("OK")
