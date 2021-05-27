from  lexer import Lexer
from tokenType import TokenType

def main():
    input = "If+-123 foo*For/ true false"
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

main()