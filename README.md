# Projet 3 BIG DATA DigiFromagerie

Ce projet contient des scripts et des configurations pour l'installation et la gestion de HBase et Hadoop, ainsi que des outils pour l'importation de données et la visualisation dans Power BI.

## Structure du Projet

```
projet_fromagerie
    ├── /hbase
    │   ├── hbase_c.py  # Script d'importation des données dans HBase
    ├── /data
    │   └── dataw_fro03_mini_1000.csv # Fichier de données à importer pour les test
        └── dataw_fro03.csv # Fichier de données à importer (pour le projet)
    ├── /powerbi
    │   ├── dashboard.pbix      # Fichier Power BI pour visualisation
    └── /hadoop
        ├── /map
        │   └── mapper.py       # Script de mappage pour Hadoop
        └── /reducer
            └── reducer.py      # Script de réduction pour Hadoop
```

## Prérequis

Avant d'utiliser les scripts, assurez-vous que les éléments suivants sont installés et configurés :

- **HBase** : Suivez les instructions dans le répertoire `/hbase` pour installer et configurer HBase.
- **Hadoop** : Suivez les instructions dans le répertoire `/hadoop` pour installer et configurer Hadoop.
- **Python 3** : Assurez-vous que Python 3 est installé sur votre machine.
- **Bibliothèques Python** : Installez les bibliothèques nécessaires avec la commande suivante :
  ```bash
  pip install pandas happybase
  ```

## Configuration HBase

Avant de lancer le script d'importation, assurez-vous que le fichier de configuration `hbase-site.xml` est correctement configuré et que le serveur HBase est en cours d'exécution.

- **Vérifiez la connexion HBase** : Testez la connexion à HBase avant d'exécuter les scripts d'importation.

## Fichier CSV

Le fichier `dataw_fro03_mini_1000.csv` dans le répertoire `/data` doit contenir les colonnes suivantes pour être compatible avec le script d'importation :

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
   python hbase/hbase_c.py
   ```

### Détails du Script

- **Validation des Dates** : Le script vérifie que les dates sont au format `'%Y-%m-%d'`. Si nécessaire, vous pouvez ajuster le format de date dans la fonction `is_valid_date`.
- **Filtrage des Données** : Les lignes contenant des valeurs NULL ou des dates invalides sont automatiquement exclues de l'importation.
- **Insertion dans HBase** : Les données valides sont insérées dans HBase, en utilisant l'`id` comme clé primaire.

## MapReduce avec Hadoop

Le répertoire `/hadoop` contient des scripts pour traiter les données via Hadoop MapReduce.

- **Mapper** : Le script `mapper.py` est utilisé pour mapper les données.
- **Reducer** : Le script `reducer.py` gère l'agrégation ou la réduction des données.

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
