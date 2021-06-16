import time
import threading

import serial

serialcom = serial.Serial('COM5', 9600)
serialcom.timeout = 1


#####################################
# Led control variables and functions
#####################################

ledMatrix = [[False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False]]

isBlinkingMatrix = [[False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False]]

ledDecimalList = [0, 0, 0, 0, 0, 0, 0, 0]

def getBinaryList():
    binaryList = []
    row = 0
    while row < len(ledMatrix):
        binaryString = ""
        column = 0
        while column < len(ledMatrix[0]):
            if ledMatrix[row][column]:
                binaryString += "1"
            else:
                binaryString += "0"
            column += 1
        binaryList.append(binaryString)
        row += 1
    return binaryList

# Function that updates the decimal list based on the ledMatrix
def updateDecimalList():
    # Led matrix is transformed intro its equivalent list of binary number
    # The the binary number is passed into a decimal number that represents a row
    binaryList = getBinaryList()
    count = 0
    while count < len(binaryList):
        decimalNumber = int(binaryList[count], 2)
        ledDecimalList[count] = decimalNumber
        count += 1


def sendLedInstructions():
    # Sends the ledDecimelList to the Arduino
    message = str(ledDecimalList)
    serialcom.write(message.encode())

    time.sleep(1.25)


#############################
## LIST Built in functions ##
#############################

# used in list(range(amount_of_elements, value))
def createList(amountElements, value):
    result = []
    i = 0
    while i< amountElements:
        result += [value]
        i+=1
    return result

# used in listVar[1:3] = [true, false]
# listVar -> variable
# 1 -> firstIndex
# 3 -> lastIndex
# [true, false] -> valueList
def modifyList(variable, firstIndex, lastIndex, valueList):
    i = firstIndex
    j = 0
    while i < lastIndex:
        variable[i] = valueList[j]
        j+=1
        i+=1

# used in listVar[3] = true
# listVar -> variable
# 3 -> index
# true -> value
# if value is a number then it has to apply the Neg function
def modifyElement(variable, index, value):
    if isinstance(value, int):
        if variable[index] == True:
            variable[index] = False
        elif variable[index] == False:
            variable[index] = True
    elif value == True:
        variable[index] = True
    elif value == False:
        variable[index] = False

###############################
## MATRIX Built in functions ##
###############################

# Changes the boolean values of a matrix row
# used for matrix[row].Neg
# inputs: matrix -> matrix to modify
#         row -> row of the matrix to modify
def modifyMatrixRow(matrix, row):
    # Change the boolean values of the given row
    column = 0
    while column < len(matrix[row]):
        if matrix[row][column]:
            matrix[row][column] = False
        else:
            matrix[row][column] = True
        column += 1

# Changes the boolean values of a matrix element
# used for matrix[row, column].Neg
# inputs: matrix -> matrix to modify
#         row -> row of the element to modify
#         column -> column of the element to modify
def modifyMatrixElem(matrix, row, column):
    # Change the boolean value of the given element
    if matrix[row][column]:
            matrix[row][column] = False
    else:
        matrix[row][column] = True

# Changes the boolean values of a matrix column
# used for matrix[:,column].Neg
# inputs: matrix -> matrix to modify
#         column -> column of the element to modify
def modifyMatrixColumn(matrix, column):
    # Change the boolean values of the given column
    row = 0
    while row < len(matrix):
        if matrix[row][column]:
            matrix[row][column] = False
        else:
            matrix[row][column] = True
        row += 1

# Modify the boolean value of the entire matrix
def modifyMatrix(matrix):
    row = 0
    while row < len(matrix):
        column = 0
        while column < len(matrix):
            if matrix[row][column]:
                matrix[row][column] = False
            else:
                matrix[row][column] = True
            column += 1
        row += 1

# Inserts row at the end of the matrix
# used for matrix.insert(row, 0)
# inputs: matrix -> matrix to modify
#         row -> row to insert
def insertMatrixRow(matrix, row):
    # Inserts a row into the matrix at the end of it (as last row)
    matrix.append(row)

# Inserts row at a specific position of the matrix
# used for matrix.insert(row, 0, pos)
# inputs: matrix -> matrix to modify
#         row -> row to insert
#         pos -> position of insertion
def insertMatrixRowAtPos(matrix, row, pos):
    # Inserts a row into a matrix at the position given
    matrix.insert(pos, row)


# Inserts column at the end of the matrix
# used for matrix.insert(column, 1)
# inputs: matrix -> matrix to modify
#         column -> column to insert
def insertMatrixColumn(matrix, column):
    # Inserts a column into the matrix at the end of it (as last column)
    count = 0
    row = 0
    while row < len(matrix):
        matrix[row].append(column[count])
        row += 1
        count += 1

# Inserts column at a specific position of the matrix
# used for matrix.insert(column, 1, pos)
# inputs: matrix -> matrix to modify
#         column -> column to insert
#         pos -> position of insertion
def insertMatrixColumnAtPos(matrix, column, pos):
    # Inserts a column into a matrix at the position given
    count = 0
    row = 0
    while row < len(matrix):
        matrix[row].insert(pos, column[count])
        count += 1
        row += 1

