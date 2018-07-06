def calculate(soil,rain,temp,hum,forecast):
	global pump
	global status
	pump = 'OFF'
	# START FUZZIFIKASI
	# inisialisasi linguistik
	#soil
	basah 	= 0;
	sedang	= 0;
	kering	= 0;

	#rain
	hujan 	  = 0;
	tdk_hujan = 0;

	#temp
	dingin	= 0;
	sejuk	= 0;
	panas	= 0;

	#hum
	lembab	= 0;
	normal	= 0;
	kekeringan = 0;
	
	#openweather
	f_cerah	  = 0;
	f_mendung = 0;
	f_hujan   = 0;

#inisialisasi batas
	#soil
	l_kering = 0;
	u_kering = 50;
	l_sedang = 200;
	u_sedang = 350;
	l_basah	 = 500;
	u_basah  = 1024;

	#rain
	l_tdkhujan = 0;
	u_tdkhujan = 200;
	l_hujan	 = 400;
	u_hujan	 = 1024;

	#temp
	l_dingin = 0;
	u_dingin = 19;
	l_sejuk = 22;
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
	#soil
	if soil < u_kering:
		kering = 1;
	elif soil >= u_kering and soil <= l_sedang:
		kering = (soil * (-1.0) + l_sedang) / (l_sedang - u_kering);
		sedang = (soil - u_kering) * 1.0 / (l_sedang - u_kering);
	elif soil >= l_sedang and soil < u_sedang:
		sedang = 1;
	elif soil >= u_sedang and soil <= l_basah:
		sedang = (soil * (-1.0) + l_basah) / (l_basah - u_sedang);
		basah = (soil - u_sedang) * 1.0 / (l_basah - u_sedang);
	elif soil >= l_basah:
		basah = 1;

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

	#rain
	if rain < u_tdkhujan:
		tdk_hujan = 1;
	elif rain >= u_tdkhujan and rain <= l_hujan:
		tdk_hujan = (rain * (-1.0) + l_hujan) / (l_hujan - u_tdkhujan);
		hujan  = (rain - u_tdkhujan) * 1.0 / (l_hujan - u_tdkhujan);
	elif rain > l_hujan:
		hujan = 1;

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

#openweather	
	if forecast == 0:
		f_cerah 	= 1;
	elif forecast == 1:
		f_mendung 	= 1;
	elif forecast == 2:
		f_hujan 	= 1;

#print linguistik
	print("======================")
	print("FUZZYFIKASI");
	print("======================")
	print("-SOIL = %d-" % (soil));
	print("BASAH  : "+str(basah));
	print("SEDANG : "+str(sedang));
	print("KERING : "+str(kering));

	print("-RAIN = %d-" % (rain));
	print("HUJAN  	 : "+str(hujan));
	print("TDK_HUJAN : "+str(tdk_hujan));

	print("-TEMP = %d " % (temp)+"C-");
	print("DINGIN  : "+str(dingin));
	print("SEJUK : "+str(sejuk));
	print("PANAS : "+str(panas));

	print("-HUM = %d-" % (hum));
	print("LEMBAB : "+str(lembab));
	print("NORMAL : "+str(normal));
	print("KEKERINGAN : "+str(kekeringan));

	print("-openweather-");
	print("CERAH  : "+str(f_cerah));
	print("MENDUNG: "+str(f_mendung));
	print("HUJAN  : "+str(f_hujan));

#Inferensi
	nkRendah=[];
	nkTinggi=[];
	rendah=0;
	tinggi=0;

	for i in range(162):
		nkRendah.append(0);
		nkTinggi.append(0);

