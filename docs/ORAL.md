# Trame courte pour l'oral

Bonjour, je vais présenter mon projet fil rouge d'usine logicielle.

J'ai choisi de réaliser une API REST JSON simple en Python avec Flask. L'application permet de gérer une liste de tâches avec des endpoints pour créer, lire, modifier et supprimer des tâches.

L'objectif n'était pas de faire une application complexe, mais de démontrer une chaîne DevOps complète : gestion du code source, tests automatisés, qualité du code, sécurité, containerisation, pipeline CI/CD, Infrastructure as Code et déploiement automatisé sur Azure.

Le repository GitHub contient le code source, les tests pytest, un Dockerfile, deux workflows GitHub Actions, ainsi qu'une infrastructure Terraform.

La pipeline CI se déclenche sur push et pull request. Elle installe les dépendances, lance Ruff pour la qualité du code, Bandit pour la sécurité, pytest avec une couverture minimale, puis construit l'image Docker.

La pipeline de déploiement Azure se déclenche sur la branche main ou manuellement. Elle se connecte à Azure, construit l'image Docker, la pousse dans Azure Container Registry puis déploie l'application sur Azure Web App for Containers.

L'infrastructure est décrite avec Terraform. Elle crée le Resource Group, l'Azure Container Registry, l'App Service Plan et l'Azure Web App.

Ce projet respecte donc les principes d'une usine logicielle : automatisation, reproductibilité, qualité, sécurité, traçabilité et déploiement fiable.
