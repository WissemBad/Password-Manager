import os
import random
import requests

from utils._config import style

def console(arg: str, text: str, mode: str = "colors", action = print):
    return action(f"{style[mode][arg]}{text}{style["reset"]}")

# Nettoyer le terminal utilisateur
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Attendre que l'utilisateur clique pour démarrer
def pending_load():
    return console("cyan", "\n→ Appuyez sur ENTER pour vous connecter...", "colors", input)

# Récupérer le prochain incrément d'une liste
def auto_increment(data: list) -> int:
    if len(data) == 0: return 1
    index = len(data) - 1
    increment = data[index]["id"] + 1
    return increment

# Demander confirmation avant une autre action
def confirm(confirmation:str) -> bool:
    while True:
        confirm = console("yellow", f"[🛈] Voulez-vous vraiment {confirmation} ? [Oui/Non]\n→ ", "colors", input)
        if confirm.lower().strip() in ["oui", "non"]: return True if confirm.lower() == "oui" else False

# Générer un mot aléatoire
def get_random_word(size):
    response = requests.get(f"https://trouve-mot.fr/api/size/{size}")
    response = response.json()
    return response[0]["name"]

def get_random_caps(word):
    response = ""
    for char in word:
        response += char.upper() if random.choice([True, False]) else char.lower()
    return response

# Fonction pour effectuer le test de primalité de Miller-Rabin
def is_prime(n, k=5):
    if n == 2 or n == 3: return True
    if n == 1 or n % 2 == 0: return False

    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        if is_prime(candidate): return candidate