#kering
	if kering and panas and kekeringan and hujan and f_cerah:
		nkTinggi[0]=min(kering,panas,kekeringan,hujan,f_cerah)
	if kering and panas and kekeringan and hujan and f_mendung:
		nkTinggi[1]=min(kering,panas,kekeringan,hujan,f_mendung)
	if kering and panas and kekeringan and hujan and f_hujan:
		nkTinggi[2]=min(kering,panas,kekeringan,hujan,f_hujan)
	if kering and panas and kekeringan and tdk_hujan and f_cerah:
		nkTinggi[3]=min(kering,panas,kekeringan,tdk_hujan,f_cerah)
	if kering and panas and kekeringan and tdk_hujan and f_mendung:
		nkTinggi[4]=min(kering,panas,kekeringan,tdk_hujan,f_mendung)
	if kering and panas and kekeringan and tdk_hujan and f_hujan:
		nkTinggi[5]=min(kering,panas,kekeringan,tdk_hujan,f_hujan)     
	if kering and panas and normal and hujan and f_cerah:
		nkTinggi[6]=min(kering,panas,normal,hujan,f_cerah)
	if kering and panas and normal and hujan and f_mendung:
		nkTinggi[7]=min(kering,panas,normal,hujan,f_mendung)
	if kering and panas and normal and hujan and f_hujan:
		nkTinggi[8]=min(kering,panas,normal,hujan,f_hujan)
	if kering and panas and normal and tdk_hujan and f_cerah:
		nkTinggi[9]=min(kering,panas,normal,tdk_hujan,f_cerah)
	if kering and panas and normal and tdk_hujan and f_mendung:
		nkTinggi[10]=min(kering,panas,normal,tdk_hujan,f_mendung)
	if kering and panas and normal and tdk_hujan and f_hujan:
		nkTinggi[11]=min(kering,panas,normal,tdk_hujan,f_hujan)
	if kering and panas and lembab and hujan and f_cerah:
		nkTinggi[12]=min(kering,panas,lembab,hujan,f_cerah)
	if kering and panas and lembab and hujan and f_mendung:
		nkTinggi[13]=min(kering,panas,lembab,hujan,f_mendung)
	if kering and panas and lembab and hujan and f_hujan:
		nkTinggi[14]=min(kering,panas,lembab,hujan,f_hujan)
	if kering and panas and lembab and tdk_hujan and f_cerah:
		nkTinggi[15]=min(kering,panas,lembab,tdk_hujan,f_cerah)
	if kering and panas and lembab and tdk_hujan and f_mendung:
		nkTinggi[16]=min(kering,panas,lembab,tdk_hujan,f_mendung)
	if kering and panas and lembab and tdk_hujan and f_hujan:
		nkTinggi[17]=min(kering,panas,lembab,tdk_hujan,f_hujan)

	if kering and sejuk and kekeringan and hujan and f_cerah:
		nkTinggi[18]=min(kering,sejuk,kekeringan,hujan,f_cerah)
	if kering and sejuk and kekeringan and hujan and f_mendung:
		nkTinggi[19]=min(kering,sejuk,kekeringan,hujan,f_mendung)
	if kering and sejuk and kekeringan and hujan and f_hujan:
		nkTinggi[20]=min(kering,sejuk,kekeringan,hujan,f_hujan)
	if kering and sejuk and kekeringan and tdk_hujan and f_cerah:
		nkTinggi[21]=min(kering,sejuk,kekeringan,tdk_hujan,f_cerah)
	if kering and sejuk and kekeringan and tdk_hujan and f_mendung:
		nkTinggi[22]=min(kering,sejuk,kekeringan,tdk_hujan,f_mendung)
	if kering and sejuk and kekeringan and tdk_hujan and f_hujan:
		nkTinggi[23]=min(kering,sejuk,kekeringan,tdk_hujan,f_hujan)     
	if kering and sejuk and normal and hujan and f_cerah:
		nkTinggi[24]=min(kering,sejuk,normal,hujan,f_cerah)
	if kering and sejuk and normal and hujan and f_mendung:
		nkTinggi[25]=min(kering,sejuk,normal,hujan,f_mendung)
	if kering and sejuk and normal and hujan and f_hujan:
		nkTinggi[26]=min(kering,sejuk,normal,hujan,f_hujan)
	if kering and sejuk and normal and tdk_hujan and f_cerah:
		nkTinggi[27]=min(kering,sejuk,normal,tdk_hujan,f_cerah)
	if kering and sejuk and normal and tdk_hujan and f_mendung:
		nkTinggi[28]=min(kering,sejuk,normal,tdk_hujan,f_mendung)
	if kering and sejuk and normal and tdk_hujan and f_hujan:
		nkTinggi[29]=min(kering,sejuk,normal,tdk_hujan,f_hujan)
	if kering and sejuk and lembab and hujan and f_cerah:
		nkTinggi[30]=min(kering,sejuk,lembab,hujan,f_cerah)
	if kering and sejuk and lembab and hujan and f_mendung:
		nkTinggi[31]=min(kering,sejuk,lembab,hujan,f_mendung)
	if kering and sejuk and lembab and hujan and f_hujan:
		nkTinggi[32]=min(kering,sejuk,lembab,hujan,f_hujan)
	if kering and sejuk and lembab and tdk_hujan and f_cerah:
		nkTinggi[33]=min(kering,sejuk,lembab,tdk_hujan,f_cerah)
	if kering and sejuk and lembab and tdk_hujan and f_mendung:
		nkTinggi[34]=min(kering,sejuk,lembab,tdk_hujan,f_mendung)
	if kering and sejuk and lembab and tdk_hujan and f_hujan:
		nkTinggi[35]=min(kering,sejuk,lembab,tdk_hujan,f_hujan)

	if kering and dingin and kekeringan and hujan and f_cerah:
		nkTinggi[36]=min(kering,dingin,kekeringan,hujan,f_cerah)
	if kering and dingin and kekeringan and hujan and f_mendung:
		nkTinggi[37]=min(kering,dingin,kekeringan,hujan,f_mendung)
	if kering and dingin and kekeringan and hujan and f_hujan:
		nkTinggi[38]=min(kering,dingin,kekeringan,hujan,f_hujan)
	if kering and dingin and kekeringan and tdk_hujan and f_cerah:
		nkTinggi[39]=min(kering,dingin,kekeringan,tdk_hujan,f_cerah)
	if kering and dingin and kekeringan and tdk_hujan and f_mendung:
		nkTinggi[40]=min(kering,dingin,kekeringan,tdk_hujan,f_mendung)
	if kering and dingin and kekeringan and tdk_hujan and f_hujan:
		nkTinggi[41]=min(kering,dingin,kekeringan,tdk_hujan,f_hujan)     
	if kering and dingin and normal and hujan and f_cerah:
		nkTinggi[42]=min(kering,dingin,normal,hujan,f_cerah)
	if kering and dingin and normal and hujan and f_mendung:
		nkTinggi[43]=min(kering,dingin,normal,hujan,f_mendung)
	if kering and dingin and normal and hujan and f_hujan:
		nkTinggi[44]=min(kering,dingin,normal,hujan,f_hujan)
	if kering and dingin and normal and tdk_hujan and f_cerah:
		nkTinggi[45]=min(kering,dingin,normal,tdk_hujan,f_cerah)
	if kering and dingin and normal and tdk_hujan and f_mendung:
		nkTinggi[46]=min(kering,dingin,normal,tdk_hujan,f_mendung)
	if kering and dingin and normal and tdk_hujan and f_hujan:
		nkTinggi[47]=min(kering,dingin,normal,tdk_hujan,f_hujan)
	if kering and dingin and lembab and hujan and f_cerah:
		nkRendah[48]=min(kering,dingin,lembab,hujan,f_cerah)
	if kering and dingin and lembab and hujan and f_mendung:
		nkRendah[49]=min(kering,dingin,lembab,hujan,f_mendung)
	if kering and dingin and lembab and hujan and f_hujan:
		nkRendah[50]=min(kering,dingin,lembab,hujan,f_hujan)
	if kering and dingin and lembab and tdk_hujan and f_cerah:
		nkTinggi[51]=min(kering,dingin,lembab,tdk_hujan,f_cerah)
	if kering and dingin and lembab and tdk_hujan and f_mendung:
		nkTinggi[52]=min(kering,dingin,lembab,tdk_hujan,f_mendung)
	if kering and dingin and lembab and tdk_hujan and f_hujan:
		nkTinggi[53]=min(kering,dingin,lembab,tdk_hujan,f_hujan)
