import argparse


class Label:
    def __init__(self, parser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers(dest='command')
        self.register_subcommands()

    def register_subcommands(self):
        """Enregistre toutes les sous-commandes de label."""

        # Commande 'add'
        add_parser = self.subparsers.add_parser("add", help="Ajoute une nouvelle étiquette.")
        add_parser.add_argument("name", help="Nom de l'étiquette.")  # Supprimez 'required=True'
        add_parser.set_defaults(func=self.add)

        # Commande 'remove'
        remove_parser = self.subparsers.add_parser("remove", help="Supprime une étiquette.")
        remove_parser.add_argument("name", help="Nom de l'étiquette à supprimer.")  # Supprimez 'required=True'
        remove_parser.set_defaults(func=self.remove)

        # Commande 'edit'
        edit_parser = self.subparsers.add_parser("edit", help="Modifie une étiquette existante.")
        edit_parser.add_argument("old_name", help="Nom de l'étiquette à modifier.")  # Supprimez 'required=True'
        edit_parser.add_argument("new_name", help="Nouveau nom pour l'étiquette.")  # Supprimez 'required=True'
        edit_parser.set_defaults(func=self.edit)

        # Commande 'list'
        list_parser = self.subparsers.add_parser("list", help="Liste toutes les étiquettes.")
        list_parser.set_defaults(func=self.list)

    def add(self, args):
        """Logique associée à la commande 'add'."""
        print(f"Ajout de l'étiquette : {args.name}")

    def remove(self, args):
        """Logique associée à la commande 'remove'."""
        print(f"Suppression de l'étiquette : {args.name}")

    def edit(self, args):
        """Logique associée à la commande 'edit'."""
        print(f"Modification de l'étiquette {args.old_name} en {args.new_name}")

    def list(self, args):
        """Logique associée à la commande 'list'."""
        print("Liste de toutes les étiquettes :")
        # Exemple d'étiquettes simulées
        labels = ["Travail", "Personnel", "Urgent"]
        for label in labels:
            print(f"  - {label}")
