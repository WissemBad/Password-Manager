import os
import sys
import random
import requests

from utils.configuration import style


def console(arg: str, text: str, mode: str = "colors", action=print):
    """→ Afficher du texte stylé dans la console."""
    return action(f"{style[mode][arg]}{text}{style["reset"]}")


def clear_terminal():
    """→ Nettoyer le terminal utilisateur."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pending_load():
    """→ Attendre que l'utilisateur clique pour démarrer."""
    return console("cyan", "\n→ Appuyez sur ENTER pour vous connecter...", "colors", input)


def auto_increment(data: list) -> int:
    """→ Récupérer le prochain incrément d'une liste."""
    if len(data) == 0: return 1
    index = len(data) - 1
    increment = data[index]["id"] + 1
    return increment


def confirm(confirmation: str) -> bool:
    """→ Confirmation de l'utilisateur."""
    while True:
        confirm = console("yellow", f"[🛈] Voulez-vous vraiment {confirmation} ? [Oui/Non]\n→ ", "colors", input)
        if confirm.lower().strip() in ["oui", "non"]: return True if confirm.lower() == "oui" else False


def secure_input(prompt: str):
    """→ Saisie sécurisée de l'utilisateur."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    password = ""

    if os.name == 'nt':  # Windows
        import msvcrt
        while True:
            char = msvcrt.getch()
            if char in {b'\r', b'\n'}:
                break
            elif char == b'\x08' and password:
                password = password[:-1]
                sys.stdout.write('\b \b')
            else:
                password += char.decode('utf-8')
                sys.stdout.write("*")
            sys.stdout.flush()
    else:  # Unix/Linux/MacOS
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in {'\n', '\r'}:
                    break
                elif char == '\x7f' and password:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                else:
                    password += char
                    sys.stdout.write("*")
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    sys.stdout.write("\n")
    return password


def get_random_word(size):
    """→ Générer un mot aléatoire."""
    response = requests.get(f"https://trouve-mot.fr/api/size/{size}")
    response = response.json()
    return response[0]["name"]


def get_random_caps(word):
    """→ Générer un mot avec des majuscules aléatoires."""
    response = ""
    for char in word:
        response += char.upper() if random.choice([True, False]) else char.lower()
    return response


def is_prime(n, k=5):
    """→ Test de primalité de Miller-Rabin."""
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


def generate_prime(bits):
    """→ Générer un nombre premier aléatoire."""
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0: num += 1
        if is_prime(num): return num
