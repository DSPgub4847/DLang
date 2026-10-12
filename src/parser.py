from lexer import TokenType


class PrintStatement:
    def __init__(self, expression):
        self.expression = expression


class Assignment:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression


class IfStatement:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body or []


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

    def match(self, *types):
        if self.current().type in types:
            return self.advance()
        return None

    def expect(self, token_type, message):
        if self.current().type != token_type:
            token = self.current()
            raise SyntaxError(
                f"Line {token.line}: {message}"
            )
        return self.advance()

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            pass

    def parse(self):
        statements = []
        self.skip_newlines()

        while self.current().type != TokenType.EOF:
            if self.current().type == TokenType.DEDENT:
                token = self.current()
                raise SyntaxError(
                    f"Line {token.line}: Unexpected indentation"
                )

            statements.append(self.parse_statement())
            self.skip_newlines()

        return statements

    def parse_statement(self):
        if self.current().type == TokenType.IF:
            return self.parse_if()

        if self.current().type == TokenType.PRINT:
            self.advance()
            self.expect(TokenType.LPAREN, "Expected '(' after print")

            expression = self.parse_expression()

            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            self.expect(TokenType.NEWLINE, "Expected end of line")

            return PrintStatement(expression)

        if self.current().type == TokenType.IDENTIFIER:
            name = self.advance().value

            self.expect(TokenType.ASSIGN, "Expected '=' after variable name")
            expression = self.parse_expression()

            self.expect(TokenType.NEWLINE, "Expected end of line")

            return Assignment(name, expression)

        token = self.current()
        raise SyntaxError(
            f"Line {token.line}: Invalid statement"
        )

    def parse_if(self):
        self.expect(TokenType.IF, "Expected 'if'")

        condition = self.parse_expression()
        self.expect(TokenType.NEWLINE, "Expected ':' after condition")

        then_body = self.parse_block()
        else_body = []

        if self.match(TokenType.ELSE):
            self.expect(TokenType.NEWLINE, "Expected ':' after else")
            else_body = self.parse_block()

        return IfStatement(condition, then_body, else_body)

    def parse_block(self):
        self.expect(TokenType.INDENT, "Expected an indented block")

        statements = []
        self.skip_newlines()

        while self.current().type not in (
            TokenType.DEDENT,
            TokenType.EOF
        ):
            statements.append(self.parse_statement())
            self.skip_newlines()

        self.expect(TokenType.DEDENT, "Expected end of block")

        return statements

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        expression = self.parse_addition()

        comparison_types = (
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
        )

        while self.current().type in comparison_types:
            operator = self.advance().value
            right = self.parse_addition()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def parse_addition(self):
        expression = self.parse_multiplication()

        while self.current().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.advance().value
            right = self.parse_multiplication()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def parse_multiplication(self):
        expression = self.parse_primary()

        while self.current().type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            operator = self.advance().value
            right = self.parse_primary()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def parse_primary(self):
        token = self.current()

        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(int(token.value))

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(token.value)

        if self.match(TokenType.LPAREN):
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')'")

            return expression

        raise SyntaxError(
            f"Line {token.line}: Expected a value"
        )
