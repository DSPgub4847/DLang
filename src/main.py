def run_dlang(code):
    for line in code.splitlines():
        line = line.strip()

        if line.startswith("print(") and line.endswith(")"):
            value = line[6:-1].strip()

            if value.startswith('"') and value.endswith('"'):
                print(value[1:-1])
            else:
                print("Invalid print statement")


if __name__ == "__main__":
    program = '''
print("Hello DLang!")
print("My first programming language")
'''

    run_dlang(program)