# Deletes the indicated row of the given matrix
# used for matrix.delete(rowNumber, 0)
def deleteMatrixRow(matrix, pos):
    # Deletes the indicated row of the given matrix
    matrix.pop(pos)

# Deletes the indicated column of the given matrix 
# used for matrix.delete(columnNumber, 1)
def deleteMatrixColumn(matrix, pos):
    # Deletes the indicated column of the given matrix
    row = 0
    while row < len(matrix):
        matrix[row].pop(pos)
        row += 1


######################################
## PrintLed and PrintLedX functions ##
######################################

# changes the value of a given position in ledMatrix
def printLed(column, row, value):
    # Changes the ledMatrix[row][column] into valule
    # Then calls the updateDecimalList to update the list
    # Last, it calls the sendLedIntruction with the decimal list
    ledMatrix[row][column] = value
    updateDecimalList()
    
    if value:
        sendLedInstructions()

# changes the value of a given row, column or matrix elements in ledMatrix
# inputs:
# ObjectType: specifies if the object to changes is a row ("R"), column ("C") or the matrix ("M")
# pos: in case of row or column it changes the position given
# array: the array with the new values to change
def printLedX(objectType, pos, array):
    if objectType == "R": # Row case
        limit = min(8, len(array))
        j = 0
        while j < 8:
            if j < limit:
                ledMatrix[pos][j] = array[j]
            else: # False of the given array is longer than 8 elements
                ledMatrix[pos][j] = False
            j += 1
    elif objectType == "C":
        limit = min(8, len(array))
        i = 0
        while i < 8:
            if i < limit:
                ledMatrix[i][pos] = array[i]
            else: # False of the given array is longer than 8 elements
                ledMatrix[i][pos] = False
            i += 1
    else:
        limitRow = min(8, len(array))
        limitColumn = min(8, len(array[0]))
        i = 0
        while i < 8:
            j = 0
            while j < 8:
                if i < limitRow and j < limitColumn:
                    ledMatrix[i][j] = array[i][j]
                else: # False of the given array is longer than 8 elements
                    ledMatrix[i][j] = False
                j += 1
            i += 1
    updateDecimalList()
    print(str(ledDecimalList))
    sendLedInstructions()
        
    #time.sleep(3)

###############################
## Blink and Delay functions ##
###############################

# this function makes one led of the ledMatrix blink with a given frequency
# until it receives a false state for the same led
# inputs:
# row and column indicate the position of the led
# delay determines the amount of time between bliks
# timeRange indicates the units of the time range it could be in 
# seconds ("Sec"), miliseconds ("Mil") or minute ("Min")
def blinkLed(row, column, delay, timeRange, state):
    # This has to be done in a different thread
    # Change the ledMatrix with the given time
    if state:
        threading.Thread(target=blinkLed_aux, args=(row, column, delay, timeRange)).start
    else:
        isBlinkingMatrix[row][column] = False

# blink led auxiliar function to keep everything out of the main thread
def blinkLed_aux(row, column, delay, timeRange):
    factor = 1 # In case of seconds
    if timeRange == "Min":
        factor *= 60
    elif timeRange == "Mil":
        factor /= 1000
    while isBlinkingMatrix[row][column]: # blink until the matrix element becomes false
        if ledMatrix[row][column]:
            printLed(row, column, False)
            ledMatrix[row][column] = False
        else:
            printLed(row, column, True)
            ledMatrix[row][column] = True
        time.sleep(delay*factor)


# this function makes a delay between every instructions, it doesn't need a thread
# it has to stop the entire program.
# inputs:
# time -> amount of time of the delay
# unit -> units of the emount of time, it could be seconds ("Sec"), miliseconds ("Mil") or minute ("Min")
def delay(amount, unit):
    factor = 1 # in case time is in seconds
    if unit == "Min":
        factor *= 60
    elif unit == "Mil":
        factor /= 1000
    time.sleep(amount*factor)


print(ledMatrix)
modifyMatrix(ledMatrix)
print(ledMatrix)

'''
matrix = ledMatrix
#print(matrix)

#modifyMatrixRow(matrix, 2)
#print(matrix)

#modifyMatrixElem(matrix, 4, 5)
#print(matrix)

#modifyMatrixColumn(matrix, 4)
#print(matrix)

#insertMatrixRow(matrix, [True, True, True, True, True, True, True, True])
#print(matrix)

#insertMatrixColumn(matrix, [True, True, True, True, True, True, True, True])
#print(matrix)

#insertMatrixRowAtPos(matrix, [True, True, True, True, True, True, True, True], 0)
#print(matrix)

#insertMatrixColumnAtPos(matrix, [True, True, True, True, True, True, True, True], 1)
#print(matrix)

#deleteMatrixRow(matrix, 2)
#print(matrix)

#deleteMatrixColumn(matrix, 0)
#print(matrix)

#print(ledMatrix)

#printLed(1, 1, True)
#print(ledMatrix)
#print(ledDecimalList)

printLedX("R", 1, [True, False, True, True, True, True, True, True])
print(ledMatrix)
print(ledDecimalList)

printLedX("C", 1, [True, False, True, True, True, True, True, True])
print(ledMatrix)
print(ledDecimalList)

printLedX("M", 1, [[False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, True, False, False, False, False, False, False]])
print(ledMatrix)
print(ledDecimalList)
'''