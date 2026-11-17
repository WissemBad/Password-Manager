# Password Manager

A command-line password manager in Python, written in December 2024 as a programming project during my first year at IMT Nord Europe. It is a school exercise, kept here as it was handed in: it is not maintained and should not hold real passwords.

## What it does

- Accounts with Argon2-hashed master passwords.
- Credentials (website, login, password) encrypted with one of three methods: AES-256 (PyCryptodome), RSA (one hand-written implementation, one with PyCryptodome) and a Caesar cipher written by hand.
- Strength rating (weak, medium, strong, excellent) and a generator that takes length, character sets and target strength into account.
- History of previous versions of each password, labels, and search by login, label, strength or encryption method.
- Breach check through the Have I Been Pwned range API: only the first five characters of the SHA-1 hash are sent.
- Dictionary words for generated passphrases, fetched from the trouve-mot.fr API.
- An interactive terminal with `help`, `help <command>` and `help <command> <subcommand>`.

## Run it

Python 3.13 or later.

```bash
pip install -r requirements.txt
python main.py
```

The first run generates the global keys into a `.env` file and creates an empty JSON database, which takes a few seconds. Settings such as key sizes live in `utils/configuration.py`.

## Design

- `application/`: the application, authentication, users, credentials and the terminal commands.
- `database/`: reads and writes the JSON database.
- `security/`: key management, hashing, encryption and decryption. The AES and Caesar keys are stored encrypted in `security/keys/`.
- `utils/`: configuration, shared helpers and console output.

The master password is never stored. At sign-in it is checked against its Argon2 hash and used to derive, with PBKDF2, the vector used by the AES layer; the derived value is dropped at sign-out.

## Limits

These are the known weaknesses of the project, stated as they are:

- The Caesar cipher and the hand-written RSA are there for learning. They provide no real protection.
- The global RSA and AES keys sit in plain text in `.env`, next to the application.
- The AES layer uses CBC with a global key and a vector derived from the master password with an empty salt, so the same password always gives the same vector. There is no authentication of the ciphertext.
- Data is a single JSON file; the SQLite mode in the configuration was never implemented.
- The unit tests written during development were removed before submission, so the repository has none.
- Known bugs: repeated edits can corrupt a password, multi-criteria searches sometimes fail, and editing a password encrypted with a custom Caesar key does not work.
- The interface and the code comments are in French.

## Licence

[MIT](LICENSE)
