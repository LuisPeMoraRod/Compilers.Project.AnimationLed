import sys
#from typing import type_check_only
from lexer import *

# Parser object keeps track of current token and checks if the code matches the grammar.


class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.hasMainProcedure = False #Helps to know if there is one and only one Main procedure
        self.symbols = []    # Variables declared so far and their types and values        
        self.procedures = [] # Procedures declared so far with their parameter names

        #Variables used for procedure call
        self.tempProcedureCall = None
        self.tempParameterCall = []
        self.tempMainCalls = [] #Needed for ignoring Main procedure calls temporaly

        #Variables used for logic validations in Procedures
        self.tempProcedure = None
        self.tempParameters = []
        #Variables used for logic validations: e.g. check if a variable already exists
        self.tempIdent  = None 
        self.tempType = None
        self.tempValue = None #Variables values
        self.tempRows = None #Amount of rows for matrixes
        self.tempColumns = None #Amount of columns for matrixes

        # Emitter variables
        self.indentation = ""
        self.currentLineText = ""
        self.tempOperation = "" #An arithmetic operation

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

    # Finished the program to indicate an Error
    def abort(self, message):
        sys.exit("Error. " + message + " at Line " + str(self.lexer.curLine))

    # Finished the program to indicate an Error
    def abortLine(self, message, lineNumber):
        sys.exit("Error. " + message + " at Line " + str(lineNumber))

        # Production rules.

    # program ::= {statement}
    def program(self):
        self.emitter.headerLine("import out_aux")

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
           self.procedure() # The whole program made of procedures

        #Checks the pending Main procedure calls (were not checed before)
        for mainCall in self.tempMainCalls:
            if not self.procedureExists(mainCall[0], len(mainCall[1])):
                self.abortLine("Undefined procedure call " + mainCall[0] + " (" + str(len(mainCall[1])) + ")", mainCall[2]-1)

    # procedure := Procedure IDENT "(" {params} ")" "{" {statement} "}"
    def procedure(self):
        self.match(TokenType.Procedure)
        print("STATEMENT-PROCEDURE-DEFINITION")
        self.tempProcedure = self.curToken.text

        #Has only one Main procedure validations
        if self.hasMainProcedure and self.tempProcedure == 'Main':
            self.abort("Multiple definition of Main method")

        # Ignore identation in Main method
        if not self.tempProcedure == 'Main':
            self.currentLineText += "def " + self.tempProcedure


        #Checks if the first procedure is Main
        if not self.hasMainProcedure:
            if self.tempProcedure != 'Main':
                self.abort("First Procedure is not Main")
            else:
                self.hasMainProcedure = True

        self.nextToken()
        self.match(TokenType.ROUNDBRACKETLEFT)

        if not self.tempProcedure == 'Main':
            self.currentLineText += "("

        #Procedure without parameters
        if self.checkToken(TokenType.ROUNDBRACKETRIGHT):
            self.tempParameters = []
            if not self.tempProcedure == 'Main':
                self.currentLineText += "):"
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""
                self.indentation += '\t'
            self.nextToken()

        #Procedure with parameters
        else:
            self.params(self.tempParameters)
            if not self.tempProcedure == 'Main':
                for param in self.tempParameters:
                    self.currentLineText += param + ","
                self.currentLineText = self.currentLineText[:-1]
                self.currentLineText += '):'
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""
                self.indentation += '\t'


        #Checks if the Main method has no parameters
        if len(self.tempParameters) != 0 and self.tempProcedure == 'Main':
            self.abort("Main method has parameters and needs zero (0) parameters")

        # Save the procedure name if doesn't exists yet
        if not self.procedureExists(self.tempProcedure, len(self.tempParameters)):
            self.addProcedure(self.tempProcedure, len(self.tempParameters), self.tempParameters)

        else:
            self.abort("The procedure " + self.tempProcedure + " (" + str(len(self.tempParameters)) + ") is already defined")

        # Define parameters as local variables
        for param in self.tempParameters:
            self.addSymbol(param, None, self.tempProcedure, None, None, None)

        self.match(TokenType.CURLYBRACKETLEFT)

        # Zero or more statements in the body.
        statementCounter = 0
        while not self.checkToken(TokenType.CURLYBRACKETRIGHT):
            statementCounter+=1
            self.statement(self.tempProcedure)
        
        if statementCounter == 0:
            self.emitter.emitLine(self.indentation + "pass")

        self.match(TokenType.CURLYBRACKETRIGHT)
        if not self.tempProcedure == 'Main':
            self.indentation = self.indentation[:-1]
        


        self.tempProcedure = None
        self.tempParameters = []
        # Newline.
        self.semicolon()

    # One of the following statements...
    def statement(self, procedure):
        #Check the first token to see what kind of statement this is.

        #Call procedure parsing
        #statement := Call IDENT "(" ")"
        if self.checkToken(TokenType.Call):
            print("STATEMENT-PROCEDURE-CALL")
            self.nextToken()
            self.checkToken(TokenType.IDENT)
            self.tempProcedureCall = self.curToken.text # Saves name for validations
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            self.currentLineText += self.indentation + self.tempProcedureCall + '('

            if self.checkToken(TokenType.ROUNDBRACKETRIGHT):
                self.tempParameterCall = []
                self.currentLineText += ')'
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""
                self.nextToken()
            else:
                self.paramsCall(self.tempParameterCall)
                for param in self.tempParameterCall:
                    self.currentLineText += param + ","
                self.currentLineText = self.currentLineText[:-1]
                self.currentLineText += ')'
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""


            # Program checks Main procedure calls at the end of the program (due to scope restrictions)
            if not procedure == 'Main':
                # Checks if the called procedure exists
                if self.procedureExists(self.tempProcedureCall, len(self.tempParameterCall)):
                    self.tempProcedureCall = None
                    self.tempParameterCall = []
                else:
                    self.abort("Undefined procedure call at " + self.tempProcedureCall + " (" + str(len(self.tempParameterCall)) + ")")
            else:
                self.tempMainCalls.append((self.tempProcedureCall, self.tempParameterCall, self.lexer.curLine))
                self.tempProcedureCall = None
                self.tempParameterCall =[]

        #Simple variable declaration/assignation
        # statement := ident "=" (expression | true | false) ";" 
        #Var =  
        elif self.checkToken(TokenType.IDENT) and self.peekToken.kind == TokenType.EQ:
            self.tempIdent = self.curToken.text
            self.currentLineText += self.indentation + self.tempIdent
            self.nextToken()
            self.match(TokenType.EQ) # identifier followed by =
            self.currentLineText += '='
            print("STATEMENT-SIMPLE VAR ASSIGNATION")
            if self.sintaxVar(self.tempIdent):
                self.assignation(procedure)
            else:
                self.abort("Invalid identifier: "+self.tempIdent)
        
        #Compound variable declaration/assignation
        #statement := IDENT compoundIdent "=" compoundDeclaration ";"
        #compoundIdent := {"," IDENT compoundIdent}
        #Compound variable declaration/assignation
        #statement := IDENT compoundIdent "=" compoundDeclaration ";"
        #compoundIdent := {"," IDENT compoundIdent}
        elif self.checkToken(TokenType.IDENT) and self.peekToken.kind == TokenType.COMA:
            variables = []

            self.tempIdent = self.curToken.text
            self.match(TokenType.IDENT)

            if self.sintaxVar(self.tempIdent):
                variables.append(self.tempIdent)
            else:
                self.abort("Invalid identifier: "+self.tempIdent)
            
            
            print("STATEMENT-COMPOUND VAR ASSIGNATION")

            while not self.checkToken(TokenType.EQ):
                self.match(TokenType.COMA)
                self.tempIdent = self.curToken.text
                self.match(TokenType.IDENT)
                if self.sintaxVar(self.tempIdent):
                    variables.append(self.tempIdent)
                else:
                    self.abort("Invalid identifier: "+self.tempIdent)
            
            self.match(TokenType.EQ)

            self.tempIdent = variables[0]

            self.currentLineText = self.tempIdent + '='
            self.assignation(procedure)


            for i in range(1, len(variables)):
                self.match(TokenType.COMA)
                self.tempIdent = variables[i]
                self.currentLineText = self.tempIdent + '='
                self.assignation(procedure)
        
        #List operations or modifiers
        elif self.isListIdent(procedure) and self.checkPeek(TokenType.SQRBRACKETLEFT):
            self.currentLineText += self.indentation
            print("STATEMENT-LIST MODIFIER")
            self.nextToken()
            is_range = False
            delimiters = self.squareBrackets(self.tempIdent)
            if isinstance(delimiters, tuple):
                is_range = True
                print(is_range)
            
            if self.checkToken(TokenType.EQ): #Validation for List modifiers e.g: listvar[3] = true; listvar[1:3] = [true, false];
                                            #statement := IDENT squareBrackets "=" ("[" boolean listValues "]" | boolean)
                self.match(TokenType.EQ)
                if is_range: #range assignation: listvar[1:3] = [true, false]
                    self.match(TokenType.SQRBRACKETLEFT)
                    self.currentLineText += '['
                    list_range = delimiters[1] - delimiters[0]
                    self.checkLstElmnt() #first element
                    for i in range(list_range - 1):
                        self.match(TokenType.COMA)
                        self.currentLineText += ', '
                        self.checkLstElmnt()
                    self.match(TokenType.SQRBRACKETRIGHT)
                    self.currentLineText += '])'
                    self.emitter.emitLine(self.currentLineText)
                    self.currentLineText = ""
                else:
                    self.checkLstElmnt()
                    self.currentLineText += ')'
                    self.emitter.emitLine(self.currentLineText)
                    self.currentLineText = ""

            elif self.checkToken(TokenType.DOT): #Validation for list operations: listvar[0].Neg; listvar[0].T; listvar[0].F;
                                                #statement := IDENT squareBrackets "." ("Neg" | "T" | "F")
                print("DOT")
                self.match(TokenType.DOT)
                if self.checkToken(TokenType.Neg) or self.checkToken(TokenType.F) or self.checkToken(TokenType.T):
                    if self.checkToken(TokenType.Neg):
                        self.currentLineText += '0)'
                    elif self.checkToken(TokenType.F):
                        self.currentLineText += 'False)'
                    elif self.checkToken(TokenType.T):
                        self.currentLineText += 'True)'
                    self.emitter.emitLine(self.currentLineText)
                    self.currentLineText = ""
                    self.nextToken()
                else:
                    self.abort("Unrecognized statement at: " + self.curToken.text)
        
        #Insert or delete elements from list
        elif self.isListIdent(procedure) and self.checkPeek(TokenType.DOT):
            self.currentLineText += self.indentation + self.curToken.text + '.'
            self.nextToken()
            self.match(TokenType.DOT)
            if self.curToken.text == "insert": #listvar.Insert(5,true);
                self.currentLineText += "insert("
                print("STATEMENT - INSERT")
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETLEFT)
                self.currentLineText += self.curToken.text
                size = self.getSymbolValue(self.tempIdent)
                self.inRange(size, procedure)
                self.match(TokenType.COMA)
                self.currentLineText += ', '
                self.checkLstElmnt()
                self.currentLineText += ')'
                self.match(TokenType.ROUNDBRACKETRIGHT)
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""

            elif self.curToken.text == "delete":
                self.currentLineText += "delete("
                print("STATEMENT - DELETE")
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETLEFT)
                self.currentLineText += self.curToken.text + ')'
                size = self.getSymbolValue(self.tempIdent) - 1
                self.inRange(size, procedure)
                self.match(TokenType.ROUNDBRACKETRIGHT)
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""
            else:
                self.abort("Invalid identifier "+ self.curToken.text)
        
        #Matrix operations or modifiers
        elif self.isMatrixIdent(procedure) and self.checkPeek(TokenType.SQRBRACKETLEFT):
            print("STATEMENT-MATRIX MODIFIER")

            self.nextToken() #This should be the [
            self.nextToken() #This is what is next to the [
            
            #Checks if the token is a number:
            if self.checkToken(TokenType.NUMBER):
                rowIndex = int(self.curToken.text)
                self.checkRows(self.getMatrixRows(self.tempIdent), rowIndex)
                self.nextToken()

                #This is true when user is trying to access a row
                if self.checkToken(TokenType.SQRBRACKETRIGHT): #Checks for matrix[index]
                    self.nextToken()


                elif self.checkToken(TokenType.COMA): #Checks for matrix[row,column]
                    self.getMatrixEl(procedure)
                    if self.checkToken(TokenType.EQ):
                        self.nextToken()
                        self.checkLstElmnt()
                        
                else:
                    self.abort("Expected an int or :, got: "+ self.curToken.text)

                #Checks for matrix1[].Neg operation
                self.checkNeg(procedure)

            #Checks for the operation matrix[:,column]
            elif self.checkToken(TokenType.DOUBLEDOT):
                self.getAColumn(procedure)
            
            else:
                self.abort("Expected an int or :, got: "+ self.curToken.text)
            
            #Checks for matrix1[].Neg operation
            self.checkNeg(procedure)
        
        #Matrix modifiers
        elif self.isMatrixIdent(procedure) and self.checkPeek(TokenType.DOT):

            matrixColumns = self.getMatrixColumns(self.tempIdent)
            matrixRows = self.getMatrixRows(self.tempIdent)
            matrix = self.tempIdent
            self.nextToken()
            self.nextToken()
                
                #Checks if the user wants to retrieve the rows and columns of a matrix
            if self.checkToken(TokenType.ShapeF) or self.checkToken(TokenType.ShapeC):
                print("GET MATRIX SHAPE: " + matrix)
                self.nextToken()
                
            #Checks if the user wants to add an element in the matrix
            elif self.checkToken(TokenType.Insert):
                print("INSERT ELEMENT IN MATRIX: "+ matrix)
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETLEFT)
                elements = 0

                #checks if the element is a list already created
                if self.checkToken(TokenType.IDENT):
                    self.isListIdent(procedure)
                    self.nextToken()
                    self.match(TokenType.COMA)
                    elements = self.getSymbolValue(self.tempIdent)
                    
                #checks if the element is a new list
                elif self.checkToken(TokenType.SQRBRACKETLEFT):
                    self.nextToken()
                    self.checkLstElmnt() #first element
                    elements = 1
        
                    while not self.checkToken(TokenType.SQRBRACKETRIGHT):
                        self.match(TokenType.COMA)
                        self.checkLstElmnt()
                        elements = elements + 1
                            
                    self.match(TokenType.SQRBRACKETRIGHT)
                    self.match(TokenType.COMA)
                else:
                    self.abort("Invalid token: " + self.curToken.text)

                #Checks for the operation number 0 for rows and 1 for columns
                if self.checkToken(TokenType.NUMBER):
                    operation = int(self.curToken.text)
                    if operation == 0 or operation == 1:
                        self.nextToken()

                            #Checks if the user wants to select a specific index matrix.insert(element, operation, index)
                        if self.checkToken(TokenType.COMA):
                            self.nextToken()
                            if self.checkToken(TokenType.NUMBER):
                                index = int(self.curToken.text)
                                if operation == 0:
                                    self.checkRows(matrixRows, index)
                                    print("Columns: ", matrixColumns)
                                    print("Elelemnts: ", elements)
                                    if matrixColumns == elements:
                                        self.addRows(matrix, procedure)
                                    else:
                                        self.abort("The element that is trying to be added to the matrix doesn't match the matrix size")
                                        
                                else:
                                    self.checkColumns(matrixColumns, index)
                                    if matrixRows == elements:
                                        self.addColumns(matrix, procedure)
                                    else:
                                        self.abort("The element that is trying to be added to the matrix doesn't match the matrix size")
                                    
                                self.nextToken()
                            else:
                                self.abort("Expected an int, got: " + self.curToken.text)
                            
                        #Insert operation without index matrix.insert(element, operation)
                        elif(self.checkToken(TokenType.ROUNDBRACKETRIGHT)):
                            if operation == 0:
                                if matrixColumns == elements:
                                    self.addRows(matrix, procedure)
                                else:
                                    self.abort("The element that is trying to be added to the matrix doesn't match the matrix size")
                                        
                            else:
                                if matrixRows == elements:
                                    self.addColumns(matrix, procedure)
                                else:
                                    self.abort("The element that is trying to be added to the matrix doesn't match the matrix size")
                                
                        else:
                            self.abort("Expected a , or an int, got: " + self.curToken.text)
                            
                        self.match(TokenType.ROUNDBRACKETRIGHT)
                else:
                    self.abort("Expected an int, got: " + self.curToken.text)
                
                #Delete operation
            elif self.checkToken(TokenType.Del):
                print("DELETE ELEMENT FROM MATRIX: "+ self.curToken.text)
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETLEFT)

                    #Checks for a valid index
                if self.checkToken(TokenType.NUMBER):
                    index = int(self.curToken.text)
                    self.nextToken()
                    self.match(TokenType.COMA)

                        #Checks for the operation: 0 for rows and 1 for columns
                    if self.checkToken(TokenType.NUMBER):
                        operation = int(self.curToken.text)
                        if operation == 0:
                            self.checkRows(matrixRows, index)
                            self.deleteRows(matrix, procedure)
                        elif operation == 1:
                            self.checkColumns(matrixColumns, index)
                            self.deleteColumns(matrix, procedure)
                        else:
                            self.abort("Expected a 0 or a 1, got: " + self.curToken.text)
                    else:
                        self.abort("Expected a 0 or a 1, got: " + self.curToken.text)
                else:
                    self.abort("Expected an int, got: " + self.curToken.text)
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETRIGHT)

            else:
                self.abort("Invalid token: "+ self.curToken.text)


        #Statement if
        #statement := If comparison "{" {statement} "}" ";"
        elif self.checkToken(TokenType.If):
            print("STATEMENT-IF")
            self.nextToken()
            self.tempProcedure = procedure
            self.comparison(procedure)

            self.match(TokenType.CURLYBRACKETLEFT)

            # Zero or more statements in the body.
            while not self.checkToken(TokenType.CURLYBRACKETRIGHT):
                self.statement(procedure)

            self.match(TokenType.CURLYBRACKETRIGHT)
        
        #Statement for
        #Statement := For variable "In" iterable "Step" num "{" {statement} "}" ";"
        elif self.checkToken(TokenType.For):
            print("STATEMENT-FOR")
            self.nextToken()

            if self.checkToken(TokenType.IDENT):
                iterable = self.curToken.text
                if self.sintaxVar(iterable):
                    self.addSymbol(iterable, TokenType.NUMBER, procedure, 0, None, None)
                    self.nextToken()
                    self.match(TokenType.In)

                    #Checks if the iterable is a list
                    if self.isListIdent(procedure):
                        listLength = self.getSymbolValue(self.curToken.text)
                        self.nextToken()
                        if self.checkToken(TokenType.SQRBRACKETLEFT):
                            self.nextToken()
                            if self.checkToken(TokenType.NUMBER):
                                index1 = int(self.curToken.text)
                                self.nextToken()
                                self.match(TokenType.DOUBLEDOT)
                                if self.checkToken(TokenType.NUMBER):
                                    index2 = int(self.curToken.text)
                                    self.checkRange(listLength, index1, index2)
                                else:
                                    self.abort("Invalid token: " + self.curToken.text)
                                self.nextToken()
                                self.match(TokenType.SQRBRACKETRIGHT)
                            else:
                                self.abort("Invalid token: " + self.curToken.text)

                    #Checks if the iterable is a number 
                    elif self.checkToken(TokenType.NUMBER):
                        self.nextToken()
                    else:
                        self.abort("Invalid iterable: " + self.curToken.text)

                    if self.checkToken(TokenType.Step):
                        self.nextToken()
                        self.match(TokenType.NUMBER)
                        
                else:
                    self.abort("Invalid variable name: "+ self.tempIdent)
            else:
                self.abort("Invalid statement: " + self.tempIdent)
            
            self.match(TokenType.CURLYBRACKETLEFT)

            # Zero or more statements in the body.
            while not self.checkToken(TokenType.CURLYBRACKETRIGHT):
                self.statement(procedure)

            self.match(TokenType.CURLYBRACKETRIGHT)
            self.deleteSymbol(iterable, procedure)


        #Blink statement: Blink( x[1],5, “Seg”, True); Blink( x[1:3],5, “Seg”, True); Blink( x,5, “Seg”, True);
        elif self.checkToken(TokenType.Blink):
            print("STATEMENT - BLINK")
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            if self.isListIdent(procedure):
                self.nextToken()
                self.squareBrackets(self.tempIdent)
                self.match(TokenType.COMA)
                self.matchNumber(procedure)
                self.match(TokenType.COMA)
                self.match(TokenType.APOST)
                if self.checkToken(TokenType.Mil) or self.checkToken(TokenType.Seg) or self.checkToken(TokenType.Min):
                    self.nextToken()
                    self.match(TokenType.APOST)
                    self.match(TokenType.COMA)
                    self.checkLstElmnt()
                    self.match(TokenType.ROUNDBRACKETRIGHT)
                else:
                    self.abort("Invalid time unit: "+self.curToken.text)
        
        #Delay statement: Delay(5, "Mil")
        elif self.checkToken(TokenType.Delay):
            print("STATEMENT - DELAY")
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            self.matchNumber(procedure)
            self.match(TokenType.COMA)
            self.match(TokenType.APOST)
            if self.checkToken(TokenType.Mil) or self.checkToken(TokenType.Seg) or self.checkToken(TokenType.Min):
                self.nextToken()
                self.match(TokenType.APOST)
                self.match(TokenType.ROUNDBRACKETRIGHT)
            else:
                self.abort("Invalid time unit: "+self.curToken.text)

        #PrintLed statement
        elif self.checkToken(TokenType.PrintLed):
            print("STATEMENT - PrintLed")
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            self.matchColRow(procedure)
            self.match(TokenType.COMA)
            self.matchColRow(procedure)
            self.match(TokenType.COMA)
            self.checkLstElmnt()
            self.match(TokenType.ROUNDBRACKETRIGHT)

        #PrintLedX statement
        elif self.checkToken(TokenType.PrintLedX):
            print("STATEMENT - PrintLedX")
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            self.match(TokenType.APOST)
            if self.checkToken(TokenType.R) or self.checkToken(TokenType.C) or self.checkToken(TokenType.M):
                objType = self.curToken.text
                self.nextToken()
                self.match(TokenType.APOST)
                self.match(TokenType.COMA)
                self.matchColRow(procedure)
                self.match(TokenType.COMA)
                if objType == "M":
                    if self.isMatrixIdent(procedure):
                        self.nextToken()
                    else:
                        self.match(TokenType.IDENT)
                else:
                    if self.isListIdent(procedure):
                        self.nextToken()
                    else:
                        self.match(TokenType.IDENT)
                self.match(TokenType.ROUNDBRACKETRIGHT)
            
            else:
                self.abort("Invalid object type: " + self.curToken.text)

        
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
    
    def paramsCall(self, parameterList):
        print("PARAMETERS - CALL")
        while True:
            if self.checkToken(TokenType.IDENT) or self.checkToken(TokenType.NUMBER)\
                or self.checkToken(TokenType.true) or self.checkToken(TokenType.false):
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
        #self.match(TokenType.SEMICOLON)
        if not self.checkToken(TokenType.SEMICOLON):
            self.abortLine("Expected SEMICOLON at the end of instruction", self.lexer.curLine-1)
        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.SEMICOLON):
            self.nextToken()

    def isData(self):
        if self.checkPeek(TokenType.NUMBER) or self.checkPeek(TokenType.true) or self.checkPeek(TokenType.false) or self.checkPeek(TokenType.IDENT):
            self.nextToken()
            return True
        return False
    
    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self, procedure):
        print("COMPARISON")

        self.expression(procedure)
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.nextToken()
            if self.checkToken(TokenType.true):
                self.match(TokenType.true)
            elif self.checkToken(TokenType.false):
                self.match(TokenType.false)
            else:
                self.expression(procedure)
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression(procedure)
    
    def isComparisonOperator(self):

            return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    # expression ::= term {( "-" | "+" ) term}
    def expression(self, procedure):
        print("EXPRESSION")

        self.term(procedure)
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            if self.checkToken(TokenType.PLUS):
                self.currentLineText += '+'
            elif self.checkToken(TokenType.MINUS):
                self.currentLineText += '-'
            self.tempOperation = self.tempOperation + self.curToken.text
            self.nextToken()
            self.term(procedure)

     # term ::= unary {( "/" | "//" | "*" ) unary}
    def term(self, procedure):
        print("TERM")

        self.unary(procedure)
        # Can have 0 or more * / and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.SLASHD):
            if self.checkToken(TokenType.ASTERISK):
                self.currentLineText += '*'
            elif self.checkToken(TokenType.SLASH):
                self.currentLineText += '/'
            elif self.checkToken(TokenType.SLASHD):
                self.currentLineText += '//'
            self.tempOperation = self.tempOperation + self.curToken.text
            self.nextToken()
            self.unary(procedure)


    # unary ::= ["+" | "-"] primary
    def unary(self, procedure):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            if self.checkToken(TokenType.PLUS):
                self.currentLineText += '+'
            elif self.checkToken(TokenType.MINUS):
                self.currentLineText += '-'
            self.tempOperation = self.tempOperation + self.curToken.text
            self.nextToken()        
        self.module(procedure)

    #module ::= exp {("%") exp}
    def module(self, procedure):
        self.exp(procedure)
        while self.checkToken(TokenType.MODULE):
            self.currentLineText += '%'
            self.tempOperation = self.tempOperation + self.curToken.text
            print("MODULE")
            self.nextToken()
            self.exp(procedure)

    #exp ::= primary {("**") primary}
    def exp(self, procedure):
        self.primary(procedure)
        while self.checkToken(TokenType.ASTERISKD):
            self.currentLineText += '**'
            self.tempOperation = self.tempOperation + self.curToken.text
            print("EXPONENT")
            self.nextToken()
            self.primary(procedure)
         

    # primary ::= number | ident{squareBrackets} | "(" expression ")"
    def primary(self, procedure):
        print("PRIMARY ( \'" + self.curToken.text + "\' )")

        if self.checkToken(TokenType.NUMBER):
            self.currentLineText += self.curToken.text
            self.tempOperation = self.tempOperation + self.curToken.text 
            self.nextToken()

        elif self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            self.currentLineText += self.tempIdent
            if self.symbolExists(self.tempIdent, self.tempProcedure):
                if self.getSymbolType(self.tempIdent, procedure) == TokenType.NUMBER:
                    self.tempOperation = self.tempOperation + str(self.getSymbolValue(self.tempIdent))
                else:
                    self.abort("Invalid identifier in arithmetic expression: "+ self.tempIdent)
                    
                self.nextToken()
                #self.squareBrackets(self.tempIdent)
            else:
                 self.abort("Attempting to access an undeclared variable: " + self.tempIdent)

        elif self.checkToken(TokenType.ROUNDBRACKETLEFT):
            self.currentLineText += '('
            self.tempOperation = self.tempOperation + self.curToken.text
            self.nextToken()
            self.expression(procedure)
            print("PRIMARY ( \'" + self.curToken.text + "\' )")
            self.match(TokenType.ROUNDBRACKETRIGHT)
            self.currentLineText +=')'
            if self.checkToken(TokenType.ROUNDBRACKETRIGHT):
                self.tempOperation = self.tempOperation + self.curToken.text
                self.nextToken()
            else:
                self.abort("Missing ) in the expression")
            
        
        elif self.checkToken(TokenType.Len): #Len statement
            print("STATEMENT - Len")
            self.currentLineText += 'len('
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            if self.isListIdent(self.tempProcedure):
                self.currentLineText += self.curToken.text
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETRIGHT)
                self.currentLineText += ')'
            else:
                self.match(TokenType.IDENT)
            

        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)  
    
    #squareBrackets ::= "[" ( expression {":" number} | ":" "," number) "]"
    def squareBrackets(self, identifier):
        if self.checkToken(TokenType.SQRBRACKETLEFT):
            print("SQUARE BRACKETS")
            if self.getSymbolType(identifier, self.tempProcedure) == TokenType.LIST: #column: listvar[:,5]
                self.nextToken()
                if self.checkToken(TokenType.DOUBLEDOT):
                    self.match(TokenType.DOUBLEDOT)
                    self.match(TokenType.COMA)
                    
                    size = self.getSymbolValue(identifier)
                    self.inRange(size, self.tempProcedure) 
                    self.match(TokenType.SQRBRACKETRIGHT)

                elif self.checkToken(TokenType.NUMBER): #range: listvar[1:6] or simple id listvar[0]
                    tempCurrentText1 = "out_aux.modifyList(" + identifier + ', '
                    tempCurrentText2 = "out_aux.modifyElement(" + identifier + ', '
                    size = self.getSymbolValue(identifier)
                    num1 = int(self.curToken.text)
                    tempCurrentText1 += self.curToken.text + ', '
                    tempCurrentText2 += self.curToken.text + ', '
                    self.inRange(size, self.tempProcedure)
                    if self.checkToken(TokenType.DOUBLEDOT):
                        self.match(TokenType.DOUBLEDOT)
                        self.currentLineText += tempCurrentText1
                        num2 = int(self.curToken.text)
                        self.currentLineText += self.curToken.text + ', '
                        if num1 < num2:
                            self.inRange(size, self.tempProcedure)
                            self.match(TokenType.SQRBRACKETRIGHT)
                            return (num1, num2)
                        else:
                            self.abort("Invalid range")
                    else:
                        self.currentLineText += tempCurrentText2
                    self.match(TokenType.SQRBRACKETRIGHT)


                else:
                    self.abort("Invalid range") 

            else:
                self.abort("Attempting to access an element of a NON LIST identifier: " + identifier)
    
    #Checks if delimiters inside brackets are in valid range
    def inRange(self, size, procedure):
        if self.checkToken(TokenType.NUMBER):
            number = int(self.curToken.text)
            if 0 <= number <= size:
                self.match(TokenType.NUMBER)
                return True
            else:
                self.abort("Index: " + self.curToken.text +" out of range")
        else:
            self.abort("Expected NUMBER, got" + self.curToken.kind.name)
    
    #Checks if symbol already exists
    def symbolExists(self, identifier, scope):
        for symbol in self.symbols:
            if symbol[0] == identifier and (symbol[2] == scope or symbol[2] == 'Main'):
                return True
        return False
    
    #Add new variable to set
    def addSymbol(self, identifier, dataType, scope, value, rows, columns):
        newSymbol = [identifier, dataType, scope, value, rows, columns]
        self.symbols.append(newSymbol)

    #Returns data type of given identifier. If variable hasn't been declared, returns None
    def getSymbolType(self, identifier, scope):
        for symbol in self.symbols:
            if symbol[0] == identifier \
                and (symbol[2] == scope or symbol[2] == 'Main'):
                return symbol[1]
        return None
    
    def getSymbolValue(self, identifier):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                return symbol[3]
        return None
    
    def getMatrixRows(self, identifier):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                return symbol[4]
        return None
    
    def getMatrixColumns(self, identifier):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                return symbol[5]
        return None

    #Add new procedure
    def addProcedure(self, identifier, numberOfParams, paramList):
        newProcedure = [identifier] + [numberOfParams] + paramList
        self.procedures.append(newProcedure)

    #Checks if token is a valid list element: boolean
    def checkLstElmnt (self):
        if self.checkToken(TokenType.true):
            self.match(TokenType.true)
            self.currentLineText += "True"

        elif self.checkToken(TokenType.false):
            self.match(TokenType.false)
            self.currentLineText += "False"
            
        elif self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            self.currentLineText += self.tempIdent
            self.tempType = self.getSymbolType(self.tempIdent, self.tempProcedure)
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

    #Simple variable assignation
    def assignation(self, procedure):
        curSymbol = self.getSymbolType(self.tempIdent, procedure)
        if self.checkToken(TokenType.true): # = true
            if curSymbol != TokenType.BOOLEAN and curSymbol != None:
                self.abort("Attempting to assign a BOOLEAN to a " + curSymbol.name + " typed variable: " + self.tempIdent)

            self.match(TokenType.true)
            self.tempType = TokenType.BOOLEAN
            self.tempValue = True
            
            self.currentLineText += " True"
            self.emitter.emitLine(self.currentLineText)
            self.currentLineText = ""

        elif self.checkToken(TokenType.false): # = false
            if curSymbol != TokenType.BOOLEAN and curSymbol != None:
                self.abort("Attempting to assign a BOOLEAN to a " + curSymbol.name + " typed variable: " + self.tempIdent)

            self.match(TokenType.false)
            self.tempType = TokenType.BOOLEAN
            self.tempValue = False
            self.currentLineText += " False"
            self.emitter.emitLine(self.currentLineText)
            self.currentLineText = ""
        
        #Check for lists and matrixes
        elif self.checkToken(TokenType.SQRBRACKETLEFT): 

            self.currentLineText += "["
            matrixIdent = self.tempIdent
            self.nextToken()
            elementsSize = [] #To keep track of the size of the lists that are being added to the matrix
            rows = 0

            # Validation of a matrix
            if self.checkToken(TokenType.SQRBRACKETLEFT) or (self.checkToken(TokenType.IDENT) and self.isListIdent(procedure)):
                
                while not self.checkToken(TokenType.SQRBRACKETRIGHT): 
                    
                    #Checks if the element of the matrix is a new list
                    if self.checkToken(TokenType.SQRBRACKETLEFT):

                        self.currentLineText += "["
                        self.nextToken()
                        listIdent = self.tempIdent
                        self.checkLstElmnt() #first element
                        elements = 1
        
                        while not self.checkToken(TokenType.SQRBRACKETRIGHT):
                            self.match(TokenType.COMA)
                            self.currentLineText += ", "
                            self.checkLstElmnt()
                            elements = elements + 1
                        
                        self.currentLineText += "]"
                        
                        elementsSize.append(elements)
                            
                        self.match(TokenType.SQRBRACKETRIGHT)

                        if self.checkToken(TokenType.COMA):
                            rows = rows+1
                            self.currentLineText += ", "
                            self.nextToken()
                        elif self.checkToken(TokenType.SQRBRACKETRIGHT):
                            rows = rows+1
                            self.currentLineText += "]"
                            break;
                        else:
                            self.abort("Invalidad token: " + self.curToken.text)
                    
                    #Checks if the token ident is a list already declared
                    elif self.checkToken(TokenType.IDENT):
                        if self.isListIdent(procedure):
                            self.currentLineText += self.curToken
                            self.nextToken()
                        else:
                            self.abort("Trying to add an invalid element to the matrix")

                        elementsSize.append(self.getSymbolValue(self.tempIdent))

                        if self.checkToken(TokenType.COMA):
                            rows = rows + 1
                            self.currentLineText += " ,"
                            self.nextToken()
                        elif self.checkToken(TokenType.SQRBRACKETRIGHT):
                            rows = rows + 1
                            self.currentLineText += "]"
                            break;
                        else:
                            self.abort("Invalidad token: " + self.curToken.text)
                    
                    else:
                        self.abort("Invalid token: " + self.curToken.text)
     
                self.nextToken() #This should be ; at this point
                
                columns = elementsSize[0] #This is for reference

                #Checks if the list that contain the matrix are all the same size
                for i in elementsSize:
                    if i != columns:
                        self.abort("Mismatch in matrix elements sizes ")
                
                #Gives the type matrix to the current variable
                self.tempIdent = matrixIdent
                self.tempType = TokenType.MATRIX
                self.tempRows = rows
                self.tempColumns = columns

                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""

            #Validation of a list
            else:
                elements = 0;
                if curSymbol != TokenType.LIST and curSymbol != None:
                    self.abort("Attempting to assign a LIST to a " + curSymbol.name + " typed variable: " + self.tempIdent)

                listIdent = self.tempIdent
                if not self.checkToken(TokenType.SQRBRACKETRIGHT):
                    self.checkLstElmnt() #first element
                    elements = 1
                    while not self.checkToken(TokenType.SQRBRACKETRIGHT):
                        self.match(TokenType.COMA)
                        self.currentLineText += ", "
                        self.checkLstElmnt()
                        elements += 1          
                self.match(TokenType.SQRBRACKETRIGHT)
                self.currentLineText += ']'
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""

                self.tempIdent = listIdent
                self.tempType = TokenType.LIST
                self.tempValue = elements #init size of list (could be changed with insert or del built-in functions)
        
        elif self.checkToken(TokenType.List):
            listIdent = self.tempIdent
            self.nextToken()
            self.match(TokenType.ROUNDBRACKETLEFT)
            elements = 0
            if self.checkToken(TokenType.Range):
                self.nextToken()
                self.match(TokenType.ROUNDBRACKETLEFT)
                self.currentLineText += "out_aux.createList("
                self.matchNumber(procedure)
                if self.checkToken(TokenType.NUMBER):
                    elements = int(self.curToken.text)
                elif self.checkToken(TokenType.IDENT):
                    if self.getSymbolType(self.tempIdent, procedure) == TokenType.NUMBER:
                        elements = self.getSymbolValue(self.curToken.text)
                else:
                    self.abort("Invalid identifier: "+ self.curToken.text)
                
                self.nextToken()
                self.match(TokenType.COMA)
                self.currentLineText += ', '
                self.checkLstElmnt()
                self.match(TokenType.ROUNDBRACKETRIGHT)
                self.match(TokenType.ROUNDBRACKETRIGHT)
                self.currentLineText += ')'
                self.emitter.emitLine(self.currentLineText)
                self.currentLineText = ""
            else:
                self.abort("Expected the word range, got: " + self.curToken.text)

            self.tempIdent = listIdent
            self.tempType = TokenType.LIST
            self.tempValue = elements
        

        else: # aritmetic expression
            if curSymbol != TokenType.NUMBER and curSymbol != None:
                self.abort("Attempting to assign a NUMBER to a " + curSymbol.name + " typed variable: " + self.tempIdent)

            ident = self.tempIdent
            self.tempProcedure = procedure
            self.expression()
            self.emitter.emitLine(self.currentLineText)
            self.currentLineText = ""
            self.tempType = TokenType.NUMBER
            self.tempIdent = ident
            self.tempValue = None


            if self.getSymbolType(self.curToken.text, procedure) == TokenType.MATRIX:
                self.tempType = TokenType.MATRIX
                self.tempIdent = ident
                self.tempValue = None
                self.tempColumns = self.getMatrixColumns(self.curToken.text)
                self.tempRows = self.getMatrixRows(self.curToken.text)
                self.nextToken()

            elif self.getSymbolType(self.curToken.text, procedure) == TokenType.LIST:
                ident = self.curToken.text
                self.nextToken()
                if self.checkToken(TokenType.SQRBRACKETLEFT):
                    self.nextToken()
                    if self.checkToken(TokenType.NUMBER):
                        index = int(self.curToken.text)
                        if index>self.getSymbolValue(ident)-1 and index>=0:
                            self.abort("Index out of range")
                        else:
                            self.nextToken()
                        if self.checkToken(TokenType.DOUBLEDOT):
                            self.nextToken()
                            if self.checkToken(TokenType.NUMBER):
                                index2 = int(self.curToken.text)
                                if index2>=self.getSymbolValue(ident) - 1 and index2 >= index:
                                    self.nextToken()
                                    self.tempType = TokenType.LIST
                                    self.tempValue = index2 - index

                                else:
                                    print(index2)
                                    self.abort("Invalid range")
                            else:
                                self.abort("Expected a number, got: " + self.curToken.text)
                        elif self.checkToken(TokenType.SQRBRACKETRIGHT):
                            self.tempType = TokenType.NUMBER
                            self.tempIdent = ident
                            self.tempValue = None
                        self.match(TokenType.SQRBRACKETRIGHT)
            
            else:
                self.expression(procedure)
                self.tempType = TokenType.NUMBER
                self.tempIdent = ident
                self.tempValue = eval(self.tempOperation)
        
        
        if not self.symbolExists(self.tempIdent, procedure):
            print("Adding "+ self.tempIdent+ " ("+ self.tempType.name + ")")
            self.addSymbol(self.tempIdent, self.tempType, procedure, self.tempValue, self.tempRows, self.tempColumns)
            self.tempOperation = ""
    

    #Checks if token is a list identifier 
    def isListIdent(self, procedure):
        if self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            if self.symbolExists(self.tempIdent, procedure):
                if self.getSymbolType(self.tempIdent, procedure) == TokenType.LIST:
                    return True
            else:
                 self.abort("Attempting to access an undeclared variable: " + self.tempIdent)
        else:
            return False

    #Checks if token is a matrix identifier 
    def isMatrixIdent(self, procedure):
        if self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            if self.symbolExists(self.tempIdent, procedure):
                if self.getSymbolType(self.tempIdent, procedure) == TokenType.MATRIX:
                    return True
            else:
                 self.abort("Attempting to access an undeclared variable: " + self.tempIdent)
        else:
            return False

    #Checks if token matches with a NUMBER type (could be a primitive or a variable)
    def matchNumber(self, procedure):
        if self.checkToken(TokenType.NUMBER):
            self.currentLineText += self.curToken.text
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            self.currentLineText += self.tempIdent
            if self.symbolExists(self.tempIdent, procedure):
                if self.getSymbolType(self.tempIdent, procedure) == TokenType.NUMBER:
                    self.nextToken()
                else:
                    self.abort("Attempting to access an NON NUMBER type variable")
            else:
                 self.abort("Attempting to access an undeclared variable: " + self.tempIdent)
        else:
            self.match(TokenType.NUMBER)

    #Checks if index is valid for 8x8 LEDs matrix
    def matchColRow(self, procedure):
        if self.checkToken(TokenType.NUMBER):
            value = int(self.curToken.text)
            if 0 <= value <= 7:
                self.nextToken()
            else:
                self.abort("Index: " + self.curToken.text +" out of range")
        elif self.checkToken(TokenType.IDENT):
            self.tempIdent = self.curToken.text
            if self.symbolExists(self.tempIdent, procedure):
                if self.getSymbolType(self.tempIdent, procedure) == TokenType.NUMBER:
                    self.nextToken()
                else:
                    self.abort("Attempting to access an NON NUMBER type variable")
            else:
                 self.abort("Attempting to access an undeclared variable: " + self.tempIdent)
        else:
            self.match(TokenType.NUMBER)

    #Checks if the name of a variable has a valid name format
    def sintaxVar(self, tokenText):
        if len(tokenText) <= 10 and tokenText[0].islower():
            i = 1
            while i<len(tokenText):
                if tokenText[i].isalpha() or tokenText[i].isdigit() or tokenText[i] == "@" or tokenText[i] == "_" or tokenText[i] == "?":
                    i = i+1
                else:
                    return False
            return True
        else:
            return False 

    #Checks if the indexes that are trying to be accessed are within a valid list range
    def checkRange(self, listLength, index1, index2):
        if index1 >=0 and index1 < listLength and index2 >=0 and index2 < listLength and index1 <= index2:
            return True
        else:
            self.abort("Invalid range")
    
    #Checks if the index that is being tried to access is in a valid column range
    def checkRows(self, matrixRows, rowAccesed):
        if matrixRows - 1 < rowAccesed:
            self.abort("Trying to access a row out of range")
    
    #Checks if the index that is being tried to access is in a valid column range
    def checkColumns(self, matrixColumns, columnAccesed):
        if matrixColumns - 1 < columnAccesed:
            self.abort("Trying to access a column out of range")
    
    #Increases the amount of rows of a specific matrix
    def addRows(self, identifier, procedure):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                currentRows = symbol[4]
                symbol[4] = currentRows + 1 
                return True
    
    #Reduces the amount of rows of a specific matrix
    def deleteRows(self, identifier, procedure):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                currentRows = symbol[4]
                symbol[4] = currentRows - 1
                return True
    
    #Increase the amount of columns of a specific matrix
    def addColumns(self, identifier, procedure):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                currentColumns = symbol[5]
                symbol[5] = currentColumns + 1 
                return True

    #Reduces the amount of columns of a specific matrix
    def deleteColumns(self, identifier, procedure):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                currentColumns = symbol[5]
                symbol[5] = currentColumns - 1 
                return True
    
    def getAColumn(self, procedure):
        self.checkToken(TokenType.SQRBRACKETLEFT)
        self.nextToken()
        self.match(TokenType.COMA)
        if self.checkToken(TokenType.NUMBER):
            columnIndex = int(self.curToken.text)
            self.checkColumns(self.getMatrixColumns(self.tempIdent), columnIndex)
            self.nextToken()
            self.match(TokenType.SQRBRACKETRIGHT)
            return True
        else:
            self.abort("Expected a number, got: " + self.curToken.text)
    
    def getMatrixEl(self, procedure):
        self.nextToken()
        if self.checkToken(TokenType.NUMBER):
            columnIndex = int(self.curToken.text)
            self.checkColumns(self.getMatrixColumns(self.tempIdent), columnIndex) 
            self.nextToken()
            self.match(TokenType.SQRBRACKETRIGHT)
            return True
        else:
            self.abort("Expected an int, got: "+ self.curToken.text)

    def checkNeg(self, procedure):
        if self.checkToken(TokenType.DOT):
                    self.nextToken()
                    if self.curToken.text == "Neg":
                        self.nextToken()
                    else:
                        self.abort("Expected Neg, got: " + self.curToken.text)
    
    def deleteSymbol(self, identifier, procedure):
        counter = 0
        for symbol in self.symbols:
            if symbol[0] == identifier:
                del self.symbols[counter]
                return True
            else:
                counter = counter + 1
        return False


