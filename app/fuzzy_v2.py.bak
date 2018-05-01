import datetime, time

def calculate(soil,rain,forecast,forecast2):
	# START FUZZIFIKASI
	# inisialisasi linguistik
	basah 	= 0;
	sedang	= 0;
	kering	= 0;

	hujan 	  = 0;
	tdk_hujan = 0;

	f_cerah	  = 0;
	f_mendung = 0;
	f_hujan   = 0;

	f2_cerah  = 0;
	f2_mendung= 0;
	f2_hujan  = 0;

	#inisialisasi batas
	l_kering = 0;
	u_kering = 50;
	l_sedang = 200;
	u_sedang = 350;
	l_basah	 = 500;
	u_basah  = 1024;

	l_tdkhujan = 0;
	u_tdkhujan = 200;
	l_hujan	 = 400;
	u_hujan	 = 1024;

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

	#temperature
	if rain < u_tdkhujan:
		tdk_hujan = 1;
	elif rain >= u_tdkhujan and rain <= l_hujan:
		tdk_hujan = (rain * (-1.0) + l_hujan) / (l_hujan - u_tdkhujan);
		hujan  = (rain - u_tdkhujan) * 1.0 / (l_hujan - u_tdkhujan);
	elif rain > l_hujan:
		hujan = 1;

	if forecast == 0:
		f_cerah 	= 1;
	elif forecast == 1:
		f_mendung 	= 1;
	elif forecast == 2:
		f_hujan 	= 1;
	
	if forecast2 == 0:
		f2_cerah 	= 1;
	elif forecast2 == 1:
		f2_mendung 	= 1;
	elif forecast2 == 2:
		f2_hujan 	= 1;
	
	#print linguistik
	print "FUZZYFIKASI";
	print "SOIL = %d" % (soil);
	print "BASAH  : "+str(basah);
	print "SEDANG : "+str(sedang);
	print "KERING : "+str(kering);

	# # print "SUHU = %d" % (suhu);
	# # print "DINGIN : "+str(dingin);
	# # print "SEJUK  : "+str(sejuk);
	# # print "PANAS  : "+str(panas);

	print "HUJAN";
	print "HUJAN  	 : "+str(hujan);
	print "TDK_HUJAN : "+str(tdk_hujan);

	# # print "CURRENT WEATHER";
	# # print "CERAH  : "+str(w_cerah);
	# # print "MENDUNG: "+str(w_mendung);
	# # print "HUJAN  : "+str(w_hujan);

	print "FORECAST 1";
	print "CERAH  : "+str(f_cerah);
	print "MENDUNG: "+str(f_mendung);
	print "HUJAN  : "+str(f_hujan);

	print "FORECAST 2";
	print "CERAH  : "+str(f2_cerah);
	print "MENDUNG: "+str(f2_mendung);
	print "HUJAN  : "+str(f2_hujan);


	#Inferensi
	nkRendah=[];
	nkTinggi=[];
	rendah=0;
	tinggi=0;

	for i in range(54):
 		nkRendah.append(0);
 		nkTinggi.append(0);

 	if kering and tdk_hujan and f_cerah and f2_cerah:
 		nkTinggi[0]=min(kering,tdk_hujan,f_cerah,f2_cerah)
 	if kering and tdk_hujan and f_cerah and f2_mendung:
 		nkTinggi[1]=min(kering,tdk_hujan,f_cerah,f2_mendung)
 	if kering and tdk_hujan and f_cerah and f2_hujan:
 		nkTinggi[2]=min(kering,tdk_hujan,f_cerah,f2_hujan)
 	if kering and tdk_hujan and f_mendung and f2_cerah:
 		nkTinggi[3]=min(kering,tdk_hujan,f_mendung,f2_cerah)
 	if kering and tdk_hujan and f_mendung and f2_mendung:
 		nkTinggi[4]=min(kering,tdk_hujan,f_mendung,f2_mendung)
 	if kering and tdk_hujan and f_mendung and f2_hujan:
 		nkTinggi[5]=min(kering,tdk_hujan,f_mendung,f2_hujan)
 	if kering and tdk_hujan and f_hujan and f2_cerah:
 		nkTinggi[6]=min(kering,tdk_hujan,f_hujan,f2_cerah)
 	if kering and tdk_hujan and f_hujan and f2_mendung:
 		nkTinggi[7]=min(kering,tdk_hujan,f_hujan,f2_mendung)
 	if kering and tdk_hujan and f_hujan and f2_hujan:
 		nkTinggi[8]=min(kering,tdk_hujan,f_hujan,f2_hujan)
 	if kering and hujan and f_cerah and f2_cerah:
 		nkTinggi[9]=min(kering,hujan,f_cerah,f2_cerah)
 	if kering and hujan and f_cerah and f2_mendung:
 		nkTinggi[10]=min(kering,hujan,f_cerah,f2_mendung)
 	if kering and hujan and f_cerah and f2_hujan:
 		nkTinggi[11]=min(kering,hujan,f_cerah,f2_hujan)
 	if kering and hujan and f_mendung and f2_cerah:
 		nkTinggi[12]=min(kering,hujan,f_mendung,f2_cerah)
 	if kering and hujan and f_mendung and f2_mendung:
 		nkTinggi[13]=min(kering,hujan,f_mendung,f2_mendung)
 	if kering and hujan and f_mendung and f2_hujan:
 		nkTinggi[14]=min(kering,hujan,f_mendung,f2_hujan)
 	if kering and hujan and f_hujan and f2_cerah:
 		nkTinggi[15]=min(kering,hujan,f_hujan,f2_cerah)
 	if kering and hujan and f_hujan and f2_mendung:
 		nkTinggi[16]=min(kering,hujan,f_hujan,f2_mendung)
 	if kering and hujan and f_hujan and f2_hujan:
 		nkRendah[17]=min(kering,hujan,f_hujan,f2_hujan)

 	if sedang and tdk_hujan and f_cerah and f2_cerah:
 		nkTinggi[18]=min(sedang,tdk_hujan,f_cerah,f2_cerah)
 	if sedang and tdk_hujan and f_cerah and f2_mendung:
 		nkTinggi[19]=min(sedang,tdk_hujan,f_cerah,f2_mendung)
 	if sedang and tdk_hujan and f_cerah and f2_hujan:
 		nkTinggi[20]=min(sedang,tdk_hujan,f_cerah,f2_hujan)
 	if sedang and tdk_hujan and f_mendung and f2_cerah:
 		nkTinggi[21]=min(sedang,tdk_hujan,f_mendung,f2_cerah)
 	if sedang and tdk_hujan and f_mendung and f2_mendung:
 		nkTinggi[22]=min(sedang,tdk_hujan,f_mendung,f2_mendung)
 	if sedang and tdk_hujan and f_mendung and f2_hujan:
 		nkTinggi[23]=min(sedang,tdk_hujan,f_mendung,f2_hujan)
 	if sedang and tdk_hujan and f_hujan and f2_cerah:
 		nkTinggi[24]=min(sedang,tdk_hujan,f_hujan,f2_cerah)
 	if sedang and tdk_hujan and f_hujan and f2_mendung:
 		nkTinggi[25]=min(sedang,tdk_hujan,f_hujan,f2_mendung)
 	if sedang and tdk_hujan and f_hujan and f2_hujan:
 		nkRendah[26]=min(sedang,tdk_hujan,f_hujan,f2_hujan)
 	if sedang and hujan and f_cerah and f2_cerah:
 		nkRendah[27]=min(sedang,hujan,f_cerah,f2_cerah)
 	if sedang and hujan and f_cerah and f2_mendung:
 		nkRendah[28]=min(sedang,hujan,f_cerah,f2_mendung)
 	if sedang and hujan and f_cerah and f2_hujan:
 		nkRendah[29]=min(sedang,hujan,f_cerah,f2_hujan)
 	if sedang and hujan and f_mendung and f2_cerah:
 		nkRendah[30]=min(sedang,hujan,f_mendung,f2_cerah)
 	if sedang and hujan and f_mendung and f2_mendung:
 		nkRendah[31]=min(sedang,hujan,f_mendung,f2_mendung)
 	if sedang and hujan and f_mendung and f2_hujan:
 		nkRendah[32]=min(sedang,hujan,f_mendung,f2_hujan)
 	if sedang and hujan and f_hujan and f2_cerah:
 		nkRendah[33]=min(sedang,hujan,f_hujan,f2_cerah)
 	if sedang and hujan and f_hujan and f2_mendung:
 		nkRendah[34]=min(sedang,hujan,f_hujan,f2_mendung)
 	if sedang and hujan and f_hujan and f2_hujan:
 		nkRendah[35]=min(sedang,hujan,f_hujan,f2_hujan)

 	if basah and tdk_hujan and f_cerah and f2_cerah:
 		nkRendah[36]=min(basah,tdk_hujan,f_cerah,f2_cerah)
 	if basah and tdk_hujan and f_cerah and f2_mendung:
 		nkRendah[37]=min(basah,tdk_hujan,f_cerah,f2_mendung)
 	if basah and tdk_hujan and f_cerah and f2_hujan:
 		nkRendah[38]=min(basah,tdk_hujan,f_cerah,f2_hujan)
 	if basah and tdk_hujan and f_mendung and f2_cerah:
 		nkRendah[39]=min(basah,tdk_hujan,f_mendung,f2_cerah)
 	if basah and tdk_hujan and f_mendung and f2_mendung:
 		nkRendah[40]=min(basah,tdk_hujan,f_mendung,f2_mendung)
 	if basah and tdk_hujan and f_mendung and f2_hujan:
 		nkRendah[41]=min(basah,tdk_hujan,f_mendung,f2_hujan)
 	if basah and tdk_hujan and f_hujan and f2_cerah:
 		nkRendah[42]=min(basah,tdk_hujan,f_hujan,f2_cerah)
 	if basah and tdk_hujan and f_hujan and f2_mendung:
 		nkRendah[43]=min(basah,tdk_hujan,f_hujan,f2_mendung)
 	if basah and tdk_hujan and f_hujan and f2_hujan:
 		nkRendah[44]=min(basah,tdk_hujan,f_hujan,f2_hujan)
 	if basah and hujan and f_cerah and f2_cerah:
 		nkRendah[45]=min(basah,hujan,f_cerah,f2_cerah)
 	if basah and hujan and f_cerah and f2_mendung:
 		nkRendah[46]=min(basah,hujan,f_cerah,f2_mendung)
 	if basah and hujan and f_cerah and f2_hujan:
 		nkRendah[47]=min(basah,hujan,f_cerah,f2_hujan)
 	if basah and hujan and f_mendung and f2_cerah:
 		nkRendah[48]=min(basah,hujan,f_mendung,f2_cerah)
 	if basah and hujan and f_mendung and f2_mendung:
 		nkRendah[49]=min(basah,hujan,f_mendung,f2_mendung)
 	if basah and hujan and f_mendung and f2_hujan:
 		nkRendah[50]=min(basah,hujan,f_mendung,f2_hujan)
 	if basah and hujan and f_hujan and f2_cerah:
 		nkRendah[51]=min(basah,hujan,f_hujan,f2_cerah)
 	if basah and hujan and f_hujan and f2_mendung:
 		nkRendah[52]=min(basah,hujan,f_hujan,f2_mendung)
 	if basah and hujan and f_hujan and f2_hujan:
 		nkRendah[53]=min(basah,hujan,f_hujan,f2_hujan)
	
	#nkRendah.append(5);
	#nkRendah.insert(1,6);
	print "FUZZY OUTPUT";
	for i in range(54):
		if nkRendah[i]>0:
			print "Rule "+str(i+1)+ " Rendah : "+str(nkRendah[i]);
			if nkRendah[i]>rendah:
				rendah=nkRendah[i];
		if nkTinggi[i]>0:
			print "Rule "+str(i+1)+ " Tinggi : "+str(nkTinggi[i]);
			if nkTinggi[i]>tinggi:
				tinggi=nkTinggi[i];

	if rendah>0:
	 	print "Rendah("+str(rendah)+")";
	if tinggi>0:
	 	print "Tinggi("+str(tinggi)+")";


	#DEFUZIFIKASI
	#batas
	print "DEFUZZYFIKASI";
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
		print str(count) + ":" + str(y[i]);
		i += 1;
	mamdani = mamdani_pembilang/mamdani_penyebut;
	#print "Nilai Kelayakan : "+str(mamdani);
	return mamdani;
