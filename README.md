# éléments de l'approche adoptée:
Aprés avoir crée un environement virtuel (conda, venv...)
## Lecture de données
- Extraire les données de tous les fichiers de manière globale avec glob.
- La lecture des fichiers se fait avec l'utilisation de pandas.
- Entamer la partie transformation et nettoyage de données, ici juste un petit exemple a été fait
- Ensuite, l'idée était de construire une base de données pour y créer les tables analogues à nos dataframes (pandas).
- Il est clair que ça aurait été plus simple d'exploiter les dataframes

## Construction du fichier json finale
- Construction des dataframes soit par la base de données soit par lecture fichier.
- On crée un dict (corréspendant à la structure sur le pdf) python pour pouvoir y insérer les données qui nous interessent lors du parcours 
- On parcours drugs, clinical_trials et pubmed pour gérer les citations, dates de citation etc et donc remplir le dict.
- Enfin, on dump le dict vers un fichier qui s'appelera result.json.


## Structure
- Ici, on a 2 dossiers, le src, data:
    - Dans src, le fichier fetch_data?py permet de soliciter la base, récupérer les données, construire le json et le output.
    - data_ingestion.py permet de lire les fichiers puis de les introduire dans une base.
    - ad_hoc.py, la solution pour lla question liée au parcours du json final.
    - sql_requests.sql, les requêtes de la partie sql du test.
- A la racine on retruve le ficher json final, ce readme et un fichiers requirements.
- Ca aurait été plus interessant de mettre un fichier main à la racine qui fera ensuite appel aux fichiers src etc..

# Améliorations
- Conteneurisation de la solution (avec docker par exemple).
- Choisir un modèle unifié pour les données et leur types.
- Utilisation d'outils plus performant lors du traitement de données massives car pandas ne peut pas gérer ce genre de situations, utiliser pySpark par exemple.
- Exploitation d'un environement de travail plus adéquat à la gestion de grande masses de donées avec une faculté de scalabilité auto par exemple...(gcp,aws)