## Built in functions ##

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

'''
list = [True, True, True]
print(list)
modifyElement(list, 2, False)
print(list)
'''
