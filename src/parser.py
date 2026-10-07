from lexer import TokenType


class PrintStatement:
    def __init__(self, value):
        self.value = value


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
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

        token = self.current()

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}"
        )

    def parse_print(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)

        value = self.expect(TokenType.STRING)

        self.expect(TokenType.RPAREN)

        return PrintStatement(value.value)
