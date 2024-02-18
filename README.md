# FloreAPI

API non officiel et open source de la Base de données des Trachéophytes de France métropolitaine et régions avoisinantes (bdtfx) de Tela Botanica, avec des **images** d'identiplante.

## Table des matières

* [À propos du projet](#à-propos-du-projet)
* [Documentation](#documentation)
* [Construit avec](#construit-avec)
* [Pour commencer](#pour-commencer)
  * [Prérequis](#prérequis)
  * [Installation](#installation)
* [Contributions](#contributions)
* [Auteurs](#autheurs)
* [Remerciements](#remerciements)

## À propos du projet

FloreAPI est une api pour obtenir des images de plante classé par plante. Les données des plantes sont tiré du site Tela botanica et les images d'Identiplante.

## Documentation

Voir la [documentation](https://bump.sh/instelce/doc/flore-api).

## Construit avec

* Django
* Django Rest Framework.

## Pour commencer

Pour mettre en place une copie locale de l'API et de la faire fonctionner, suivez ces étapes simples.

### Prérequis

* télécharger les données pour remplir la bdd [ici]()
* télécharger [python](https://www.python.org/)

### Installation

1. Cloner le repo et allez dans le dossier `flore-api`

```shell
git clone https://github.com/<Votre-Pseudo>/FloreAPI.git
cd flore-api
```

2. Créer un environnement virtuel et activez le

```shell
python -m venv env
./env/scripts/activate
```

3. Installer les dépendances

```shell
pip install -r requirements.txt
```

4. Dupliquez le fichier `.env.example` et renommez le `.env` et remplisser le.

5. Créer les tables

```shell
python ./manage.py migrate
```

6. Déziper le fichier `json_data` que vous avez télécharger et placer le dans le repo

7. Remplir la bdd

```shell
python .\manage.py runscript database_filler
```

8. Lancer le serveur de développement

```shell
python ./manage.py runserver
```

## Contributions

Les contributions que vous faites seront grandement appréciées.

* Si vous avez des suggestions pour ajouter ou supprimer des projets, n’hésitez pas à ouvrir une issue pour en discuter, ou à créer directement une Pull Request après avoir ajouter votre fonctionnalité.
* Assurez-vous de vérifier votre orthographe et votre grammaire.

### Créer une Pull Request

* Fork le projet
* Créer ta banche (git checkout -b feature/SuperFonctionnalité)
* Commit tes changements (git commit -m 'Ajout d'une SuperFonctionnalité')
* Push vers ta branche (git push origin feature/SuperFonctionnalité)
* Ouvre une Pull Request

# Auteurs

* *Célestin* - **Etudiant** - Instelce - Discord `instelce`

## Remerciements

- [Tela Botanica](https://www.tela-botanica.org/)
- [Identiplante](https://www.tela-botanica.org/appli:identiplante)
- [BDTFX](http://referentiels.tela-botanica.org/referentiel/index.php?module=Informations&ref=bdtfx)
