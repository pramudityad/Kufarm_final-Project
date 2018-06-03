def calculate(soil,rain,temp,hum,forecast,forecast2):
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
	
	#openweather
	f_cerah	  = 0;
	f_mendung = 0;
	f_hujan   = 0;

	#wundergound
	f2_cerah  = 0;
	f2_mendung= 0;
	f2_hujan  = 0;

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
	l_sejuk = 21;
	u_sejuk = 28;
	l_panas = 30;
	u_panas = 50;

	#hum
	l_lembab = 0;
	u_lembab = 39;
	l_normal = 40;
	u_normal = 80;

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
	elif temp >= u_sejuk and temp <= l_basah:
		sejuk = (temp * (-1.0) + l_basah) / (l_basah - u_sejuk);
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
	if hum < u_lembab:
		lembab = 1;
	elif hum >= u_lembab and hum <= l_normal:
		lembab = (hum * (-1.0) + l_normal) / (l_normal - u_lembab);
		normal  = (hum - u_lembab) * 1.0 / (l_normal - u_lembab);
	elif hum > l_normal:
		normal = 1;

	#openweather	
	if forecast == 0:
		f_cerah 	= 1;
	elif forecast == 1:
		f_mendung 	= 1;
	elif forecast == 2:
		f_hujan 	= 1;
	
	#wundergound
	if forecast2 == 0:
		f2_cerah 	= 1;
	elif forecast2 == 1:
		f2_mendung 	= 1;
	elif forecast2 == 2:
		f2_hujan 	= 1;
	
	#print linguistik
	print("======================")
	print("FUZZYFIKASI");
	print("======================")
	print("-SOIL = %d-" % (soil));
	print("BASAH  : "+str(basah));
	print("SEDANG : "+str(sedang));
	print("KERING : "+str(kering));

	print("-RAIN-");
	print("HUJAN  	 : "+str(hujan));
	print("TDK_HUJAN : "+str(tdk_hujan));

	print("-TEMP = %d " % (temp)+"C-");
	print("DINGIN  : "+str(basah));
	print("SEJUK : "+str(sedang));
	print("PANAS : "+str(kering));

	print("-HUM = %d-" % (hum));
	print("LEMBAB  	 : "+str(lembab));
	print("NORMAL : "+str(normal));

	print("-openweather-");
	print("CERAH  : "+str(f_cerah));
	print("MENDUNG: "+str(f_mendung));
	print("HUJAN  : "+str(f_hujan));

	print("-wundergound-");
	print("CERAH  : "+str(f2_cerah));
	print("MENDUNG: "+str(f2_mendung));
	print("HUJAN  : "+str(f2_hujan));


	#Inferensi
	nkRendah=[];
	nkTinggi=[];
	rendah=0;
	tinggi=0;

	for i in range(324):
 		nkRendah.append(0);
 		nkTinggi.append(0);

	if kering and tdk_hujan and panas and normal and f_cerah and f2_cerah:
	 		nkTinggi[0]=min(kering,tdk_hujan,panas,normal,f_cerah,f2_cerah)
	if kering and tdk_hujan and panas and normal and f_cerah and f2_mendung:
	 		nkTinggi[1]=min(kering,tdk_hujan,panas,normal,f_cerah,f2_mendung)
	if kering and tdk_hujan and panas and normal and f_cerah and f2_hujan:
	 		nkTinggi[2]=min(kering,tdk_hujan,panas,normal,f_cerah,f2_hujan)
	if kering and tdk_hujan and panas and normal and f_mendung and f2_cerah:
	 		nkTinggi[3]=min(kering,tdk_hujan,panas,normal,f_mendung,f2_cerah)
	if kering and tdk_hujan and panas and normal and f_mendung and f2_mendung:
	 		nkTinggi[4]=min(kering,tdk_hujan,panas,normal,f_mendung,f2_mendung)
	if kering and tdk_hujan and panas and normal and f_mendung and f2_hujan:
	 		nkTinggi[5]=min(kering,tdk_hujan,panas,normal,f_mendung,f2_hujan)
	if kering and tdk_hujan and panas and normal and f_hujan and f2_cerah:
	 		nkTinggi[6]=min(kering,tdk_hujan,panas,normal,f_hujan,f2_cerah)
	if kering and tdk_hujan and panas and normal and f_hujan and f2_mendung:
	 		nkTinggi[7]=min(kering,tdk_hujan,panas,normal,f_hujan,f2_mendung)
	if kering and tdk_hujan and panas and normal and f_hujan and f2_hujan:
	 		nkTinggi[8]=min(kering,tdk_hujan,panas,normal,f_hujan,f2_hujan)
	if kering and tdk_hujan and panas and lembab and f_cerah and f2_cerah:
	 		nkTinggi[9]=min(kering,tdk_hujan,panas,lembab,f_cerah,f2_cerah) 		
	if kering and tdk_hujan and panas and lembab and f_cerah and f2_mendung:
	 		nkTinggi[10]=min(kering,tdk_hujan,panas,lembab,f_cerah,f2_mendung)
	if kering and tdk_hujan and panas and lembab and f_cerah and f2_hujan:
	 		nkTinggi[11]=min(kering,tdk_hujan,panas,lembab,f_cerah,f2_hujan)
	if kering and tdk_hujan and panas and lembab and f_mendung and f2_cerah:
	 		nkTinggi[12]=min(kering,tdk_hujan,panas,lembab,f_mendung,f2_cerah)
	if kering and tdk_hujan and panas and lembab and f_mendung and f2_mendung:
	 		nkTinggi[13]=min(kering,tdk_hujan,panas,lembab,f_mendung,f2_mendung)
	if kering and tdk_hujan and panas and lembab and f_mendung and f2_hujan:
	 		nkTinggi[14]=min(kering,tdk_hujan,panas,lembab,f_mendung,f2_hujan)
	if kering and tdk_hujan and panas and lembab and f_hujan and f2_cerah:
	 		nkTinggi[15]=min(kering,tdk_hujan,panas,lembab,f_hujan,f2_cerah)
	if kering and tdk_hujan and panas and lembab and f_hujan and f2_mendung:
	 		nkTinggi[16]=min(kering,tdk_hujan,panas,lembab,f_hujan,f2_mendung)
	if kering and tdk_hujan and panas and lembab and f_hujan and f2_hujan:
	 		nkTinggi[17]=min(kering,tdk_hujan,panas,lembab,f_hujan,f2_hujan)
	if kering and tdk_hujan and sejuk and normal and f_cerah and f2_cerah:
	 		nkTinggi[18]=min(kering,tdk_hujan,sejuk,normal,f_cerah,f2_cerah)
	if kering and tdk_hujan and sejuk and normal and f_cerah and f2_mendung:
	 		nkTinggi[19]=min(kering,tdk_hujan,sejuk,normal,f_cerah,f2_mendung)
	if kering and tdk_hujan and sejuk and normal and f_cerah and f2_hujan:
	 		nkTinggi[20]=min(kering,tdk_hujan,sejuk,normal,f_cerah,f2_hujan)
	if kering and tdk_hujan and sejuk and normal and f_mendung and f2_cerah:
	 		nkTinggi[21]=min(kering,tdk_hujan,sejuk,normal,f_mendung,f2_cerah)
	if kering and tdk_hujan and sejuk and normal and f_mendung and f2_mendung:
	 		nkTinggi[22]=min(kering,tdk_hujan,sejuk,normal,f_mendung,f2_mendung)
	if kering and tdk_hujan and sejuk and normal and f_mendung and f2_hujan:
	 		nkTinggi[23]=min(kering,tdk_hujan,sejuk,normal,f_mendung,f2_hujan)
	if kering and tdk_hujan and sejuk and normal and f_hujan and f2_cerah:
	 		nkTinggi[24]=min(kering,tdk_hujan,sejuk,normal,f_hujan,f2_cerah)
	if kering and tdk_hujan and sejuk and normal and f_hujan and f2_mendung:
	 		nkTinggi[25]=min(kering,tdk_hujan,sejuk,normal,f_hujan,f2_mendung)
	if kering and tdk_hujan and sejuk and normal and f_hujan and f2_hujan:
	 		nkTinggi[26]=min(kering,tdk_hujan,sejuk,normal,f_hujan,f2_hujan)
	if kering and tdk_hujan and sejuk and lembab and f_cerah and f2_cerah:
	 		nkTinggi[27]=min(kering,tdk_hujan,sejuk,lembab,f_cerah,f2_cerah)
	if kering and tdk_hujan and sejuk and lembab and f_cerah and f2_mendung:
	 		nkTinggi[28]=min(kering,tdk_hujan,sejuk,lembab,f_cerah,f2_mendung)
	if kering and tdk_hujan and sejuk and lembab and f_cerah and f2_hujan:
	 		nkTinggi[29]=min(kering,tdk_hujan,sejuk,lembab,f_cerah,f2_hujan) 		
	if kering and tdk_hujan and sejuk and lembab and f_mendung and f2_cerah:
	 		nkTinggi[30]=min(kering,tdk_hujan,sejuk,lembab,f_mendung,f2_cerah)
	if kering and tdk_hujan and sejuk and lembab and f_mendung and f2_mendung:
	 		nkTinggi[31]=min(kering,tdk_hujan,sejuk,lembab,f_mendung,f2_mendung)
	if kering and tdk_hujan and sejuk and lembab and f_mendung and f2_hujan:
	 		nkTinggi[32]=min(kering,tdk_hujan,sejuk,lembab,f_mendung,f2_hujan)
	if kering and tdk_hujan and sejuk and lembab and f_hujan and f2_cerah:
	 		nkTinggi[33]=min(kering,tdk_hujan,sejuk,lembab,f_hujan,f2_cerah)
	if kering and tdk_hujan and sejuk and lembab and f_hujan and f2_mendung:
	 		nkTinggi[34]=min(kering,tdk_hujan,sejuk,lembab,f_hujan,f2_mendung)
	if kering and tdk_hujan and sejuk and lembab and f_hujan and f2_hujan:
	 		nkTinggi[35]=min(kering,tdk_hujan,sejuk,lembab,f_hujan,f2_hujan)
	if kering and tdk_hujan and dingin and normal and f_cerah and f2_cerah:
	 		nkTinggi[36]=min(kering,tdk_hujan,dingin,normal,f_cerah,f2_cerah)
	if kering and tdk_hujan and dingin and normal and f_cerah and f2_mendung:
	 		nkTinggi[37]=min(kering,tdk_hujan,dingin,normal,f_cerah,f2_mendung)
	if kering and tdk_hujan and dingin and normal and f_cerah and f2_hujan:
	 		nkTinggi[38]=min(kering,tdk_hujan,dingin,normal,f_cerah,f2_hujan)
	if kering and tdk_hujan and dingin and normal and f_mendung and f2_cerah:
	 		nkTinggi[39]=min(kering,tdk_hujan,dingin,normal,f_mendung,f2_cerah)
	if kering and tdk_hujan and dingin and normal and f_mendung and f2_mendung:
	 		nkTinggi[40]=min(kering,tdk_hujan,dingin,normal,f_mendung,f2_mendung)
	if kering and tdk_hujan and dingin and normal and f_mendung and f2_hujan:
	 		nkTinggi[41]=min(kering,tdk_hujan,dingin,normal,f_mendung,f2_hujan)
	if kering and tdk_hujan and dingin and normal and f_hujan and f2_cerah:
	 		nkTinggi[42]=min(kering,tdk_hujan,dingin,normal,f_hujan,f2_cerah)
	if kering and tdk_hujan and dingin and normal and f_hujan and f2_mendung:
	 		nkTinggi[43]=min(kering,tdk_hujan,dingin,normal,f_hujan,f2_mendung)
	if kering and tdk_hujan and dingin and normal and f_hujan and f2_hujan:
	 		nkTinggi[44]=min(kering,tdk_hujan,dingin,normal,f_hujan,f2_hujan)
	if kering and tdk_hujan and dingin and lembab and f_cerah and f2_cerah:
	 		nkTinggi[45]=min(kering,tdk_hujan,dingin,lembab,f_cerah,f2_cerah)
	if kering and tdk_hujan and dingin and lembab and f_cerah and f2_mendung:
	 		nkTinggi[46]=min(kering,tdk_hujan,dingin,lembab,f_cerah,f2_mendung)
	if kering and tdk_hujan and dingin and lembab and f_cerah and f2_hujan:
	 		nkTinggi[47]=min(kering,tdk_hujan,dingin,lembab,f_cerah,f2_hujan)
	if kering and tdk_hujan and dingin and lembab and f_mendung and f2_cerah:
	 		nkTinggi[48]=min(kering,tdk_hujan,dingin,lembab,f_mendung,f2_cerah)
	if kering and tdk_hujan and dingin and lembab and f_mendung and f2_mendung:
	 		nkTinggi[49]=min(kering,tdk_hujan,dingin,lembab,f_mendung,f2_mendung) 		
	if kering and tdk_hujan and dingin and lembab and f_mendung and f2_hujan:
	 		nkTinggi[50]=min(kering,tdk_hujan,dingin,lembab,f_mendung,f2_hujan)
	if kering and tdk_hujan and dingin and lembab and f_hujan and f2_cerah:
	 		nkTinggi[51]=min(kering,tdk_hujan,dingin,lembab,f_hujan,f2_cerah)
	if kering and tdk_hujan and dingin and lembab and f_hujan and f2_mendung:
	 		nkTinggi[52]=min(kering,tdk_hujan,dingin,lembab,f_hujan,f2_mendung)
	if kering and tdk_hujan and dingin and lembab and f_hujan and f2_hujan:
	 		nkTinggi[53]=min(kering,tdk_hujan,dingin,lembab,f_hujan,f2_hujan)

	if kering and hujan and panas and normal and f_cerah and f2_cerah:
	 		nkTinggi[54]=min(kering,hujan,panas,normal,f_cerah,f2_cerah)
	if kering and hujan and panas and normal and f_cerah and f2_mendung:
	 		nkTinggi[55]=min(kering,hujan,panas,normal,f_cerah,f2_mendung)
	if kering and hujan and panas and normal and f_cerah and f2_hujan:
	 		nkTinggi[56]=min(kering,hujan,panas,normal,f_cerah,f2_hujan)
	if kering and hujan and panas and normal and f_mendung and f2_cerah:
	 		nkTinggi[57]=min(kering,hujan,panas,normal,f_mendung,f2_cerah)
	if kering and hujan and panas and normal and f_mendung and f2_mendung:
	 		nkTinggi[58]=min(kering,hujan,panas,normal,f_mendung,f2_mendung)
	if kering and hujan and panas and normal and f_mendung and f2_hujan:
	 		nkTinggi[59]=min(kering,hujan,panas,normal,f_mendung,f2_hujan)
	if kering and hujan and panas and normal and f_hujan and f2_cerah:
	 		nkTinggi[60]=min(kering,hujan,panas,normal,f_hujan,f2_cerah)
	if kering and hujan and panas and normal and f_hujan and f2_mendung:
	 		nkTinggi[61]=min(kering,hujan,panas,normal,f_hujan,f2_mendung)
	if kering and hujan and panas and normal and f_hujan and f2_hujan:
	 		nkTinggi[62]=min(kering,hujan,panas,normal,f_hujan,f2_hujan)
	if kering and hujan and panas and lembab and f_cerah and f2_cerah:
	 		nkTinggi[63]=min(kering,hujan,panas,lembab,f_cerah,f2_cerah) 		
	if kering and hujan and panas and lembab and f_cerah and f2_mendung:
	 		nkTinggi[64]=min(kering,hujan,panas,lembab,f_cerah,f2_mendung)
	if kering and hujan and panas and lembab and f_cerah and f2_hujan:
	 		nkTinggi[65]=min(kering,hujan,panas,lembab,f_cerah,f2_hujan)
	if kering and hujan and panas and lembab and f_mendung and f2_cerah:
	 		nkTinggi[66]=min(kering,hujan,panas,lembab,f_mendung,f2_cerah)
	if kering and hujan and panas and lembab and f_mendung and f2_mendung:
	 		nkTinggi[67]=min(kering,hujan,panas,lembab,f_mendung,f2_mendung)
	if kering and hujan and panas and lembab and f_mendung and f2_hujan:
	 		nkTinggi[68]=min(kering,hujan,panas,lembab,f_mendung,f2_hujan)
	if kering and hujan and panas and lembab and f_hujan and f2_cerah:
	 		nkTinggi[69]=min(kering,hujan,panas,lembab,f_hujan,f2_cerah)
	if kering and hujan and panas and lembab and f_hujan and f2_mendung:
	 		nkTinggi[70]=min(kering,hujan,panas,lembab,f_hujan,f2_mendung)
	if kering and hujan and panas and lembab and f_hujan and f2_hujan:
	 		nkTinggi[71]=min(kering,hujan,panas,lembab,f_hujan,f2_hujan)
	if kering and hujan and sejuk and normal and f_cerah and f2_cerah:
	 		nkTinggi[72]=min(kering,hujan,sejuk,normal,f_cerah,f2_cerah)
	if kering and hujan and sejuk and normal and f_cerah and f2_mendung:
	 		nkTinggi[73]=min(kering,hujan,sejuk,normal,f_cerah,f2_mendung)
	if kering and hujan and sejuk and normal and f_cerah and f2_hujan:
	 		nkTinggi[74]=min(kering,hujan,sejuk,normal,f_cerah,f2_hujan)
	if kering and hujan and sejuk and normal and f_mendung and f2_cerah:
	 		nkTinggi[75]=min(kering,hujan,sejuk,normal,f_mendung,f2_cerah)
	if kering and hujan and sejuk and normal and f_mendung and f2_mendung:
	 		nkTinggi[76]=min(kering,hujan,sejuk,normal,f_mendung,f2_mendung)
	if kering and hujan and sejuk and normal and f_mendung and f2_hujan:
	 		nkTinggi[77]=min(kering,hujan,sejuk,normal,f_mendung,f2_hujan)
	if kering and hujan and sejuk and normal and f_hujan and f2_cerah:
	 		nkTinggi[78]=min(kering,hujan,sejuk,normal,f_hujan,f2_cerah)
	if kering and hujan and sejuk and normal and f_hujan and f2_mendung:
	 		nkTinggi[79]=min(kering,hujan,sejuk,normal,f_hujan,f2_mendung)
	if kering and hujan and sejuk and normal and f_hujan and f2_hujan:
	 		nkTinggi[80]=min(kering,hujan,sejuk,normal,f_hujan,f2_hujan)
	if kering and hujan and sejuk and lembab and f_cerah and f2_cerah:
	 		nkTinggi[81]=min(kering,hujan,sejuk,lembab,f_cerah,f2_cerah)
	if kering and hujan and sejuk and lembab and f_cerah and f2_mendung:
	 		nkTinggi[82]=min(kering,hujan,sejuk,lembab,f_cerah,f2_mendung)
	if kering and hujan and sejuk and lembab and f_cerah and f2_hujan:
	 		nkTinggi[83]=min(kering,hujan,sejuk,lembab,f_cerah,f2_hujan) 		
	if kering and hujan and sejuk and lembab and f_mendung and f2_cerah:
	 		nkTinggi[84]=min(kering,hujan,sejuk,lembab,f_mendung,f2_cerah)
	if kering and hujan and sejuk and lembab and f_mendung and f2_mendung:
	 		nkTinggi[85]=min(kering,hujan,sejuk,lembab,f_mendung,f2_mendung)
	if kering and hujan and sejuk and lembab and f_mendung and f2_hujan:
	 		nkTinggi[86]=min(kering,hujan,sejuk,lembab,f_mendung,f2_hujan)
	if kering and hujan and sejuk and lembab and f_hujan and f2_cerah:
	 		nkTinggi[87]=min(kering,hujan,sejuk,lembab,f_hujan,f2_cerah)
	if kering and hujan and sejuk and lembab and f_hujan and f2_mendung:
	 		nkTinggi[88]=min(kering,hujan,sejuk,lembab,f_hujan,f2_mendung)
	if kering and hujan and sejuk and lembab and f_hujan and f2_hujan:
	 		nkRendah[89]=min(kering,hujan,sejuk,lembab,f_hujan,f2_hujan)
	if kering and hujan and dingin and normal and f_cerah and f2_cerah:
	 		nkTinggi[90]=min(kering,hujan,dingin,normal,f_cerah,f2_cerah)
	if kering and hujan and dingin and normal and f_cerah and f2_mendung:
	 		nkTinggi[91]=min(kering,hujan,dingin,normal,f_cerah,f2_mendung)
	if kering and hujan and dingin and normal and f_cerah and f2_hujan:
	 		nkTinggi[92]=min(kering,hujan,dingin,normal,f_cerah,f2_hujan)
	if kering and hujan and dingin and normal and f_mendung and f2_cerah:
	 		nkTinggi[93]=min(kering,hujan,dingin,normal,f_mendung,f2_cerah)
	if kering and hujan and dingin and normal and f_mendung and f2_mendung:
	 		nkTinggi[94]=min(kering,hujan,dingin,normal,f_mendung,f2_mendung)
	if kering and hujan and dingin and normal and f_mendung and f2_hujan:
	 		nkTinggi[95]=min(kering,hujan,dingin,normal,f_mendung,f2_hujan)
	if kering and hujan and dingin and normal and f_hujan and f2_cerah:
	 		nkTinggi[96]=min(kering,hujan,dingin,normal,f_hujan,f2_cerah)
	if kering and hujan and dingin and normal and f_hujan and f2_mendung:
	 		nkTinggi[97]=min(kering,hujan,dingin,normal,f_hujan,f2_mendung)
	if kering and hujan and dingin and normal and f_hujan and f2_hujan:
	 		nkRendah[98]=min(kering,hujan,dingin,normal,f_hujan,f2_hujan)
	if kering and hujan and dingin and lembab and f_cerah and f2_cerah:
	 		nkTinggi[99]=min(kering,hujan,dingin,lembab,f_cerah,f2_cerah)
	if kering and hujan and dingin and lembab and f_cerah and f2_mendung:
	 		nkTinggi[100]=min(kering,hujan,dingin,lembab,f_cerah,f2_mendung)
	if kering and hujan and dingin and lembab and f_cerah and f2_hujan:
	 		nkTinggi[101]=min(kering,hujan,dingin,lembab,f_cerah,f2_hujan)
	if kering and hujan and dingin and lembab and f_mendung and f2_cerah:
	 		nkTinggi[102]=min(kering,hujan,dingin,lembab,f_mendung,f2_cerah)
	if kering and hujan and dingin and lembab and f_mendung and f2_mendung:
	 		nkTinggi[103]=min(kering,hujan,dingin,lembab,f_mendung,f2_mendung) 		
	if kering and hujan and dingin and lembab and f_mendung and f2_hujan:
	 		nkTinggi[104]=min(kering,hujan,dingin,lembab,f_mendung,f2_hujan)
	if kering and hujan and dingin and lembab and f_hujan and f2_cerah:
	 		nkTinggi[105]=min(kering,hujan,dingin,lembab,f_hujan,f2_cerah)
	if kering and hujan and dingin and lembab and f_hujan and f2_mendung:
	 		nkTinggi[106]=min(kering,hujan,dingin,lembab,f_hujan,f2_mendung)
	if kering and hujan and dingin and lembab and f_hujan and f2_hujan:
	 		nkRendah[107]=min(kering,hujan,dingin,lembab,f_hujan,f2_hujan)

	if sedang and tdk_hujan and panas and normal and f_cerah and f2_cerah:
	 		nkTinggi[108]=min(sedang,tdk_hujan,panas,normal,f_cerah,f2_cerah)
	if sedang and tdk_hujan and panas and normal and f_cerah and f2_mendung:
	 		nkTinggi[109]=min(sedang,tdk_hujan,panas,normal,f_cerah,f2_mendung)
	if sedang and tdk_hujan and panas and normal and f_cerah and f2_hujan:
	 		nkTinggi[110]=min(sedang,tdk_hujan,panas,normal,f_cerah,f2_hujan)
	if sedang and tdk_hujan and panas and normal and f_mendung and f2_cerah:
	 		nkTinggi[111]=min(sedang,tdk_hujan,panas,normal,f_mendung,f2_cerah)
	if sedang and tdk_hujan and panas and normal and f_mendung and f2_mendung:
	 		nkTinggi[112]=min(sedang,tdk_hujan,panas,normal,f_mendung,f2_mendung)
	if sedang and tdk_hujan and panas and normal and f_mendung and f2_hujan:
	 		nkTinggi[113]=min(sedang,tdk_hujan,panas,normal,f_mendung,f2_hujan)
	if sedang and tdk_hujan and panas and normal and f_hujan and f2_cerah:
	 		nkTinggi[114]=min(sedang,tdk_hujan,panas,normal,f_hujan,f2_cerah)
	if sedang and tdk_hujan and panas and normal and f_hujan and f2_mendung:
	 		nkTinggi[115]=min(sedang,tdk_hujan,panas,normal,f_hujan,f2_mendung)
	if sedang and tdk_hujan and panas and normal and f_hujan and f2_hujan:
	 		nkTinggi[116]=min(sedang,tdk_hujan,panas,normal,f_hujan,f2_hujan)
	if sedang and tdk_hujan and panas and lembab and f_cerah and f2_cerah:
	 		nkTinggi[117]=min(sedang,tdk_hujan,panas,lembab,f_cerah,f2_cerah) 		
	if sedang and tdk_hujan and panas and lembab and f_cerah and f2_mendung:
	 		nkTinggi[118]=min(sedang,tdk_hujan,panas,lembab,f_cerah,f2_mendung)
	if sedang and tdk_hujan and panas and lembab and f_cerah and f2_hujan:
	 		nkTinggi[119]=min(sedang,tdk_hujan,panas,lembab,f_cerah,f2_hujan)
	if sedang and tdk_hujan and panas and lembab and f_mendung and f2_cerah:
	 		nkTinggi[120]=min(sedang,tdk_hujan,panas,lembab,f_mendung,f2_cerah)
	if sedang and tdk_hujan and panas and lembab and f_mendung and f2_mendung:
	 		nkTinggi[121]=min(sedang,tdk_hujan,panas,lembab,f_mendung,f2_mendung)
	if sedang and tdk_hujan and panas and lembab and f_mendung and f2_hujan:
	 		nkTinggi[122]=min(sedang,tdk_hujan,panas,lembab,f_mendung,f2_hujan)
	if sedang and tdk_hujan and panas and lembab and f_hujan and f2_cerah:
	 		nkTinggi[123]=min(sedang,tdk_hujan,panas,lembab,f_hujan,f2_cerah)
	if sedang and tdk_hujan and panas and lembab and f_hujan and f2_mendung:
	 		nkTinggi[124]=min(sedang,tdk_hujan,panas,lembab,f_hujan,f2_mendung)
	if sedang and tdk_hujan and panas and lembab and f_hujan and f2_hujan:
	 		nkTinggi[125]=min(sedang,tdk_hujan,panas,lembab,f_hujan,f2_hujan)
	if sedang and tdk_hujan and sejuk and normal and f_cerah and f2_cerah:
	 		nkTinggi[126]=min(sedang,tdk_hujan,sejuk,normal,f_cerah,f2_cerah)
	if sedang and tdk_hujan and sejuk and normal and f_cerah and f2_mendung:
	 		nkTinggi[127]=min(sedang,tdk_hujan,sejuk,normal,f_cerah,f2_mendung)
	if sedang and tdk_hujan and sejuk and normal and f_cerah and f2_hujan:
	 		nkTinggi[128]=min(sedang,tdk_hujan,sejuk,normal,f_cerah,f2_hujan)
	if sedang and tdk_hujan and sejuk and normal and f_mendung and f2_cerah:
	 		nkTinggi[129]=min(sedang,tdk_hujan,sejuk,normal,f_mendung,f2_cerah)
	if sedang and tdk_hujan and sejuk and normal and f_mendung and f2_mendung:
	 		nkTinggi[130]=min(sedang,tdk_hujan,sejuk,normal,f_mendung,f2_mendung)
	if sedang and tdk_hujan and sejuk and normal and f_mendung and f2_hujan:
	 		nkTinggi[131]=min(sedang,tdk_hujan,sejuk,normal,f_mendung,f2_hujan)
	if sedang and tdk_hujan and sejuk and normal and f_hujan and f2_cerah:
	 		nkTinggi[132]=min(sedang,tdk_hujan,sejuk,normal,f_hujan,f2_cerah)
	if sedang and tdk_hujan and sejuk and normal and f_hujan and f2_mendung:
	 		nkTinggi[133]=min(sedang,tdk_hujan,sejuk,normal,f_hujan,f2_mendung)
	if sedang and tdk_hujan and sejuk and normal and f_hujan and f2_hujan:
	 		nkTinggi[134]=min(sedang,tdk_hujan,sejuk,normal,f_hujan,f2_hujan)
	if sedang and tdk_hujan and sejuk and lembab and f_cerah and f2_cerah:
	 		nkTinggi[135]=min(sedang,tdk_hujan,sejuk,lembab,f_cerah,f2_cerah)
	if sedang and tdk_hujan and sejuk and lembab and f_cerah and f2_mendung:
	 		nkTinggi[136]=min(sedang,tdk_hujan,sejuk,lembab,f_cerah,f2_mendung)
	if sedang and tdk_hujan and sejuk and lembab and f_cerah and f2_hujan:
	 		nkTinggi[137]=min(sedang,tdk_hujan,sejuk,lembab,f_cerah,f2_hujan) 		
	if sedang and tdk_hujan and sejuk and lembab and f_mendung and f2_cerah:
	 		nkTinggi[138]=min(sedang,tdk_hujan,sejuk,lembab,f_mendung,f2_cerah)
	if sedang and tdk_hujan and sejuk and lembab and f_mendung and f2_mendung:
	 		nkTinggi[139]=min(sedang,tdk_hujan,sejuk,lembab,f_mendung,f2_mendung)
	if sedang and tdk_hujan and sejuk and lembab and f_mendung and f2_hujan:
	 		nkTinggi[140]=min(sedang,tdk_hujan,sejuk,lembab,f_mendung,f2_hujan)
	if sedang and tdk_hujan and sejuk and lembab and f_hujan and f2_cerah:
	 		nkTinggi[141]=min(sedang,tdk_hujan,sejuk,lembab,f_hujan,f2_cerah)
	if sedang and tdk_hujan and sejuk and lembab and f_hujan and f2_mendung:
	 		nkTinggi[142]=min(sedang,tdk_hujan,sejuk,lembab,f_hujan,f2_mendung)
	if sedang and tdk_hujan and sejuk and lembab and f_hujan and f2_hujan:
	 		nkTinggi[143]=min(sedang,tdk_hujan,sejuk,lembab,f_hujan,f2_hujan)
	if sedang and tdk_hujan and dingin and normal and f_cerah and f2_cerah:
	 		nkTinggi[144]=min(sedang,tdk_hujan,dingin,normal,f_cerah,f2_cerah)
	if sedang and tdk_hujan and dingin and normal and f_cerah and f2_mendung:
	 		nkTinggi[145]=min(sedang,tdk_hujan,dingin,normal,f_cerah,f2_mendung)
	if sedang and tdk_hujan and dingin and normal and f_cerah and f2_hujan:
	 		nkTinggi[146]=min(sedang,tdk_hujan,dingin,normal,f_cerah,f2_hujan)
	if sedang and tdk_hujan and dingin and normal and f_mendung and f2_cerah:
	 		nkTinggi[147]=min(sedang,tdk_hujan,dingin,normal,f_mendung,f2_cerah)
	if sedang and tdk_hujan and dingin and normal and f_mendung and f2_mendung:
	 		nkTinggi[148]=min(sedang,tdk_hujan,dingin,normal,f_mendung,f2_mendung)
	if sedang and tdk_hujan and dingin and normal and f_mendung and f2_hujan:
	 		nkTinggi[149]=min(sedang,tdk_hujan,dingin,normal,f_mendung,f2_hujan)
	if sedang and tdk_hujan and dingin and normal and f_hujan and f2_cerah:
	 		nkTinggi[150]=min(sedang,tdk_hujan,dingin,normal,f_hujan,f2_cerah)
	if sedang and tdk_hujan and dingin and normal and f_hujan and f2_mendung:
	 		nkTinggi[151]=min(sedang,tdk_hujan,dingin,normal,f_hujan,f2_mendung)
	if sedang and tdk_hujan and dingin and normal and f_hujan and f2_hujan:
	 		nkTinggi[152]=min(sedang,tdk_hujan,dingin,normal,f_hujan,f2_hujan)
	if sedang and tdk_hujan and dingin and lembab and f_cerah and f2_cerah:
	 		nkTinggi[153]=min(sedang,tdk_hujan,dingin,lembab,f_cerah,f2_cerah)
	if sedang and tdk_hujan and dingin and lembab and f_cerah and f2_mendung:
	 		nkTinggi[154]=min(sedang,tdk_hujan,dingin,lembab,f_cerah,f2_mendung)
	if sedang and tdk_hujan and dingin and lembab and f_cerah and f2_hujan:
	 		nkTinggi[155]=min(sedang,tdk_hujan,dingin,lembab,f_cerah,f2_hujan)
	if sedang and tdk_hujan and dingin and lembab and f_mendung and f2_cerah:
	 		nkTinggi[156]=min(sedang,tdk_hujan,dingin,lembab,f_mendung,f2_cerah)
	if sedang and tdk_hujan and dingin and lembab and f_mendung and f2_mendung:
	 		nkTinggi[157]=min(sedang,tdk_hujan,dingin,lembab,f_mendung,f2_mendung) 		
	if sedang and tdk_hujan and dingin and lembab and f_mendung and f2_hujan:
	 		nkTinggi[158]=min(sedang,tdk_hujan,dingin,lembab,f_mendung,f2_hujan)
	if sedang and tdk_hujan and dingin and lembab and f_hujan and f2_cerah:
	 		nkTinggi[159]=min(sedang,tdk_hujan,dingin,lembab,f_hujan,f2_cerah)
	if sedang and tdk_hujan and dingin and lembab and f_hujan and f2_mendung:
	 		nkTinggi[160]=min(sedang,tdk_hujan,dingin,lembab,f_hujan,f2_mendung)
	if sedang and tdk_hujan and dingin and lembab and f_hujan and f2_hujan:
	 		nkTinggi[161]=min(sedang,tdk_hujan,dingin,lembab,f_hujan,f2_hujan) 	

	if sedang and hujan and panas and normal and f_cerah and f2_cerah:
	 		nkRendah[162]=min(sedang,hujan,panas,normal,f_cerah,f2_cerah)
	if sedang and hujan and panas and normal and f_cerah and f2_mendung:
	 		nkRendah[163]=min(sedang,hujan,panas,normal,f_cerah,f2_mendung)
	if sedang and hujan and panas and normal and f_cerah and f2_hujan:
	 		nkRendah[164]=min(sedang,hujan,panas,normal,f_cerah,f2_hujan)
	if sedang and hujan and panas and normal and f_mendung and f2_cerah:
	 		nkRendah[165]=min(sedang,hujan,panas,normal,f_mendung,f2_cerah)
	if sedang and hujan and panas and normal and f_mendung and f2_mendung:
	 		nkRendah[166]=min(sedang,hujan,panas,normal,f_mendung,f2_mendung)
	if sedang and hujan and panas and normal and f_mendung and f2_hujan:
	 		nkRendah[167]=min(sedang,hujan,panas,normal,f_mendung,f2_hujan)
	if sedang and hujan and panas and normal and f_hujan and f2_cerah:
	 		nkRendah[168]=min(sedang,hujan,panas,normal,f_hujan,f2_cerah)
	if sedang and hujan and panas and normal and f_hujan and f2_mendung:
	 		nkRendah[169]=min(sedang,hujan,panas,normal,f_hujan,f2_mendung)
	if sedang and hujan and panas and normal and f_hujan and f2_hujan:
	 		nkRendah[170]=min(sedang,hujan,panas,normal,f_hujan,f2_hujan)
	if sedang and hujan and panas and lembab and f_cerah and f2_cerah:
	 		nkRendah[171]=min(sedang,hujan,panas,lembab,f_cerah,f2_cerah) 		
	if sedang and hujan and panas and lembab and f_cerah and f2_mendung:
	 		nkRendah[172]=min(sedang,hujan,panas,lembab,f_cerah,f2_mendung)
	if sedang and hujan and panas and lembab and f_cerah and f2_hujan:
	 		nkRendah[173]=min(sedang,hujan,panas,lembab,f_cerah,f2_hujan)
	if sedang and hujan and panas and lembab and f_mendung and f2_cerah:
	 		nkRendah[174]=min(sedang,hujan,panas,lembab,f_mendung,f2_cerah)
	if sedang and hujan and panas and lembab and f_mendung and f2_mendung:
	 		nkRendah[175]=min(sedang,hujan,panas,lembab,f_mendung,f2_mendung)
	if sedang and hujan and panas and lembab and f_mendung and f2_hujan:
	 		nkRendah[176]=min(sedang,hujan,panas,lembab,f_mendung,f2_hujan)
	if sedang and hujan and panas and lembab and f_hujan and f2_cerah:
	 		nkRendah[177]=min(sedang,hujan,panas,lembab,f_hujan,f2_cerah)
	if sedang and hujan and panas and lembab and f_hujan and f2_mendung:
	 		nkRendah[178]=min(sedang,hujan,panas,lembab,f_hujan,f2_mendung)
	if sedang and hujan and panas and lembab and f_hujan and f2_hujan:
	 		nkRendah[179]=min(sedang,hujan,panas,lembab,f_hujan,f2_hujan)
	if sedang and hujan and sejuk and normal and f_cerah and f2_cerah:
	 		nkRendah[180]=min(sedang,hujan,sejuk,normal,f_cerah,f2_cerah)
	if sedang and hujan and sejuk and normal and f_cerah and f2_mendung:
	 		nkRendah[181]=min(sedang,hujan,sejuk,normal,f_cerah,f2_mendung)
	if sedang and hujan and sejuk and normal and f_cerah and f2_hujan:
	 		nkRendah[182]=min(sedang,hujan,sejuk,normal,f_cerah,f2_hujan)
	if sedang and hujan and sejuk and normal and f_mendung and f2_cerah:
	 		nkRendah[183]=min(sedang,hujan,sejuk,normal,f_mendung,f2_cerah)
	if sedang and hujan and sejuk and normal and f_mendung and f2_mendung:
	 		nkRendah[184]=min(sedang,hujan,sejuk,normal,f_mendung,f2_mendung)
	if sedang and hujan and sejuk and normal and f_mendung and f2_hujan:
	 		nkRendah[185]=min(sedang,hujan,sejuk,normal,f_mendung,f2_hujan)
	if sedang and hujan and sejuk and normal and f_hujan and f2_cerah:
	 		nkRendah[186]=min(sedang,hujan,sejuk,normal,f_hujan,f2_cerah)
	if sedang and hujan and sejuk and normal and f_hujan and f2_mendung:
	 		nkRendah[187]=min(sedang,hujan,sejuk,normal,f_hujan,f2_mendung)
	if sedang and hujan and sejuk and normal and f_hujan and f2_hujan:
	 		nkRendah[188]=min(sedang,hujan,sejuk,normal,f_hujan,f2_hujan)
	if sedang and hujan and sejuk and lembab and f_cerah and f2_cerah:
	 		nkRendah[189]=min(sedang,hujan,sejuk,lembab,f_cerah,f2_cerah)
	if sedang and hujan and sejuk and lembab and f_cerah and f2_mendung:
	 		nkRendah[190]=min(sedang,hujan,sejuk,lembab,f_cerah,f2_mendung)
	if sedang and hujan and sejuk and lembab and f_cerah and f2_hujan:
	 		nkRendah[191]=min(sedang,hujan,sejuk,lembab,f_cerah,f2_hujan) 		
	if sedang and hujan and sejuk and lembab and f_mendung and f2_cerah:
	 		nkRendah[192]=min(sedang,hujan,sejuk,lembab,f_mendung,f2_cerah)
	if sedang and hujan and sejuk and lembab and f_mendung and f2_mendung:
	 		nkRendah[193]=min(sedang,hujan,sejuk,lembab,f_mendung,f2_mendung)
	if sedang and hujan and sejuk and lembab and f_mendung and f2_hujan:
	 		nkRendah[194]=min(sedang,hujan,sejuk,lembab,f_mendung,f2_hujan)
	if sedang and hujan and sejuk and lembab and f_hujan and f2_cerah:
	 		nkRendah[195]=min(sedang,hujan,sejuk,lembab,f_hujan,f2_cerah)
	if sedang and hujan and sejuk and lembab and f_hujan and f2_mendung:
	 		nkRendah[196]=min(sedang,hujan,sejuk,lembab,f_hujan,f2_mendung)
	if sedang and hujan and sejuk and lembab and f_hujan and f2_hujan:
	 		nkRendah[197]=min(sedang,hujan,sejuk,lembab,f_hujan,f2_hujan)
	if sedang and hujan and dingin and normal and f_cerah and f2_cerah:
	 		nkRendah[198]=min(sedang,hujan,dingin,normal,f_cerah,f2_cerah)
	if sedang and hujan and dingin and normal and f_cerah and f2_mendung:
	 		nkRendah[199]=min(sedang,hujan,dingin,normal,f_cerah,f2_mendung)
	if sedang and hujan and dingin and normal and f_cerah and f2_hujan:
	 		nkRendah[200]=min(sedang,hujan,dingin,normal,f_cerah,f2_hujan)
	if sedang and hujan and dingin and normal and f_mendung and f2_cerah:
	 		nkRendah[201]=min(sedang,hujan,dingin,normal,f_mendung,f2_cerah)
	if sedang and hujan and dingin and normal and f_mendung and f2_mendung:
	 		nkRendah[202]=min(sedang,hujan,dingin,normal,f_mendung,f2_mendung)
	if sedang and hujan and dingin and normal and f_mendung and f2_hujan:
	 		nkRendah[203]=min(sedang,hujan,dingin,normal,f_mendung,f2_hujan)
	if sedang and hujan and dingin and normal and f_hujan and f2_cerah:
	 		nkRendah[204]=min(sedang,hujan,dingin,normal,f_hujan,f2_cerah)
	if sedang and hujan and dingin and normal and f_hujan and f2_mendung:
	 		nkRendah[205]=min(sedang,hujan,dingin,normal,f_hujan,f2_mendung)
	if sedang and hujan and dingin and normal and f_hujan and f2_hujan:
	 		nkRendah[206]=min(sedang,hujan,dingin,normal,f_hujan,f2_hujan)
	if sedang and hujan and dingin and lembab and f_cerah and f2_cerah:
	 		nkRendah[207]=min(sedang,hujan,dingin,lembab,f_cerah,f2_cerah)
	if sedang and hujan and dingin and lembab and f_cerah and f2_mendung:
	 		nkRendah[208]=min(sedang,hujan,dingin,lembab,f_cerah,f2_mendung)
	if sedang and hujan and dingin and lembab and f_cerah and f2_hujan:
	 		nkRendah[209]=min(sedang,hujan,dingin,lembab,f_cerah,f2_hujan)
	if sedang and hujan and dingin and lembab and f_mendung and f2_cerah:
	 		nkRendah[210]=min(sedang,hujan,dingin,lembab,f_mendung,f2_cerah)
	if sedang and hujan and dingin and lembab and f_mendung and f2_mendung:
	 		nkRendah[211]=min(sedang,hujan,dingin,lembab,f_mendung,f2_mendung) 		
	if sedang and hujan and dingin and lembab and f_mendung and f2_hujan:
	 		nkRendah[212]=min(sedang,hujan,dingin,lembab,f_mendung,f2_hujan)
	if sedang and hujan and dingin and lembab and f_hujan and f2_cerah:
	 		nkRendah[213]=min(sedang,hujan,dingin,lembab,f_hujan,f2_cerah)
	if sedang and hujan and dingin and lembab and f_hujan and f2_mendung:
	 		nkRendah[214]=min(sedang,hujan,dingin,lembab,f_hujan,f2_mendung)
	if sedang and hujan and dingin and lembab and f_hujan and f2_hujan:
	 		nkRendah[215]=min(sedang,hujan,dingin,lembab,f_hujan,f2_hujan)

	if basah and tdk_hujan and panas and normal and f_cerah and f2_cerah:
	 		nkRendah[216]=min(basah,tdk_hujan,panas,normal,f_cerah,f2_cerah)
	if basah and tdk_hujan and panas and normal and f_cerah and f2_mendung:
	 		nkRendah[217]=min(basah,tdk_hujan,panas,normal,f_cerah,f2_mendung)
	if basah and tdk_hujan and panas and normal and f_cerah and f2_hujan:
	 		nkRendah[218]=min(basah,tdk_hujan,panas,normal,f_cerah,f2_hujan)
	if basah and tdk_hujan and panas and normal and f_mendung and f2_cerah:
	 		nkRendah[219]=min(basah,tdk_hujan,panas,normal,f_mendung,f2_cerah)
	if basah and tdk_hujan and panas and normal and f_mendung and f2_mendung:
	 		nkRendah[220]=min(basah,tdk_hujan,panas,normal,f_mendung,f2_mendung)
	if basah and tdk_hujan and panas and normal and f_mendung and f2_hujan:
	 		nkRendah[221]=min(basah,tdk_hujan,panas,normal,f_mendung,f2_hujan)
	if basah and tdk_hujan and panas and normal and f_hujan and f2_cerah:
	 		nkRendah[222]=min(basah,tdk_hujan,panas,normal,f_hujan,f2_cerah)
	if basah and tdk_hujan and panas and normal and f_hujan and f2_mendung:
	 		nkRendah[223]=min(basah,tdk_hujan,panas,normal,f_hujan,f2_mendung)
	if basah and tdk_hujan and panas and normal and f_hujan and f2_hujan:
	 		nkRendah[224]=min(basah,tdk_hujan,panas,normal,f_hujan,f2_hujan)
	if basah and tdk_hujan and panas and lembab and f_cerah and f2_cerah:
	 		nkRendah[225]=min(basah,tdk_hujan,panas,lembab,f_cerah,f2_cerah) 		
	if basah and tdk_hujan and panas and lembab and f_cerah and f2_mendung:
	 		nkRendah[226]=min(basah,tdk_hujan,panas,lembab,f_cerah,f2_mendung)
	if basah and tdk_hujan and panas and lembab and f_cerah and f2_hujan:
	 		nkRendah[227]=min(basah,tdk_hujan,panas,lembab,f_cerah,f2_hujan)
	if basah and tdk_hujan and panas and lembab and f_mendung and f2_cerah:
	 		nkRendah[228]=min(basah,tdk_hujan,panas,lembab,f_mendung,f2_cerah)
	if basah and tdk_hujan and panas and lembab and f_mendung and f2_mendung:
	 		nkRendah[229]=min(basah,tdk_hujan,panas,lembab,f_mendung,f2_mendung)
	if basah and tdk_hujan and panas and lembab and f_mendung and f2_hujan:
	 		nkRendah[230]=min(basah,tdk_hujan,panas,lembab,f_mendung,f2_hujan)
	if basah and tdk_hujan and panas and lembab and f_hujan and f2_cerah:
	 		nkRendah[231]=min(basah,tdk_hujan,panas,lembab,f_hujan,f2_cerah)
	if basah and tdk_hujan and panas and lembab and f_hujan and f2_mendung:
	 		nkRendah[232]=min(basah,tdk_hujan,panas,lembab,f_hujan,f2_mendung)
	if basah and tdk_hujan and panas and lembab and f_hujan and f2_hujan:
	 		nkRendah[233]=min(basah,tdk_hujan,panas,lembab,f_hujan,f2_hujan)
	if basah and tdk_hujan and sejuk and normal and f_cerah and f2_cerah:
	 		nkRendah[234]=min(basah,tdk_hujan,sejuk,normal,f_cerah,f2_cerah)
	if basah and tdk_hujan and sejuk and normal and f_cerah and f2_mendung:
	 		nkRendah[235]=min(basah,tdk_hujan,sejuk,normal,f_cerah,f2_mendung)
	if basah and tdk_hujan and sejuk and normal and f_cerah and f2_hujan:
	 		nkRendah[236]=min(basah,tdk_hujan,sejuk,normal,f_cerah,f2_hujan)
	if basah and tdk_hujan and sejuk and normal and f_mendung and f2_cerah:
	 		nkRendah[237]=min(basah,tdk_hujan,sejuk,normal,f_mendung,f2_cerah)
	if basah and tdk_hujan and sejuk and normal and f_mendung and f2_mendung:
	 		nkRendah[238]=min(basah,tdk_hujan,sejuk,normal,f_mendung,f2_mendung)
	if basah and tdk_hujan and sejuk and normal and f_mendung and f2_hujan:
	 		nkRendah[239]=min(basah,tdk_hujan,sejuk,normal,f_mendung,f2_hujan)
	if basah and tdk_hujan and sejuk and normal and f_hujan and f2_cerah:
	 		nkRendah[240]=min(basah,tdk_hujan,sejuk,normal,f_hujan,f2_cerah)
	if basah and tdk_hujan and sejuk and normal and f_hujan and f2_mendung:
	 		nkRendah[241]=min(basah,tdk_hujan,sejuk,normal,f_hujan,f2_mendung)
	if basah and tdk_hujan and sejuk and normal and f_hujan and f2_hujan:
	 		nkRendah[242]=min(basah,tdk_hujan,sejuk,normal,f_hujan,f2_hujan)
	if basah and tdk_hujan and sejuk and lembab and f_cerah and f2_cerah:
	 		nkRendah[243]=min(basah,tdk_hujan,sejuk,lembab,f_cerah,f2_cerah)
	if basah and tdk_hujan and sejuk and lembab and f_cerah and f2_mendung:
	 		nkRendah[244]=min(basah,tdk_hujan,sejuk,lembab,f_cerah,f2_mendung)
	if basah and tdk_hujan and sejuk and lembab and f_cerah and f2_hujan:
	 		nkRendah[245]=min(basah,tdk_hujan,sejuk,lembab,f_cerah,f2_hujan) 		
	if basah and tdk_hujan and sejuk and lembab and f_mendung and f2_cerah:
	 		nkRendah[246]=min(basah,tdk_hujan,sejuk,lembab,f_mendung,f2_cerah)
	if basah and tdk_hujan and sejuk and lembab and f_mendung and f2_mendung:
	 		nkRendah[247]=min(basah,tdk_hujan,sejuk,lembab,f_mendung,f2_mendung)
	if basah and tdk_hujan and sejuk and lembab and f_mendung and f2_hujan:
	 		nkRendah[248]=min(basah,tdk_hujan,sejuk,lembab,f_mendung,f2_hujan)
	if basah and tdk_hujan and sejuk and lembab and f_hujan and f2_cerah:
	 		nkRendah[249]=min(basah,tdk_hujan,sejuk,lembab,f_hujan,f2_cerah)
	if basah and tdk_hujan and sejuk and lembab and f_hujan and f2_mendung:
	 		nkRendah[250]=min(basah,tdk_hujan,sejuk,lembab,f_hujan,f2_mendung)
	if basah and tdk_hujan and sejuk and lembab and f_hujan and f2_hujan:
	 		nkRendah[251]=min(basah,tdk_hujan,sejuk,lembab,f_hujan,f2_hujan)
	if basah and tdk_hujan and dingin and normal and f_cerah and f2_cerah:
	 		nkRendah[252]=min(basah,tdk_hujan,dingin,normal,f_cerah,f2_cerah)
	if basah and tdk_hujan and dingin and normal and f_cerah and f2_mendung:
	 		nkRendah[253]=min(basah,tdk_hujan,dingin,normal,f_cerah,f2_mendung)
	if basah and tdk_hujan and dingin and normal and f_cerah and f2_hujan:
	 		nkRendah[254]=min(basah,tdk_hujan,dingin,normal,f_cerah,f2_hujan)
	if basah and tdk_hujan and dingin and normal and f_mendung and f2_cerah:
	 		nkRendah[255]=min(basah,tdk_hujan,dingin,normal,f_mendung,f2_cerah)
	if basah and tdk_hujan and dingin and normal and f_mendung and f2_mendung:
	 		nkRendah[256]=min(basah,tdk_hujan,dingin,normal,f_mendung,f2_mendung)
	if basah and tdk_hujan and dingin and normal and f_mendung and f2_hujan:
	 		nkRendah[257]=min(basah,tdk_hujan,dingin,normal,f_mendung,f2_hujan)
	if basah and tdk_hujan and dingin and normal and f_hujan and f2_cerah:
	 		nkRendah[258]=min(basah,tdk_hujan,dingin,normal,f_hujan,f2_cerah)
	if basah and tdk_hujan and dingin and normal and f_hujan and f2_mendung:
	 		nkRendah[259]=min(basah,tdk_hujan,dingin,normal,f_hujan,f2_mendung)
	if basah and tdk_hujan and dingin and normal and f_hujan and f2_hujan:
	 		nkRendah[260]=min(basah,tdk_hujan,dingin,normal,f_hujan,f2_hujan)
	if basah and tdk_hujan and dingin and lembab and f_cerah and f2_cerah:
	 		nkRendah[261]=min(basah,tdk_hujan,dingin,lembab,f_cerah,f2_cerah)
	if basah and tdk_hujan and dingin and lembab and f_cerah and f2_mendung:
	 		nkRendah[262]=min(basah,tdk_hujan,dingin,lembab,f_cerah,f2_mendung)
	if basah and tdk_hujan and dingin and lembab and f_cerah and f2_hujan:
	 		nkRendah[263]=min(basah,tdk_hujan,dingin,lembab,f_cerah,f2_hujan)
	if basah and tdk_hujan and dingin and lembab and f_mendung and f2_cerah:
	 		nkRendah[264]=min(basah,tdk_hujan,dingin,lembab,f_mendung,f2_cerah)
	if basah and tdk_hujan and dingin and lembab and f_mendung and f2_mendung:
	 		nkRendah[265]=min(basah,tdk_hujan,dingin,lembab,f_mendung,f2_mendung) 		
	if basah and tdk_hujan and dingin and lembab and f_mendung and f2_hujan:
	 		nkRendah[266]=min(basah,tdk_hujan,dingin,lembab,f_mendung,f2_hujan)
	if basah and tdk_hujan and dingin and lembab and f_hujan and f2_cerah:
	 		nkRendah[267]=min(basah,tdk_hujan,dingin,lembab,f_hujan,f2_cerah)
	if basah and tdk_hujan and dingin and lembab and f_hujan and f2_mendung:
	 		nkRendah[268]=min(basah,tdk_hujan,dingin,lembab,f_hujan,f2_mendung)
	if basah and tdk_hujan and dingin and lembab and f_hujan and f2_hujan:
	 		nkRendah[269]=min(basah,tdk_hujan,dingin,lembab,f_hujan,f2_hujan)

	if basah and hujan and panas and normal and f_cerah and f2_cerah:
	 		nkRendah[270]=min(basah,hujan,panas,normal,f_cerah,f2_cerah)
	if basah and hujan and panas and normal and f_cerah and f2_mendung:
	 		nkRendah[271]=min(basah,hujan,panas,normal,f_cerah,f2_mendung)
	if basah and hujan and panas and normal and f_cerah and f2_hujan:
	 		nkRendah[272]=min(basah,hujan,panas,normal,f_cerah,f2_hujan)
	if basah and hujan and panas and normal and f_mendung and f2_cerah:
	 		nkRendah[273]=min(basah,hujan,panas,normal,f_mendung,f2_cerah)
	if basah and hujan and panas and normal and f_mendung and f2_mendung:
	 		nkRendah[274]=min(basah,hujan,panas,normal,f_mendung,f2_mendung)
	if basah and hujan and panas and normal and f_mendung and f2_hujan:
	 		nkRendah[275]=min(basah,hujan,panas,normal,f_mendung,f2_hujan)
	if basah and hujan and panas and normal and f_hujan and f2_cerah:
	 		nkRendah[276]=min(basah,hujan,panas,normal,f_hujan,f2_cerah)
	if basah and hujan and panas and normal and f_hujan and f2_mendung:
	 		nkRendah[277]=min(basah,hujan,panas,normal,f_hujan,f2_mendung)
	if basah and hujan and panas and normal and f_hujan and f2_hujan:
	 		nkRendah[278]=min(basah,hujan,panas,normal,f_hujan,f2_hujan)
	if basah and hujan and panas and lembab and f_cerah and f2_cerah:
	 		nkRendah[279]=min(basah,hujan,panas,lembab,f_cerah,f2_cerah) 		
	if basah and hujan and panas and lembab and f_cerah and f2_mendung:
	 		nkRendah[280]=min(basah,hujan,panas,lembab,f_cerah,f2_mendung)
	if basah and hujan and panas and lembab and f_cerah and f2_hujan:
	 		nkRendah[281]=min(basah,hujan,panas,lembab,f_cerah,f2_hujan)
	if basah and hujan and panas and lembab and f_mendung and f2_cerah:
	 		nkRendah[282]=min(basah,hujan,panas,lembab,f_mendung,f2_cerah)
	if basah and hujan and panas and lembab and f_mendung and f2_mendung:
	 		nkRendah[283]=min(basah,hujan,panas,lembab,f_mendung,f2_mendung)
	if basah and hujan and panas and lembab and f_mendung and f2_hujan:
	 		nkRendah[284]=min(basah,hujan,panas,lembab,f_mendung,f2_hujan)
	if basah and hujan and panas and lembab and f_hujan and f2_cerah:
	 		nkRendah[285]=min(basah,hujan,panas,lembab,f_hujan,f2_cerah)
	if basah and hujan and panas and lembab and f_hujan and f2_mendung:
	 		nkRendah[286]=min(basah,hujan,panas,lembab,f_hujan,f2_mendung)
	if basah and hujan and panas and lembab and f_hujan and f2_hujan:
	 		nkRendah[287]=min(basah,hujan,panas,lembab,f_hujan,f2_hujan)
	if basah and hujan and sejuk and normal and f_cerah and f2_cerah:
	 		nkRendah[288]=min(basah,hujan,sejuk,normal,f_cerah,f2_cerah)
	if basah and hujan and sejuk and normal and f_cerah and f2_mendung:
	 		nkRendah[289]=min(basah,hujan,sejuk,normal,f_cerah,f2_mendung)
	if basah and hujan and sejuk and normal and f_cerah and f2_hujan:
	 		nkRendah[290]=min(basah,hujan,sejuk,normal,f_cerah,f2_hujan)
	if basah and hujan and sejuk and normal and f_mendung and f2_cerah:
	 		nkRendah[291]=min(basah,hujan,sejuk,normal,f_mendung,f2_cerah)
	if basah and hujan and sejuk and normal and f_mendung and f2_mendung:
	 		nkRendah[292]=min(basah,hujan,sejuk,normal,f_mendung,f2_mendung)
	if basah and hujan and sejuk and normal and f_mendung and f2_hujan:
	 		nkRendah[293]=min(basah,hujan,sejuk,normal,f_mendung,f2_hujan)
	if basah and hujan and sejuk and normal and f_hujan and f2_cerah:
	 		nkRendah[294]=min(basah,hujan,sejuk,normal,f_hujan,f2_cerah)
	if basah and hujan and sejuk and normal and f_hujan and f2_mendung:
	 		nkRendah[295]=min(basah,hujan,sejuk,normal,f_hujan,f2_mendung)
	if basah and hujan and sejuk and normal and f_hujan and f2_hujan:
	 		nkRendah[296]=min(basah,hujan,sejuk,normal,f_hujan,f2_hujan)
	if basah and hujan and sejuk and lembab and f_cerah and f2_cerah:
	 		nkRendah[297]=min(basah,hujan,sejuk,lembab,f_cerah,f2_cerah)
	if basah and hujan and sejuk and lembab and f_cerah and f2_mendung:
	 		nkRendah[298]=min(basah,hujan,sejuk,lembab,f_cerah,f2_mendung)
	if basah and hujan and sejuk and lembab and f_cerah and f2_hujan:
	 		nkRendah[299]=min(basah,hujan,sejuk,lembab,f_cerah,f2_hujan) 		
	if basah and hujan and sejuk and lembab and f_mendung and f2_cerah:
	 		nkRendah[300]=min(basah,hujan,sejuk,lembab,f_mendung,f2_cerah)
	if basah and hujan and sejuk and lembab and f_mendung and f2_mendung:
	 		nkRendah[301]=min(basah,hujan,sejuk,lembab,f_mendung,f2_mendung)
	if basah and hujan and sejuk and lembab and f_mendung and f2_hujan:
	 		nkRendah[302]=min(basah,hujan,sejuk,lembab,f_mendung,f2_hujan)
	if basah and hujan and sejuk and lembab and f_hujan and f2_cerah:
	 		nkRendah[303]=min(basah,hujan,sejuk,lembab,f_hujan,f2_cerah)
	if basah and hujan and sejuk and lembab and f_hujan and f2_mendung:
	 		nkRendah[304]=min(basah,hujan,sejuk,lembab,f_hujan,f2_mendung)
	if basah and hujan and sejuk and lembab and f_hujan and f2_hujan:
	 		nkRendah[305]=min(basah,hujan,sejuk,lembab,f_hujan,f2_hujan)
	if basah and hujan and dingin and normal and f_cerah and f2_cerah:
	 		nkRendah[306]=min(basah,hujan,dingin,normal,f_cerah,f2_cerah)
	if basah and hujan and dingin and normal and f_cerah and f2_mendung:
	 		nkRendah[307]=min(basah,hujan,dingin,normal,f_cerah,f2_mendung)
	if basah and hujan and dingin and normal and f_cerah and f2_hujan:
	 		nkRendah[308]=min(basah,hujan,dingin,normal,f_cerah,f2_hujan)
	if basah and hujan and dingin and normal and f_mendung and f2_cerah:
	 		nkRendah[309]=min(basah,hujan,dingin,normal,f_mendung,f2_cerah)
	if basah and hujan and dingin and normal and f_mendung and f2_mendung:
	 		nkRendah[310]=min(basah,hujan,dingin,normal,f_mendung,f2_mendung)
	if basah and hujan and dingin and normal and f_mendung and f2_hujan:
	 		nkRendah[311]=min(basah,hujan,dingin,normal,f_mendung,f2_hujan)
	if basah and hujan and dingin and normal and f_hujan and f2_cerah:
	 		nkRendah[312]=min(basah,hujan,dingin,normal,f_hujan,f2_cerah)
	if basah and hujan and dingin and normal and f_hujan and f2_mendung:
	 		nkRendah[313]=min(basah,hujan,dingin,normal,f_hujan,f2_mendung)
	if basah and hujan and dingin and normal and f_hujan and f2_hujan:
	 		nkRendah[314]=min(basah,hujan,dingin,normal,f_hujan,f2_hujan)
	if basah and hujan and dingin and lembab and f_cerah and f2_cerah:
	 		nkRendah[315]=min(basah,hujan,dingin,lembab,f_cerah,f2_cerah)
	if basah and hujan and dingin and lembab and f_cerah and f2_mendung:
	 		nkRendah[316]=min(basah,hujan,dingin,lembab,f_cerah,f2_mendung)
	if basah and hujan and dingin and lembab and f_cerah and f2_hujan:
	 		nkRendah[317]=min(basah,hujan,dingin,lembab,f_cerah,f2_hujan)
	if basah and hujan and dingin and lembab and f_mendung and f2_cerah:
	 		nkRendah[318]=min(basah,hujan,dingin,lembab,f_mendung,f2_cerah)
	if basah and hujan and dingin and lembab and f_mendung and f2_mendung:
	 		nkRendah[319]=min(basah,hujan,dingin,lembab,f_mendung,f2_mendung) 		
	if basah and hujan and dingin and lembab and f_mendung and f2_hujan:
	 		nkRendah[320]=min(basah,hujan,dingin,lembab,f_mendung,f2_hujan)
	if basah and hujan and dingin and lembab and f_hujan and f2_cerah:
	 		nkRendah[321]=min(basah,hujan,dingin,lembab,f_hujan,f2_cerah)
	if basah and hujan and dingin and lembab and f_hujan and f2_mendung:
	 		nkRendah[322]=min(basah,hujan,dingin,lembab,f_hujan,f2_mendung)
	if basah and hujan and dingin and lembab and f_hujan and f2_hujan:
	 		nkRendah[323]=min(basah,hujan,dingin,lembab,f_hujan,f2_hujan)
	
	#nkRendah.append(5);
	#nkRendah.insert(1,6);
	print("======================")
	print("FUZZY OUTPUT");
	print("======================")
	for i in range(324):
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
	mamdani = 0;
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
	mamdani = mamdani_pembilang/mamdani_penyebut;
	#print "Nilai Kelayakan : "+str(mamdani);
	return mamdani;
