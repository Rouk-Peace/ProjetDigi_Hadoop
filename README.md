# Projet 3 BIG DATA BigFromagerie

Ce projet utilise Hadoop MapReduce, Hbase et Power BI pour traiter et analyser les données de commandes clients d'une fromagerie. Le but est de filtrer les données, calculer la fidélité des clients, et générer des rapports exploitables pour la visualisation. 
Le projet s'exécute dans un ecosystème via une VM Hidora, avec des outils comme PuTTY et FileZilla pour la gestion des fichiers et connexions, ainsi que Docker pour l'architecture distribuée. Il contient des scripts et des configurations pour l'installation et la gestion de HBase et Hadoop HDFS, ainsi que des outils pour l'importation de données et la visualisation dans Power BI.
## Structure du Projet

```
projet_fromagerie
    ├── /hbase
    │   ├── hbase_c.py  # Script d'importation des données dans HBase
        ├── hbase_finale.py  # Script d'importation des données dans HBase
        ├── hbase_extract_csv.py  # Script d'importation des données dans HBase
    ├── /data
    │   └── dataw_fro03.csv            # Fichier de données à importer pour le final 
        └── dataw_fro03_mini_1000.csv  # Fichier de données à importer pour le test
    └── /HDFS
        ├── /map
        │   └── mapper.py       # Script de mappage pour Hadoop
        └── /reducer
            └── reducer.py      # Script de réduction pour Hadoop
            job.sh              # Script pour exécuter le job Hadoop et gérer les fichiers HDFS
```

## Prérequis

Avant d'utiliser les scripts, assurez-vous que les éléments suivants sont installés et configurés :

- **HBase** : Suivez les instructions dans le répertoire `/hbase` pour installer et configurer HBase.
- **Hadoop HDFS** : Suivez les instructions dans le répertoire `/hadoop HDFS` pour installer et configurer Hadoop.
- **Python 3** : Assurez-vous que Python 3 est installé sur votre machine.
- **FileZilla** : pour le transfert de fichiers
- **VM  avec Docker et Hadoop HDFS configurés
- **Bibliothèques Python** : Installez les bibliothèques nécessaires avec la commande suivante :
  ```bash
  pip install pandas happybase
  ```

## Configuration HBase

Avant de lancer le script d'importation, assurez-vous que le fichier de configuration `hbase-site.xml` est correctement configuré et que le serveur HBase est en cours d'exécution.

- **Vérifiez la connexion HBase** : Testez la connexion à HBase avant d'exécuter les scripts d'importation.

## Fichier CSV

Le fichier `dataw_fro03_mini_1000.csv ` dans le répertoire `/dataw_fro03_mini_1000.csv ` doit contenir les colonnes suivantes pour être compatible avec le script d'importation :

- `id` : Identifiant unique pour chaque enregistrement.
- `date_column` : Colonne contenant les dates qui seront vérifiées.
- `column1`, `column2`, etc. : Colonnes contenant les données à importer dans HBase.

## Script d'Importation

Le script `import_to_hbase.py` situé dans le répertoire `/hbase` gère l'importation des données dans HBase. Ce script vérifie et nettoie les données avant de les insérer dans la base.

### Utilisation du Script

1. **Configurer les paramètres HBase** : Avant d'exécuter le script, modifiez les variables suivantes dans le fichier `import_to_hbase.py` :

   - `HBASE_HOST` : L'adresse de votre serveur HBase.
   - `HBASE_PORT` : Le port de votre serveur HBase (par défaut, 9090).
   - `TABLE_NAME` : Le nom de la table HBase dans laquelle les données seront importées.

2. **Exécuter le script** :
   ```bash
   python hbase/import_to_hbase.py
   ```

### Détails du Script

- **Validation des Dates** : Le script vérifie que les dates sont au format `'%Y-%m-%d'`. Si nécessaire, vous pouvez ajuster le format de date dans la fonction `is_valid_date`.
- **Filtrage des Données** : Les lignes contenant des valeurs NULL ou des dates invalides sont automatiquement exclues de l'importation.
- **Insertion dans HBase** : Les données valides sont insérées dans HBase, en utilisant l'`id` comme clé primaire.

## MapReduce avec Hadoop

Le répertoire `/hadoop` contient des scripts pour traiter les données via Hadoop MapReduce.
**Étapes d'installation et d'exécution**
Transfert des fichiers vers la VM : Utilisez FileZilla pour transférer les fichiers mapper_projet.py, reducer_projet.py, dataw_fro03.csv, et job.sh vers la VM.

Connexion à la VM : Utilisez PuTTY pour vous connecter à votre VM  et accéder au système de fichiers HDFS orchestré via docker.
Accéder à l'OS master-Hadoop: Copié les fichiers dans le master
Exécution du script job.sh : exécutez le script job.sh pour gérer le workflow complet :

- **Mapper** : Le script `mapper.py` est utilisé pour mapper les données. Le Mapper traite les données, extrait et filtre les informations pertinentes (clients, objets, points de fidélité, etc.). Il génère des paires clé-valeur pour chaque client."
- **Reducer** : Le script `reducer.py` agrège les données par client et calcule les résultats finaux (somme des points de fidélité, objets commandés).

### Exécution de Hadoop

Assurez-vous que Hadoop est configuré correctement avant d'exécuter ces scripts. Vous pouvez exécuter une tâche MapReduce en utilisant les commandes Hadoop adaptées, en spécifiant les scripts de mappage et de réduction.

## Visualisation avec Power BI

Le fichier Power BI `dashboard.pbix` dans le répertoire `/powerbi` contient des visualisations basées sur les données importées dans HBase.


## Contribution

Pour contribuer à ce projet, suivez les étapes suivantes :

1. **Forker le dépôt** : Créez une copie du projet sur votre propre compte GitHub.

2. **Créer une branche pour vos modifications** :
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Commiter vos modifications** :
   ```bash
   git commit -am 'Ajout d'une nouvelle fonctionnalité'
   ```

4. **Pousser la branche sur votre fork** :
   ```bash
   git push origin feature/your-feature
   ```

5. **Créer une Pull Request** : Soumettez vos modifications pour examen en créant une Pull Request vers le dépôt principal.

## Licence

Ce projet est distribué sous la licence [MIT License](LICENSE).
