import out_aux
blank=[[False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False]]
def M_Letter():
	m0=[[False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True]]
	m1=[[False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True]]
	m2=[[False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, True], [False, False, False, False, False, True, True, True], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, False]]
	m3=[[False, False, False, False, True, True, False, False], [False, False, False, False, True, True, True, False], [False, False, False, False, True, True, True, True], [False, False, False, False, True, True, False, True], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False]]
	m4=[[False, False, False, True, True, False, False, False], [False, False, False, True, True, True, False, False], [False, False, False, True, True, True, True, True], [False, False, False, True, True, False, True, True], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False]]
	m5=[[False, False, True, True, False, False, False, False], [False, False, True, True, True, False, False, True], [False, False, True, True, True, True, True, True], [False, False, True, True, False, True, True, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False]]
	m6=[[False, True, True, False, False, False, False, True], [False, True, True, True, False, False, True, True], [False, True, True, True, True, True, True, True], [False, True, True, False, True, True, False, True], [False, True, True, False, False, False, False, True], [False, True, True, False, False, False, False, True], [False, True, True, False, False, False, False, True], [False, True, True, False, False, False, False, True]]
	m7=[[True, True, False, False, False, False, True, True], [True, True, True, False, False, True, True, True], [True, True, True, True, True, True, True, True], [True, True, False, True, True, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True], [True, True, False, False, False, False, True, True]]
	m8=[[True, False, False, False, False, True, True, False], [True, True, False, False, True, True, True, False], [True, True, True, True, True, True, True, False], [True, False, True, True, False, True, True, False], [True, False, False, False, False, True, True, False], [True, False, False, False, False, True, True, False], [True, False, False, False, False, True, True, False], [True, False, False, False, False, True, True, False]]
	m9=[[False, False, False, False, True, True, False, False], [True, False, False, True, True, True, False, False], [True, True, True, True, True, True, False, False], [False, True, True, False, True, True, False, False], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False]]
	m10=[[False, False, False, True, True, False, False, False], [False, False, True, True, True, False, False, False], [True, True, True, True, True, False, False, False], [True, True, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False]]
	m11=[[False, False, True, True, False, False, False, False], [False, True, True, True, False, False, False, False], [True, True, True, True, False, False, False, False], [True, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False]]
	m12=[[False, True, True, False, False, False, False, False], [True, True, True, False, False, False, False, False], [True, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False]]
	m13=[[True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False]]
	m14=[[True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False]]
	out_aux.printLedX("M", 0, "M", blank)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m0)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m1)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m2)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m3)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m4)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m5)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m6)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m7)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m8)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m9)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m10)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m11)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m12)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m13)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", m14)
	out_aux.delay(1, "Seg")
	out_aux.printLedX("M", 0, "M", blank)
	out_aux.delay(1, "Seg")
