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

# Fonction pour remplacer les valeurs nulles ou vides par une chaîne vide
def replace_null_or_empty(value):
    if value == 'NULL':
        return ""
    if value is None:
        return ""
    return value if value else ""

# Connexion à HBase
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()

# Supprimer la table et la recréer
try:
    connection.disable_table('DigiFromagerie')
    connection.delete_table('DigiFromagerie')
    print('La table DigiFromagerie est supprimée')
except Exception as e:
    pass

try:
    madesc = {'cf': dict()}  # Création de la famille 'cf'
    connection.create_table('BigFromagerie', madesc)
    print("La table BigFromagerie est créée")
except Exception as e:
    pass

# Positionnement sur la table 'BigFromagerie'
table = connection.table('BigFromagerie')

# Lecture du fichier CSV et importation en lots avec encodage UTF-8
with open('dataw_fro03.csv', mode='r', encoding='utf-8') as csvfile:  # Spécifie l'encodage utf-8 ici
    print('1')
    reader = csv.reader(csvfile)
    row_id = 1

    # Parcourir le fichier CSV ligne par ligne
    for row in reader:
        # Contraintes :
        print('2')
        prenomcli = replace_null_or_empty(row[3].strip())  # Champ prenomcli
        datcde = replace_null_or_empty(row[7].strip())     # Champ datcde

        # 1. Si prenomcli est vide, on ignore la ligne
        if not prenomcli:
            continue
        
        # 2. Si la date est invalide, on ignore la ligne
        if not is_valid_date(datcde):
            continue
        
        # 3. Si l'année est 2004, on ignore la ligne
        year = datcde.split('-')[0]  # Extraire l'année
        if year == '2004':
            continue

        # Construction des données sans valeurs NULL
        data = {
            b'cf:codcli': replace_null_or_empty(row[0]).encode('utf-8'),
            b'cf:genrecli': replace_null_or_empty(row[1]).encode('utf-8'),
            b'cf:nomcli': replace_null_or_empty(row[2]).encode('utf-8'),
            b'cf:prenomcli': prenomcli.encode('utf-8'),
            b'cf:cpcli': replace_null_or_empty(row[4]).encode('utf-8'),
            b'cf:villecli': replace_null_or_empty(row[5]).encode('utf-8'),
            b'cf:codcde': replace_null_or_empty(row[6]).encode('utf-8'),
            b'cf:datcde': datcde.encode('utf-8'),
            b'cf:timbrecli': replace_null_or_empty(row[8]).encode('utf-8'),
            b'cf:timbrecde': replace_null_or_empty(row[9]).encode('utf-8'),
            b'cf:Nbcolis': replace_null_or_empty(row[10]).encode('utf-8'),
            b'cf:cheqcli': replace_null_or_empty(row[11]).encode('utf-8'),
            b'cf:barchive': replace_null_or_empty(row[12]).encode('utf-8'),
            b'cf:bstock': replace_null_or_empty(row[13]).encode('utf-8'),
            b'cf:codobj': replace_null_or_empty(row[14]).encode('utf-8'),
            b'cf:qte': replace_null_or_empty(row[15]).encode('utf-8'),
            b'cf:Colis': replace_null_or_empty(row[16]).encode('utf-8'),
            b'cf:libobj': replace_null_or_empty(row[17]).encode('utf-8'),
            b'cf:Tailleobj': replace_null_or_empty(row[18]).encode('utf-8'),
            b'cf:Poidsobj': replace_null_or_empty(row[19]).encode('utf-8'),
            b'cf:points': replace_null_or_empty(row[20]).encode('utf-8'),
            b'cf:indispobj': replace_null_or_empty(row[21]).encode('utf-8'),
            b'cf:libcondit': replace_null_or_empty(row[22]).encode('utf-8'),
            b'cf:prixcond': replace_null_or_empty(row[23]).encode('utf-8'),
            b'cf:puobj': replace_null_or_empty(row[24]).encode('utf-8')
        }

        # Insertion dans la table HBase
        table.put(b'%i' % row_id, data)
        row_id += 1
        print(row_id)

# Fermeture de la connexion
connection.close()
