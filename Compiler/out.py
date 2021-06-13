import out_aux

matrix1 = [[True, True, True, True, True, True, True, True],
[True, True, True, True, True, True, True, False],
[True, True, True, True, True, True, False, False],
[True, True, True, True, True, False, False, False],
[True, True, True, True, False, False, False, False],
[True, True, True, False, False, False, False, False],
[True, True, False, False, False, False, False, False],
[True, False, False, False, False, False, False, False]]

matrix2 = [[True, True, True, True, True, True, True, True],
	[False, True, True, True, True, True, True, True],
	[False, False, True, True, True, True, True, True],
	[False, False, False, True, True, True, True, True],
	[False, False, False, False, True, True, True, True],
	[False, False, False, False, False, True, True, True],
	[False, False, False, False, False, False, True, True],
	[False, False, False, False, False, False, False, True]]

matrix3 = [[False, False, False, False, False, False, False, True],
	[False, False, False, False, False, False, True, True],
	[False, False, False, False, False, True, True, True],
	[False, False, False, False, True, True, True, True],
	[False, False, False, True, True, True, True, True],
	[False, False, True, True, True, True, True, True],
	[False, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True]]

matrix4 = [[True, False, False, False, False, False, False, False],
	[True, True, False, False, False, False, False, False],
	[True, True, True, False, False, False, False, False],
	[True, True, True, True, False, False, False, False],
	[True, True, True, True, True, False, False, False],
	[True, True, True, True, True, True, False, False],
	[True, True, True, True, True, True, True, False],
	[True, True, True, True, True, True, True, True]]

recoverList = [True, True, True, True, True, True, True, True]

for elem in recoverList:
    out_aux.printLedX("M", 0, matrix1)
    out_aux.delay(1, "Sec")
    out_aux.printLedX("M", 0, matrix2)
    out_aux.delay(1, "Sec")
    out_aux.printLedX("M", 0, matrix3)
    out_aux.delay(1, "Sec")
    out_aux.printLedX("M", 0, matrix4)
    out_aux.delay(1, "Sec")
