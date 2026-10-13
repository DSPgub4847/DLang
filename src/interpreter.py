from parser import (
    PrintStatement,
    Assignment,
    IfStatement,
    WhileStatement,
    FunctionDefinition,
    ReturnStatement,
    FunctionCall,
    InputExpression,
    TypeConversion,
    Variable,
    Literal,
    BinaryExpression,
)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.variables = {}
        self.functions = {}

    def run(self):
        for statement in self.statements:
            if isinstance(statement, FunctionDefinition):
                if statement.name in self.functions:
                    raise RuntimeError(
                        f"Function already defined: {statement.name}"
                    )
                self.functions[statement.name] = statement

        self.execute_block(self.statements)

    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, FunctionDefinition):
            return

        if isinstance(statement, Assignment):
            self.variables[statement.name] = self.evaluate(
                statement.expression
            )
            return

        if isinstance(statement, PrintStatement):
            print(self.evaluate(statement.expression))
            return

        if isinstance(statement, ReturnStatement):
            raise ReturnSignal(self.evaluate(statement.expression))

        if isinstance(statement, FunctionCall):
            self.call_function(statement.name, statement.arguments)
            return

        if isinstance(statement, IfStatement):
            if self.evaluate(statement.condition):
                self.execute_block(statement.then_body)
                return

            for condition, body in statement.elif_branches:
                if self.evaluate(condition):
                    self.execute_block(body)
                    return

            self.execute_block(statement.else_body)
            return

        if isinstance(statement, WhileStatement):
            while self.evaluate(statement.condition):
                self.execute_block(statement.body)
            return

        raise RuntimeError(
            f"Unknown statement: {type(statement).__name__}"
        )

    def call_function(self, name, argument_expressions):
        if name not in self.functions:
            raise RuntimeError(f"Undefined function: {name}")

        function = self.functions[name]

        if len(argument_expressions) != len(function.parameters):
            raise RuntimeError(
                f"Function '{name}' expects "
                f"{len(function.parameters)} argument(s), got "
                f"{len(argument_expressions)}"
            )

        argument_values = [
            self.evaluate(expression)
            for expression in argument_expressions
        ]

        previous_variables = self.variables
        self.variables = dict(zip(function.parameters, argument_values))

        try:
            self.execute_block(function.body)
        except ReturnSignal as result:
            return result.value
        finally:
            self.variables = previous_variables

        return None

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Variable):
            if expression.name not in self.variables:
                raise RuntimeError(
                    f"Undefined variable: {expression.name}"
                )
            return self.variables[expression.name]

        if isinstance(expression, InputExpression):
            try:
                return input()
            except EOFError:
                raise RuntimeError("No input provided") from None

        if isinstance(expression, TypeConversion):
            value = self.evaluate(expression.expression)

            try:
                if expression.conversion_type == "int":
                    if isinstance(value, bool):
                        return int(value)
                    return int(value)

                if expression.conversion_type == "str":
                    return str(value)

            except (ValueError, TypeError, OverflowError):
                raise RuntimeError(
                    f"Cannot convert {value!r} to "
                    f"{expression.conversion_type}"
                ) from None

        if isinstance(expression, FunctionCall):
            return self.call_function(
                expression.name, expression.arguments
            )

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
