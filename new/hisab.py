from jdcal import gcal2jd, jd2gcal
import datetime
import math

def hitungMatahari(TZ,LA,LO,H):
	now = datetime.datetime.now()
	jd2000 = gcal2jd(now.year,now.month,now.day)
	#jd2000 = gcal2jd(2004,2,24)
	mjd = jd2000[1] - 51544
	#print mjd

	L = 280.461 + 0.9856474 * mjd
	#print L
	if L>360 :
		while L > 360:
			L = L - 360
	elif L<0:
		while L < 0:
			L = L + 360
	#print L

	g = 357.528 + 0.9856003 * mjd
	if g>360 :
		while g > 360:
			g = g - 360
	elif g<0:
		while g < 0:
			g = g + 360
	#print g

	lmda = L + (1.915 *  math.sin(math.radians(g))) + (0.020 * math.sin(math.radians(2*g)))
	# print lmda

	epsilon = 23.439 - 0.0000004 * mjd
	# print epsilon

	Y = math.cos(math.radians(epsilon)) * math.sin(math.radians(lmda))
	# print Y

	# print math.cos(math.radians(335.2185823))
	X = math.cos(math.radians(lmda))
	# print X

	a = math.degrees(math.atan(Y/X))
	# print a
        if X < 0 :
                alpha = a + 180
	elif Y < 0 :
		alpha = a + 360
	else:
		alpha = a
	delta = math.degrees(math.asin(math.sin(math.radians(epsilon))*math.sin(math.radians(lmda))))
	et = (L-alpha) * 4
	# print alpha
	# print delta
	# print et 

	Z = 12 + (TZ * 15 - LO)/15.0 - et/60.0
	# print Z
	# print str(int(math.floor(Z)))+":"+str(int(math.floor((Z%1)*60)))

	# U = math.degrees((math.acos((math.sin(math.radians(-0.833-0.0347*math.sqrt(H))))-math.sin(math.radians(delta))*math.sin(math.radians(LA)))/(math.cos(math.radians(delta))*math.cos(math.radians(LA))))/15.0)
	# (arrcos((sin(-0,833-0.0347*sqrt(H))-sin(delta)*sin(LA))/(cos(delta)*cos(LA)))/15)
	# U = math.degrees((math.acos((math.sin(math.radians(-0.833-0.03347*math.sqrt(H))))
	# 	-math.sin(math.radians(delta))*math.sin(math.radians(LA)))/(math.cos(math.radians(delta))*math.cos(math.radians(LA))))/15)
	cosU = math.sin(math.radians(-0.8333-0.0347*math.sqrt(H))) - math.sin(math.radians(delta))*math.sin(math.radians(LA))/(math.cos(math.radians(delta))*math.cos(math.radians(LA)))
	hourU = math.degrees(math.acos(cosU))
	U = hourU/15
	# print U

	terbit = Z-U
	terbenam = Z+U

	return Z,U

	# print terbit
	# print terbenam
	# print str(int(math.floor(terbit)))+":"+str(int(math.floor((terbit%1)*60)))
	# print str(int(math.floor(terbenam)))+":"+str(int(math.floor((terbenam%1)*60)))
	
def terbit(TZ,LA,LO,H):
	calc = hitungMatahari(TZ,LA,LO,H)
	Z = calc[0]
	U = calc[1]
	terbit = Z-U
	return terbit;

def terbenam(TZ,LA,LO,H):
	calc = hitungMatahari(TZ,LA,LO,H)
	Z = calc[0]
	U = calc[1]
	terbenam = Z+U
	return terbenam

def siang(TZ,LA,LO,H):
	calc = hitungMatahari(TZ,LA,LO,H)
	Z = calc[0]
	return Z
