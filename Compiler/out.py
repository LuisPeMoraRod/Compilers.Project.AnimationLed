import aled_api
mat=[[False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
def M_Letter():
	newColumn=[[True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True], [False, True, True, False, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, True, True, False, False, False, False, False], [True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
	i1 = 0
	for column in newColumn:
		aled_api.printLedX("M", 0, mat)
		aled_api.delay(0.7, "Seg")
		aled_api.deleteMatrixColumn(mat,0)
		aled_api.insertMatrixColumn(mat,column)
def A_Letter():
	newColumn=[[False, False, True, True, True, True, True, True], [False, True, True, True, True, True, True, True], [True, True, False, False, True, True, False, False], [True, True, False, False, True, True, False, False], [True, True, False, False, True, True, False, False], [True, True, False, False, True, True, False, False], [False, True, True, True, True, True, True, True], [False, False, True, True, True, True, True, True], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
	i2 = 0
	for column in newColumn:
		aled_api.printLedX("M", 0, mat)
		aled_api.delay(0.7, "Seg")
		aled_api.deleteMatrixColumn(mat,0)
		aled_api.insertMatrixColumn(mat,column)
def R_Letter():
	newColumn=[[True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True], [True, True, False, False, True, True, False, False], [True, True, False, False, True, True, False, False], [True, True, False, False, True, True, False, False], [True, True, True, True, True, True, True, False], [True, True, True, True, False, False, True, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
	i3 = 0
	for column in newColumn:
		aled_api.printLedX("M", 0, mat)
		aled_api.delay(0.7, "Seg")
		aled_api.deleteMatrixColumn(mat,0)
		aled_api.insertMatrixColumn(mat,column)
def C_Letter():
	newColumn=[[False, False, False, False, False, False, False, False], [False, False, True, True, True, True, False, False], [False, True, True, True, True, True, True, False], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
	i4 = 0
	for column in newColumn:
		aled_api.printLedX("M", 0, mat)
		aled_api.delay(0.7, "Seg")
		aled_api.deleteMatrixColumn(mat,0)
		aled_api.insertMatrixColumn(mat,column)
def O_Letter():
	newColumn=[[False, False, True, True, True, True, False, False], [False, True, True, True, True, True, True, False], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [False, True, True, True, True, True, True, False], [False, False, True, True, True, True, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
	i5 = 0
	for column in newColumn:
		aled_api.printLedX("M", 0, mat)
		aled_api.delay(0.7, "Seg")
		aled_api.deleteMatrixColumn(mat,0)
		aled_api.insertMatrixColumn(mat,column)
M_Letter()
A_Letter()
R_Letter()
C_Letter()
O_Letter()