#sedang
	if sedang and panas and kekeringan and hujan and f_cerah:
		nkTinggi[54]=min(sedang,panas,kekeringan,hujan,f_cerah)
	if sedang and panas and kekeringan and hujan and f_mendung:
		nkTinggi[55]=min(sedang,panas,kekeringan,hujan,f_mendung)
	if sedang and panas and kekeringan and hujan and f_hujan:
		nkTinggi[56]=min(sedang,panas,kekeringan,hujan,f_hujan)
	if sedang and panas and kekeringan and tdk_hujan and f_cerah:
		nkTinggi[57]=min(sedang,panas,kekeringan,tdk_hujan,f_cerah)
	if sedang and panas and kekeringan and tdk_hujan and f_mendung:
		nkTinggi[58]=min(sedang,panas,kekeringan,tdk_hujan,f_mendung)
	if sedang and panas and kekeringan and tdk_hujan and f_hujan:
		nkTinggi[59]=min(sedang,panas,kekeringan,tdk_hujan,f_hujan)     
	if sedang and panas and normal and hujan and f_cerah:
		nkTinggi[60]=min(sedang,panas,normal,hujan,f_cerah)
	if sedang and panas and normal and hujan and f_mendung:
		nkTinggi[61]=min(sedang,panas,normal,hujan,f_mendung)
	if sedang and panas and normal and hujan and f_hujan:
		nkTinggi[62]=min(sedang,panas,normal,hujan,f_hujan)
	if sedang and panas and normal and tdk_hujan and f_cerah:
		nkTinggi[63]=min(sedang,panas,normal,tdk_hujan,f_cerah)
	if sedang and panas and normal and tdk_hujan and f_mendung:
		nkTinggi[64]=min(sedang,panas,normal,tdk_hujan,f_mendung)
	if sedang and panas and normal and tdk_hujan and f_hujan:
		nkTinggi[65]=min(sedang,panas,normal,tdk_hujan,f_hujan)
	if sedang and panas and lembab and hujan and f_cerah:
		nkTinggi[66]=min(sedang,panas,lembab,hujan,f_cerah)
	if sedang and panas and lembab and hujan and f_mendung:
		nkTinggi[67]=min(sedang,panas,lembab,hujan,f_mendung)
	if sedang and panas and lembab and hujan and f_hujan:
		nkTinggi[68]=min(sedang,panas,lembab,hujan,f_hujan)
	if sedang and panas and lembab and tdk_hujan and f_cerah:
		nkTinggi[69]=min(sedang,panas,lembab,tdk_hujan,f_cerah)
	if sedang and panas and lembab and tdk_hujan and f_mendung:
		nkTinggi[70]=min(sedang,panas,lembab,tdk_hujan,f_mendung)
	if sedang and panas and lembab and tdk_hujan and f_hujan:
		nkTinggi[71]=min(sedang,panas,lembab,tdk_hujan,f_hujan)

	if sedang and sejuk and kekeringan and hujan and f_cerah:
		nkRendah[72]=min(sedang,sejuk,kekeringan,hujan,f_cerah)
	if sedang and sejuk and kekeringan and hujan and f_mendung:
		nkRendah[73]=min(sedang,sejuk,kekeringan,hujan,f_mendung)
	if sedang and sejuk and kekeringan and hujan and f_hujan:
		nkRendah[74]=min(sedang,sejuk,kekeringan,hujan,f_hujan)
	if sedang and sejuk and kekeringan and tdk_hujan and f_cerah:
		nkTinggi[75]=min(sedang,sejuk,kekeringan,tdk_hujan,f_cerah)
	if sedang and sejuk and kekeringan and tdk_hujan and f_mendung:
		nkTinggi[76]=min(sedang,sejuk,kekeringan,tdk_hujan,f_mendung)
	if sedang and sejuk and kekeringan and tdk_hujan and f_hujan:
		nkTinggi[77]=min(sedang,sejuk,kekeringan,tdk_hujan,f_hujan)     
	if sedang and sejuk and normal and hujan and f_cerah:
		nkRendah[78]=min(sedang,sejuk,normal,hujan,f_cerah)
	if sedang and sejuk and normal and hujan and f_mendung:
		nkRendah[79]=min(sedang,sejuk,normal,hujan,f_mendung)
	if sedang and sejuk and normal and hujan and f_hujan:
		nkRendah[80]=min(sedang,sejuk,normal,hujan,f_hujan)
	if sedang and sejuk and normal and tdk_hujan and f_cerah:
		nkRendah[81]=min(sedang,sejuk,normal,tdk_hujan,f_cerah)
	if sedang and sejuk and normal and tdk_hujan and f_mendung:
		nkRendah[82]=min(sedang,sejuk,normal,tdk_hujan,f_mendung)
	if sedang and sejuk and normal and tdk_hujan and f_hujan:
		nkRendah[83]=min(sedang,sejuk,normal,tdk_hujan,f_hujan)
	if sedang and sejuk and lembab and hujan and f_cerah:
		nkRendah[84]=min(sedang,sejuk,lembab,hujan,f_cerah)
	if sedang and sejuk and lembab and hujan and f_mendung:
		nkRendah[85]=min(sedang,sejuk,lembab,hujan,f_mendung)
	if sedang and sejuk and lembab and hujan and f_hujan:
		nkRendah[86]=min(sedang,sejuk,lembab,hujan,f_hujan)
	if sedang and sejuk and lembab and tdk_hujan and f_cerah:
		nkRendah[87]=min(sedang,sejuk,lembab,tdk_hujan,f_cerah)
	if sedang and sejuk and lembab and tdk_hujan and f_mendung:
		nkRendah[88]=min(sedang,sejuk,lembab,tdk_hujan,f_mendung)
	if sedang and sejuk and lembab and tdk_hujan and f_hujan:
		nkRendah[89]=min(sedang,sejuk,lembab,tdk_hujan,f_hujan)

	if sedang and dingin and kekeringan and hujan and f_cerah:
		nkRendah[90]=min(sedang,dingin,kekeringan,hujan,f_cerah)
	if sedang and dingin and kekeringan and hujan and f_mendung:
		nkRendah[91]=min(sedang,dingin,kekeringan,hujan,f_mendung)
	if sedang and dingin and kekeringan and hujan and f_hujan:
		nkRendah[92]=min(sedang,dingin,kekeringan,hujan,f_hujan)
	if sedang and dingin and kekeringan and tdk_hujan and f_cerah:
		nkRendah[93]=min(sedang,dingin,kekeringan,tdk_hujan,f_cerah)
	if sedang and dingin and kekeringan and tdk_hujan and f_mendung:
		nkRendah[94]=min(sedang,dingin,kekeringan,tdk_hujan,f_mendung)
	if sedang and dingin and kekeringan and tdk_hujan and f_hujan:
		nkRendah[95]=min(sedang,dingin,kekeringan,tdk_hujan,f_hujan)     
	if sedang and dingin and normal and hujan and f_cerah:
		nkRendah[96]=min(sedang,dingin,normal,hujan,f_cerah)
	if sedang and dingin and normal and hujan and f_mendung:
		nkRendah[97]=min(sedang,dingin,normal,hujan,f_mendung)
	if sedang and dingin and normal and hujan and f_hujan:
		nkRendah[98]=min(sedang,dingin,normal,hujan,f_hujan)
	if sedang and dingin and normal and tdk_hujan and f_cerah:
		nkRendah[99]=min(sedang,dingin,normal,tdk_hujan,f_cerah)
	if sedang and dingin and normal and tdk_hujan and f_mendung:
		nkRendah[100]=min(sedang,dingin,normal,tdk_hujan,f_mendung)
	if sedang and dingin and normal and tdk_hujan and f_hujan:
		nkRendah[101]=min(sedang,dingin,normal,tdk_hujan,f_hujan)
	if sedang and dingin and lembab and hujan and f_cerah:
		nkRendah[102]=min(sedang,dingin,lembab,hujan,f_cerah)
	if sedang and dingin and lembab and hujan and f_mendung:
		nkRendah[103]=min(sedang,dingin,lembab,hujan,f_mendung)
	if sedang and dingin and lembab and hujan and f_hujan:
		nkRendah[104]=min(sedang,dingin,lembab,hujan,f_hujan)
	if sedang and dingin and lembab and tdk_hujan and f_cerah:
		nkRendah[105]=min(sedang,dingin,lembab,tdk_hujan,f_cerah)
	if sedang and dingin and lembab and tdk_hujan and f_mendung:
		nkRendah[106]=min(sedang,dingin,lembab,tdk_hujan,f_mendung)
	if sedang and dingin and lembab and tdk_hujan and f_hujan:
		nkRendah[107]=min(sedang,dingin,lembab,tdk_hujan,f_hujan)
