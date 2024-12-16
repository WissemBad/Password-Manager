class Label():
    def __init__(self, args):
        self.arguments = args

        self.subcommand = self.arguments[1]

        match self.subcommand:
            case "add":
                return