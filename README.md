# Linkapp

Linkapp est une application web développée avec Django permettant de gérer et d'organiser des profils ainsi que leurs informations de contact.

## Présentation

L'objectif de Linkapp est de centraliser les informations relatives aux profils et de faciliter leur consultation et leur gestion à travers une interface web.

Le projet a été réalisé avec Django et permet de mettre en pratique le développement web, la gestion d'une base de données et l'organisation d'une application selon l'architecture Django.

## Fonctionnalités

* Création de profils
* Consultation des profils
* Modification des profils
* Suppression des profils
* Gestion des informations de contact
* Gestion des données avec une base de données
* Interface web
* Administration des données avec l'interface Django Admin

## Technologies utilisées

* Python
* Django
* HTML5
* CSS3
* Bootstrap
* SQLite3
* Git
* GitHub

## Prérequis

Pour exécuter le projet, vous devez disposer de :

* Python 3.11
* pip
* Git

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Felicianozan/Linkapp.git
```

Accéder ensuite au projet :

```bash
cd Linkapp
```

### 2. Créer un environnement virtuel

Sous Windows :

```bash
python -m venv venv
```

Activer l'environnement virtuel :

```bash
venv\Scripts\activate
```

Sous Linux ou macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

Si le fichier requirements.txt est présent :

```bash
pip install -r requirements.txt
```

Sinon, vous pouvez installer Django avec :

```bash
pip install django
```

## Configuration de la base de données

Le projet utilise SQLite3 pour le développement local.

La configuration se trouve dans le fichier :

```text
settings.py
```

Configuration utilisée :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Migrations

Avant de lancer l'application, appliquez les migrations :

```bash
python manage.py makemigrations
python manage.py migrate
```

## Lancer le projet

Démarrez le serveur de développement :

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse :

```text
http://127.0.0.1:8000/
```

## Interface d'administration

Pour créer un compte administrateur :

```bash
python manage.py createsuperuser
```

Suivez les instructions affichées dans le terminal.

L'interface d'administration est ensuite accessible à :

```text
http://127.0.0.1:8000/admin/
```

## Structure du projet

La structure générale du projet Django est organisée de la manière suivante :

```text
Linkapp/
│
├── README.md
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── Linkapp/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── application/
    ├── migrations/
    ├── templates/
    ├── static/
    ├── admin.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── forms.py
```

Le nom du dossier de l'application peut être différent selon l'organisation réelle du projet.

## Commandes principales

Créer les migrations :

```bash
python manage.py makemigrations
```

Appliquer les migrations :

```bash
python manage.py migrate
```

Créer un administrateur :

```bash
python manage.py createsuperuser
```

Lancer le serveur :

```bash
python manage.py runserver
```

Exécuter les tests :

```bash
python manage.py test
```

## Compétences mises en pratique

Ce projet permet notamment de mettre en pratique :

* Développement web avec Django
* Programmation Python
* Conception de modèles de données
* Gestion d'une base de données
* Création de vues et d'URLs
* Gestion des formulaires
* Utilisation des templates Django
* Gestion des migrations
* Utilisation de Django Admin
* Gestion de projet avec Git et GitHub

## Améliorations possibles

Les évolutions suivantes peuvent être ajoutées au projet :

* Authentification des utilisateurs
* Gestion des permissions
* Recherche de profils
* Filtrage des données
* Pagination
* API REST
* Système de notifications
* Amélioration de l'interface utilisateur
* Migration vers MySQL
* Déploiement en ligne

## Auteur

Feliciano Zannou

Licence en Systèmes Informatiques et Logiciels / Génie Informatique

GitHub :
https://github.com/Felicianozan

Portfolio :
https://feliciano-zan.netlify.app

## Licence

Ce projet a été développé à des fins d'apprentissage, de démonstration et de mise en pratique des compétences en développement informatique.
