import sys

sys.path.insert(0, "src")

from lexer import Lexer
from parser import Parser, PrintStatement


source = 'print("Hello DLang!")'

tokens = Lexer(source).tokenize()
statements = Parser(tokens).parse()

for statement in statements:
    if isinstance(statement, PrintStatement):
        print("PRINT:", statement.value)
