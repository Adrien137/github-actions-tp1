# Architecture technique

## Vue générale

Le projet suit une architecture simple adaptée à un projet pédagogique d'usine logicielle.

```text
Développeur
   |
   v
GitHub Repository
   |
   v
GitHub Actions CI
   |-- Ruff
   |-- Bandit
   |-- pytest
   |-- Docker build
   |
   v
Azure Container Registry
   |
   v
Azure Web App for Containers
```

## Choix techniques

### Flask

Flask a été choisi car il est simple, rapide à mettre en place et adapté à une API REST JSON légère.

### GitHub Actions

GitHub Actions est utilisé car il s'intègre directement au repository GitHub et permet d'automatiser les tests, la qualité, la sécurité et le déploiement.

### Docker

Docker permet de rendre l'application portable et reproductible entre l'environnement local, la CI et Azure.

### Terraform

Terraform permet de créer l'infrastructure Azure de manière déclarative et versionnée.

### Ansible

Ansible est fourni comme complément si un déploiement sur VM Azure est demandé. Dans cette version, le déploiement principal se fait via Azure Web App for Containers, plus simple pour le projet.
