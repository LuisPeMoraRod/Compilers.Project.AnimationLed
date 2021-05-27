from lexer import TokenType
import sys
from lexer import *

# Parser object keeps track of current token and checks if the code matches the grammar.


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = []    # Variables declared so far and their types and values
        self.procedures = [] # Procedures declared so far with their parameter names

        #Variables used for procedure call
        self.tempProcedureCall = None
        self.tempParameterCall = []

        #Variables used for logic validations in Procedures
        self.tempProcedure = None
        self.tempParameters = []

        #Variables used for logic validations: e.g. check if a variable already exists
        self.tempIdent  = None 
        self.tempType = None
        self.tempIsGlobal = None

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name +
                       ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.

    def abort(self, message):
        sys.exit("Error. " + message)

        # Production rules.

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # One of the following statements...
    def statement(self):
        # Check the first token to see what kind of statement this is.

        #statement := Call IDENT "(" ")"
        if self.checkToken(TokenType.Call):
            print("STATEMENT-PROCEDURE-CALL")
            self.nextToken()
            self.checkToken(TokenType.IDENT)
            self.tempProcedureCall = self.curToken.text
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)

            if self.checkToken(TokenType.ROUNDBRACKETRIGHT):
                self.tempParameterCall = []
            else:
                self.params(self.tempParameterCall)

            if self.procedureExists(self.tempProcedureCall, len(self.tempParameterCall)):
                    self.tempProcedureCall = None
                    self.tempParameterCall = []
            else:
                self.abort("Undefined procedure call at " + self.tempProcedureCall + " (" + str(len(self.tempParameterCall)) + ")")

        # statement := ident "=" (expression | true | false) ";" 
        elif self.checkToken(TokenType.IDENT):

            print("STATEMENT-VAR DEFINITION")
            self.tempIdent = self.curToken.text

            self.nextToken()
            self.match(TokenType.EQ)

            if self.checkToken(TokenType.true):
                if self.getSymbolType(self.tempIdent) == TokenType.NUMBER:
                    self.abort("Attempting to assign a BOOLEAN to a NUMBER typed variable: " + self.tempIdent)

                self.match(TokenType.true)
                self.tempType = TokenType.BOOLEAN

            elif self.checkToken(TokenType.false):
                if self.getSymbolType(self.tempIdent) == TokenType.NUMBER:
                    self.abort("Attempting to assign a BOOLEAN to a NUMBER typed variable: " + self.tempIdent)

                self.match(TokenType.false)
                self.tempType = TokenType.BOOLEAN
            
            elif self.checkToken(TokenType.SQRBRACKETLEFT):
                listIdent = self.tempIdent
                self.match(TokenType.SQRBRACKETLEFT)
                for i in range(7): #7 elements + COMMA
                    self.checkLstElmnt()
                    self.match(TokenType.COMA)
                self.checkLstElmnt() #last element
                self.match(TokenType.SQRBRACKETRIGHT)

                self.tempIdent = listIdent
                self.tempType = TokenType.LIST


            else:
                self.expression()
                self.tempType = TokenType.NUMBER
                symbolType = self.getSymbolType(self.tempIdent) 
                if symbolType == TokenType.BOOLEAN:
                    self.abort("Attempting to assign a NUMBER to a BOOLEAN typed variable: " + self.tempIdent)

                elif symbolType == TokenType.LIST:
                    self.abort("Attempting to assign a NUMBER to a LIST typed variable: " + self.tempIdent)
            
            
            if not self.symbolExists(self.tempIdent):
                print("Adding "+ self.tempIdent)
                self.addSymbol(self.tempIdent, self.tempType, True) #OJO True means that they are all global variables (needs to be changed when Procedures are implemented)

        elif self.checkToken(TokenType.If):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.CURLYBRACKETLEFT)

            # Zero or more statements in the body.
            while not self.checkToken(TokenType.CURLYBRACKETRIGHT):
                self.statement()

            self.match(TokenType.CURLYBRACKETRIGHT)

        elif self.checkToken(TokenType.Procedure):
            print("STATEMENT-PROCEDURE-DEFINITION")
            self.nextToken()
            self.tempProcedure = self.curToken.text
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)

            #Procedure without parameters
            if self.checkToken(TokenType.ROUNDBRACKETRIGHT):
                self.tempParameters = []
                self.nextToken()

            #Procedure with parameters
            else:
                self.params(self.tempParameters)

            # Save the procedure name if doesn't exists yet
            if not self.procedureExists(self.tempProcedure, len(self.tempParameters)):
                self.addProcedure(self.tempProcedure, len(self.tempParameters), self.tempParameters)
                self.tempProcedure = None
                self.tempParameters = []
            else:
                self.abort("The procedure " + self.tempProcedure + " (" + str(len(self.tempParameters)) + ") is already defined")

            self.match(TokenType.CURLYBRACKETLEFT)

            # Zero or more statements in the body.
            while not self.checkToken(TokenType.CURLYBRACKETRIGHT):
                self.statement()

            self.match(TokenType.CURLYBRACKETRIGHT)

        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")


        # Newline.
        self.semicolon()

    def params(self, parameterList):
        print("PARAMETERS")
        while True:
            if self.checkToken(TokenType.IDENT):
                parameterList.append(self.curToken.text)
            else:
                self.abort("Invalid parameter statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")
            self.nextToken()
            if self.checkToken(TokenType.ROUNDBRACKETRIGHT):
                self.nextToken()
                break
            if not self.checkToken(TokenType.COMA):
                self.abort("Expected a COMA ',' at " + self.curToken.text)
            self.nextToken()
        

    # semicolon ::= ';'+
    def semicolon(self):
        print("SEMICOLON")
        # Require at least one newline.
        self.match(TokenType.SEMICOLON)
        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.SEMICOLON):
            self.nextToken()

    def isData(self):
        if self.checkPeek(TokenType.NUMBER) or self.checkPeek(TokenType.true) or self.checkPeek(TokenType.false) or self.checkPeek(TokenType.IDENT):
            self.nextToken()
            return True
        return False
    
    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.nextToken()
            if self.checkToken(TokenType.true):
                self.match(TokenType.true)
            elif self.checkToken(TokenType.false):
                self.match(TokenType.false)
            else:
                self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    def isComparisonOperator(self):
            return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

     # term ::= unary {( "/" | "//" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        # Can have 0 or more * / and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.SLASHD):
            self.nextToken()
            self.unary()


    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()        
        self.module()

    #module ::= exp {("%") exp}
    def module(self):
        self.exp()
        while self.checkToken(TokenType.MODULE):
            print("MODULE")
            self.nextToken()
            self.exp()

    #exp ::= primary {("**") primary}
    def exp(self):
        self.primary()
        while self.checkToken(TokenType.ASTERISKD):
            print("EXPONENT")
            self.nextToken()
            self.primary()
         

    # primary ::= number | ident{squareBrackets} | "(" expression ")"
    def primary(self):
        print("PRIMARY ( \'" + self.curToken.text + "\' )")

        if self.checkToken(TokenType.NUMBER): 
            self.nextToken()

        elif self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            if self.symbolExists(self.tempIdent):
                self.nextToken()
                self.squareBrackets()
            else:
                 self.abort("Attempting to access an undeclared variable: " + self.tempIdent)

        elif self.checkToken(TokenType.ROUNDBRACKETLEFT):
            self.nextToken()
            self.expression()
            print("PRIMARY ( \'" + self.curToken.text + "\' )")
            self.match(TokenType.ROUNDBRACKETRIGHT)

        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)  
    
    #squareBrackets ::= "[" ( expression | ":" "," number) "]"
    def squareBrackets(self):
        if self.checkToken(TokenType.SQRBRACKETLEFT):
            print("SQUARE BRACKETS")
            self.nextToken()
            if self.checkToken(TokenType.DOUBLEDOT):
                self.match(TokenType.DOUBLEDOT)
                self.match(TokenType.COMA)
                self.expression()
                #self.match(TokenType.NUMBER) # OJO missing validation for range overload (unexistent column)
                self.match(TokenType.SQRBRACKETRIGHT)
            else:
                self.expression()
                self.match(TokenType.SQRBRACKETRIGHT)
    
    #Checks if symbol already exists
    def symbolExists(self, identifier):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                return True
        return False
    
    #Add new variable to set
    def addSymbol(self, identifier, dataType, isGlobal):
        newSymbol = [identifier, dataType, isGlobal]
        self.symbols.append(newSymbol)

    #Returns data type of given identifier. If variable hasn't been declared, returns None
    def getSymbolType(self, identifier):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                return symbol[1]
        return None

    #Add new procedure
    def addProcedure(self, identifier, numberOfParams, paramList):
        newProcedure = [identifier] + [numberOfParams] + paramList
        self.procedures.append(newProcedure)

    def checkLstElmnt (self):
        if self.checkToken(TokenType.true):
            self.match(TokenType.true)

        elif self.checkToken(TokenType.false):
            self.match(TokenType.false)
            
        elif self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            self.tempType = self.getSymbolType(self.tempIdent)
            if self.tempType != None:
                if self.tempType == TokenType.BOOLEAN:
                    self.nextToken()
                else:
                    self.abort("Attempting to assign a NON BOOLEAN variable to a list element: " + self.tempIdent)
            else:
                self.abort("Attempting to access an undeclared variable: " + self.tempIdent)
        else: 
            self.match(TokenType.BOOLEAN) #abort: invalid data type. must be a boolean


    #Check if procedure already exists
    def procedureExists(self, identifier, paramLenght):
        for procedure in self.procedures:
            # True if has the same name and the same amount of parameters
            if procedure[0] == identifier and procedure[1] == paramLenght:
                return True
        return False
