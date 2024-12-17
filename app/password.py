from utils import methods
from utils import _config as configuration

from app.user import User

import random

class Credentials:
    def __init__(self, app, user, website, username, password, encryption):
        self.app = app
        self.database = self.app.database

        self.user:User = user
        self.user_id:int = self.user.id

        self.website:str = website
        self.username:str = username
        self.password:str = password

        self.strength:int = self.get_strength(password)
        self.encryption:str = encryption

def get_strength(password):
    strength = 1
    numbers = 0
    specials = 0
    length = len(password)

    for char in password:
        if char.isdigit(): numbers += 1
        if char in configuration.characters["special"]: specials += 1

    if not password.islower() and not password.isupper(): strength += 1  # - Ne contient pas que des lettres majuscules ou minuscules.
    if length > 8: strength += 1    # - Au moins 8 caractères
    if numbers >= 2: strength += 1  # - Au moins 2 chiffres
    if specials > 0: strength += 1  # - Au moins 1 caractère spécial

    return strength


def generate_password(strength=4, use_dictionary=False, require_numbers=True, require_special=True, mixed_case=True, length=4):

    password = ""
    match strength:
        case 1:
            characters = configuration.characters["alphabet"]
            length = max(length, 8)
        case 2:
            if not mixed_case: return False
            characters = configuration.characters["alphabet"] + configuration.characters["ALPHABET"]
            length = max(length, 8)
        case 3:
            if not mixed_case or not require_numbers: return False
            characters = configuration.characters["alphabet"] + configuration.characters["ALPHABET"] + configuration.characters["numbers"]
            length = max(length, 10)
        case 4:
            if not mixed_case or not require_numbers or not require_special: return False
            characters = configuration.characters["alphabet"] + configuration.characters["ALPHABET"] + configuration.characters["numbers"] + configuration.characters["special"]
            length = max(length, 12)
        case _:
            return False


    if use_dictionary:
        if strength == 1: password = methods.get_random_word(length)
        else: password = methods.get_random_word(random.randint(length//2, length))
    else:
        for i in range(length): password += random.choice(configuration.characters["alphabet"])

    if strength >= 2: password = methods.get_random_caps(password)

    if strength >= 3:
        password += random.choice(configuration.characters["numbers"])
        password += random.choice(configuration.characters["numbers"])

    if strength == 4: password += random.choice(configuration.characters["special"])

    while len(password) < length: password += random.choice(characters)
    return password


# Exemple d'utilisation :
generated_password = generate_password(4,True)

