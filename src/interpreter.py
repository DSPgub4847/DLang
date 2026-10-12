from parser import (
    PrintStatement,
    Assignment,
    Variable,
    Literal,
    BinaryExpression,
)
from lexer import TokenType


class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.variables = {}

    def run(self):
        for statement in self.statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, Assignment):
            self.variables[statement.name] = (
                self.evaluate(statement.value)
            )
            return

        if isinstance(statement, PrintStatement):
            print(self.evaluate(statement.value))
            return

        raise RuntimeError(
            f"Unknown statement: {type(statement).__name__}"
        )

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Variable):
            if expression.name not in self.variables:
                raise RuntimeError(
                    f"Undefined variable: {expression.name}"
                )

            return self.variables[expression.name]

        if isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)

            if expression.operator == TokenType.PLUS:
                return left + right

            if expression.operator == TokenType.MINUS:
                return left - right

            if expression.operator == TokenType.STAR:
                return left * right

            if expression.operator == TokenType.SLASH:
                if right == 0:
                    raise RuntimeError("Division by zero")

                return left / right

        raise RuntimeError(
            f"Unknown expression: {type(expression).__name__}"
        )
