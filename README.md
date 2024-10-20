# Documentation technique

## Stack technique

### Django

Framework Web Python avec une architecture MVC.

<https://www.djangoproject.com/>

#### DRF

Django REST framework (DRF) : application (module) Django pour l'API RESTful.

<https://www.django-rest-framework.org/>

### Amazon Aurora / PostgreSQL

Base de données relationnelle avec la version de comptabilité complète avec PostgreSQL.

<https://aws.amazon.com/fr/rds/aurora/>

### Docker

L'application est prévue pour être utilisée dans un containeur et un Dockerfile est présent.

## Configuration pour Django (src/app/settings.py)

- Pour la BDD on la configure comme pour PostgreSQL.
- Pour toutes les valeurs nécessaires à la connexion de la BDD on utilise des variables d'environnement. Si les variables n'existent pas alors les valeurs sont prisent depuis le fichier ".env" (utilisation locale).
- La valeur de la variable DEBUG vient aussi des variables d'environnement. Le déploiement automatique de la branch dev est en mode debug.

## CI/CD Pipeline

Les commit dans les branches main et dev ont des GitHub Actions.

### Tests

GitHub Actions exécute des tests avec pytest et un rapport de coverage (couverture) du code pour toutes les branches. Si les tests échouent la suite n'est pas exécutée.

### Déploiement

Ensuite, l'image est build et push dans le dépot d'aws ECR (Elastic Container Resgistry). Une mise à jour de la tache correspondante est effectuée (aws ECS Elastic Container Service) pour changer l'URI de l'image. Le service ECS prend le relais pour déployer la nouvelle définition de la tache.

**Il ne faut pas s'arrêter à la confirmation de GitHub**, le déploiement du containeur peut avoir des problèmes. Il est peut être nécessaire d'aller voir les logs de la tâche dans aws ECS.

Les fichier pour GitHub Actions sont dans le dossier `.github/workflows`.

## API RESTful

La fonction principale du back est de proposer une API RESTful.

On utilise les guidelines (lignes de conduite) usuelles car il n'existe pas de norme.

En mode debug l'API est auto documentée par drf-spectacular qui crée un schéma OpenAPI 3 et une mise en page avec Swagger UI et une autre avec redoc.

- <https://drf-spectacular.readthedocs.io/en/latest/>
- <https://swagger.io/tools/swagger-ui/>
- <https://github.com/Redocly/redoc>

Si le mode debug est désactivé alors l'API fournit uniquement les fichiers json en réponse aux requêtes, il y a aucune documentation.

Par exemple pour l'application DJango api et en local sur le port 8000 on trouve la documentation aux URLs suivantes :

- <http://localhost:8000/api/v1/swagger-ui/>
- <http://localhost:8000/api/v1/redoc/>

le schema :

- <http://localhost:8000/api/v1/schema/>

et les informations fournies par le rendu web de DRF :

- <http://localhost:8000/api/v1/>

## Développement en local

- Créer et configurer un fichier `.env`, copier `.env.example` comme modèle à éditer.
- Créer un containeur PostgreSQL pour avoir une BDD local.

Exemple:

```bash
docker volume create jo24-db-data
docker run -p 5432:5432 --name jo24-db -e POSTGRES_PASSWORD=jo24 -e POSTGRES_USER=jo24 -d --name jo24-db -v jo24-db-data:/var/lib/postgresql/data postgres:15.4
```

- Faire les migrations Django : `./manage.py migrate`.
- Charger les fixtures : `./manage.py loaddata ./api/fixtures/*json` (si besoin : `find -iwholename "*fixtures/*json" | xargs ./manage.py loaddata`.
- Lancer le serveur de dev : `./manage.py runserver`.
