import happybase
import csv 

'''
On se connecte de notre Host H1 pour interroger notre client Hbase
de notre Docker sur le port 16010 : ZooKeeper : HMASTER
'''
connection = happybase.Connection('127.0.0.1',9090) #9090
'''
A partir de l'objet connection (HBASE) : je fais open() pour me connecter
'''
connection.open()
'''
Je plante si on ne peut pas se connecter ....
'''

''' Supprimer la Table et la recréer '''
try:
    # Disable de la Table : maTable
    connection.disable_table('SuperFromagerie')
    # Puis delete de la Table : maTable
    connection.delete_table('SuperFromagerie')
    print('la table SuperFromagerie est supprimée')
except:
    pass
try:
    # Jecrée maTable avec une famille : 'CF'
    madesc = {'cf': dict()}
    connection.create_table('SuperFromagerie',madesc)
    print("ma Table est créée")
    #connection.enable_table('Fromagerie')
except:
    pass
'''
Je me positionne sur la Table 'maTable'
'''
table = connection.table('SuperFromagerie')
'''
si la table n'existe pas je plante
'''
print('table : ', table)

# Lecture du fichier CSV et importation en lots
with open('dataw_fro03_mini_1000.csv', mode='r') as csvfile:
    reader = csv.reader(csvfile)
    row_id = 1  
    # Parcourir le fichier CSV ligne par ligne
    for row in reader:
        # Utiliser une colonne comme clé de ligne HBase (ex. row[0] est un ID)


        # Insérer les autres colonnes dans HBase sous la famille de colonnes 'cf'
        table.put(b'%i'%(row_id), {
            b'cf:codcli': row[0].encode('utf-8'),  
            b'cf:genrecli': row[1].encode('utf-8'),  
            b'cf:nomcli': row[2].encode('utf-8'),  
            b'cf:prenomcli': row[3].encode('utf-8'), 
            b'cf:cpcli': row[4].encode('utf-8'), 
            b'cf:villecli': row[5].encode('utf-8'), 
            b'cf:codcde ': row[6].encode('utf-8'), 
            b'cf:datcde': row[7].encode('utf-8'), 
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
            b'cf:puobj': row[24].encode('utf-8'),
             
            # Ajoutez plus de colonnes si nécessaire...
        })
        row_id+=1













'''
A partir de l'objet table, je désire faire un scan sur la Famille => COLUMN : 'cf'
'''
# datas = table.scan(row_start='cf')
'''
si la famille n'existe pas je plante
'''
# print(datas)
'''
J'affiche l'instance de l'objet : datas
'''
'''
Je vais lire le RowId : 1 de maTable
'''
# try:
#     data = table.row(b'1') # j'encode le str '1'  en Byte : b'1' -> J'encode en Byte
#     # Data est un Dictionnaire {colonne : la famille et le nom de la colonne : la valeur correspondante}
#     # Attention on récupére dans le dicot des données en byte b'cf:a' : b'Test'
#     print(data)
#     print(data.get(b'cf:a').decode()) # Je récupére la valeur de ma clé (KEY) en string
# except:
#     print('le rowId 1 non trouvé !')
#     pass

# ajout d'une nouvelle ligne (row) dans ma maTable (HBASE)
# C'est vous qui gérait le contenu du RowId



connection.close()
