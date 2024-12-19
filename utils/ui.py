import sys
import time
import random


def starting_app():
    """→ Affiche le message de démarrage de l'application."""
    print("")
    print("╔═════════════════════════════════════╗")
    print("║       \033[1m\033[94mBienvenue sur UNCRACKED\033[0m       ║")
    print("║   \033[1mVotre PasswordManager Sécurisé\033[0m    ║")
    print("║       → Réalisé par Wissem B.       ║")
    print("╚═════════════════════════════════════╝")


def loading_app(min_speed, max_speed, wait_time=1):
    """→ Affiche une barre de chargement."""
    progress = 0
    while progress < 100:
        increment = random.randint(1, 5)
        progress = min(progress + increment, 100)
        bar = ('█' * (progress // 5)).ljust(20)
        sys.stdout.write(f"\r[Chargement] : [{bar}] {progress}%")
        sys.stdout.flush()
        time.sleep(random.uniform(min_speed, max_speed))
    time.sleep(wait_time)


def menu_auth(pending):
    """→ Affiche le menu d'authentification."""
    print("╔════════════════════════════════╗")
    print("║        \033[1mAUTHENTIFICATION\033[0m        ║")
    print("║    Sélectionner une action :   ║")
    print("╚════════════════════════════════╝")
    pending()
    print("══════════════════════════════════")


def menu_login(pending):
    """→ Affiche le menu de connexion."""
    print("╔════════════════════════════════╗")
    print("║           \033[1mCONNEXION\033[0m            ║")
    print("║    Entrez vos identifiants :   ║")
    print("╚════════════════════════════════╝")
    response = pending()
    print("══════════════════════════════════")
    return response


def menu_register(pending):
    """→ Affiche le menu d'enregistrement."""
    print("╔════════════════════════════════╗")
    print("║       \033[1mCRÉATION DE COMPTE\033[0m       ║")
    print("║    Entrez vos informations :   ║")
    print("╚════════════════════════════════╝")
    response = pending()
    print("══════════════════════════════════")
    return response


def menu_main(pending):
    """→ Affiche le menu principal."""
    print("╔════════════════════════════════╗")
    print("║        \033[1mMENU PRINCIPAL\033[0m          ║")
    print("║   Que souhaitez-vous faire ?   ║")
    print("╚════════════════════════════════╝")
    pending()
    print("══════════════════════════════════")


def menu_terminal():
    """→ Affiche le menu du terminal."""
    print("╔════════════════════════════════════╗")
    print("║        \033[1mTERMINAL DE COMMANDE\033[0m        ║")
    print("║    Entrez une ligne de commande    ║")
    print("║                                    ║")
    print("║   \033[2m\033[3m'help' pour consulter la liste\033[0m   ║")
    print("║      \033[2m\033[3mdes commandes existantes.\033[0m     ║")
    print("╚════════════════════════════════════╝")


def help_specific():
    """→ Affiche l'aide spécifique."""
    print("╔════════════════════════════════════╗")
    print("║             \033[1mMENU D'AIDE\033[0m            ║")
    print("║     Description des commandes :    ║")
    print("╚════════════════════════════════════╝")


def help_global():
    """→ Affiche l'aide générale."""
    print("╔════════════════════════════════════╗")
    print("║             \033[1mMENU D'AIDE\033[0m            ║")
    print("║  Voici les commandes existantes :  ║")
    print("╚════════════════════════════════════╝")


def settings_menu():
    """→ Affiche le menu des paramètres."""
    print("╔════════════════════════════════╗")
    print("║           PARAMÈTRES           ║")
    print("║     Définissez vos réglages    ║")
    print("╚════════════════════════════════╝")
