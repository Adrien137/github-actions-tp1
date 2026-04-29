# Projet Usine Logicielle – API REST Task Manager

## Présentation

Projet réalisé dans le cadre du module d’usine logicielle.

L’objectif est de mettre en place une API REST en Python avec Flask permettant la gestion de tâches (CRUD), tout en intégrant une vraie logique DevOps :

* CI/CD avec GitHub Actions
* conteneurisation Docker
* Infrastructure as Code avec Terraform
* configuration automatisée avec Ansible
* déploiement sur VM Azure
* supervision avec Prometheus et Grafana
* bonnes pratiques GitOps

Le projet permet de simuler une petite usine logicielle complète, proche d’un environnement professionnel.

---

## Fonctionnalités

L’API permet de :

* lire les tâches
* ajouter une tâche
* modifier une tâche
* supprimer une tâche
* vérifier l’état de l’application avec `/health`
* consulter les métriques avec `/metrics`

Routes principales :

* `GET /`
* `GET /health`
* `GET /metrics`
* `GET /api/tasks`
* `POST /api/tasks`
* `PUT /api/tasks/{id}`
* `DELETE /api/tasks/{id}`

---

## Structure de l’application

L’application est séparée en 3 fichiers pour garder un code propre et maintenable.

### `__init__.py`

Initialise Flask et enregistre les routes.

### `routes.py`

Contient toutes les routes HTTP de l’API REST.

### `services.py`

Contient la logique métier : ajout, modification, suppression et lecture des tâches.

Cela permet de séparer :

```text
configuration
↓
routes API
↓
logique métier
```

---

## Réalisation initiale du projet

Le projet était initialement prévu pour être déployé entièrement sur Azure avec une approche DevOps complète :

* Azure Web App
* Azure Container Registry (ACR)
* Service Principal
* App Registration
* déploiement GitHub → Azure
* Terraform
* Ansible

L’objectif était de reproduire une vraie architecture cloud moderne.

Cependant, les limitations du compte étudiant Azure ont empêché l’utilisation complète de Entra ID et la création du Service Principal nécessaire à l’authentification GitHub → Azure.

Le projet a donc été réorienté vers une solution plus réaliste et compatible :

## VM Azure Ubuntu + déploiement SSH

Cette solution permet :

* de contourner les limitations Azure
* de garder Terraform et Ansible
* de conserver un vrai déploiement automatisé
* de rester cohérent avec les principes DevOps

GitHub Actions se connecte donc en SSH sur la VM Azure pour exécuter le déploiement du conteneur.

---

## Connexion Azure en ligne de commande

Avant Terraform, il faut se connecter à Azure :

```powershell
az login
```

Cela ouvre la fenêtre de connexion Microsoft et permet à Terraform d’utiliser le compte Azure directement.

Cette méthode permet d’éviter le blocage lié au Service Principal sur le compte étudiant.

---

## Terraform – Création de la VM Azure

Terraform permet de créer automatiquement :

* Resource Group
* Réseau virtuel
* IP publique
* NSG
* VM Ubuntu Linux

Exécution :

```powershell
terraform init
terraform plan
terraform apply
```

Terraform permet de versionner l’infrastructure et d’éviter la création manuelle sur Azure.

---

## Clé SSH et pipeline

Lors de la création de la VM Azure, une clé SSH est générée.

Cette clé est obligatoire pour permettre à GitHub Actions de se connecter à la VM.

### Important

Il faut récupérer :

## la clé privée

Exemple :

```text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

et non la clé publique :

```text
ssh-rsa AAAA...
```

Cette clé privée est stockée dans GitHub Secrets.

---

## Déploiement Docker local

En parallèle, un déploiement local Docker a été conservé pour les tests rapides.

### Build de l’image

```powershell
docker build -t task-api .
```

### Lancer le conteneur

```powershell
docker run -d --name task-api -p 5000:5000 task-api
```

### Vérification

```text
http://localhost:5000/
http://localhost:5000/health
http://localhost:5000/metrics
http://localhost:5000/api/tasks
```

### Stop / suppression

```powershell
docker stop task-api
docker rm task-api
```

---

## Gestion des tâches avec PowerShell

### Ajouter une tâche

```powershell
$body = '{"title":"Nouvelle tache"}'

