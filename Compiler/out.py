import out_aux

trueList = out_aux.createList(8, True)

falseList = out_aux.createList(8, False)

row = 0

while True:
    if row < 8:
        row += 1
    else:
        row = 0
    out_aux.printLedX("R", row, trueList)
    if row == 0:
        out_aux.printLedX("R", 7, falseList)
    else:
        out_aux.printLedX("R", row-1, falseList)
    out_aux.delay(1, "Sec")
