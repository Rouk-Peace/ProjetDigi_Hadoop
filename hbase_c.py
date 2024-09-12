import happybase
import csv
import datetime

# Fonction pour vérifier la validité de la date
def is_valid_date(date_str):
    try:
        # Format attendu : AAAA-MM-JJ (modifie selon ton fichier)
        datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

# Connexion à HBase
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()

# Supprimer la table et la recréer
try:
    connection.disable_table('SuperFromagerie')
    connection.delete_table('SuperFromagerie')
    print('La table SuperFromagerie est supprimée')
except Exception as e:
    pass

try:
    madesc = {'cf': dict()}  # Création de la famille 'cf'
    connection.create_table('SuperFromagerie', madesc)
    print("La table SuperFromagerie  est créée")
except Exception as e:
    pass

# Positionnement sur la table 'SuperFromagerie'
table = connection.table('SuperFromagerie')
#print('Table :', table)

# Lecture du fichier CSV et importation en lots
with open('dataw_fro03_mini_1000.csv', mode='r') as csvfile:
    print('1')
    reader = csv.reader(csvfile)
    row_id = 1

    # Parcourir le fichier CSV ligne par ligne
    for row in reader:
        # Contraintes :
        print('2')
        prenomcli = row[3].strip()  # Champ prenomcli
        datcde = row[7].strip()     # Champ datcde

        # 1. Si prenomcli est vide, on ignore la ligne
        
        
        # 2. Si la date est invalide, on ignore la ligne
        if not is_valid_date(datcde):
            continue
        
        # 3. Si l'année est 2004, on ignore la ligne
        year = datcde.split('-')[0]  # Extraire l'année
        if year == '2004':
            continue

        # Construction des données sans valeurs NULL
        data = {
            b'cf:codcli': row[0].encode('utf-8'),
            b'cf:genrecli': row[1].encode('utf-8'),
            b'cf:nomcli': row[2].encode('utf-8'),
            b'cf:prenomcli': prenomcli.encode('utf-8'),
            b'cf:cpcli': row[4].encode('utf-8'),
            b'cf:villecli': row[5].encode('utf-8'),
            b'cf:codcde ': row[6].encode('utf-8'),
            b'cf:datcde': datcde.encode('utf-8'),
            b'cf:timbrecli': row[8].encode('utf-8'),
            b'cf:timbrecde': row[9].encode('utf-8'),
            b'cf:Nbcolis': row[10].encode('utf-8'),
            b'cf:cheqcli': row[11].encode('utf-8'),
            b'cf:barchive': row[12].encode('utf-8'),
            b'cf:bstock': row[13].encode('utf-8'),
            b'cf:codobj': row[14].encode('utf-8'),
            b'cf:qte': row[15].encode('utf-8'),
            b'cf:Colis': row[16].encode('utf-8'),
            b'cf:libobj': row[17].encode('utf-8'),
            b'cf:Tailleobj': row[18].encode('utf-8'),
            b'cf:Poidsobj': row[19].encode('utf-8'),
            b'cf:points': row[20].encode('utf-8'),
            b'cf:indispobj': row[21].encode('utf-8'),
            b'cf:libcondit': row[22].encode('utf-8'),
            b'cf:prixcond': row[23].encode('utf-8'),
            b'cf:puobj': row[24].encode('utf-8')
        }

        # Filtrer les champs qui sont à NULL ou vides
        # data_filtered = {k: v for k, v in data.items() if v.strip()}

        # Insertion dans la table HBase
        table.put(b'%i' % row_id, data)
        row_id += 1
        print(row_id)


# Fermeture de la connexion
connection.close()
