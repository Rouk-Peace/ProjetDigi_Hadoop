#!/usr/bin/env python
"""mapper.py"""
import csv
import sys


# fonction pour vérifier si une valeur est vide, Null ou None
def invalid(value):
    return not value or value.lower() == 'null' or value.strip() == ''

# input comes from STDIN (standard input)
# Utilisation de csv.reader


reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')


for columns in reader:

    # Extraction dse colonnes pertinnentes
    codcli = columns[0].strip()
    nom = columns[2].strip()
    prenom = columns[3].strip()
    dpt = columns[4].strip()
    ville = columns[5].strip()
    date = columns[7].strip()
    qte = columns[15].strip()
    lbobj = columns[17].strip()
    points = columns[20].strip()

    # verification des colonnes extraites pour s'assurer qu'elles ne sont pas vides ou Null
    if any(invalid(val) for val in [nom, prenom]):
        sys.stderr.write("Ignored due to invalid data: %s\n" % str(columns))
        continue  # ignore si une valeur pertinente est vide ou null

    # verification du département, extraction des deux premiers caractères du cpville
    if len(dpt) >= 5:
        dpt = dpt[:2]
    else:
        sys.stderr.write("Ignored due to invalid department format: %s\n" % dpt)
        continue

    # verification et conversion de la quantité en entier
    try:
        qte = int(qte)
    except ValueError:
        sys.stderr.write("Ignored due to invalid quantity: %s\n" % qte)
        continue

    # verification et conversion de la quantité en entier
    try:
        points = int(points)
    except ValueError:
        sys.stderr.write("Ignored due to invalid points: %s\n" % points)
        continue

    # Extraire l'année de la date formatée
    try:
        year = int(date.split('-')[0])
    except ValueError:
        sys.stderr.write("Ignored due to invalid date: %s\n" % date)
        continue  # Ignore les lignes si l'année ne peut pas être extraite

    # Filtrer les données : entre 2008 et 2012 et pour les départements spécifiques
    if dpt in ['53', '61', '75', '28'] and 2008 <= year <= 2012:
        # Émettre la clé (nom prenom) et les valeurs pertinentes
        print("%s %s\t,%s,%s,%s,%i,%i" % (nom.lower(), prenom.lower(), dpt, ville.lower(), lbobj.lower(), qte, points))
    else:
        sys.stderr.write("Ignored due to filter conditions: %s\n" % str(columns))



