#!/usr/bin/env python
"""mapper.py"""

import sys
from datetime import datetime

# fonction pour vérifier si une valeur est vide, Null ou None
def invalid(value):
    return not value or value.lower() == 'null' or None or value.strip() == ''

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip() # il supprime les espaces devant et derrière
    # split the line into words
    columns = line.split(',') # le séparateur par défaut est la virgule

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
    for val in [codcli, nom, prenom, dpt, ville, date, qte, lbobj, points]:
        if any(invalid(val)):
            continue # ignore si une valeur pertinente est vide ou null

    # verification du département, extraction des deux premiers caractères du cpville
    if dpt.isdigit() and len(dpt) == 5:
        dpt = dpt[:2]
    else:
        continue

    # reformatage de la date au format YYY-MM-DD
    reformatted_date = None
    if '/' in date:
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y %H:%M')
            date_obj.timestamp()
            reformatted_date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            continue  # Ignore les lignes avec des dates mal formatées
        else:
            reformatted_date = date  # Garde le format original si déjà correct

    # verification et conversion de la quantité en entier
    try:
        qte = int(qte)
    except ValueError:
        continue

    # verification et conversion de la quantité en entier
    try:
        points  = int(points)
    except ValueError:
        continue


    # Extraire l'année de la date formatée
    year = int(reformatted_date.split('-')[0]) if '-' in reformatted_date else None
    if year is None:
        continue  # Ignore les lignes si l'année ne peut pas être extraite

    # Filtrer les données : entre 2008 et 2012 et pour les départements spécifiques
    if dpt in ['53', '61', '75', '28'] and 2008 <= year <= 2012:
        # Émettre la clé (nom prenom) et les valeurs pertinentes
        print("%i,%s\t%s,%s,%i,%s,%i,%i" % (codcli, nom.lower(), prenom.lower(), ville.lower(), dpt, lbobj.lower(), qte, points))


'''
hadoop jar hadoop-streaming-2.7.2.jar -file mapper.py -mapper "python3 mapper.py" -file reducer.py -reducer "python3 reducer.py" -input input/word.txt -output output01
'''