Invoke-RestMethod -Method POST `
  -Uri "http://localhost:5000/api/tasks" `
  -ContentType "application/json" `
  -Body $body
```

### Modifier une tâche

```powershell
$body = '{"done": true}'

Invoke-RestMethod -Method PUT `
  -Uri "http://localhost:5000/api/tasks/2" `
  -ContentType "application/json" `
  -Body $body
```

### Supprimer une tâche

```powershell
Invoke-RestMethod -Method DELETE `
  -Uri "http://localhost:5000/api/tasks/1"
```

### Voir les tâches

```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://localhost:5000/api/tasks"
```

---

## GitHub Actions – CI/CD

Deux workflows sont utilisés.

## 1er workflows : `ci.yml`

Exécuté sur :

* `develop`
* `main`

Contient :

### Ruff

Analyse qualité du code Python.

### Bandit

Analyse sécurité du code Python.

### Pytest

Tests automatisés de l’API.

### Coverage

Mesure le pourcentage de code testé.

### Docker Build

Validation du Dockerfile.

### Trivy

Scan de sécurité de l’image Docker.

### Son but

Valider le projet avant le déploiement.

---

## 2ème workflows : `deploy.yml`

Exécuté sur :

* `main`
* `develop`

Contient :

* connexion SSH à la VM Azure
* git pull
* docker build
* docker run
* redéploiement automatique

---

## GitOps / Git Flow

Le développement se fait sur :

```text
develop
```

Processus complet :

1. développement sur `develop`
2. push GitHub
3. lancement automatique des tests CI
4. validation
5. merge vers `main`
6. déploiement automatique sur la VM Azure

Cela respecte les bonnes pratiques GitOps de l'usine logiciel.

---

## GitHub Secrets

Stockage :

```text
GitHub → Settings → Secrets and variables → Actions
```

Secrets utilisés :

* `VM_HOST`
* `VM_USER`
* `VM_SSH_KEY`
* `VM_APP_PATH`
* `SONAR_TOKEN`

Ils permettent à GitHub Actions de se connecter en SSH à la VM Azure sans exposer d’informations sensibles dans le code. Ainsi que la connexion vers le sonarcloud.

---

## Supervision – Prometheus + Grafana

Une supervision a été ajoutée pour suivre l’état de l’application.

## `/health`

Permet de vérifier rapidement si l’application fonctionne.

Exemple :

```json
{
  "status": "ok",
  "service": "task-api"
}
```

## `/metrics`

Permet de récupérer des métriques applicatives :

* service
* version
* nombre total de tâches
* tâches terminées
* tâches en attente

Exemple :

```json
{
  "service": "task-api",
  "version": "1.0.0",
  "total_tasks": 5,
  "completed_tasks": 2,
  "pending_tasks": 3
}
```

## Pourquoi Prometheus + Grafana

Prometheus permet de récupérer automatiquement les métrriques de supervision.

Grafana permet d’afficher ces données dans des dashboards plus lisibles.

Cela permet :

* supervision applicative
* suivi de disponibilité
* visibilité sur l’activité
* démonstration DevOps plus complète

Cela apporte une vraie dimension monitoring au projet grâce à des dashboard plus compréhensibles et plus beaux que des metrics simples et directes

---

## Technologies utilisées

* Python
* Flask
* Docker
* GitHub
* GitHub Actions
* Terraform
* Ansible
* Azure VM
* Prometheus
* Grafana
* Ruff
* Bandit
* Pytest
* Trivy
* Sonarcloud

---

## Conclusion

Ce projet permet de démontrer :

* API REST
* CI/CD
* conteneurisation
* sécurité DevSecOps
* Infrastructure as Code
* déploiement cloud
* supervision
* l'opération GitOps
