from security import init as key

# 0: JSON  -  1: SQL #
database = 0

keys = {
    "AES": key.aes_key_load(),
    "CESAR": key.csr_key_load()
}

characters = {
    "special": [
        "!", "@", "#", "$", "€", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
        "[", "]", "{", "}", "|", "\\", ":", ";", "'", '"', "<", ">", ",", ".",
        "?", "/", "~", "`"
    ],
    "alphabet": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
    "ALPHABET": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
}

characters["allowed"] = characters["alphabet"] + characters["ALPHABET"] + characters["special"]

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


template = {
    "database": {
        "utilisateur": [],
        "credentials": [],
        "label": []
    },

    "user": {
        "id": 1,
        "username": "admin",
        "password": "hashed_password",
        "vector": "unique_vector"
    },

    "credentials": {
        "id": 1,
        "website": "example.com",
        "login": "admin",
        "password": "hashed_password",
        "strength": 5,
        "is_expired": False,
        "user_id": 1,
        "vector": "unique_vector"
    },

    "label": {
        "id": 1,
        "text": "Important",
        "credentials_id": 1
    }
}