#basah
	if basah and panas and kekeringan and hujan and f_cerah:
		nkRendah[108]=min(basah,panas,kekeringan,hujan,f_cerah)
	if basah and panas and kekeringan and hujan and f_mendung:
		nkRendah[109]=min(basah,panas,kekeringan,hujan,f_mendung)
	if basah and panas and kekeringan and hujan and f_hujan:
		nkRendah[110]=min(basah,panas,kekeringan,hujan,f_hujan)
	if basah and panas and kekeringan and tdk_hujan and f_cerah:
		nkRendah[111]=min(basah,panas,kekeringan,tdk_hujan,f_cerah)
	if basah and panas and kekeringan and tdk_hujan and f_mendung:
		nkRendah[112]=min(basah,panas,kekeringan,tdk_hujan,f_mendung)
	if basah and panas and kekeringan and tdk_hujan and f_hujan:
		nkRendah[113]=min(basah,panas,kekeringan,tdk_hujan,f_hujan)     
	if basah and panas and normal and hujan and f_cerah:
		nkRendah[114]=min(basah,panas,normal,hujan,f_cerah)
	if basah and panas and normal and hujan and f_mendung:
		nkRendah[115]=min(basah,panas,normal,hujan,f_mendung)
	if basah and panas and normal and hujan and f_hujan:
		nkRendah[116]=min(basah,panas,normal,hujan,f_hujan)
	if basah and panas and normal and tdk_hujan and f_cerah:
		nkRendah[117]=min(basah,panas,normal,tdk_hujan,f_cerah)
	if basah and panas and normal and tdk_hujan and f_mendung:
		nkRendah[118]=min(basah,panas,normal,tdk_hujan,f_mendung)
	if basah and panas and normal and tdk_hujan and f_hujan:
		nkRendah[119]=min(basah,panas,normal,tdk_hujan,f_hujan)
	if basah and panas and lembab and hujan and f_cerah:
		nkRendah[120]=min(basah,panas,lembab,hujan,f_cerah)
	if basah and panas and lembab and hujan and f_mendung:
		nkRendah[121]=min(basah,panas,lembab,hujan,f_mendung)
	if basah and panas and lembab and hujan and f_hujan:
		nkRendah[122]=min(basah,panas,lembab,hujan,f_hujan)
	if basah and panas and lembab and tdk_hujan and f_cerah:
		nkRendah[123]=min(basah,panas,lembab,tdk_hujan,f_cerah)
	if basah and panas and lembab and tdk_hujan and f_mendung:
		nkRendah[124]=min(basah,panas,lembab,tdk_hujan,f_mendung)
	if basah and panas and lembab and tdk_hujan and f_hujan:
		nkRendah[125]=min(basah,panas,lembab,tdk_hujan,f_hujan)

	if basah and sejuk and kekeringan and hujan and f_cerah:
		nkRendah[126]=min(basah,sejuk,kekeringan,hujan,f_cerah)
	if basah and sejuk and kekeringan and hujan and f_mendung:
		nkRendah[127]=min(basah,sejuk,kekeringan,hujan,f_mendung)
	if basah and sejuk and kekeringan and hujan and f_hujan:
		nkRendah[128]=min(basah,sejuk,kekeringan,hujan,f_hujan)
	if basah and sejuk and kekeringan and tdk_hujan and f_cerah:
		nkRendah[129]=min(basah,sejuk,kekeringan,tdk_hujan,f_cerah)
	if basah and sejuk and kekeringan and tdk_hujan and f_mendung:
		nkRendah[130]=min(basah,sejuk,kekeringan,tdk_hujan,f_mendung)
	if basah and sejuk and kekeringan and tdk_hujan and f_hujan:
		nkRendah[131]=min(basah,sejuk,kekeringan,tdk_hujan,f_hujan)     
	if basah and sejuk and normal and hujan and f_cerah:
		nkRendah[132]=min(basah,sejuk,normal,hujan,f_cerah)
	if basah and sejuk and normal and hujan and f_mendung:
		nkRendah[133]=min(basah,sejuk,normal,hujan,f_mendung)
	if basah and sejuk and normal and hujan and f_hujan:
		nkRendah[134]=min(basah,sejuk,normal,hujan,f_hujan)
	if basah and sejuk and normal and tdk_hujan and f_cerah:
		nkRendah[135]=min(basah,sejuk,normal,tdk_hujan,f_cerah)
	if basah and sejuk and normal and tdk_hujan and f_mendung:
		nkRendah[136]=min(basah,sejuk,normal,tdk_hujan,f_mendung)
	if basah and sejuk and normal and tdk_hujan and f_hujan:
		nkRendah[137]=min(basah,sejuk,normal,tdk_hujan,f_hujan)
	if basah and sejuk and lembab and hujan and f_cerah:
		nkRendah[138]=min(basah,sejuk,lembab,hujan,f_cerah)
	if basah and sejuk and lembab and hujan and f_mendung:
		nkRendah[139]=min(basah,sejuk,lembab,hujan,f_mendung)
	if basah and sejuk and lembab and hujan and f_hujan:
		nkRendah[140]=min(basah,sejuk,lembab,hujan,f_hujan)
	if basah and sejuk and lembab and tdk_hujan and f_cerah:
		nkRendah[141]=min(basah,sejuk,lembab,tdk_hujan,f_cerah)
	if basah and sejuk and lembab and tdk_hujan and f_mendung:
		nkRendah[142]=min(basah,sejuk,lembab,tdk_hujan,f_mendung)
	if basah and sejuk and lembab and tdk_hujan and f_hujan:
		nkRendah[143]=min(basah,sejuk,lembab,tdk_hujan,f_hujan)

	if basah and dingin and kekeringan and hujan and f_cerah:
		nkRendah[144]=min(basah,dingin,kekeringan,hujan,f_cerah)
	if basah and dingin and kekeringan and hujan and f_mendung:
		nkRendah[145]=min(basah,dingin,kekeringan,hujan,f_mendung)
	if basah and dingin and kekeringan and hujan and f_hujan:
		nkRendah[146]=min(basah,dingin,kekeringan,hujan,f_hujan)
	if basah and dingin and kekeringan and tdk_hujan and f_cerah:
		nkRendah[147]=min(basah,dingin,kekeringan,tdk_hujan,f_cerah)
	if basah and dingin and kekeringan and tdk_hujan and f_mendung:
		nkRendah[148]=min(basah,dingin,kekeringan,tdk_hujan,f_mendung)
	if basah and dingin and kekeringan and tdk_hujan and f_hujan:
		nkRendah[149]=min(basah,dingin,kekeringan,tdk_hujan,f_hujan)     
	if basah and dingin and normal and hujan and f_cerah:
		nkRendah[150]=min(basah,dingin,normal,hujan,f_cerah)
	if basah and dingin and normal and hujan and f_mendung:
		nkRendah[151]=min(basah,dingin,normal,hujan,f_mendung)
	if basah and dingin and normal and hujan and f_hujan:
		nkRendah[152]=min(basah,dingin,normal,hujan,f_hujan)
	if basah and dingin and normal and tdk_hujan and f_cerah:
		nkRendah[153]=min(basah,dingin,normal,tdk_hujan,f_cerah)
	if basah and dingin and normal and tdk_hujan and f_mendung:
		nkRendah[154]=min(basah,dingin,normal,tdk_hujan,f_mendung)
	if basah and dingin and normal and tdk_hujan and f_hujan:
		nkRendah[155]=min(basah,dingin,normal,tdk_hujan,f_hujan)
	if basah and dingin and lembab and hujan and f_cerah:
		nkRendah[156]=min(basah,dingin,lembab,hujan,f_cerah)
	if basah and dingin and lembab and hujan and f_mendung:
		nkRendah[157]=min(basah,dingin,lembab,hujan,f_mendung)
	if basah and dingin and lembab and hujan and f_hujan:
		nkRendah[158]=min(basah,dingin,lembab,hujan,f_hujan)
	if basah and dingin and lembab and tdk_hujan and f_cerah:
		nkRendah[159]=min(basah,dingin,lembab,tdk_hujan,f_cerah)
	if basah and dingin and lembab and tdk_hujan and f_mendung:
		nkRendah[160]=min(basah,dingin,lembab,tdk_hujan,f_mendung)
	if basah and dingin and lembab and tdk_hujan and f_hujan:
		nkRendah[161]=min(basah,dingin,lembab,tdk_hujan,f_hujan)
	
	print("======================")
	print("FUZZY OUTPUT");
	print("======================")
	for i in range(162):
		if nkRendah[i]>0:
			print("Rule "+str(i+1)+ " Rendah : "+str(nkRendah[i]));
			if nkRendah[i]>rendah:
				rendah=nkRendah[i];
		if nkTinggi[i]>0:
			print("Rule "+str(i+1)+ " Tinggi : "+str(nkTinggi[i]));
			if nkTinggi[i]>tinggi:
				tinggi=nkTinggi[i];

	if rendah>0:
		print("Rendah("+str(rendah)+")");
	if tinggi>0:
		print("Tinggi("+str(tinggi)+")");

	#DEFUZIFIKASI
	#batas
	print("======================")
	print("DEFUZZYFIKASI");
	print("======================")
	b_rendah = 50;
	b_tinggi = 80;
	m1 = 0;
	m2 = 0;
	count = 0;
	y=[];
	i = 0;
	mamdani_pembilang = 0;
	mamdani_penyebut = 0;
	status = 0;
	while count<100:
		count += 5;
		val = 0;
		if count<=b_rendah:
			val = rendah;
		elif count>=b_tinggi:
			val = tinggi;
		elif count > b_rendah and count < b_tinggi:
			m1 = (b_tinggi - (count*1.0)) / (b_tinggi - b_rendah);
			m2 = ((count*1.0) - b_rendah) / (b_tinggi - b_rendah);
			
			if(count<=(b_rendah+b_tinggi)/2):
				if m1>rendah:
					m1 = rendah;
				val = max(m1,m2);

			elif count>=(b_rendah+b_tinggi)/2:
				if m2>tinggi:
					m2 = tinggi;
				val = max(m1,m2);

		y.append(val);
		mamdani_pembilang = mamdani_pembilang + (count*val);
		mamdani_penyebut  = mamdani_penyebut + val;
		print(str(count) + ":" + str(y[i]));
		i += 1;
	status = mamdani_pembilang/mamdani_penyebut;
	#print ("Nilai Kelayakan : " +str(status))
	return status;