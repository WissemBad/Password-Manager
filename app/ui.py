import sys
import time
import getpass
from app._config import style

def starting_app():
    print("")
    print("╔═════════════════════════════════════╗")
    print("║       \033[1m\033[32mBienvenue sur UNCRACKED\033[0m       ║")
    print("║  \033[1m[Votre Password Manager Sécurisé]\033[0m  ║")
    print("║       \033[34m→ Réalisé par Wissem B.\033[0m       ║")
    print("╚═════════════════════════════════════╝")

def loading_app(speed, wait_time):
    for i in range(101):
        bar = ('█' * (i // 5)).ljust(20)
        sys.stdout.write(f"\r[Chargement] : [{bar}] {i}%")
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(wait_time)

def menu_connexion(data):
    print("╔════════════════════════════════╗")
    print("║        MENU PRINCIPAL          ║")
    print("║  Que souhaitez-vous faire ?    ║")
    print("╚════════════════════════════════╝")
    for i, option in enumerate(data):
        print(f"{i}: {option}")
    print("══════════════════════════════════")

def menu_login():
    print("╔════════════════════════════════╗")
    print("║           CONNEXION            ║")
    print("║    Entrez vos identifiants     ║")
    print("╚════════════════════════════════╝")
    username, password = input("→ Nom d'utilisateur : "), input("→ Mot de passe : ")
    print("══════════════════════════════════")
    return username, password

def main_menu(data):
    print("╔════════════════════════════════╗")
    print("║        MENU PRINCIPAL          ║")
    print("║  Que souhaitez-vous faire ?    ║")
    print("╚════════════════════════════════╝")
    for i, option in enumerate(data):
        print(f"{i}: {option}")
    print("══════════════════════════════════")

def mode_selection(data):
    print("╔════════════════════════════════╗")
    print("║          MODE DE JEU           ║")
    print("║  Sélectionnez le mode de jeu   ║")
    print("╚════════════════════════════════╝")
    for i, option in enumerate(data):
        print(f"{i}: {option}")
    print("══════════════════════════════════")

def settings_menu():
    print("╔════════════════════════════════╗")
    print("║           PARAMÈTRES           ║")
    print("║     Définissez vos réglages    ║")
    print("╚════════════════════════════════╝")

def console(arg: str, text: str, mode: str = "colors", action = print):
    return action(f"{style[mode][arg]}{text}{style["reset"]}")
