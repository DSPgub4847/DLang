from lexer import TokenType


class PrintStatement:
    def __init__(self, value):
        self.value = value


class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name


class Literal:
    def __init__(self, value):
        self.value = value


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()

        if token.type != TokenType.EOF:
            self.position += 1

        return token

    def expect(self, token_type):
        token = self.current()

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.name}, "
                f"got {token.type.name} "
                f"at line {token.line}"
            )

        return self.advance()

    def parse(self):
        statements = []

        while self.current().type != TokenType.EOF:
            statements.append(self.parse_statement())

        return statements

    def parse_statement(self):
        if self.current().type == TokenType.PRINT:
            return self.parse_print()

        if self.current().type == TokenType.IDENTIFIER:
            return self.parse_assignment()

        token = self.current()

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}"
        )

    def parse_assignment(self):
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.EQUAL)
        value = self.parse_expression()

        return Assignment(name, value)

    def parse_print(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        value = self.parse_expression()
        self.expect(TokenType.RPAREN)

        return PrintStatement(value)

    def parse_expression(self):
        return self.parse_addition()

    def parse_addition(self):
        expression = self.parse_multiplication()

        while self.current().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.advance().type
            right = self.parse_multiplication()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def parse_multiplication(self):
        expression = self.parse_primary()

        while self.current().type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):
            operator = self.advance().type
            right = self.parse_primary()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def parse_primary(self):
        token = self.current()

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(int(token.value))

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)

        if token.type == TokenType.LPAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expression

        raise SyntaxError(
            f"Expected a value at line {token.line}"
        )
