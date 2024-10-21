# Cahier des charges : Application de suivi des flux de biodéchets, BioTrack'in

## 1. **Contexte et Objectifs**

### 1.1 **Contexte**
L'entreprise **Anthropile** cherche à améliorer la gestion des biodéchets en Guadeloupe en développant une application dédiée. Les biodéchets, issus de la cuisine, du jardinage ou d'activités professionnelles, peuvent être valorisés via des procédés comme le compostage ou la méthanisation. L'objectif est d'optimiser la collecte de ces déchets afin de réduire les coûts logistiques et améliorer l'efficacité du recyclage.

### 1.2 **Objectifs de l'application**
- **Suivre les flux** de biodéchets produits par les particuliers et les entreprises.
- **Optimiser la collecte** en fonction des volumes et des fréquences de génération.
- **Planifier les tournées de collecte** de manière plus efficace.
- **Classer les biodéchets** en catégories pour orienter la collecte vers les filières de traitement appropriées.

## 2. **Fonctionnalités principales**

### 2.1 **Enregistrement des utilisateurs**
- Gestion des comptes utilisateurs : particuliers et entreprises.
- Collecte d’informations telles que : nom, adresse, type de biodéchets générés, volume estimé, fréquence souhaitée pour la collecte.

### 2.2 **Suivi des quantités de biodéchets**
- Saisie manuelle des quantités par les utilisateurs à travers une interface simple.
- Intégration possible de **capteurs connectés** pour une saisie automatique des quantités à l’avenir.

### 2.3 **Tableau de bord pour visualisation des flux**
- **Statistiques** sur les quantités de biodéchets générées sur une période donnée (semaine, mois, année).
- **Graphiques interactifs** permettant de suivre l’évolution des flux.
- Historique des données avec une vue détaillée par type de biodéchet.

### 2.4 **Cartographie des points de collecte**
- Visualisation des points de collecte sur une carte interactive (intégration de **Google Maps**).
- Affichage des quantités associées à chaque point de collecte.
- **Planification des tournées** optimisée en fonction des données collectées, pour améliorer les trajets et réduire les coûts.

### 2.5 **Notifications**
- Envoi de **notifications** pour informer les utilisateurs des prochaines collectes prévues selon les données saisies (fréquences ajustées dynamiquement).
- Rappel aux utilisateurs pour saisir les quantités de biodéchets en temps opportun.

## 3. **Fonctionnalités secondaires**

### 3.1 **Analyse des données**
- Analyse pour optimiser les tournées de collecte en fonction des volumes et types de biodéchets.
- Suggestions automatiques pour ajuster les itinéraires et fréquences de collecte basées sur les données historiques.

### 3.2 **Rapports et statistiques**
- Génération de **rapports** pour permettre aux utilisateurs de voir la répartition des types de biodéchets qu'ils génèrent.
- **Analyse des flux** pour améliorer l’efficacité des processus de recyclage ou de traitement.

### 3.3 **Catégorisation des biodéchets**
- Système de classification des biodéchets : **déchets de cuisine**, **déchets verts**, **huiles usagées**, **effluents animaux**, etc.
- Association de chaque type de biodéchet à des **instructions spécifiques** pour la collecte (ex. : fréquence de ramassage plus élevée pour les déchets périssables).
- Filtre permettant aux utilisateurs de consulter leur historique par type de biodéchet.

## 4. **Contraintes techniques**

### 4.1 **Technologies à utiliser**
- Développement de l’application mobile en Flask
- Utilisation de bases de données telle que **MySQL** pour stocker les informations (utilisateurs, biodéchets, tournées).
- **Google Maps API** pour la gestion de la cartographie des points de collecte.

### 4.2 **Sécurité et authentification**
- Authentification des utilisateurs avec un système sécurisé.
- Gestion des rôles : accès restreint à certaines fonctionnalités (gestion des tournées, visualisation des flux) pour les administrateurs et certaines entreprises.

## 5. **Ergonomie et interface utilisateur**

### 5.1 **Interface mobile**
- Interface **intuitive** et facile à utiliser, avec des boutons et des icônes clairs.
- Chaque type de biodéchet sera associé à une **couleur** ou une **icône** distincte pour simplifier l’identification.
- Utilisation de **menus déroulants** pour la saisie des informations (par exemple, la sélection des types de biodéchets).

### 5.2 **Tableau de bord**
- Tableau de bord accessible depuis l’accueil, avec des graphiques et des statistiques mis à jour en temps réel.
- Possibilité de filtrer les données selon une période choisie (semaine, mois, année) ou par type de biodéchet.

## 6. **Délais**

### 6.1 **Développement**
- Durée estimée du développement : **90 heures**.
- Intégration des tests utilisateurs et corrections avant le déploiement final.
