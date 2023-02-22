# Environnement de développement

## Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On définit les variables d'environnement dans le fichier `.env`.
On peut utiliser le fichier d'example `.env.sample` comme ceci:

    cd /my/project/folder/
    cp .env.sample .env

Puis changer les valeurs dans le fichier `.env` pour votre environnement.   
Les variables d'environnement sont automatiquement intégrées au process uWSGI via
le fichier `ecc/wsgi.py` de même pour le fichier `webdav/wsgi.py`.


# Environnement de développement avec Docker
On peut utiliser Docker pour gagner du temps d'installation. Par contre ca utilise plus de mémoire. 

Si vous ne voulez pas utiliser Docker, voir le paragraphe suivant.

## Prérequis

- Nous utilisons [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/) pour installer l'environnement de dévelopement

Autres technos utilisées (pas besoin de les installer localement, elles sont sur docker):
 - Python
 - Django
 - RabbitMQ
 - PostgreSQL


## Présentation des containers
Nous utilisons trois containers Docker : un pour postgres, un pour rabbitmq et un pour django (cf https://github.com/ccomptes-fr/e-controle/blob/develop/docker-compose.yml).

Les containers postgres et rabbitmq ont une image standard, le django est une image fait maison (cf https://github.com/ccomptes-fr/e-controle/blob/develop/Dockerfile).

Quand on lance le container django avec `docker-compose run django`, il commence par exécuter https://github.com/ccomptes-fr/e-controle/blob/develop/startLocal.sh. Ce script migre la base postgres si necessaire, lance le serveur django et le process celery.

Le filesystem de la machine hôte est partagé avec le container django : le dossier `.` en local (root du repo git) est le même que le dossier `/code` sur le container. Les modifs en local apparaissent dans le container sans le relancer.

L'application webdav n'est pas utilisable en dev.

## Notre Docker Django

L'image docker pour Django peut être construite à partir de plusieurs images :  
- sur la base une image Node pour builder la partie front
- sur la base une image Python

Pour changer l'image de base, il faut changer l'option `dockerfile` specifiée dans `docker-compose.yml`.

## Lancement en dev avec docker-compose

Installer node et npm.
```
node --version
scoop install nodejs@16.14.2
```

Installer les dependances node :  
```
npm install
```

Builder le front :  
```
npm run build-all 
```
(pour developper par la suite, on pourra utiliser les commandes watch qui rebuildent au fur et à mesure des modifications. Voir package.json)

Créer le fichier avec les variables d'environnement :

    cp .env.sample .env

Optionnel, mais pratique : configurer l'envoi de mails.
Les users non-admin n'ont pas de mot de passe, ils recoivent un lien par mail pour se logger. Sans config mail, vous ne pourrez utiliser que des users admin (avec mot de passe, depuis l'interface admin : `<server url>/admin`).
 - Se créer un compte sur debug mail : https://debugmail.io
 - Les informations de connection SMTP se trouve dans les "settings" de debugmail
 - Modifier `.env` avec les informations de connection SMTP

Créer les variables d'environnement pour docker-compose :

    cp .env.docker-compose.sample .env.docker-compose


Builder l'image Docker pour django (`build` utilise la `Dockerfile`):

     docker-compose --env-file .env.docker-compose build

Dezipper les fichiers de `media.zip` dans un dossier `media` à la racine de ce projet.

Lancer le container `django`. Comme les container postgres et rabbitmq sont défini comme un dépendance (voir `links` dans docker-compose.yml), ils sont lancés aussi.

    docker-compose --env-file .env.docker-compose up -d

(en cas d'erreur `standard_init_linux.go:228: exec user process caused: no such file or directory` vérifier le type de retour chariot du fichier startLocal.sh, il doit être de type LF)

On peut accéder au site sur le port 8080 du localhost :  
http://localhost:8080/  
http://localhost:8080/admin  

L'email pour se connecter au site s'affiche dans les logs, recuperer le lien de connexion et le récuperer le code, exemple :  
https://example.com/chargement/code/dbd5ded602763add30832106cf676fca4bff9cce/  
=>   
http://localhost:8080/chargement/code/dbd5ded602763add30832106cf676fca4bff9cce/  

Pour demarrer celery : 
```
cd /code
celery multi start worker1\
        --beat -A ecc -l info\
        --scheduler=django_celery_beat.schedulers:DatabaseScheduler\
        --pidfile=/var/log/celery.pid\
        --logfile=/var/log/ecc-celery.log
```        

Pour construire les fichiers bundles du front en mode watch, en fonction des fichiers js/vue/css qui sont utilisés par la page, executer depuis votre PC, la commande npm run watch-XXX qui convient, exemple :  
```
npm run watch-questionnaire-detail  
```

## Configurer IDE pour utiliser un interpréteur depuis une image docker

Pour récupérer les dépendances, votre IDE va générer des fichiers dans un répertoire. Il est possible que le répertoire utilisé 
par défaut soit bloqué par l'antivirus. Il faut donc personnaliser le chemin d'accès et sélectionner celui que vous désirez.   
Veuillez consulter la page https://www.jetbrains.com/help/pycharm/directories-used-by-the-ide-to-store-settings-caches-plugins-and-logs.html pour plus d'informations et accéder au paramétrage des chemins d'accès.

Exemple de configuration : 
```
idea.base.path=C:/Workspace/Pycharm
idea.config.path=${idea.base.path}/config
idea.system.path=${idea.base.path}/system
idea.plugins.path=${idea.config.path}/plugins
idea.log.path=${idea.system.path}/log
```


# Environnement de développement sans Docker

Surtout utile si Docker utilise trop de mémoire (2 GB). C'est aussi plus simple pour connecter un IDE (comme VSCode ou autre).

## Postgres
Suivre ce tutorial pour installer postgres, et créer un user nommé `ecc` et une database nommée `ecc`.
https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/

Loader le dump dans la base de données qu'on vient de créer : voir paragraphe "Restaurer la base de données en dev"

## Node
Installer node et npm.

Installer les dependances node : `npm install`

Builder le front : `npm bun build-all` (pour developper par la suite, on pourra utiliser les commandes `watch` qui rebuildent au fur et à mesure des modifications. Voir `package.json`)

## Python et Django
Installer python 3 (sur mac il y a déja python 2 par default, il faut ajouter python 3 : https://docs.python-guide.org/starting/install3/osx/)

Installer un environnement virtuel python (pipenv ou virtualenv) : https://docs.python-guide.org/dev/virtualenvs/

Installer les dépendences python : `pip install -r requirements.txt`

Dans le fichier `.env`, modifier l'adresse de la db, puis sourcer l'environnement :
```
export DATABASE_URL=postgres://ecc:ecc@localhost:5432/ecc
. .env
```

Migrer la db : `python manage.py migrate`

Collecter les fichiers statiques : `python manage.py collectstatic --noinput`

Lancer le serveur local sur le port 8080 : `python manage.py runserver 0:8080`

Aller sur `http://localhost:8080/admin` et se logger avec un des utilisateurs mentionnés ci-dessous.


# Restaurer/Sauvegarder la base de données en dev

## Docker only : Se connecter à postgres
Pour se connecter à postgres avec l'installation docker, une méthode simple est de lancer un autre container, depuis lequel on se connecte à postgres. Par exemple le container `django`, sans la commande `dev` (on ne lance pas le serveur), avec la commande `bash` pour obtenir un terminal :

    docker-compose run django bash

## Charger le dump dans la base
Ensuite charger le dump dans la base.

Pour l'installation avec docker :

    psql -h postgres -U ecc -d ecc < db.dump

Pour l'installation sans docker :

    psql -h localhost -U ecc -d ecc < db.dump

Le mot de passe est `ecc` (défini dans docker-compose.yml pour Docker, et créé plus haut si pas de Docker)

Voilà des utilisateurs admin qui existent par défaut quand on utilise le dump de démo:
- Admin: admin@demo.com / demo12345
- Controlé: robert@demo.com / demo12345
- Contrôleur: martine@demo.com / demo12345

Note : Pour créer un nouveau dump :

    pg_dump --verbose --clean --no-acl --no-owner -h postgres -U ecc -d ecc > db.dump

# Login et envoi d'emails

Les utlisateurs admin peuvent se logger sans envoi d'email à http://localhost:8080/admin.
(Si vous avez utilisé le dump ci-dessus, essayez admin@demo.com / demo12345)

Les utilisateurs non-admin n'ont pas de mot de passe, ils recoivent un email contenant un lien de connexion. Votre serveur doit donc être configuré pour envoyer des mails.

## Serveur d'email en local
Python contient un petit serveur SMTP, qui printe les mail dans la console au lieu de les envoyer. C'est le plus simple pour developper.
Ajoutez les settings suivants dans `.env` :
```
export EMAIL_HOST='localhost'
export EMAIL_PORT=1025
export EMAIL_HOST_USER=''
export EMAIL_HOST_PASSWORD=''
export EMAIL_USE_TLS=False
export DEFAULT_FROM_EMAIL='testing@example.com'
```
Et lancez le serveur :
`python -m smtpd -n -c DebuggingServer localhost:1025`

(Merci à https://gist.github.com/andreagrandi/7027319)

# libmagic
Le serveur Django utilise libmagic (pour vérifier les types des fichiers uploadés), qui doit être présent sur la machine. Vous pouvez essayer de démarrer sans, et si le serveur raise une erreur c'est qu'il faut l'installer à la main sur votre machine.

Instructions d'installation données par django-magic, le package que nous utilisons : https://github.com/ahupp/python-magic#installation


# Des commandes utiles
Pour l'install docker :

    docker-compose --env-file .env.docker-compose run django
    docker-compose --env-file .env.docker-compose run django python3.6 manage.py runserver 0:8080
    docker-compose --env-file .env.docker-compose run django python3.6 manage.py shell_plus
    docker-compose --env-file .env.docker-compose run django <any-command>
    docker-compose --env-file .env.docker-compose up -d

    # lancer les tests unitaires sur un container django :
    docker-compose run django bash # l'environnement est sourcé par le docker-entrypoint.sh
    pytest


# Lancement en prod

- Une base PostgreSQL 11 doit être fournie.


# Définition des locales

Cette plateforme utilise l'encodage UTF-8 à plusieurs endroit, notament pour les nom de fichiers uploadés.

Pour que cela fonctionne, il faut rendre configurer correctement les 'locales',
par example comme ceci:

    localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8
    export LANG=fr_FR.UTF-8
    export LC_ALL=fr_FR.UTF-8

# Envoi d'emails périodiques

On utilise Celery Beat et RabbitMQ pour gérer l'envoi d'emails périodiques.

La fréquence des envois est configurée dans django admin, avec l'applicaiton 'django_celery_beat'.

Pour démarrer celery beat, il y a la commande suivante:

    celery worker --beat -A ecc -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &


# Gunicorn
Le server d'application Gunicorn est utilisé.   
Pour plus de détail : https://docs.gunicorn.org/en/stable/

# Parcel : Bundler JS

Nous avons fait le choix d'utiliser le bundler parcel qui est une alternative à Webpack.
Voir le fichier ``package.json`` pour plus de détails.

Quelques commandes bash utiles:

    npm install  # Pour installer les dépendences

    npm run build-all

    npm run watch-control-detail  # Pour construire le fichier bundle en mode watch
    npm run build-control-detail  # Pour construire le fichier bundle

    npm run watch-questionnaire-create
    npm run watch-questionnaire-detail
    npm run watch-session-management

# Tests

## Backend tests

La config est dans le fichier setup.cfg, cf partie `[tool:pytest]`

Lancer les tests :
`pytest -s <dossier>`
(le flag -s sert a laisser le debugger prendre le controle si besoin).
Exemple :
`pytest -s user_profiles`

Lancer un fichier de tests en particulier, exemple :
`pytest control/tests/test_api_questionnaire.py`

Lancer tous les tests :
`pytest`

## Frontend tests
Ils se situent dans `static/src/` avec le code, dans des dossiers `test`. Ce sont des tests Jest, pour trouver de la doc googler "test Vue with Jest" par exemple.

Lancer les tests : `npm test`

(npm install -g jest@26.1.0)

Tester un fichier en particulier :

`npm test <tout ou partie du nom de fichier>`.

Par exemple : `npm test Metadata` trouve le fichier `static/src/questionnaires/test/QuestionnaireMetadataCreate.spec.js`.

Debugger un test : plusieurs debuggers sont possibles, dont Chrome Dev Tools et Webstorm/Pycharm. Voir https://jestjs.io/docs/en/troubleshooting

Pour VScode, il y a une config pour debugger directement dans l'éditeur : `.vscode/launch.json`. La config s'appelle "Debug Jest Tests". Pour la lancer : ![image](https://user-images.githubusercontent.com/911434/72448689-ba28cb80-37b7-11ea-84b8-635040f8eaf1.png)
Ou voir la doc plus complète de VScode : https://code.visualstudio.com/docs/editor/debugging
