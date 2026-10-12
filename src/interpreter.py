from parser import (
    PrintStatement,
    Assignment,
    IfStatement,
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
        self.execute_block(self.statements)

    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, Assignment):
            self.variables[statement.name] = (
                self.evaluate(statement.expression)
            )
            return

        if isinstance(statement, PrintStatement):
            print(self.evaluate(statement.expression))
            return

        if isinstance(statement, IfStatement):
            condition = self.evaluate(statement.condition)

            if condition:
                self.execute_block(statement.then_body)
            else:
                self.execute_block(statement.else_body)
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
            operator = expression.operator

            try:
                if operator == "+":
                    return left + right

                if operator == "-":
                    return left - right

                if operator == "*":
                    return left * right

                if operator == "/":
                    if right == 0:
                        raise RuntimeError("Division by zero")
                    return left / right

                if operator == ">":
                    return left > right

                if operator == "<":
                    return left < right

                if operator == ">=":
                    return left >= right

                if operator == "<=":
                    return left <= right

                if operator == "==":
                    return left == right

                if operator == "!=":
                    return left != right

            except TypeError:
                raise RuntimeError(
                    "Incompatible value types in expression"
                ) from None

        raise RuntimeError(
            f"Unknown expression: {type(expression).__name__}"
        )
