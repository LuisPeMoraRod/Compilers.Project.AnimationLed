import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.curLine = 1    # Current line in the code (for error handling)
        self.specialCharacters = "ºª\!|#$&?'¿¡`^¨´_<>@"
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r' or self.curChar == '\n':
            # Update line number
            if self.curChar == '\n':
                self.curLine +=1
            self.nextChar()
		
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            if self.peek() == "#":
                while self.curChar != '\n':
                    self.nextChar()
                self.nextChar()

    # Helper function to skip comments (this allows the user to place them everywhere)
    def isCommentOrWhiteSpace(self):
        if self.curChar in "#\n\t\r ":
            return True
        return False

    # Return the next token.
    def getToken(self):

        while self.isCommentOrWhiteSpace():
            self.skipComment()
            self.skipWhitespace()

        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)

        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == '*':
            if self.peek() == "*":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.ASTERISKD)
            else:
                token = Token(self.curChar, TokenType.ASTERISK)

        elif self.curChar == '/':
            # check whether this token is / or //
            if self.peek() == '/':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.SLASHD)
            else:
                token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '%':
            token = Token(self.curChar, TokenType.MODULE)

        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == '<':
                # Check whether this is token is < or <=
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        
        elif self.curChar == '\"':
            # Get the apostrophe '"'
            token = Token(self.curChar, TokenType.APOST)

        elif self.curChar == '{':
            # Get the curly bracket '{'
            token = Token(self.curChar, TokenType.CURLYBRACKETLEFT)

        elif self.curChar == '}':
            # Get the curly bracket '{'
            token = Token(self.curChar, TokenType.CURLYBRACKETRIGHT)

        elif self.curChar == '(':
            # Get the round bracket '('
            token = Token(self.curChar, TokenType.ROUNDBRACKETLEFT)

        elif self.curChar == ')':
            # Get the round bracket ')'
            token = Token(self.curChar, TokenType.ROUNDBRACKETRIGHT)

        elif self.curChar == '[':
            # Get the square bracket '['
            token = Token(self.curChar, TokenType.SQRBRACKETLEFT)

        elif self.curChar == ']':
            # Get the square bracket ']'
            token = Token(self.curChar, TokenType.SQRBRACKETRIGHT)
        
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)

        elif self.curChar == '.':
            # Get the dot '.'
            token = Token(self.curChar, TokenType.DOT)

        elif self.curChar == ':':
            # Get the double dot ':'
            token = Token(self.curChar, TokenType.DOUBLEDOT)

        elif self.curChar == ',':
            # Get the coma ','
            token = Token(self.curChar, TokenType.COMA)

        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit(): 
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum() or any(c in self.specialCharacters for c in self.peek()):
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)

        elif self.curChar == ';':
            token = Token(self.curChar, TokenType.SEMICOLON)

        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)

        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token


# Token contains the original text and the type of token.
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    SEMICOLON = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    DOT = 4
    COMA = 5
    NEWLINE = 6
    DOUBLEDOT = 7
    BOOLEAN = 8
    LIST = 9
    MATRIX = 10

    # Keywords.
    For = 101
    In = 102
    If = 103
    Procedure = 104
    true = 105
    false = 106
    Call = 107
    Range = 108
    Insert = 109
    Del = 110
    Len = 111
    Neg = 112
    T = 113
    F = 114
    Blink = 115
    Seg = 116
    Mil = 117
    Min = 118
    Delay = 119
    C = 120
    R = 121
    M = 122
    ShapeF = 123
    ShapeC = 124
    Step = 125
    PrintLed = 126
    PrintLedX = 127
    List = 128

    # Operators.
    EQ = 201
    PLUS = 202 
    MINUS = 203 
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206 
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    SLASHD = 212
    ASTERISKD = 213 
    MODULE = 214

    # Other symbols
    CURLYBRACKETLEFT = 301
    CURLYBRACKETRIGHT = 302
    ROUNDBRACKETLEFT = 303
    ROUNDBRACKETRIGHT = 304
    SQRBRACKETLEFT = 305
    SQRBRACKETRIGHT = 306
    APOST = 307
