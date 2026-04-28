# Projet Fil Rouge – API REST Task Manager

## Présentation

Projet réalisé dans le cadre du module d’usine logicielle.

L’objectif est de mettre en place une petite API REST en Python avec Flask permettant la gestion de tâches (CRUD), tout en intégrant une pipeline CI/CD avec GitHub Actions, Docker et de bonnes pratiques GitOps.

---

## Fonctionnalités

L’API permet de :

* lire les tâches
* ajouter une tâche
* modifier une tâche
* supprimer une tâche
* vérifier l’état de l’application avec `/health`

Exemples de routes :

* `GET /health`
* `GET /api/tasks`

---

## Déploiement

Au vu de la situation ne permettant pas l’utilisation complète des services Azure (droits limités sur Entra ID / App Registration), le déploiement a été réalisé en local via Docker.

L’objectif reste le même : conteneuriser l’application et automatiser son exécution.

---

## Lancer le conteneur Docker

### Build de l’image

```powershell
docker build -t task-api .
```

### Lancer le conteneur

```powershell
docker run -d --name task-api -p 5000:5000 task-api
```

### Vérifier l’API

```text
http://localhost:5000/
http://localhost:5000/health
http://localhost:5000/api/tasks
```

### Stop / suppression

```powershell
docker stop task-api
docker rm task-api
```

---

## Gestion des tâches avec curl (PowerShell)

## Ajouter une tâche

```powershell
curl -Method POST `
  -Uri http://localhost:5000/api/tasks `
  -ContentType "application/json" `
  -Body '{"title":"Nouvelle tâche"}'
```

## Modifier une tâche

```powershell
curl -Method PUT `
  -Uri http://localhost:5000/api/tasks/1 `
  -ContentType "application/json" `
  -Body '{"done": true}'
```

## Supprimer une tâche

```powershell
curl -Method DELETE `
  -Uri http://localhost:5000/api/tasks/1
```

---

## GitHub Actions – Pipeline CI/CD

La pipeline se lance automatiquement sur les branches `main` et `develop`.

### Étapes :

1. Vérification du code avec Ruff
2. Scan sécurité avec Bandit
3. Lancement des tests avec pytest
4. Vérification de la couverture de tests
5. Build de l’image Docker

Si une étape échoue, la pipeline s’arrête.

---

## GitOps / Git Flow

Le développement se fait sur la branche secondaire :

```text
develop
```

### Processus

1. Développement sur `develop`
2. Push sur GitHub
3. GitHub Actions lance les tests
4. Si tout est valide → merge vers `main`

Cela permet d’éviter de pousser directement en production et respecte les bonnes pratiques GitOps.

---

## Secrets GitHub

Les secrets sont stockés dans :

```text
GitHub → Settings → Secrets and variables → Actions
```

Ils permettent de stocker de façon sécurisée les informations sensibles (credentials, clés SSH, variables de déploiement, etc.) sans les écrire dans le code.

Exemple :

* VM_HOST
* VM_USER
* VM_SSH_KEY

---

## Technologies utilisées

* Python
* Flask
* Docker
* GitHub
* GitHub Actions
* Ruff
* Bandit
* Pytest
* Azure (VM)

---

## Auteur

Projet réalisé dans le cadre du projet fil rouge – Usine Logicie
