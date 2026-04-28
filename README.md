# Projet Fil Rouge - Usine Logicielle

## Objectif

Ce projet est une API REST JSON simple réalisée en Python avec Flask. Elle sert de support au projet d'usine logicielle : code source documenté, tests automatisés, pipeline CI/CD, Docker, Infrastructure as Code et déploiement automatisé sur Azure.

## Fonctionnalités

L'API permet de gérer une liste de tâches :

- Vérifier l'état de santé de l'application
- Lister les tâches
- Consulter une tâche
- Créer une tâche
- Modifier une tâche
- Supprimer une tâche

## Stack technique

- Python 3.12
- Flask
- pytest
- pytest-cov
- Ruff
- Bandit
- Docker
- GitHub Actions
- Terraform
- Ansible
- Azure Web App for Containers
- Azure Container Registry

## Architecture du repository

```text
.
├── app/                    # Code source Flask
├── tests/                  # Tests automatisés pytest
├── .github/workflows/      # Pipelines GitHub Actions
├── infra/
│   ├── terraform/          # Infrastructure as Code Azure
│   └── ansible/            # Exemple de déploiement VM
├── docs/                   # Documentation complémentaire
├── Dockerfile              # Image Docker de l'application
├── requirements.txt        # Dépendances production
├── requirements-dev.txt    # Dépendances de développement
└── README.md
```

## Lancer le projet en local

### 1. Créer l'environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

Sous Windows :

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements-dev.txt
```

### 3. Lancer l'application

```bash
python main.py
```

L'API est disponible sur :

```text
http://127.0.0.1:5000
```

## Endpoints API

### Health check

```http
GET /health
```

Réponse :

```json
{
  "status": "ok",
  "service": "task-api"
}
```

### Lister les tâches

```http
GET /api/tasks
```

### Créer une tâche

```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Nouvelle tâche"
}
```

### Modifier une tâche

```http
PUT /api/tasks/1
Content-Type: application/json

{
  "done": true
}
```

### Supprimer une tâche

```http
DELETE /api/tasks/1
```

## Tests automatisés

Lancer les tests :

```bash
pytest
```

Lancer les tests avec couverture :

```bash
pytest --cov=app --cov-report=term-missing
```

## Qualité et sécurité du code

Lint avec Ruff :

```bash
ruff check .
```

Scan sécurité avec Bandit :

```bash
bandit -r app
```

## Docker

Construire l'image :

```bash
docker build -t task-api:latest .
```

Lancer le conteneur :

```bash
docker run -p 5000:5000 task-api:latest
```

Tester :

```bash
curl http://localhost:5000/health
```

## Pipeline CI/CD

Le projet contient deux workflows GitHub Actions.

### CI

Fichier : `.github/workflows/ci.yml`

Déclenchement :

- push sur `main` ou `develop`
- pull request vers `main` ou `develop`

Étapes :

1. Checkout du repository
2. Installation Python
3. Installation des dépendances
4. Analyse Ruff
5. Scan Bandit
6. Tests pytest avec couverture minimale de 80 %
7. Build Docker

### Déploiement Azure

Fichier : `.github/workflows/deploy-azure.yml`

Déclenchement :

- push sur `main`
- lancement manuel via `workflow_dispatch`

Étapes :

1. Connexion Azure
2. Build Docker
3. Push vers Azure Container Registry
4. Déploiement sur Azure Web App for Containers

## Infrastructure as Code avec Terraform

Le dossier `infra/terraform` permet de créer :

- un Resource Group Azure
- un Azure Container Registry
- un App Service Plan Linux
- une Azure Web App for Containers

### Initialisation

```bash
cd infra/terraform
terraform init
```

### Planification

```bash
terraform plan -var-file="terraform.tfvars"
```

### Application

```bash
terraform apply -var-file="terraform.tfvars"
```

Un fichier d'exemple est fourni :

```bash
cp terraform.tfvars.example terraform.tfvars
```

Il faut modifier les valeurs `acr_name` et `webapp_name` car elles doivent être uniques mondialement dans Azure.

## Secrets GitHub à configurer

Dans GitHub :

```text
Settings > Secrets and variables > Actions > New repository secret
```

Secrets nécessaires :

| Secret | Description |
|---|---|
| AZURE_CREDENTIALS | Identifiants Azure au format JSON pour azure/login |
| AZURE_RESOURCE_GROUP | Nom du Resource Group |
| AZURE_WEBAPP_NAME | Nom de l'Azure Web App |
| ACR_NAME | Nom de l'Azure Container Registry |
| ACR_LOGIN_SERVER | URL du registry, exemple acrtaskapi12345.azurecr.io |

## Commande Azure pour créer AZURE_CREDENTIALS

```bash
az ad sp create-for-rbac \
  --name "github-actions-task-api" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID> \
  --sdk-auth
```

Copier le JSON obtenu dans le secret `AZURE_CREDENTIALS`.

## Git Flow conseillé

Branches recommandées :

- `main` : production
- `develop` : intégration
- `feature/*` : développement de fonctionnalités
- `hotfix/*` : correction urgente

Exemple :

```bash
git checkout -b feature/add-task-endpoint
git add .
git commit -m "Add task endpoint"
git push origin feature/add-task-endpoint
```

Ensuite, ouvrir une Pull Request vers `develop`, puis vers `main` après validation.

## Livrables couverts

| Livrable demandé | Présent |
|---|---|
| Repository GitHub complet | Oui |
| Code source documenté | Oui |
| README Markdown | Oui |
| Pipeline CI/CD fonctionnel | Oui |
| Infrastructure as Code | Oui, Terraform |
| Déploiement automatisé Azure | Oui, GitHub Actions + Azure Web App |
| Tests automatisés | Oui, pytest |
| Containerisation | Oui, Docker |
| Qualité du code | Oui, Ruff |
| Sécurité | Oui, Bandit |
