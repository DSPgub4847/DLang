from parser import PrintStatement


class Interpreter:
    def __init__(self, statements):
        self.statements = statements

    def run(self):
        for statement in self.statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, PrintStatement):
            print(statement.value)
            return

        raise RuntimeError(
            f"Unknown statement: {type(statement).__name__}"
        )
