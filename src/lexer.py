from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    PRINT = auto()
    FUNC = auto()
    RETURN = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    COLON = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    indent: int = 0


class Lexer:
    def __init__(self, source):
        self.source = source

    def tokenize(self):
        tokens = []
        indent_stack = [0]
        lines = self.source.splitlines()

        for line_number, line in enumerate(lines, start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue

            indent_text = line[:len(line) - len(line.lstrip())]
            if "\t" in indent_text:
                raise SyntaxError(
                    f"Line {line_number}: Use spaces for indentation"
                )

            indent = len(indent_text)

            if indent > indent_stack[-1]:
                indent_stack.append(indent)
                tokens.append(Token(TokenType.INDENT, "", line_number, indent))
            elif indent < indent_stack[-1]:
                while indent < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(Token(TokenType.DEDENT, "", line_number, indent))
                if indent != indent_stack[-1]:
                    raise SyntaxError(f"Line {line_number}: Invalid indentation")

            i = indent

            while i < len(line):
                char = line[i]

                if char.isspace():
                    i += 1
                    continue

                if char == "#":
                    break

                if char in ('"', "'"):
                    quote = char
                    i += 1
                    value = ""

                    while i < len(line) and line[i] != quote:
                        if line[i] == "\\" and i + 1 < len(line):
                            i += 1
                            escaped = line[i]
                            if escaped == "n":
                                value += "\n"
                            elif escaped == "t":
                                value += "\t"
                            else:
                                value += escaped
                        else:
                            value += line[i]
                        i += 1

                    if i >= len(line):
                        raise SyntaxError(
                            f"Line {line_number}: Unterminated string"
                        )

                    i += 1
                    tokens.append(Token(TokenType.STRING, value, line_number, indent))
                    continue

                if char.isdigit():
                    start = i
                    has_dot = False
                    while i < len(line):
                        if line[i].isdigit():
                            i += 1
                        elif line[i] == "." and not has_dot:
                            has_dot = True
                            i += 1
                        else:
                            break
                    tokens.append(
                        Token(TokenType.NUMBER, line[start:i], line_number, indent)
                    )
                    continue

                if char.isalpha() or char == "_":
                    start = i
                    while i < len(line) and (
                        line[i].isalnum() or line[i] == "_"
                    ):
                        i += 1

                    word = line[start:i]
                    keywords = {
                        "print": TokenType.PRINT,
                        "func": TokenType.FUNC,
                        "return": TokenType.RETURN,
                        "if": TokenType.IF,
                        "elif": TokenType.ELIF,
                        "else": TokenType.ELSE,
                        "while": TokenType.WHILE,
                    }
                    tokens.append(
                        Token(
                            keywords.get(word, TokenType.IDENTIFIER),
                            word,
                            line_number,
                            indent,
                        )
                    )
                    continue

                two_char = line[i:i + 2]
                two_char_tokens = {
                    ">=": TokenType.GREATER_EQUAL,
                    "<=": TokenType.LESS_EQUAL,
                    "==": TokenType.EQUAL_EQUAL,
                    "!=": TokenType.NOT_EQUAL,
                }

                if two_char in two_char_tokens:
                    tokens.append(
                        Token(two_char_tokens[two_char], two_char, line_number, indent)
                    )
                    i += 2
                    continue

                single_char_tokens = {
                    "(": TokenType.LPAREN,
                    ")": TokenType.RPAREN,
                    ",": TokenType.COMMA,
                    "=": TokenType.ASSIGN,
                    "+": TokenType.PLUS,
                    "-": TokenType.MINUS,
                    "*": TokenType.MULTIPLY,
                    "/": TokenType.DIVIDE,
                    ">": TokenType.GREATER,
                    "<": TokenType.LESS,
                    ":": TokenType.COLON,
                }

                if char in single_char_tokens:
                    tokens.append(
                        Token(single_char_tokens[char], char, line_number, indent)
                    )
                    i += 1
                    continue

                raise SyntaxError(
                    f"Line {line_number}: Unexpected character '{char}'"
                )

            tokens.append(Token(TokenType.NEWLINE, "\n", line_number, indent))

        while len(indent_stack) > 1:
            indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, "", len(lines) or 1, 0))

        tokens.append(Token(TokenType.EOF, "", len(lines) or 1, 0))
        return tokens
