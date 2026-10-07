import sys

sys.path.insert(0, "src")

from lexer import Lexer, TokenType


source = 'print("Hello DLang")'

tokens = Lexer(source).tokenize()

for token in tokens:
    print(
        f"{token.type.name:<12} "
        f"{token.value!r:<20} "
        f"line={token.line}"
    )
