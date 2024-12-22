import sys
import time
import random


def starting_app() -> None:
    """ → Affiche le message de démarrage de l'application."""
    print("")
    print("╔═════════════════════════════════════╗")
    print("║       \033[1m\033[94mBienvenue sur UNCRACKED\033[0m       ║")
    print("║   \033[1mVotre PasswordManager Sécurisé\033[0m    ║")
    print("║       → Réalisé par Wissem B.       ║")
    print("╚═════════════════════════════════════╝")


def loading_app(min_speed: float, max_speed: float, wait_time: int = 1) -> None:
    """
    → Affiche une barre de chargement.
    :param min_speed: La vitesse minimale de l'animation de chargement.
    :param max_speed: La vitesse maximale de l'animation de chargement.
    :param wait_time: Le temps d'attente après le chargement (par défaut 1 seconde).
    :return: None
    """
    progress = 0
    while progress < 100:
        increment = random.randint(1, 5)
        progress = min(progress + increment, 100)
        bar = ('█' * (progress // 5)).ljust(20)
        sys.stdout.write(f"\r[Chargement] : [{bar}] {progress}%")
        sys.stdout.flush()
        time.sleep(random.uniform(min_speed, max_speed))
    time.sleep(wait_time)


def menu_auth(pending) -> None:
    """
    → Affiche le menu d'authentification.
    :param pending: Fonction qui est exécutée pendant l'attente de l'utilisateur.
    :return: None
    """
    print("╔════════════════════════════════╗")
    print("║        \033[1mAUTHENTIFICATION\033[0m        ║")
    print("║    Sélectionner une action :   ║")
    print("╚════════════════════════════════╝")
    pending()
    print("══════════════════════════════════")


def menu_login(pending) -> str:
    """
    → Affiche le menu de connexion.
    :param pending: Fonction qui est exécutée pendant l'attente de l'utilisateur.
    :return: La réponse de l'utilisateur (souvent des identifiants).
    """
    print("╔════════════════════════════════╗")
    print("║           \033[1mCONNEXION\033[0m            ║")
    print("║    Entrez vos identifiants :   ║")
    print("╚════════════════════════════════╝")
    response = pending()
    print("══════════════════════════════════")
    return response


def menu_register(pending) -> str:
    """
    → Affiche le menu d'enregistrement.
    :param pending: Fonction qui est exécutée pendant l'attente de l'utilisateur.
    :return: La réponse de l'utilisateur (souvent des informations personnelles).
    """
    print("╔════════════════════════════════╗")
    print("║       \033[1mCRÉATION DE COMPTE\033[0m       ║")
    print("║    Entrez vos informations :   ║")
    print("╚════════════════════════════════╝")
    response = pending()
    print("══════════════════════════════════")
    return response


def menu_main(pending) -> None:
    """
    → Affiche le menu principal.
    :param pending: Fonction qui est exécutée pendant l'attente de l'utilisateur.
    :return: None
    """
    print("╔════════════════════════════════╗")
    print("║        \033[1mMENU PRINCIPAL\033[0m          ║")
    print("║   Que souhaitez-vous faire ?   ║")
    print("╚════════════════════════════════╝")
    pending()
    print("══════════════════════════════════")


def menu_terminal() -> None:
    """
    → Affiche le menu du terminal.
    :return: None
    """
    print("╔════════════════════════════════════╗")
    print("║        \033[1mTERMINAL DE COMMANDE\033[0m        ║")
    print("║    Entrez une ligne de commande    ║")
    print("║                                    ║")
    print("║   \033[2m\033[3m'help' pour consulter la liste\033[0m   ║")
    print("║      \033[2m\033[3mdes commandes existantes.\033[0m     ║")
    print("╚════════════════════════════════════╝")


def help_specific() -> None:
    """
    → Affiche l'aide spécifique pour une commande.
    :return: None
    """
    print("╔════════════════════════════════════╗")
    print("║             \033[1mMENU D'AIDE\033[0m            ║")
    print("║     Description des commandes :    ║")
    print("╚════════════════════════════════════╝")


def help_global() -> None:
    """
    → Affiche l'aide générale avec les commandes existantes.
    :return: None
    """
    print("╔════════════════════════════════════╗")
    print("║             \033[1mMENU D'AIDE\033[0m            ║")
    print("║  Voici les commandes existantes :  ║")
    print("╚════════════════════════════════════╝")


def secure_print(text: str) -> None:
    """
    → Affiche un message sécurisé, encadré avec un cadre stylisé. (By Chat-GPT)
    :param text: Le texte à afficher.
    :return: None
    """
    frame_width = len(text) + 4
    top_bottom = "╔" + "═" * (frame_width - 2) + "╗"
    middle = "║ " + text + " ║"
    bottom = "╚" + "═" * (frame_width - 2) + "╝"

    # Afficher le texte avec un cadre, en texte blanc sur fond noir
    styled_text = f"\033[97m\033[40m{top_bottom}\033[0m\n"
    styled_text += f"\033[97m\033[40m{middle}\033[0m\n"
    styled_text += f"\033[97m\033[40m{bottom}\033[0m"
    print(styled_text)


def settings_menu() -> None:
    """
    → Affiche le menu des paramètres.
    :return: None
    """
    print("╔════════════════════════════════╗")
    print("║           PARAMÈTRES           ║")
    print("║     Définissez vos réglages    ║")
    print("╚════════════════════════════════╝")
