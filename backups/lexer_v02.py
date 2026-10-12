from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    PRINT = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    LPAREN = auto()
    RPAREN = auto()
    EQUAL = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int


KEYWORDS = {
    "print": TokenType.PRINT,
}


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.source):
            char = self.source[self.position]

            # Ignore spaces and tabs
            if char in " \t\r":
                self.position += 1
                continue

            # New line
            if char == "\n":
                self.line += 1
                self.position += 1
                continue

            # Parentheses
            if char == "(":
                self.add_token(TokenType.LPAREN, char)
                continue

            if char == ")":
                self.add_token(TokenType.RPAREN, char)
                continue

            # Assignment
            if char == "=":
                self.add_token(TokenType.EQUAL, char)
                continue

            # Arithmetic operators
            if char == "+":
                self.add_token(TokenType.PLUS, char)
                continue

            if char == "-":
                self.add_token(TokenType.MINUS, char)
                continue

            if char == "*":
                self.add_token(TokenType.STAR, char)
                continue

            if char == "/":
                self.add_token(TokenType.SLASH, char)
                continue

            # Strings
            if char in "\"'":
                self.tokens.append(self.read_string(char))
                continue

            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            # Identifiers and keywords
            if char.isalpha() or char == "_":
                self.tokens.append(self.read_identifier())
                continue

            raise SyntaxError(
                f"Unexpected character '{char}' "
                f"at line {self.line}"
            )

        self.tokens.append(
            Token(TokenType.EOF, "", self.line)
        )

        return self.tokens

    def add_token(self, token_type, value):
        self.tokens.append(
            Token(token_type, value, self.line)
        )
        self.position += 1

    def read_string(self, quote):
        start_line = self.line
        self.position += 1
        value = []

        while self.position < len(self.source):
            char = self.source[self.position]

            if char == quote:
                self.position += 1
                return Token(
                    TokenType.STRING,
                    "".join(value),
                    start_line
                )

            if char == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {start_line}"
                )

            if char == "\\":
                self.position += 1

                if self.position >= len(self.source):
                    break

                escaped = self.source[self.position]

                escapes = {
                    "n": "\n",
                    "t": "\t",
                    "\\": "\\",
                    "'": "'",
                    '"': '"',
                }

                value.append(escapes.get(escaped, escaped))
                self.position += 1
                continue

            value.append(char)
            self.position += 1

        raise SyntaxError(
            f"Unterminated string at line {start_line}"
        )

    def read_number(self):
        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            self.position += 1

        value = self.source[start:self.position]

        return Token(
            TokenType.NUMBER,
            value,
            self.line
        )

    def read_identifier(self):
        start = self.position

        while self.position < len(self.source):
            char = self.source[self.position]

            if char.isalnum() or char == "_":
                self.position += 1
            else:
                break

        value = self.source[start:self.position]

        return Token(
            KEYWORDS.get(value, TokenType.IDENTIFIER),
            value,
            self.line
        )
