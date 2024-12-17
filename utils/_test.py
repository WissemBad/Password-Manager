import math
from utils.methods import generate_prime

def generate_keys(key_size):
    bits = key_size // 2

    p = generate_prime(bits)
    q = generate_prime(bits)

    while p == q: q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537 if math.gcd(65537, phi) == 1 else 3
    while math.gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    # Convertir le message en entier
    m = int.from_bytes(message.encode('utf-8'), byteorder='big')
    if m >= n:
        raise ValueError("Le message est trop long pour la clé publique.")
    # Calculer le message chiffré
    c = pow(m, e, n)
    return c

def decrypt(cipher, private_key):
    d, n = private_key
    # Calculer le message en clair
    m = pow(cipher, d, n)
    # Convertir l'entier en texte
    message = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    return message

def main():
    # Taille de clé (en bits)
    key_size = 512

    # Générer les clés publique et privée
    public_key, private_key = generate_keys(key_size)

    # Message à chiffrer
    message = "CacaProutPipi"
    print("Message original :", message)

    # Chiffrement
    cipher = encrypt(message, public_key)
    print("Message chiffré :", cipher)

    # Déchiffrement
    decrypted_message = decrypt(cipher, private_key)
    print("Message déchiffré :", decrypted_message)

# Programme principal
if __name__ == "__main__":
    main()
