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
	l_sejuk = 21;
	u_sejuk = 28;
	l_panas = 30;
	u_panas = 50;

	#hum
	l_normal = 0;
	u_normal = 39;
	l_lembab = 40;
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
	if hum < u_normal:
		normal = 1;
	elif hum >= u_normal and hum <= l_lembab:
		normal = (hum * (-1.0) + l_lembab) / (l_lembab - u_normal);
		lembab  = (hum - u_normal) * 1.0 / (l_lembab - u_normal);
	elif hum > l_lembab:
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
	print("LEMBAB  	 : "+str(lembab));
	print("NORMAL : "+str(normal));

	print("-openweather-");
	print("CERAH  : "+str(f_cerah));
	print("MENDUNG: "+str(f_mendung));
	print("HUJAN  : "+str(f_hujan));

#Inferensi
	nkRendah=[];
	nkTinggi=[];
	rendah=0;
	tinggi=0;

	for i in range(108):
		nkRendah.append(0);
		nkTinggi.append(0);

#kering
	if kering and tdk_hujan and panas and normal and f_cerah:
		nkTinggi[0]=min(kering,tdk_hujan,panas,normal,f_cerah)
	if kering and tdk_hujan and panas and normal and f_mendung:
		nkTinggi[1]=min(kering,tdk_hujan,panas,normal,f_mendung)
	if kering and tdk_hujan and panas and normal and f_hujan:
		nkTinggi[2]=min(kering,tdk_hujan,panas,normal,f_hujan)
	if kering and tdk_hujan and panas and normal and f_cerah:
		nkTinggi[3]=min(kering,tdk_hujan,panas,normal,f_cerah)
	if kering and tdk_hujan and panas and normal and f_mendung:
		nkTinggi[4]=min(kering,tdk_hujan,panas,normal,f_mendung)
	if kering and tdk_hujan and panas and normal and f_hujan:
		nkTinggi[5]=min(kering,tdk_hujan,panas,normal,f_hujan)
	if kering and tdk_hujan and normal and normal and f_cerah:
		nkTinggi[6]=min(kering,tdk_hujan,normal,normal,f_cerah)
	if kering and tdk_hujan and normal and normal and f_mendung:
		nkTinggi[7]=min(kering,tdk_hujan,normal,normal,f_mendung)
	if kering and tdk_hujan and normal and normal and f_hujan:
		nkTinggi[8]=min(kering,tdk_hujan,normal,normal,f_hujan)
	if kering and tdk_hujan and normal and normal and f_cerah:
		nkTinggi[9]=min(kering,tdk_hujan,normal,normal,f_cerah)
	if kering and tdk_hujan and normal and normal and f_mendung:
		nkTinggi[10]=min(kering,tdk_hujan,normal,normal,f_mendung)
	if kering and tdk_hujan and normal and normal and f_hujan:
		nkTinggi[11]=min(kering,tdk_hujan,normal,normal,f_hujan)
	if kering and tdk_hujan and dingin and normal and f_cerah:
		nkTinggi[12]=min(kering,tdk_hujan,dingin,normal,f_cerah)
	if kering and tdk_hujan and dingin and normal and f_mendung:
		nkTinggi[13]=min(kering,tdk_hujan,dingin,normal,f_mendung)
	if kering and tdk_hujan and dingin and normal and f_hujan:
		nkTinggi[14]=min(kering,tdk_hujan,dingin,normal,f_hujan)
	if kering and tdk_hujan and dingin and normal and f_cerah:
		nkTinggi[15]=min(kering,tdk_hujan,dingin,normal,f_cerah)
	if kering and tdk_hujan and dingin and normal and f_mendung:
		nkTinggi[16]=min(kering,tdk_hujan,dingin,normal,f_mendung)
	if kering and tdk_hujan and dingin and normal and f_hujan:
		nkTinggi[17]=min(kering,tdk_hujan,dingin,normal,f_hujan)

	if kering and hujan and panas and normal and f_cerah:
		nkTinggi[18]=min(kering,hujan,panas,normal,f_cerah)
	if kering and hujan and panas and normal and f_mendung:
		nkTinggi[19]=min(kering,hujan,panas,normal,f_mendung)
	if kering and hujan and panas and normal and f_hujan:
		nkTinggi[20]=min(kering,hujan,panas,normal,f_hujan)
	if kering and hujan and panas and normal and f_cerah:
		nkTinggi[21]=min(kering,hujan,panas,normal,f_cerah)
	if kering and hujan and panas and normal and f_mendung:
		nkTinggi[22]=min(kering,hujan,panas,normal,f_mendung)
	if kering and hujan and panas and normal and f_hujan:
		nkTinggi[23]=min(kering,hujan,panas,normal,f_hujan)
	if kering and hujan and normal and normal and f_cerah:
		nkTinggi[24]=min(kering,hujan,normal,normal,f_cerah)
	if kering and hujan and normal and normal and f_mendung:
		nkTinggi[25]=min(kering,hujan,normal,normal,f_mendung)
	if kering and hujan and normal and normal and f_hujan:
		nkTinggi[26]=min(kering,hujan,normal,normal,f_hujan)
	if kering and hujan and normal and normal and f_cerah:
		nkTinggi[27]=min(kering,hujan,normal,normal,f_cerah)
	if kering and hujan and normal and normal and f_mendung:
		nkTinggi[28]=min(kering,hujan,normal,normal,f_mendung)
	if kering and hujan and normal and normal and f_hujan:
		nkTinggi[29]=min(kering,hujan,normal,normal,f_hujan)
	if kering and hujan and dingin and normal and f_cerah:
		nkTinggi[30]=min(kering,hujan,dingin,normal,f_cerah)
	if kering and hujan and dingin and normal and f_mendung:
		nkTinggi[31]=min(kering,hujan,dingin,normal,f_mendung)
	if kering and hujan and dingin and normal and f_hujan:
		nkTinggi[32]=min(kering,hujan,dingin,normal,f_hujan)
	if kering and hujan and dingin and normal and f_cerah:
		nkTinggi[33]=min(kering,hujan,dingin,normal,f_cerah)
	if kering and hujan and dingin and normal and f_mendung:
		nkTinggi[34]=min(kering,hujan,dingin,normal,f_mendung)
	if kering and hujan and dingin and normal and f_hujan:
		nkRendah[35]=min(kering,hujan,dingin,normal,f_hujan)

	#sedang
	if sedang and tdk_hujan and panas and normal and f_cerah:
		nkTinggi[36]=min(sedang,tdk_hujan,panas,normal,f_cerah)
	if sedang and tdk_hujan and panas and normal and f_mendung:
		nkTinggi[37]=min(sedang,tdk_hujan,panas,normal,f_mendung)
	if sedang and tdk_hujan and panas and normal and f_hujan:
		nkTinggi[38]=min(sedang,tdk_hujan,panas,normal,f_hujan)
	if sedang and tdk_hujan and panas and normal and f_cerah:
		nkTinggi[39]=min(sedang,tdk_hujan,panas,normal,f_cerah)
	if sedang and tdk_hujan and panas and normal and f_mendung:
		nkTinggi[40]=min(sedang,tdk_hujan,panas,normal,f_mendung)
	if sedang and tdk_hujan and panas and normal and f_hujan:
		nkTinggi[41]=min(sedang,tdk_hujan,panas,normal,f_hujan)
	if sedang and tdk_hujan and normal and normal and f_cerah:
		nkTinggi[42]=min(sedang,tdk_hujan,normal,normal,f_cerah)
	if sedang and tdk_hujan and normal and normal and f_mendung:
		nkTinggi[43]=min(sedang,tdk_hujan,normal,normal,f_mendung)
	if sedang and tdk_hujan and normal and normal and f_hujan:
		nkTinggi[44]=min(sedang,tdk_hujan,normal,normal,f_hujan)
	if sedang and tdk_hujan and normal and normal and f_cerah:
		nkTinggi[45]=min(sedang,tdk_hujan,normal,normal,f_cerah)
	if sedang and tdk_hujan and normal and normal and f_mendung:
		nkTinggi[46]=min(sedang,tdk_hujan,normal,normal,f_mendung)
	if sedang and tdk_hujan and normal and normal and f_hujan:
		nkTinggi[47]=min(sedang,tdk_hujan,normal,normal,f_hujan)
	if sedang and tdk_hujan and dingin and normal and f_cerah:
		nkTinggi[48]=min(sedang,tdk_hujan,dingin,normal,f_cerah)
	if sedang and tdk_hujan and dingin and normal and f_mendung:
		nkTinggi[49]=min(sedang,tdk_hujan,dingin,normal,f_mendung)
	if sedang and tdk_hujan and dingin and normal and f_hujan:
		nkTinggi[50]=min(sedang,tdk_hujan,dingin,normal,f_hujan)
	if sedang and tdk_hujan and dingin and normal and f_cerah:
		nkTinggi[51]=min(sedang,tdk_hujan,dingin,normal,f_cerah)
	if sedang and tdk_hujan and dingin and normal and f_mendung:
		nkTinggi[52]=min(sedang,tdk_hujan,dingin,normal,f_mendung)
	if sedang and tdk_hujan and dingin and normal and f_hujan:
		nkTinggi[53]=min(sedang,tdk_hujan,dingin,normal,f_hujan)

	if sedang and hujan and panas and normal and f_cerah:
		nkRendah[54]=min(sedang,hujan,panas,normal,f_cerah)
	if sedang and hujan and panas and normal and f_mendung:
		nkRendah[55]=min(sedang,hujan,panas,normal,f_mendung)
	if sedang and hujan and panas and normal and f_hujan:
		nkRendah[56]=min(sedang,hujan,panas,normal,f_hujan)
	if sedang and hujan and panas and normal and f_cerah:
		nkRendah[57]=min(sedang,hujan,panas,normal,f_cerah)
	if sedang and hujan and panas and normal and f_mendung:
		nkRendah[58]=min(sedang,hujan,panas,normal,f_mendung)
	if sedang and hujan and panas and normal and f_hujan:
		nkRendah[59]=min(sedang,hujan,panas,normal,f_hujan)
	if sedang and hujan and normal and normal and f_cerah:
		nkRendah[60]=min(sedang,hujan,normal,normal,f_cerah)
	if sedang and hujan and normal and normal and f_mendung:
		nkRendah[61]=min(sedang,hujan,normal,normal,f_mendung)
	if sedang and hujan and normal and normal and f_hujan:
		nkRendah[62]=min(sedang,hujan,normal,normal,f_hujan)
	if sedang and hujan and normal and normal and f_cerah:
		nkRendah[63]=min(sedang,hujan,normal,normal,f_cerah)
	if sedang and hujan and normal and normal and f_mendung:
		nkRendah[64]=min(sedang,hujan,normal,normal,f_mendung)
	if sedang and hujan and normal and normal and f_hujan:
		nkRendah[65]=min(sedang,hujan,normal,normal,f_hujan)
	if sedang and hujan and dingin and normal and f_cerah:
		nkRendah[66]=min(sedang,hujan,dingin,normal,f_cerah)
	if sedang and hujan and dingin and normal and f_mendung:
		nkRendah[67]=min(sedang,hujan,dingin,normal,f_mendung)
	if sedang and hujan and dingin and normal and f_hujan:
		nkRendah[68]=min(sedang,hujan,dingin,normal,f_hujan)
	if sedang and hujan and dingin and normal and f_cerah:
		nkRendah[69]=min(sedang,hujan,dingin,normal,f_cerah)
	if sedang and hujan and dingin and normal and f_mendung:
		nkRendah[70]=min(sedang,hujan,dingin,normal,f_mendung)
	if sedang and hujan and dingin and normal and f_hujan:
		nkRendah[71]=min(sedang,hujan,dingin,normal,f_hujan)

	#basah
	if basah and tdk_hujan and panas and normal and f_cerah:
		nkRendah[72]=min(basah,tdk_hujan,panas,normal,f_cerah)
	if basah and tdk_hujan and panas and normal and f_mendung:
		nkRendah[73]=min(basah,tdk_hujan,panas,normal,f_mendung)
	if basah and tdk_hujan and panas and normal and f_hujan:
		nkRendah[74]=min(basah,tdk_hujan,panas,normal,f_hujan)
	if basah and tdk_hujan and panas and normal and f_cerah:
		nkRendah[75]=min(basah,tdk_hujan,panas,normal,f_cerah)
	if basah and tdk_hujan and panas and normal and f_mendung:
		nkRendah[76]=min(basah,tdk_hujan,panas,normal,f_mendung)
	if basah and tdk_hujan and panas and normal and f_hujan:
		nkRendah[77]=min(basah,tdk_hujan,panas,normal,f_hujan)
	if basah and tdk_hujan and normal and normal and f_cerah:
		nkRendah[78]=min(basah,tdk_hujan,normal,normal,f_cerah)
	if basah and tdk_hujan and normal and normal and f_mendung:
		nkRendah[79]=min(basah,tdk_hujan,normal,normal,f_mendung)
	if basah and tdk_hujan and normal and normal and f_hujan:
		nkRendah[80]=min(basah,tdk_hujan,normal,normal,f_hujan)
	if basah and tdk_hujan and normal and normal and f_cerah:
		nkRendah[81]=min(basah,tdk_hujan,normal,normal,f_cerah)
	if basah and tdk_hujan and normal and normal and f_mendung:
		nkRendah[82]=min(basah,tdk_hujan,normal,normal,f_mendung)
	if basah and tdk_hujan and normal and normal and f_hujan:
		nkRendah[83]=min(basah,tdk_hujan,normal,normal,f_hujan)
	if basah and tdk_hujan and dingin and normal and f_cerah:
		nkRendah[84]=min(basah,tdk_hujan,dingin,normal,f_cerah)
	if basah and tdk_hujan and dingin and normal and f_mendung:
		nkRendah[85]=min(basah,tdk_hujan,dingin,normal,f_mendung)
	if basah and tdk_hujan and dingin and normal and f_hujan:
		nkRendah[86]=min(basah,tdk_hujan,dingin,normal,f_hujan)
	if basah and tdk_hujan and dingin and normal and f_cerah:
		nkRendah[87]=min(basah,tdk_hujan,dingin,normal,f_cerah)
	if basah and tdk_hujan and dingin and normal and f_mendung:
		nkRendah[88]=min(basah,tdk_hujan,dingin,normal,f_mendung)
	if basah and tdk_hujan and dingin and normal and f_hujan:
		nkRendah[89]=min(basah,tdk_hujan,dingin,normal,f_hujan)

	if basah and hujan and panas and normal and f_cerah:
		nkRendah[90]=min(basah,hujan,panas,normal,f_cerah)
	if basah and hujan and panas and normal and f_mendung:
		nkRendah[91]=min(basah,hujan,panas,normal,f_mendung)
	if basah and hujan and panas and normal and f_hujan:
		nkRendah[92]=min(basah,hujan,panas,normal,f_hujan)
	if basah and hujan and panas and normal and f_cerah:
		nkRendah[93]=min(basah,hujan,panas,normal,f_cerah)
	if basah and hujan and panas and normal and f_mendung:
		nkRendah[94]=min(basah,hujan,panas,normal,f_mendung)
	if basah and hujan and panas and normal and f_hujan:
		nkRendah[95]=min(basah,hujan,panas,normal,f_hujan)
	if basah and hujan and normal and normal and f_cerah:
		nkRendah[96]=min(basah,hujan,normal,normal,f_cerah)
	if basah and hujan and normal and normal and f_mendung:
		nkRendah[97]=min(basah,hujan,normal,normal,f_mendung)
	if basah and hujan and normal and normal and f_hujan:
		nkRendah[98]=min(basah,hujan,normal,normal,f_hujan)
	if basah and hujan and normal and normal and f_cerah:
		nkRendah[99]=min(basah,hujan,normal,normal,f_cerah)
	if basah and hujan and normal and normal and f_mendung:
		nkRendah[100]=min(basah,hujan,normal,normal,f_mendung)
	if basah and hujan and normal and normal and f_hujan:
		nkRendah[101]=min(basah,hujan,normal,normal,f_hujan)
	if basah and hujan and dingin and normal and f_cerah:
		nkRendah[102]=min(basah,hujan,dingin,normal,f_cerah)
	if basah and hujan and dingin and normal and f_mendung:
		nkRendah[103]=min(basah,hujan,dingin,normal,f_mendung)
	if basah and hujan and dingin and normal and f_hujan:
		nkRendah[104]=min(basah,hujan,dingin,normal,f_hujan)
	if basah and hujan and dingin and normal and f_cerah:
		nkRendah[105]=min(basah,hujan,dingin,normal,f_cerah)
	if basah and hujan and dingin and normal and f_mendung:
		nkRendah[106]=min(basah,hujan,dingin,normal,f_mendung)
	if basah and hujan and dingin and normal and f_hujan:
		nkRendah[107]=min(basah,hujan,dingin,normal,f_hujan)
	
	print("======================")
	print("FUZZY OUTPUT");
	print("======================")
	for i in range(108):
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
	print ("Nilai Kelayakan : " +str(status))
	return status;