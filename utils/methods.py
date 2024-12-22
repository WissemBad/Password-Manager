import os
import sys
import random
import hashlib
import requests
import datetime

from utils.configuration import style


def console(arg: str, text: str, mode: str = "colors", action=print) -> None:
    """
    → Afficher du texte stylé dans la console.
    :param arg: L'argument de style (ex : "cyan", "yellow").
    :param text: Le texte à afficher.
    :param mode: Le mode de style (par défaut "colors").
    :param action: La fonction à utiliser pour afficher le texte (par défaut print).
    :return: None
    """
    return action(f"{style[mode][arg]}{text}{style['reset']}")


def clear_terminal() -> None:
    """→ Nettoyer le terminal utilisateur."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pending_load() -> None:
    """→ Attendre que l'utilisateur clique pour démarrer."""
    return console("cyan", "\n→ Appuyez sur ENTER pour vous connecter...", "colors", input)


def auto_increment(data: list) -> int:
    """
    → Récupérer le prochain incrément d'une liste.
    :param data: Liste contenant les données avec un attribut "id".
    :return: Le prochain identifiant incrémenté.
    """
    if len(data) == 0:
        return 1
    index = len(data) - 1
    increment = data[index]["id"] + 1
    return increment


def confirm(confirmation: str) -> bool:
    """
    → Confirmation de l'utilisateur.
    :param confirmation: Le texte à afficher pour la confirmation.
    :return: True si l'utilisateur confirme, False sinon.
    """
    while True:
        confirm = console("yellow", f"[🛈] Voulez-vous vraiment {confirmation} ? [Oui/Non]\n→ ", "colors", input)
        if confirm.lower().strip() in ["oui", "non"]: return True if confirm.lower() == "oui" else False


def get_random_word(size: int) -> str:
    """
    → Générer un mot aléatoire.
    :param size: La taille du mot en caractères.
    :return: Le mot généré.
    """
    response = requests.get(f"https://trouve-mot.fr/api/size/{size}").json()
    return response[0]["name"]


def get_random_caps(word: str) -> str:
    """
    → Générer un mot avec des majuscules aléatoires.
    :param word: Le mot à modifier.
    :return: Le mot avec des majuscules aléatoires.
    """
    response = ""
    for char in word:
        response += char.upper() if random.choice([True, False]) else char.lower()
    return response


def is_prime(n: int, k: int = 5) -> bool:
    """
    → Test de primalité de Miller-Rabin.
    :param n: Le nombre à tester.
    :param k: Le nombre d'itérations pour le test (par défaut 5).
    :return: True si n est premier, False sinon.
    """
    if n == 2 or n == 3:
        return True
    if n == 1 or n % 2 == 0:
        return False

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


def generate_prime(bits: int) -> int:
    """
    → Générer un nombre premier aléatoire.
    :param bits: Le nombre de bits du nombre premier généré.
    :return: Un nombre premier généré.
    """
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0:
            num += 1
        if is_prime(num):
            return num


def get_current_time() -> str:
    """
    → Renvoie l'heure actuelle sous un format compatible avec JSON.
    :return: L'heure actuelle au format 'YYYY-MM-DD HH:MM:SS'.
    """
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_time


def password_audit(password: str) -> None:
    """
    → Vérifier si un mot de passe a été compromis.
    :param password: Le mot de passe à vérifier.
    :return: None, mais affiche si le mot de passe a été trouvé dans les bases de données de compromissions.
    """
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]  # Les 5 premiers caractères
    suffix = sha1_password[5:]  # Le reste du hash
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            console("red", f"[✘] Erreur : La vérification de votre mot de passe a échoué :\n→ {response.reason}")

        for line in response.text.splitlines():
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                return console("cyan", f"→ Votre mot de passe a été trouvé \033[1m{int(count)} fois\033[0m\033[36m sur Internet !")
        return console("bright_green", "→ Votre mot de passe n'a pas été trouvé dans les bases de données connues.")
    except Exception as e:
        return console("red", f"[✘] Erreur : La vérification de votre mot de passe a échoué :\n→ {e}")


def secure_input(prompt: str) -> str:
    """
    → Saisie sécurisée de l'utilisateur (mot de passe masqué).
    :param prompt: Le texte à afficher avant la saisie.
    :return: Le mot de passe saisi.
    """
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
