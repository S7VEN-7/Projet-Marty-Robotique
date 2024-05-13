# Projet-Marty-Robotique-

> THOME Vincent


Pour faire fonctionner le projet correctement, il nous faut les dépendances adaptées.
Ainsi, afin d'y parvenir il faut créer un environnement virtuel où l'on pourra installer ces dépendances. Pour ce faire, suivez les étapes ci-dessous.

Assurez-vous aussi d'avoir installé le module ***pip*** qui permet d'installer les dépendances.


## Instructions pour les utilisateur Linux / Mac

Allez simplement à la racine du dossier que vous avez créé pour le projet, rentrez dans un terminal (une invite de commandes) et tapez :

```
./config.sh
```

Après cette ligne de commandes, les dépendances devraient être bien installées.

<br>

## Instructions pour les utilisateur de Windows

Pour vous, il y a peu plus de travail, il vous faut rentrer dans le fichier `config.sh` avec un éditeur de texte par exemple, puis commenter cette ligne :

```sh
source env/bin/activate # Linux / Mac
```

Et décommenter cette ligne :

```sh
# .\env\Scripts\activate.bat # Windows
```

