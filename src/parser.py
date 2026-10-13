from dataclasses import dataclass
from lexer import TokenType


@dataclass
class PrintStatement:
    expression: object


@dataclass
class Assignment:
    name: str
    expression: object


@dataclass
class IfStatement:
    condition: object
    then_body: list
    elif_branches: list
    else_body: list


@dataclass
class WhileStatement:
    condition: object
    body: list


@dataclass
class FunctionDefinition:
    name: str
    parameters: list
    body: list


@dataclass
class ReturnStatement:
    expression: object


@dataclass
class FunctionCall:
    name: str
    arguments: list


@dataclass
class InputExpression:
    pass


@dataclass
class TypeConversion:
    conversion_type: str
    expression: object


@dataclass
class Variable:
    name: str


@dataclass
class Literal:
    value: object


@dataclass
class BinaryExpression:
    left: object
    operator: str
    right: object


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
        if token is not None:
            self.position += 1
        return token

    def skip_newlines(self):
        while (
            self.current() is not None
            and self.current().type == TokenType.NEWLINE
        ):
            self.advance()

    def expect(self, token_type, message):
        token = self.current()
        if token is None or token.type != token_type:
            raise SyntaxError(message)
        return self.advance()

    def parse(self):
        statements = []
        self.skip_newlines()

        while (
            self.current() is not None
            and self.current().type != TokenType.EOF
        ):
            if self.current().type in (
                TokenType.INDENT,
                TokenType.DEDENT,
            ):
                self.advance()
                self.skip_newlines()
                continue

            statements.append(self.parse_statement())
            self.skip_newlines()

        return statements

    def parse_statement(self):
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.type == TokenType.PRINT:
            self.advance()
            self.expect(TokenType.LPAREN, "Expected '(' after print")
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after print")
            return PrintStatement(expression)

        if token.type == TokenType.FUNC:
            return self.parse_function_definition()

        if token.type == TokenType.RETURN:
            self.advance()
            return ReturnStatement(self.parse_expression())

        if token.type == TokenType.IF:
            return self.parse_if()

        if token.type == TokenType.WHILE:
            return self.parse_while()

        if token.type == TokenType.IDENTIFIER:
            name = self.advance().value

            if (
                self.current() is not None
                and self.current().type == TokenType.LPAREN
            ):
                return FunctionCall(name, self.parse_arguments())

            self.expect(
                TokenType.ASSIGN,
                "Expected '=' after variable name",
            )
            return Assignment(name, self.parse_expression())

        raise SyntaxError(f"Unexpected token: {token.value!r}")

    def parse_function_definition(self):
        self.expect(TokenType.FUNC, "Expected 'func'")

        name = self.expect(
            TokenType.IDENTIFIER,
            "Expected function name",
        ).value

        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        parameters = []

        if (
            self.current() is not None
            and self.current().type != TokenType.RPAREN
        ):
            parameters.append(
                self.expect(
                    TokenType.IDENTIFIER,
                    "Expected parameter name",
                ).value
            )

            while (
                self.current() is not None
                and self.current().type == TokenType.COMMA
            ):
                self.advance()
                parameters.append(
                    self.expect(
                        TokenType.IDENTIFIER,
                        "Expected parameter name",
                    ).value
                )

        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        self.expect(TokenType.COLON, "Expected ':' after function definition")

        body = self.parse_block()
        return FunctionDefinition(name, parameters, body)

    def parse_if(self):
        self.expect(TokenType.IF, "Expected 'if'")
        condition = self.parse_expression()
        self.expect(TokenType.COLON, "Expected ':' after if condition")

        then_body = self.parse_block()
        elif_branches = []

        while (
            self.current() is not None
            and self.current().type == TokenType.ELIF
        ):
            self.advance()
            condition = self.parse_expression()
            self.expect(TokenType.COLON, "Expected ':' after elif condition")
            elif_branches.append((condition, self.parse_block()))

        else_body = []

        if (
            self.current() is not None
            and self.current().type == TokenType.ELSE
        ):
            self.advance()
            self.expect(TokenType.COLON, "Expected ':' after else")
            else_body = self.parse_block()

        return IfStatement(
            condition,
            then_body,
            elif_branches,
            else_body,
        )

    def parse_while(self):
        self.expect(TokenType.WHILE, "Expected 'while'")
        condition = self.parse_expression()
        self.expect(TokenType.COLON, "Expected ':' after while condition")

        return WhileStatement(condition, self.parse_block())

    def parse_block(self):
        self.skip_newlines()
        self.expect(TokenType.INDENT, "Expected an indented block")
        body = []
        self.skip_newlines()

        while (
            self.current() is not None
            and self.current().type not in (
                TokenType.DEDENT,
                TokenType.EOF,
            )
        ):
            body.append(self.parse_statement())
            self.skip_newlines()

        self.expect(TokenType.DEDENT, "Expected end of indented block")

        if not body:
            raise SyntaxError("Expected a non-empty block")

        return body

    def parse_arguments(self):
        self.expect(TokenType.LPAREN, "Expected '('")
        arguments = []

        if (
            self.current() is not None
            and self.current().type != TokenType.RPAREN
        ):
            arguments.append(self.parse_expression())

            while (
                self.current() is not None
                and self.current().type == TokenType.COMMA
            ):
                self.advance()
                arguments.append(self.parse_expression())

        self.expect(TokenType.RPAREN, "Expected ')' after arguments")
        return arguments

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        expression = self.parse_addition()

        operators = (
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
        )

        while (
            self.current() is not None
            and self.current().type in operators
        ):
            operator = self.advance().value
            right = self.parse_addition()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def parse_addition(self):
        expression = self.parse_multiplication()

        while (
            self.current() is not None
            and self.current().type in (
                TokenType.PLUS,
                TokenType.MINUS,
            )
        ):
            operator = self.advance().value
            right = self.parse_multiplication()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def parse_multiplication(self):
        expression = self.parse_unary()

        while (
            self.current() is not None
            and self.current().type in (
                TokenType.MULTIPLY,
                TokenType.DIVIDE,
            )
        ):
            operator = self.advance().value
            right = self.parse_unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def parse_unary(self):
        if (
            self.current() is not None
            and self.current().type == TokenType.MINUS
        ):
            self.advance()
            return BinaryExpression(
                Literal(0),
                "-",
                self.parse_unary(),
            )

        return self.parse_primary()

    def parse_primary(self):
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected end of expression")

        if token.type == TokenType.NUMBER:
            self.advance()
            value = (
                float(token.value)
                if "." in token.value
                else int(token.value)
            )
            return Literal(value)

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type == TokenType.IDENTIFIER:
            name = self.advance().value

            if (
                self.current() is not None
                and self.current().type == TokenType.LPAREN
            ):
                arguments = self.parse_arguments()

                if name == "input":
                    if arguments:
                        raise SyntaxError(
                            "input() does not accept arguments"
                        )
                    return InputExpression()

                if name in ("int", "str"):
                    if len(arguments) != 1:
                        raise SyntaxError(
                            f"{name}() expects one argument"
                        )
                    return TypeConversion(name, arguments[0])

                return FunctionCall(name, arguments)

            return Variable(name)

        if token.type == TokenType.LPAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')'")
            return expression

        raise SyntaxError(
            f"Unexpected expression token: {token.value!r}"
        )
