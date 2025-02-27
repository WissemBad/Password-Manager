# Mon Projet

## Introduction

Ce projet est un **gestionnaire de mots de passe** conçu pour gérer les identifiants utilisateurs de manière sécurisée, en offrant une interface en ligne de commande. Il comprend des fonctionnalités avancées comme le **cryptage des mots de passe**, l'analyse de leur **robustesse**, un **générateur de mots de passe**, ainsi que la gestion d'un **historique** et des **versions**.

Le système permet également de catégoriser les mots de passe en utilisant des **labels** et de les rechercher efficacement via des critères multiples (login, label, mot de passe).

-> __All credits to Wissem.__


---

## Table des matières
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Fonctionnalités](#fonctionnalités)
4. [Utilisation](#utilisation)
5. [Tests](#tests)
6. [Bugs & Notes](#bugs-et-notes)
7. [Licences](#licences)

## Installation
Pour installer et utiliser ce projet sur ton environnement local, suis ces étapes :

### Prérequis
- Python 3.13.1 (ou version supérieure)
- Pip (gestionnaire de paquets Python)

### Installation avec `pip`
```bash
pip install -r requirements.txt
```

Les dépendances nécessaires à l'exécution du projet sont listées ci-dessous :
- `requests` : Pour effectuer des requêtes HTTP vers des APIs.
- `python-dotenv` : Pour charger les variables d'environnement depuis un fichier `.env`.
- `pycryptodome` : Pour le chiffrement des données.
- `argon2-cffi` : Pour le hachage des mots de passe.

---

## Configuration
Lors de la **première connexion**, les clés de chiffrement sont automatiquement générées, ce qui peut prendre un peu de temps. La base de données est également créée et initialisée lors de cette première connexion.

Le projet utilise l'environnement utilisateur **dotenv** pour gérer les variables d'environnement nécessaires à la configuration.

### Modification de la configuration
Il est possible de modifier la configuration de l'application en accédant au fichier `./utils/configuration.py`.

**Important** : La modification de ce fichier est **réservée aux utilisateurs expérimentés**, car des erreurs dans la configuration peuvent affecter le bon fonctionnement de l'application.

---

## Fonctionnalités
- **Système de connexion** : Authentification sécurisée pour accéder au gestionnaire de mots de passe.
- **Cryptage des données de connexion** : Trois méthodes de chiffrement sont supportées :
    - **Chiffrement César** : Implémentation à la main de la méthode de César.
    - **Chiffrement AES-256** : Utilisation de la bibliothèque `Crypto` pour le chiffrement AES.
    - **Chiffrement RSA** : En deux temps : d'une part à la main, et d'autre part avec la bibliothèque `Crypto`.
- **Identification de la force d'un mot de passe** : Le mot de passe est évalué selon une échelle de robustesse (**Faible**, **Moyen**, **Fort**, **Excellent**).
- **Générateur de mots de passe** : Le générateur peut créer des mots de passe selon la **longueur**, les **types de caractères** et la **robustesse souhaitée**.
- **Historique et gestion des versions** : Sauvegarde automatique des mots de passe et gestion des versions précédentes.
- **Organisation par labels** : Les mots de passe peuvent être organisés avec des **labels multiples** pour faciliter la gestion.
- **Recherche avancée** : Recherche des mots de passe par **login**, **label**, **robustesse** ou **type de chiffrement**.
- **Analyse de sécurité** : Audit des mots de passe pour détecter les failles de sécurité.
- **Interface en ligne de commande** : Utilisation simple et intuitive via une interface en ligne de commande.
- **Sauvegarde automatique** : Les données sont sauvegardées automatiquement pour éviter toute perte de données.

### Aspect sécuritaire

Toutes les données sensibles sont **doublement encryptées** pour garantir leur sécurité. Le système repose sur deux couches de chiffrement :
1. **RSA** : Pour sécuriser les données principales.
2. **AES-256** : Un chiffrement dérivé du mot de passe utilisateur (connu uniquement par l'utilisateur), renforcé par l'ajout d'un **salt** afin d'augmenter la robustesse du chiffrement.

#### Gestion des clés de chiffrement
- **Clés spécifiques (AES, César)** :
  - Stockées dans des fichiers sécurisés et encryptés avec l'extension `.key`, situés dans le répertoire `security/keys/` (par exemple : `file.key`).
  - Ces clés sont générées automatiquement par l'application et restent protégées contre tout accès non autorisé.

- **Clés globales (RSA, AES)** :
  - Stockées dans le fichier `.env` sous la responsabilité du gestionnaire de l'application.
  - Bien que générées automatiquement, elles peuvent être modifiées manuellement par un administrateur si nécessaire, mais doivent être maintenues en sécurité.

#### Sécurité du mot de passe utilisateur
- **Aucune sauvegarde en clair** : Le mot de passe utilisateur n'est jamais stocké dans l'application.
- **Hachage sécurisé** : Le système d'authentification utilise **Argon2**, un des algorithmes de hachage les plus fiables et jusqu'à présent non compromis.
- **Processus temporaire** : La dérivation du mot de passe est générée uniquement à la **connexion de l'utilisateur** et est **entièrement supprimée à la déconnexion**.

#### Prévention contre la manipulation
Pour éviter toute tentative de compromission du système :
- Tant que l'utilisateur n'a pas saisi son mot de passe, l'application empêche toute tentative de manipulation (par exemple : en modifiant directement `Application.logged_in = True`).

---

## Utilisation
Le démarrage s'effectue via le fichier `main.py` situé à la racine du projet. Avant de lancer l'application, assurez-vous de bien configurer les paramètres de votre IDE pour définir le dossier source comme étant **"uncracked"** (le dossier contenant le projet). Cela est nécessaire pour garantir une communication correcte entre les fichiers.

### Première exécution
Lors de la première exécution, l'application procède à une phase d'initialisation qui génère automatiquement :
- Les premières **clés de sécurité**.
- Une **base de données vide** prête à être utilisée.

### Authentification
Après l'initialisation, vous accéderez à l'écran d'authentification pour créer votre compte. **La casse n'est pas prise en compte** (par exemple, `Wissem` est équivalent à `wissem`). Une fois votre compte créé, vous pourrez accéder au terminal principal pour effectuer vos premières requêtes.

### Commandes d'aide
Pour vous guider dans l'utilisation de l'application, plusieurs commandes d'aide sont disponibles :
- **`help`** : Affiche une liste générale des commandes disponibles.
- **`help command`** : Fournit des informations détaillées sur une commande spécifique.
- **`help command subcommand`** : Explique l'utilisation des sous-commandes d'une commande.

### Navigation dans l'interface
L'application est conçue pour être intuitive et guidée. À chaque étape, des indications claires vous orienteront dans l'utilisation des différentes fonctionnalités.

---

## Tests

#### Tests unitaires
De nombreux **tests unitaires** ont été réalisés pendant la phase de développement pour garantir le bon fonctionnement des fonctionnalités. Ces tests ont permis d'identifier et de corriger d'éventuelles anomalies dans les différentes parties de l'application.

- **Approche dynamique** : Les tests ont été progressivement supprimés une fois le code stabilisé et prêt pour la production, afin d'éviter les complications et d'améliorer les performances en environnement final.
- **Couverture complète** : Chaque fonctionnalité majeure (cryptage, authentification, génération de mots de passe, etc.) a été testée individuellement pour s'assurer de son bon fonctionnement.

#### Gestion des erreurs
L'application intègre de nombreux **blocs `try-except`** pour gérer les erreurs et prévenir les plantages imprévus :
- **Résilience** : Ces blocs permettent de maintenir l'application fonctionnelle, même en cas de comportement inattendu ou d'entrée utilisateur incorrecte.
- **Protection critique** : Dans certains cas, des **interruptions volontaires** sont appliquées pour éviter des problèmes graves, comme :
  - La corruption de la base de données.
  - Une compromission des clés de sécurité ou des données sensibles.

---

## Structure du projet

Le projet est structuré autour de classes et sous-classes interconnectées pour garantir une organisation claire et une fluidité dans son fonctionnement.

### Points clés
- **`main.py`** : Point d'entrée du projet.

### Répertoires principaux

#### `application/`
Fichiers gérant les fonctionnalités principales de l'application.
- **`main.py`** : Initialisation, structure de base et coordination.
- **`authentification.py`** : Gestion de l'authentification des utilisateurs.
- **`user.py`** : Gestion des utilisateurs de l'application.
- **`credentials.py`** : Gestion des credentials des utilisateurs.
- **`password.py`** : Gestion des mots de passe associés aux credentials.
- **`terminal.py`** : Interface de commandes et gestion des commandes simples.

#### `application/commands/`
Fichiers dédiés aux commandes principales du terminal.
- **`help.py`** : Commande `help`.
- **`credentials.py`** : Commande de gestion des credentials.

#### `database/`
Répertoire central pour toutes les interactions avec la base de données.
- **`main.py`** : Coordination des sous-classes et initialisation.
- **`credentials.py`** : Gestion des interactions credentials-base de données.
- **`user.py`** : Gestion des interactions utilisateur-base de données.
- **`_data/`** : Contient les fichiers de données, comme `database.json`.

#### `security/`
Fonctionnalités de sécurité essentielles.
- **`main.py`** : Coordination et initialisation (génération des clés spécifiques).
- **`manager.py`** : Gestion des clés globales et des clés stockées.
- **`hash.py`** : Gestion du hachage des données.
- **`encryption.py`** : Gestion du chiffrement des données.
- **`decryption.py`** : Gestion du déchiffrement des données.
- **`keys/`** : Répertoire contenant les clés globales encryptées.

#### `utils/`
Répertoire des utilitaires du projet.
- **`_test.py`** : Sandbox du projet et exécutions de tests.
- **`configuration.py`** : Configuration du projet.
- **`methods.py`** : Fonctions utilitaires générales.
- **`ui.py`** : Fonctions utilitaires pour l'interface utilisateur.

---

## Bugs et Notes

### Bugs connus
Bien que l'application ait été rigoureusement testée, certains **bugs mineurs** peuvent encore persister :
- **Gestion des erreurs** : Malgré les nombreux blocs `try-except`, des erreurs inattendues peuvent apparaître dans des conditions extrêmes ou inhabituelles.
- **Performances** : Les opérations complexes (comme le chiffrement et les recherches avancées) peuvent entraîner des ralentissements pour de grandes bases de données ou des critères multiples.
- **Corruption des données** : Des éditions successives peuvent, dans de rares cas, corrompre un mot de passe.
- **Recherche multicritères** : Les recherches impliquant plusieurs critères peuvent parfois dysfonctionner.
- **Édition de mots de passe** : Les éditions de mots de passe encryptés avec une clé César personnalisée semblent disfonctionner. *(Découverte de dernière minute.)*

### Notes
- **Génération de mots du dictionnaire** : L'application utilise des **API externes** pour générer des mots du dictionnaire aléatoires avec des critères spécifiques.
- **Vérification de fuites** : Une **API tierce** est utilisée pour vérifier si un mot de passe a été compromis dans des fuites de données publiques.

### Dépôt GitHub
Le projet est accessible sur GitHub : [Password-Manager](https://github.com/WissemBad/Password-Manager)

---

## Licence
Ce projet est distribué sous la **MIT License**, disponible à la racine du projet.



