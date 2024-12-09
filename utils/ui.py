import random
import sys
import time

def starting_app():
    print("")
    print("╔═════════════════════════════════════╗")
    print("║       \033[1m\033[94mBienvenue sur UNCRACKED\033[0m       ║")
    print("║   \033[1mVotre PasswordManager Sécurisé\033[0m    ║")
    print("║       → Réalisé par Wissem B.       ║")
    print("╚═════════════════════════════════════╝")

def loading_app(min_speed, max_speed, wait_time=1):
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
    print("╔════════════════════════════════╗")
    print("║        \033[1mAUTHENTIFICATION\033[0m        ║")
    print("║    Sélectionner une action :   ║")
    print("╚════════════════════════════════╝")
    pending()
    print("══════════════════════════════════")

def menu_login(pending):
    print("╔════════════════════════════════╗")
    print("║           \033[1mCONNEXION\033[0m            ║")
    print("║    Entrez vos identifiants :   ║")
    print("╚════════════════════════════════╝")
    response = pending()
    print("══════════════════════════════════")
    return response

def menu_register(pending):
    print("╔════════════════════════════════╗")
    print("║       \033[1mCRÉATION DE COMPTE\033[0m       ║")
    print("║    Entrez vos informations :   ║")
    print("╚════════════════════════════════╝")
    response = pending()
    print("══════════════════════════════════")
    return response



def menu_main(pending):
    print("╔════════════════════════════════╗")
    print("║        \033[1mMENU PRINCIPAL\033[0m          ║")
    print("║   Que souhaitez-vous faire ?   ║")
    print("╚════════════════════════════════╝")
    pending()
    print("══════════════════════════════════")

def menu_terminal():
    print("╔════════════════════════════════════╗")
    print("║        \033[1mTERMINAL DE COMMANDE\033[0m        ║")
    print("║    Entrez une ligne de commande    ║")
    print("║                                    ║")
    print("║   \033[3m[help] pour consulter la liste\033[0m   ║")
    print("║      \033[3mdes commandes existantes.\033[0m     ║")
    print("╚════════════════════════════════════╝")




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
