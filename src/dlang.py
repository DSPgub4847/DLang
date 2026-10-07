#!/usr/bin/env python3

import sys

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def main():
    if len(sys.argv) != 2:
        print("Usage: dlang <file.dl>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            source = file.read()

        tokens = Lexer(source).tokenize()
        statements = Parser(tokens).parse()

        Interpreter(statements).run()

    except FileNotFoundError:
        print(f"DLang: file not found: {filename}")
        sys.exit(1)

    except (SyntaxError, RuntimeError) as error:
        print(f"DLang error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
