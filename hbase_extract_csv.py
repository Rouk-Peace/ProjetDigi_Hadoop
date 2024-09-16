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
    connection.disable_table('DigiFromagerie2')
    connection.delete_table('DigiFromagerie2')
    print('La table DigiFromagerie2 est supprimée')
except Exception as e:
    pass

try:
    madesc = {'cf': dict()}  # Création de la famille 'cf'
    connection.create_table('DigiFromagerie2', madesc)
    print("La table DigiFromagerie2 est créée")
except Exception as e:
    pass

# Positionnement sur la table 'DigiFromagerie2'
table = connection.table('DigiFromagerie2')

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

# Fonction pour extraire les données de HBase vers un fichier CSV
def extract_to_csv(output_filename):
    # Récupérer la table 'BigFromagerie'
    table = connection.table('BigFromagerie')
    
    # Ouvrir un fichier CSV pour écrire les données
    with open(output_filename, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Ecrire les en-têtes dans le fichier CSV
        headers = [
            'codcli', 'genrecli', 'nomcli', 'prenomcli', 'cpcli', 'villecli',
            'codcde', 'datcde', 'timbrecli', 'timbrecde', 'Nbcolis', 'cheqcli',
            'barchive', 'bstock', 'codobj', 'qte', 'Colis', 'libobj',
            'Tailleobj', 'Poidsobj', 'points', 'indispobj', 'libcondit', 
            'prixcond', 'puobj'
        ]
        writer.writerow(headers)
        
        # Parcourir les lignes de la table HBase
        for key, data in table.scan():
            row = [
                data.get(b'cf:codcli', b'').decode('utf-8'),
                data.get(b'cf:genrecli', b'').decode('utf-8'),
                data.get(b'cf:nomcli', b'').decode('utf-8'),
                data.get(b'cf:prenomcli', b'').decode('utf-8'),
                data.get(b'cf:cpcli', b'').decode('utf-8'),
                data.get(b'cf:villecli', b'').decode('utf-8'),
                data.get(b'cf:codcde', b'').decode('utf-8'),
                data.get(b'cf:datcde', b'').decode('utf-8'),
                data.get(b'cf:timbrecli', b'').decode('utf-8'),
                data.get(b'cf:timbrecde', b'').decode('utf-8'),
                data.get(b'cf:Nbcolis', b'').decode('utf-8'),
                data.get(b'cf:cheqcli', b'').decode('utf-8'),
                data.get(b'cf:barchive', b'').decode('utf-8'),
                data.get(b'cf:bstock', b'').decode('utf-8'),
                data.get(b'cf:codobj', b'').decode('utf-8'),
                data.get(b'cf:qte', b'').decode('utf-8'),
                data.get(b'cf:Colis', b'').decode('utf-8'),
                data.get(b'cf:libobj', b'').decode('utf-8'),
                data.get(b'cf:Tailleobj', b'').decode('utf-8'),
                data.get(b'cf:Poidsobj', b'').decode('utf-8'),
                data.get(b'cf:points', b'').decode('utf-8'),
                data.get(b'cf:indispobj', b'').decode('utf-8'),
                data.get(b'cf:libcondit', b'').decode('utf-8'),
                data.get(b'cf:prixcond', b'').decode('utf-8'),
                data.get(b'cf:puobj', b'').decode('utf-8')
            ]
            
            # Ecrire chaque ligne dans le fichier CSV
            writer.writerow(row)
    
    print(f"Les données ont été exportées dans {output_filename}")

# Appelle la fonction pour extraire les données dans un fichier CSV
extract_to_csv('output_fromagerie.csv')

# Fermeture de la connexion
connection.close()
