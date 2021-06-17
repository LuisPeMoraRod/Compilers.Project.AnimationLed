import aled_api
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
	aled_api.printLedX("M", 0, "M", blank)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m0)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m1)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m2)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m3)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m4)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m5)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m6)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m7)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m8)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m9)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m10)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m11)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m12)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m13)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", m14)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", blank)
	aled_api.delay(1, "Seg")
def R_Letter():
	r0=[[False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True], [False, False, False, False, False, False, False, True]]
	r1=[[False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True], [False, False, False, False, False, False, True, True]]
	r2=[[False, False, False, False, False, True, True, True], [False, False, False, False, False, True, True, True], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, True], [False, False, False, False, False, True, True, True], [False, False, False, False, False, True, True, False], [False, False, False, False, False, True, True, False]]
	r3=[[False, False, False, False, True, True, True, True], [False, False, False, False, True, True, True, True], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, True, True], [False, False, False, False, True, True, True, True], [False, False, False, False, True, True, False, False], [False, False, False, False, True, True, False, False]]
	r4=[[False, False, False, True, True, True, True, True], [False, False, False, True, True, True, True, True], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, True, True, True], [False, False, False, True, True, True, True, True], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False]]
	r5=[[False, False, True, True, True, True, True, True], [False, False, True, True, True, True, True, True], [False, False, True, True, False, False, False, True], [False, False, True, True, False, False, False, True], [False, False, True, True, True, True, True, True], [False, False, True, True, True, True, True, True], [False, False, True, True, False, False, False, True], [False, False, True, True, False, False, False, False]]
	r6=[[False, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True], [False, True, True, False, False, False, True, True], [False, True, True, False, False, False, True, True], [False, True, True, True, True, True, True, False], [False, True, True, True, True, True, True, False], [False, True, True, False, False, False, True, True], [False, True, True, False, False, False, False, True]]
	r7=[[True, True, True, True, True, True, True, False], [True, True, True, True, True, True, True, False], [True, True, False, False, False, True, True, False], [True, True, False, False, False, True, True, False], [True, True, True, True, True, True, False, False], [True, True, True, True, True, True, False, False], [True, True, False, False, False, True, True, False], [True, True, False, False, False, False, True, True]]
	r8=[[True, True, True, True, True, True, False, False], [True, True, True, True, True, True, False, False], [True, False, False, False, True, True, False, False], [True, False, False, False, True, True, False, False], [True, True, True, True, True, False, False, False], [True, True, True, True, True, False, False, False], [True, False, False, False, True, True, False, False], [True, False, False, False, False, True, True, False]]
	r9=[[True, True, True, True, True, False, False, False], [True, True, True, True, True, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, True, True, False, False, False], [True, True, True, True, False, False, False, False], [True, True, True, True, False, False, False, False], [False, False, False, True, True, False, False, False], [False, False, False, False, True, True, False, False]]
	r10=[[True, True, True, True, False, False, False, False], [True, True, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, True, True, False, False, False, False], [True, True, True, False, False, False, False, False], [True, True, True, False, False, False, False, False], [False, False, True, True, False, False, False, False], [False, False, False, True, True, False, False, False]]
	r11=[[True, True, True, False, False, False, False, False], [True, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, True, True, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, False, True, True, False, False, False, False]]
	r12=[[True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [False, True, True, False, False, False, False, False]]
	r13=[[True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False], [True, True, False, False, False, False, False, False]]
	r14=[[False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False]]
	aled_api.printLedX("M", 0, "M", blank)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r0)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r1)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r2)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r3)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r4)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r5)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r6)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r7)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r8)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r9)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r10)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r11)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r12)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r13)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", r14)
	aled_api.delay(1, "Seg")
	aled_api.printLedX("M", 0, "M", blank)
	aled_api.delay(1, "Seg")

M_Letter()
R_Letter()
