import os
import sys

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


