from lexer import *
from parser import *
from emit import *
import sys

def main():
    print("Animation LED Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # Initialize the lexer and parser.
    lexer = Lexer(input)
    emitter = Emitter("out.py")
    parser = Parser(lexer, emitter)

    parser.program() # Start the parser.
    print("Parsing completed.")
    #emitter.writeFile()
    print("Compiling completed")

if __name__ == "__main__":
    main()
