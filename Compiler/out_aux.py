## Built in functions ##

# used in list(range(amount_of_elements, value))
def createList(amountElements, value):
    result = []
    i = 0
    while i< amountElements:
        result += [value]
        i+=1
    return result

