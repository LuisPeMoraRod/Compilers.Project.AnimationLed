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
     pass

# Changes the boolean values of a matrix element
# used for matrix[row, column].Neg
# inputs: matrix -> matrix to modify
#         row -> row of the element to modify
#         column -> column of the element to modify
def modifyMatrixElem(matrix, row, column):
    # Change the boolean value of the given element
    pass

# Changes the boolean values of a matrix column
# used for matrix[:,column].Neg
# inputs: matrix -> matrix to modify
#         column -> column of the element to modify
def modifyMatrixColumn(matrix, column):
    # Change the boolean values of the given column
    pass

# Inserts row at the end of the matrix
# used for matrix.insert(row, 0)
# inputs: matrix -> matrix to modify
#         row -> row to insert
def insertMatrixRow(matrix, row):
    # Inserts a row into the matrix at the end of it (as last row)
    pass

# Inserts row at a specific position of the matrix
# used for matrix.insert(row, 0, pos)
# inputs: matrix -> matrix to modify
#         row -> row to insert
#         pos -> position of insertion
def insertMatrixRowAtPos(matrix, row, pos):
    # Inserts a row into a matrix at the position given
    pass


# Inserts column at the end of the matrix
# used for matrix.insert(column, 1)
# inputs: matrix -> matrix to modify
#         column -> column to insert
def insertMatrixColumn(matrix, column):
    # Inserts a column into the matrix at the end of it (as last column)
    pass

# Inserts column at a specific position of the matrix
# used for matrix.insert(column, 1, pos)
# inputs: matrix -> matrix to modify
#         column -> column to insert
#         pos -> position of insertion
def insertMatrixColumnAtPos(matrix, column, pos):
    # Inserts a column into a matrix at the position given
    pass

def deleteMatrixRow(matrix, pos):
    pass

def deleteMatrixColumn(matrix, pos):
    pass


list = [True, True, True]
print(list)
modifyElement(list, 2, False)
print(list)

list.insert(2, 3)
print(list)

list.remove(1)
print(list)
