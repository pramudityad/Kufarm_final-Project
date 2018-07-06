import time, datetime

def adv_decision(temp,hum,):
# inisialisasi linguistik

#timeslot
	waktu = 0

	#tempe
	dingin	= 0;
	sejuk	= 0;
	panas	= 0;

	#hum
	lembab	= 0;
	normal	= 0;
	kekeringan = 0;

#inisialisasi batas
	#temp
	l_dingin = 0;
	u_dingin = 19;
	l_sejuk = 21;
	u_sejuk = 28;
	l_panas = 30;
	u_panas = 50;

	#hum
	l_kekeringan = 0;
	u_kekeringan = 30;
	l_normal = 32;
	u_normal = 40;
	l_lembab = 55;
	u_lembab = 80;

# hitung linguistik
	#temp
	if temp < u_dingin:
		dingin = 1;
	elif temp >= u_dingin and temp <= l_sejuk:
		dingin = (temp * (-1.0) + l_sejuk) / (l_sejuk - u_dingin);
		sejuk = (temp - u_dingin) * 1.0 / (l_sejuk - u_dingin);
	elif temp >= l_sejuk and temp < u_sejuk:
		sejuk = 1;
	elif temp >= u_sejuk and temp <= l_panas:
		sejuk = (temp * (-1.0) + l_panas) / (l_panas - u_sejuk);
		panas = (temp - u_sejuk) * 1.0 / (l_panas - u_sejuk);
	elif temp >= l_panas:
		panas = 1;

	#hum
	if hum < u_kekeringan:
		kekeringan = 1;
	elif hum >= u_kekeringan and hum <= l_normal:
		kekeringan = (hum * (-1.0) + l_normal) / (l_normal - u_kekeringan);
		normal = (hum - u_kekeringan) * 1.0 / (l_normal - u_kekeringan);
	elif hum >= l_normal and hum < u_normal:
		normal = 1;
	elif hum >= u_normal and hum <= l_lembab:
		normal = (hum * (-1.0) + l_lembab) / (l_lembab - u_normal);
		lembab = (hum - u_normal) * 1.0 / (l_lembab - u_normal);
	elif hum >= l_lembab:
		lembab = 1;
	
#print linguistik
	print("-TEMP = %d " % (temp)+"C-");
	print("DINGIN  : "+str(dingin));
	print("SEJUK : "+str(sejuk));
	print("PANAS : "+str(panas));

	print("-HUM = %d-" % (hum));
	print("LEMBAB : "+str(lembab));
	print("NORMAL : "+str(normal));
	print("KEKERINGAN : "+str(kekeringan));

	if panas and kekeringan:
		waktu = 2
	if panas and normal:
		waktu = 3
	if panas and lembab:
		waktu = 4
	if sejuk and kekeringan:
		waktu = 5
	if sejuk and normal:
		waktu = 6
	if sejuk and lembab:
		waktu = 7
	if dingin and kekeringan:
		waktu = 8
	if dingin and normal:
		waktu = 9
	if dingin and lembab:
		waktu = 10
	print ("Slot Time : " +str(waktu))
	return waktu


