# ================================
# Configuration du programme
# ================================

# → Mode de base de données
#    0: JSON | 1: SQLITE — SQLite non implémenté
database_mode = 0

# → Paramètres de sécurité
security = {
    "aes_master_key_size": 256,     # Taille de la clé AES maître (en bits)
    "rsa_master_key_size": 4096,    # Taille de la clé RSA maître (en bits)

    "aes_standard_key_size": 256,   # Taille de la clé AES standard (en bits)
    "rsa_standard_key_size": 2048   # Taille de la clé RSA standard (en bits)
}

# → Caractères autorisés pour les mots de passe
characters = {
    "special": [
        "!", "@", "#", "$", "€", "%", "^", "&", "*", "(", ")", "-", "_", "=",
        "+", "[", "]", "{", "}", "|", "\\", ":", ";", "'", '"', "<", ">", ",",
        ".", "?", "/", "~", "`"
    ],
    "numbers": [str(i) for i in range(10)],         # Chiffres de 0 à 9
    "alphabet": [chr(i) for i in range(97, 123)],   # Lettres minuscules a-z
    "ALPHABET": [chr(i) for i in range(65, 91)]     # Lettres majuscules A-Z
}
# → Combinaison de tous les caractères autorisés
characters["allowed"] = (
    characters["alphabet"] +
    characters["ALPHABET"] +
    characters["special"] +
    characters["numbers"]
)

# → Styles pour la console
style = {
    "reset": "\033[0m",
    "styles": {
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "inverse": "\033[7m",
        "hidden": "\033[8m",
        "strike": "\033[9m"
    },
    "colors": {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m"
    },
    "backgrounds": {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
        "bright_black": "\033[100m",
        "bright_red": "\033[101m",
        "bright_green": "\033[102m",
        "bright_yellow": "\033[103m",
        "bright_blue": "\033[104m",
        "bright_magenta": "\033[105m",
        "bright_cyan": "\033[106m",
        "bright_white": "\033[107m"
    },
    "cursor": {
        "up": lambda n: f"\033[{n}A",
        "down": lambda n: f"\033[{n}B",
        "forward": lambda n: f"\033[{n}C",
        "backward": lambda n: f"\033[{n}D",
        "position": lambda x, y: f"\033[{y};{x}H",
        "clear": "\033[2J",
        "clear_line": "\033[K"
    }
}

# → Modèle de base de données par défaut
template = {
    "database": {
        "utilisateur": [],  # Liste des utilisateurs
        "credentials": [],  # Liste des identifiants
    },

    # → Exemple d'utilisateur
    "user": {
        "id": 1,
        "username": "admin",
        "password": "hashed_password",
        "rsa_public_key": "public_key",
        "rsa_private_key": "encrypted_private_key"
    },

    # → Exemple d'identifiant
    "credentials": {
        "id": 1,
        "user_id": 1,  # Référence vers l'utilisateur
        "website": "example.com",
        "login": "admin",
        "password": "hashed_password",
        "strength": 4,  # Note de robustesse
        "is_expired": False,    # Expiration (Historique)
        "encryption_type": "",  # AES, RSA, CESAR
        "encryption_key": "",    # AES: Salt | CESAR: Key
        "labels": []  ,          # Références vers les labels
        "updated_at": "2021-01-01 00:00:00",
        "created_at": "2021-01-01 00:00:00",
        "history": []           # Historique des mots de passe
    },
}
