import os
import random
from Crypto.Random import get_random_bytes

# — Générer une clé secrète AES
def aes_key_generate(filename="security/keys/.aes"):
    ky = get_random_bytes(32)
    directory = os.path.dirname(filename)
    if not os.path.exists(directory): os.makedirs(directory)
    with open(filename, "wb") as ky_file: ky_file.write(ky)
    return ky

# — Charger la clé secrète AES
def aes_key_load(filename="security/keys/.aes"):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0: return aes_key_generate(filename)
    with open(filename, "rb") as ky_file: ky = ky_file.read()
    return ky

# — Générer une clé secrète César
def csr_key_generate(filename="security/keys/.csr"):
    ky = random.randint(0, 25).to_bytes(1, byteorder='big')
    directory = os.path.dirname(filename)
    if not os.path.exists(directory): os.makedirs(directory)
    with open(filename, "wb") as ky_file: ky_file.write(ky)
    return int.from_bytes(ky, byteorder='big') % 26

# — Charger la clé secrète César
def csr_key_load(filename="security/keys/.csr"):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0: return csr_key_generate(filename)
    with open(filename, "rb") as ky_file: ky = int.from_bytes(ky_file.read(), byteorder='big') % 26
    return ky
