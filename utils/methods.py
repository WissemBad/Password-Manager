import os
import sys
import random
import requests

from utils.configuration import style

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


# Étoiles à la place de la saisie lors de l'input - By ChatGPT
def secure_input(input: str):
    if os.name == 'nt':  # Windows
        import msvcrt
        sys.stdout.write(input)
        sys.stdout.flush()
        password = ""
        while True:
            char = msvcrt.getch()
            if char in {b'\r', b'\n'}:  # Enter key
                break
            elif char == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                password += char.decode('utf-8')
                sys.stdout.write("*")
                sys.stdout.flush()
        sys.stdout.write("\n")
        return password
    else:  # Unix/Linux/MacOS
        import termios
        import tty
        sys.stdout.write(input)
        sys.stdout.flush()
        password = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char == '\n' or char == '\r':  # Gérer Entrée correctement
                    break
                elif char == '\x7f':  # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')  # Supprime une étoile
                        sys.stdout.flush()
                else:
                    password += char
                    sys.stdout.write("*")  # Affiche une étoile
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Réinitialise les paramètres
        sys.stdout.write("\n")
        return password

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

# Test de nombre premier de Miller-Rabin
def is_prime(n, k=5):
    if n == 2 or n == 3: return True  # 2 et 3 sont premiers
    if n == 1 or n % 2 == 0: return False  # 1 et les nombres pairs sont non premiers

    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2  # décomposer n-1 en s * 2^d

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # calcul a^d mod n
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)  # calcul x^2 mod n
            if x == n - 1:
                break
        else:
            return False  # n n'est pas premier
    return True

# Générer un nombre premier
def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0: num += 1
        if is_prime(num): return num





