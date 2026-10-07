from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    PRINT = auto()
    IDENTIFIER = auto()
    STRING = auto()

    LPAREN = auto()
    RPAREN = auto()

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

            if char in " \t\r":
                self.position += 1
                continue

            if char == "\n":
                self.line += 1
                self.position += 1
                continue

            if char == "(":
                self.tokens.append(
                    Token(TokenType.LPAREN, char, self.line)
                )
                self.position += 1
                continue

            if char == ")":
                self.tokens.append(
                    Token(TokenType.RPAREN, char, self.line)
                )
                self.position += 1
                continue

            if char in "\"'":
                self.tokens.append(self.read_string(char))
                continue

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

    def read_string(self, quote):
        start_line = self.line
        self.position += 1

        value = ""

        while self.position < len(self.source):
            char = self.source[self.position]

            if char == quote:
                self.position += 1
                return Token(
                    TokenType.STRING,
                    value,
                    start_line
                )

            if char == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {start_line}"
                )

            value += char
            self.position += 1

        raise SyntaxError(
            f"Unterminated string at line {start_line}"
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

        token_type = KEYWORDS.get(
            value,
            TokenType.IDENTIFIER
        )

        return Token(token_type, value, self.line)
