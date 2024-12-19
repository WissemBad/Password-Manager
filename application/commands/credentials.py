import argparse


class Credentials:
    def __init__(self, parser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers(dest='command')
        self.register_subcommands()

    def register_subcommands(self):
        """Enregistre toutes les sous-commandes de credentials."""

        # Commande 'add'
        add_parser = self.subparsers.add_parser("add", help="Ajoute une nouvelle entrée d'identifiants.")
        add_parser.add_argument("--website", required=True, help="URL du site.")
        add_parser.add_argument("--login", required=True, help="Identifiant.")
        add_parser.add_argument("--password", required=True, help="Mot de passe.")
        add_parser.add_argument("--encryption-type", required=True, choices=["AES", "RSA", "CESAR"],
                                help="Type de chiffrement.")
        add_parser.set_defaults(func=self.add)

        # Commande 'remove'
        remove_parser = self.subparsers.add_parser("remove", help="Supprime une entrée.")
        remove_parser.add_argument("id", help="ID de l'entrée à supprimer.")
        remove_parser.set_defaults(func=self.remove)

        # Commande 'edit'
        edit_parser = self.subparsers.add_parser("edit", help="Modifie les détails d'une entrée existante.")
        edit_parser.add_argument("id", help="ID de l'entrée à modifier.")
        edit_parser.add_argument("--website", help="Nouvelle URL.")
        edit_parser.add_argument("--login", help="Nouveau login.")
        edit_parser.add_argument("--password", help="Nouveau mot de passe.")
        edit_parser.add_argument("--label", help="Nouvelle étiquette.")
        edit_parser.set_defaults(func=self.edit)

        # Commande 'show'
        show_parser = self.subparsers.add_parser("show", help="Affiche les détails d'une entrée spécifique.")
        show_parser.add_argument("id", help="ID de l'entrée à afficher.")
        show_parser.set_defaults(func=self.show)

        # Commande 'list'
        list_parser = self.subparsers.add_parser("list", help="Liste toutes les entrées.")
        list_parser.add_argument("--label", help="Filtre par label.")
        list_parser.set_defaults(func=self.list_entries)

        # Commande 'audit'
        audit_parser = self.subparsers.add_parser("audit", help="Effectue un audit des entrées.")
        audit_parser.add_argument("--weak", action="store_true", help="Filtrer les entrées faibles.")
        audit_parser.add_argument("--expired", action="store_true", help="Filtrer les entrées expirées.")
        audit_parser.set_defaults(func=self.audit)

    def add(self, args):
        """Logique associée à la commande 'add'."""
        print(
            f"Ajout d'une entrée : site={args.website}, login={args.login}, password={args.password}, encryption={args.encryption_type}")

    def remove(self, args):
        """Logique associée à la commande 'remove'."""
        print(f"Suppression de l'entrée {args.id}.")

    def edit(self, args):
        """Logique associée à la commande 'edit'."""
        print(
            f"Modification de l'entrée {args.id} avec les nouveaux détails : site={args.website}, login={args.login}, password={args.password}, label={args.label}")

    def show(self, args):
        """Logique associée à la commande 'show'."""
        print(f"Affichage de l'entrée {args.id}.")

    def list_entries(self, args):
        """Logique associée à la commande 'list'."""
        print(f"Liste des entrées avec filtre par label : {args.label}.")

    def audit(self, args):
        """Logique associée à la commande 'audit'."""
        print(f"Audit des entrées : faible={args.weak}, expirée={args.expired}")
