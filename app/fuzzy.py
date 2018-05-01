import datetime, time

def calculate(soil,suhu,rain,weather,forecast,forecast2):
        # START FUZZIFIKASI
        # inisialisasi linguistik
        basah   = 0;
        sedang  = 0;
        kering  = 0;

        panas   = 0;
        sejuk   = 0;
        dingin  = 0;

        hujan     = 0;
        tdk_hujan = 0;

        w_cerah   = 0;
        w_mendung = 0;
        w_hujan   = 0;

        f_cerah   = 0;
        f_mendung = 0;
        f_hujan   = 0;

        f2_cerah  = 0;
        f2_mendung= 0;
        f2_hujan  = 0;

        #inisialisasi batas
        l_kering = 0;
        u_kering = 100;
        l_sedang = 300;
        u_sedang = 400;
        l_basah  = 600;
        u_basah  = 1024;

        l_dingin = 0;
        u_dingin = 16;
        l_sejuk  = 18;
        u_sejuk  = 28;
        l_panas  = 36;
        u_panas  = 100;

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
        if suhu < u_dingin:
                dingin = 1;
        elif suhu >= u_dingin and suhu <= l_sejuk:
                dingin = (suhu * (-1.0) + l_sejuk) / (l_sejuk - u_dingin);
                sejuk  = (suhu - u_dingin) * 1.0 / (l_sejuk - u_dingin);
        elif suhu >= l_sejuk and suhu <= u_sejuk:
                sejuk = 1;
        elif suhu >= u_sejuk and suhu <= l_panas:
                sejuk = (suhu * (-1.0) + l_panas) / (l_panas - u_sejuk);
                panas = (suhu - u_sejuk) * 1.0 / (l_panas - u_sejuk);
        elif suhu > l_panas:
                panas = 1;

        # sensor rain
        if rain == 1:
                hujan = 1;
        else :
                tdk_hujan = 1;

        #sensor weather
        if weather == 0:
                w_cerah         = 1;
        elif weather == 1:
                w_mendung       = 1;
        elif weather == 2:
                w_hujan         = 1;

        if forecast == 0:
                f_cerah         = 1;
        elif forecast == 1:
                f_mendung       = 1;
        elif forecast == 2:
                f_hujan         = 1;
        
        if forecast2 == 0:
                f2_cerah        = 1;
        elif forecast2 == 1:
                f2_mendung      = 1;
        elif forecast2 == 2:
                f2_hujan        = 1;
        
        #print linguistik
        # print "FUZZYFIKASI";
        # print "SOIL = %d" % (soil);
        # print "BASAH  : "+str(basah);
        # print "SEDANG : "+str(sedang);
        # print "KERING : "+str(kering);

        # print "SUHU = %d" % (suhu);
        # print "DINGIN : "+str(dingin);
        # print "SEJUK  : "+str(sejuk);
        # print "PANAS  : "+str(panas);

        # print "HUJAN";
        # print "HUJAN           : "+str(hujan);
        # print "TDK_HUJAN : "+str(tdk_hujan);

        # print "CURRENT WEATHER";
        # print "CERAH  : "+str(w_cerah);
        # print "MENDUNG: "+str(w_mendung);
        # print "HUJAN  : "+str(w_hujan);

        # print "FORECAST 1";
        # print "CERAH  : "+str(f_cerah);
        # print "MENDUNG: "+str(f_mendung);
        # print "HUJAN  : "+str(f_hujan);

        # print "FORECAST 2";
        # print "CERAH  : "+str(f2_cerah);
        # print "MENDUNG: "+str(f2_mendung);
        # print "HUJAN  : "+str(f2_hujan);


        #Inferensi
        nkRendah=[];
        nkTinggi=[];
        rendah=0;
        tinggi=0;

        for i in range(486):
                nkRendah.append(0);
                nkTinggi.append(0);

        if basah and panas and hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[0]=min(basah,panas,hujan,w_cerah,f_cerah,f2_cerah);

        if basah and panas and hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[1]=min(basah,panas,hujan,w_cerah,f_cerah,f2_mendung);

        if basah and panas and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[2]=min(basah,panas,hujan,w_cerah,f_cerah,f2_hujan);

        if basah and panas and hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[3]=min(basah,panas,hujan,w_cerah,f_mendung,f2_cerah);
        
        if basah and panas and hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[4]=min(basah,panas,hujan,w_cerah,f_mendung,f2_mendung);
        
        if basah and panas and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[5]=min(basah,panas,hujan,w_cerah,f_mendung,f2_hujan);

        if basah and panas and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[6]=min(basah,panas,hujan,w_cerah,f_hujan,f2_cerah);

        if basah and panas and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[7]=min(basah,panas,hujan,w_cerah,f_hujan,f2_mendung);
        
        if basah and panas and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[8]=min(basah,panas,hujan,w_cerah,f_hujan,f2_hujan);

        if basah and panas and hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[9]=min(basah,panas,hujan,w_mendung,f_cerah,f2_cerah);

        if basah and panas and hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[10]=min(basah,panas,hujan,w_mendung,f_cerah,f2_mendung);

        if basah and panas and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[11]=min(basah,panas,hujan,w_mendung,f_cerah,f2_hujan);

        if basah and panas and hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[12]=min(basah,panas,hujan,w_mendung,f_mendung,f2_cerah);

        if basah and panas and hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[13]=min(basah,panas,hujan,w_mendung,f_mendung,f2_mendung);

        if basah and panas and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[14]=min(basah,panas,hujan,w_mendung,f_mendung,f2_hujan);

        if basah and panas and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[15]=min(basah,panas,hujan,w_mendung,f_hujan,f2_cerah);

        if basah and panas and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[16]=min(basah,panas,hujan,w_mendung,f_hujan,f2_mendung);

        if basah and panas and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[17]=min(basah,panas,hujan,w_mendung,f_hujan,f2_hujan);

        if basah and panas and hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[18]=min(basah,panas,hujan,w_hujan,f_cerah,f2_cerah);

        if basah and panas and hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[19]=min(basah,panas,hujan,w_hujan,f_cerah,f2_mendung);

        if basah and panas and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[20]=min(basah,panas,hujan,w_hujan,f_cerah,f2_hujan);

        if basah and panas and hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[21]=min(basah,panas,hujan,w_hujan,f_mendung,f2_cerah);

        if basah and panas and hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[22]=min(basah,panas,hujan,w_hujan,f_mendung,f2_mendung);

        if basah and panas and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[23]=min(basah,panas,hujan,w_hujan,f_mendung,f2_hujan);

        if basah and panas and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[24]=min(basah,panas,hujan,w_hujan,f_hujan,f2_cerah);

        if basah and panas and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[25]=min(basah,panas,hujan,w_hujan,f_hujan,f2_mendung);

        if basah and panas and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[26]=min(basah,panas,hujan,w_hujan,f_hujan,f2_hujan);

        if basah and panas and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[27]=min(basah,panas,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if basah and panas and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[28]=min(basah,panas,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if basah and panas and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[29]=min(basah,panas,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if basah and panas and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[30]=min(basah,panas,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if basah and panas and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[31]=min(basah,panas,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if basah and panas and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[32]=min(basah,panas,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if basah and panas and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[33]=min(basah,panas,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if basah and panas and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[34]=min(basah,panas,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if basah and panas and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[35]=min(basah,panas,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if basah and panas and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[36]=min(basah,panas,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if basah and panas and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[37]=min(basah,panas,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if basah and panas and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[38]=min(basah,panas,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if basah and panas and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[39]=min(basah,panas,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if basah and panas and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[40]=min(basah,panas,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if basah and panas and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[41]=min(basah,panas,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if basah and panas and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[42]=min(basah,panas,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if basah and panas and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[43]=min(basah,panas,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if basah and panas and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[44]=min(basah,panas,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if basah and panas and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[45]=min(basah,panas,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if basah and panas and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[46]=min(basah,panas,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if basah and panas and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[47]=min(basah,panas,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if basah and panas and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[48]=min(basah,panas,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if basah and panas and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[49]=min(basah,panas,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if basah and panas and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[50]=min(basah,panas,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if basah and panas and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[51]=min(basah,panas,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if basah and panas and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[52]=min(basah,panas,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if basah and panas and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[53]=min(basah,panas,tdk_hujan,w_hujan,f_hujan,f2_hujan);
        
        if basah and sejuk and hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[54]=min(basah,sejuk,hujan,w_cerah,f_cerah,f2_cerah);

        if basah and sejuk and hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[55]=min(basah,sejuk,hujan,w_cerah,f_cerah,f2_mendung);

        if basah and sejuk and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[56]=min(basah,sejuk,hujan,w_cerah,f_cerah,f2_hujan);

        if basah and sejuk and hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[57]=min(basah,sejuk,hujan,w_cerah,f_mendung,f2_cerah);
        
        if basah and sejuk and hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[58]=min(basah,sejuk,hujan,w_cerah,f_mendung,f2_mendung);
        
        if basah and sejuk and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[59]=min(basah,sejuk,hujan,w_cerah,f_mendung,f2_hujan);

        if basah and sejuk and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[60]=min(basah,sejuk,hujan,w_cerah,f_hujan,f2_cerah);

        if basah and sejuk and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[61]=min(basah,sejuk,hujan,w_cerah,f_hujan,f2_mendung);
        
        if basah and sejuk and hujan and w_cerah and f_hujan and f2_HHHn:
                nkRendah[62]=min(basah,sejuk,hujan,w_cerah,f_hujan,f2_hujan);

        if basah and sejuk and hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[63]=min(basah,sejuk,hujan,w_mendung,f_cerah,f2_cerah);

        if basah and sejuk and hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[64]=min(basah,sejuk,hujan,w_mendung,f_cerah,f2_mendung);

        if basah and sejuk and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[65]=min(basah,sejuk,hujan,w_mendung,f_cerah,f2_hujan);

        if basah and sejuk and hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[66]=min(basah,sejuk,hujan,w_mendung,f_mendung,f2_cerah);

        if basah and sejuk and hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[67]=min(basah,sejuk,hujan,w_mendung,f_mendung,f2_mendung);

        if basah and sejuk and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[68]=min(basah,sejuk,hujan,w_mendung,f_mendung,f2_hujan);

        if basah and sejuk and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[69]=min(basah,sejuk,hujan,w_mendung,f_hujan,f2_cerah);

        if basah and sejuk and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[70]=min(basah,sejuk,hujan,w_mendung,f_hujan,f2_mendung);

        if basah and sejuk and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[71]=min(basah,sejuk,hujan,w_mendung,f_hujan,f2_hujan);

        if basah and sejuk and hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[72]=min(basah,sejuk,hujan,w_hujan,f_cerah,f2_cerah);

        if basah and sejuk and hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[73]=min(basah,sejuk,hujan,w_hujan,f_cerah,f2_mendung);

        if basah and sejuk and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[74]=min(basah,sejuk,hujan,w_hujan,f_cerah,f2_hujan);

        if basah and sejuk and hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[75]=min(basah,sejuk,hujan,w_hujan,f_mendung,f2_cerah);

        if basah and sejuk and hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[76]=min(basah,sejuk,hujan,w_hujan,f_mendung,f2_mendung);

        if basah and sejuk and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[77]=min(basah,sejuk,hujan,w_hujan,f_mendung,f2_hujan);

        if basah and sejuk and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[78]=min(basah,sejuk,hujan,w_hujan,f_hujan,f2_cerah);

        if basah and sejuk and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[79]=min(basah,sejuk,hujan,w_hujan,f_hujan,f2_mendung);

        if basah and sejuk and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[80]=min(basah,sejuk,hujan,w_hujan,f_hujan,f2_hujan);

        if basah and sejuk and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[81]=min(basah,sejuk,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if basah and sejuk and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[82]=min(basah,sejuk,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if basah and sejuk and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[83]=min(basah,sejuk,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if basah and sejuk and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[84]=min(basah,sejuk,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if basah and sejuk and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[85]=min(basah,sejuk,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if basah and sejuk and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[86]=min(basah,sejuk,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if basah and sejuk and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[87]=min(basah,sejuk,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if basah and sejuk and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[88]=min(basah,sejuk,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if basah and sejuk and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[89]=min(basah,sejuk,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if basah and sejuk and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[90]=min(basah,sejuk,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if basah and sejuk and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[91]=min(basah,sejuk,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if basah and sejuk and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[92]=min(basah,sejuk,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if basah and sejuk and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[93]=min(basah,sejuk,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if basah and sejuk and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[94]=min(basah,sejuk,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if basah and sejuk and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[95]=min(basah,sejuk,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if basah and sejuk and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[96]=min(basah,sejuk,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if basah and sejuk and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[97]=min(basah,sejuk,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if basah and sejuk and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[98]=min(basah,sejuk,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if basah and sejuk and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[99]=min(basah,sejuk,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if basah and sejuk and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[100]=min(basah,sejuk,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if basah and sejuk and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[101]=min(basah,sejuk,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if basah and sejuk and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[102]=min(basah,sejuk,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if basah and sejuk and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[103]=min(basah,sejuk,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if basah and sejuk and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[104]=min(basah,sejuk,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if basah and sejuk and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[105]=min(basah,sejuk,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if basah and sejuk and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[106]=min(basah,sejuk,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if basah and sejuk and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[107]=min(basah,sejuk,tdk_hujan,w_hujan,f_hujan,f2_hujan);

        if basah and dingin and hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[108]=min(basah,dingin,hujan,w_cerah,f_cerah,f2_cerah);

        if basah and dingin and hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[109]=min(basah,dingin,hujan,w_cerah,f_cerah,f2_mendung);

        if basah and dingin and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[110]=min(basah,dingin,hujan,w_cerah,f_cerah,f2_hujan);

        if basah and dingin and hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[111]=min(basah,dingin,hujan,w_cerah,f_mendung,f2_cerah);
        
        if basah and dingin and hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[112]=min(basah,dingin,hujan,w_cerah,f_mendung,f2_mendung);
        
        if basah and dingin and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[113]=min(basah,dingin,hujan,w_cerah,f_mendung,f2_hujan);

        if basah and dingin and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[114]=min(basah,dingin,hujan,w_cerah,f_hujan,f2_cerah);

        if basah and dingin and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[115]=min(basah,dingin,hujan,w_cerah,f_hujan,f2_mendung);
        
        if basah and dingin and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[116]=min(basah,dingin,hujan,w_cerah,f_hujan,f2_hujan);

        if basah and dingin and hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[117]=min(basah,dingin,hujan,w_mendung,f_cerah,f2_cerah);

        if basah and dingin and hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[118]=min(basah,dingin,hujan,w_mendung,f_cerah,f2_mendung);

        if basah and dingin and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[119]=min(basah,dingin,hujan,w_mendung,f_cerah,f2_hujan);

        if basah and dingin and hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[120]=min(basah,dingin,hujan,w_mendung,f_mendung,f2_cerah);

        if basah and dingin and hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[121]=min(basah,dingin,hujan,w_mendung,f_mendung,f2_mendung);

        if basah and dingin and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[122]=min(basah,dingin,hujan,w_mendung,f_mendung,f2_hujan);

        if basah and dingin and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[123]=min(basah,dingin,hujan,w_mendung,f_hujan,f2_cerah);

        if basah and dingin and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[124]=min(basah,dingin,hujan,w_mendung,f_hujan,f2_mendung);

        if basah and dingin and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[125]=min(basah,dingin,hujan,w_mendung,f_hujan,f2_hujan);

        if basah and dingin and hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[126]=min(basah,dingin,hujan,w_hujan,f_cerah,f2_cerah);

        if basah and dingin and hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[127]=min(basah,dingin,hujan,w_hujan,f_cerah,f2_mendung);

        if basah and dingin and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[128]=min(basah,dingin,hujan,w_hujan,f_cerah,f2_hujan);

        if basah and dingin and hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[129]=min(basah,dingin,hujan,w_hujan,f_mendung,f2_cerah);

        if basah and dingin and hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[130]=min(basah,dingin,hujan,w_hujan,f_mendung,f2_mendung);

        if basah and dingin and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[131]=min(basah,dingin,hujan,w_hujan,f_mendung,f2_hujan);

        if basah and dingin and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[132]=min(basah,dingin,hujan,w_hujan,f_hujan,f2_cerah);

        if basah and dingin and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[133]=min(basah,dingin,hujan,w_hujan,f_hujan,f2_mendung);

        if basah and dingin and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[134]=min(basah,dingin,hujan,w_hujan,f_hujan,f2_hujan);

        if basah and dingin and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[135]=min(basah,dingin,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if basah and dingin and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[136]=min(basah,dingin,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if basah and dingin and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[137]=min(basah,dingin,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if basah and dingin and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[138]=min(basah,dingin,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if basah and dingin and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[139]=min(basah,dingin,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if basah and dingin and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[140]=min(basah,dingin,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if basah and dingin and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[141]=min(basah,dingin,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if basah and dingin and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[142]=min(basah,dingin,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if basah and dingin and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[143]=min(basah,dingin,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if basah and dingin and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[144]=min(basah,dingin,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if basah and dingin and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[145]=min(basah,dingin,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if basah and dingin and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[146]=min(basah,dingin,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if basah and dingin and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[147]=min(basah,dingin,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if basah and dingin and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[148]=min(basah,dingin,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if basah and dingin and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[149]=min(basah,dingin,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if basah and dingin and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[150]=min(basah,dingin,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if basah and dingin and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[151]=min(basah,dingin,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if basah and dingin and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[152]=min(basah,dingin,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if basah and dingin and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[153]=min(basah,dingin,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if basah and dingin and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[154]=min(basah,dingin,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if basah and dingin and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[155]=min(basah,dingin,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if basah and dingin and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[156]=min(basah,dingin,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if basah and dingin and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[157]=min(basah,dingin,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if basah and dingin and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[158]=min(basah,dingin,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if basah and dingin and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[159]=min(basah,dingin,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if basah and dingin and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[160]=min(basah,dingin,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if basah and dingin and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[161]=min(basah,dingin,tdk_hujan,w_hujan,f_hujan,f2_hujan);
        


        if sedang and panas and hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[162]=min(sedang,panas,hujan,w_cerah,f_cerah,f2_cerah);

        if sedang and panas and hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[163]=min(sedang,panas,hujan,w_cerah,f_cerah,f2_mendung);

        if sedang and panas and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[164]=min(sedang,panas,hujan,w_cerah,f_cerah,f2_hujan);

        if sedang and panas and hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[165]=min(sedang,panas,hujan,w_cerah,f_mendung,f2_cerah);
        
        if sedang and panas and hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[166]=min(sedang,panas,hujan,w_cerah,f_mendung,f2_mendung);
        
        if sedang and panas and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[167]=min(sedang,panas,hujan,w_cerah,f_mendung,f2_hujan);

        if sedang and panas and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[168]=min(sedang,panas,hujan,w_cerah,f_hujan,f2_cerah);

        if sedang and panas and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[169]=min(sedang,panas,hujan,w_cerah,f_hujan,f2_mendung);
        
        if sedang and panas and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[170]=min(sedang,panas,hujan,w_cerah,f_hujan,f2_hujan);

        if sedang and panas and hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[171]=min(sedang,panas,hujan,w_mendung,f_cerah,f2_cerah);

        if sedang and panas and hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[172]=min(sedang,panas,hujan,w_mendung,f_cerah,f2_mendung);

        if sedang and panas and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[173]=min(sedang,panas,hujan,w_mendung,f_cerah,f2_hujan);

        if sedang and panas and hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[174]=min(sedang,panas,hujan,w_mendung,f_mendung,f2_cerah);

        if sedang and panas and hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[175]=min(sedang,panas,hujan,w_mendung,f_mendung,f2_mendung);

        if sedang and panas and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[176]=min(sedang,panas,hujan,w_mendung,f_mendung,f2_hujan);

        if sedang and panas and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[177]=min(sedang,panas,hujan,w_mendung,f_hujan,f2_cerah);

        if sedang and panas and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[178]=min(sedang,panas,hujan,w_mendung,f_hujan,f2_mendung);

        if sedang and panas and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[179]=min(sedang,panas,hujan,w_mendung,f_hujan,f2_hujan);

        if sedang and panas and hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[180]=min(sedang,panas,hujan,w_hujan,f_cerah,f2_cerah);

        if sedang and panas and hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[181]=min(sedang,panas,hujan,w_hujan,f_cerah,f2_mendung);

        if sedang and panas and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[182]=min(sedang,panas,hujan,w_hujan,f_cerah,f2_hujan);

        if sedang and panas and hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[183]=min(sedang,panas,hujan,w_hujan,f_mendung,f2_cerah);

        if sedang and panas and hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[184]=min(sedang,panas,hujan,w_hujan,f_mendung,f2_mendung);

        if sedang and panas and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[185]=min(sedang,panas,hujan,w_hujan,f_mendung,f2_hujan);

        if sedang and panas and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[186]=min(sedang,panas,hujan,w_hujan,f_hujan,f2_cerah);

        if sedang and panas and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[187]=min(sedang,panas,hujan,w_hujan,f_hujan,f2_mendung);

        if sedang and panas and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[188]=min(sedang,panas,hujan,w_hujan,f_hujan,f2_hujan);

        if sedang and panas and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[189]=min(sedang,panas,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if sedang and panas and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[190]=min(sedang,panas,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if sedang and panas and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[191]=min(sedang,panas,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if sedang and panas and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[192]=min(sedang,panas,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if sedang and panas and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[193]=min(sedang,panas,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if sedang and panas and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[194]=min(sedang,panas,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if sedang and panas and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[195]=min(sedang,panas,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if sedang and panas and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[196]=min(sedang,panas,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if sedang and panas and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[197]=min(sedang,panas,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if sedang and panas and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[198]=min(sedang,panas,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if sedang and panas and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[199]=min(sedang,panas,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if sedang and panas and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[200]=min(sedang,panas,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if sedang and panas and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[201]=min(sedang,panas,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if sedang and panas and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[202]=min(sedang,panas,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if sedang and panas and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[203]=min(sedang,panas,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if sedang and panas and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[204]=min(sedang,panas,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if sedang and panas and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkTinggi[205]=min(sedang,panas,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if sedang and panas and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[206]=min(sedang,panas,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if sedang and panas and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[207]=min(sedang,panas,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if sedang and panas and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[208]=min(sedang,panas,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if sedang and panas and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[209]=min(sedang,panas,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if sedang and panas and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[210]=min(sedang,panas,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if sedang and panas and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[211]=min(sedang,panas,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if sedang and panas and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[212]=min(sedang,panas,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if sedang and panas and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[213]=min(sedang,panas,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if sedang and panas and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[214]=min(sedang,panas,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if sedang and panas and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[215]=min(sedang,panas,tdk_hujan,w_hujan,f_hujan,f2_hujan);
        
        if sedang and sejuk and hujan and w_cerah and f_cerah and f2_cerah:
                nkRendah[216]=min(sedang,sejuk,hujan,w_cerah,f_cerah,f2_cerah);

        if sedang and sejuk and hujan and w_cerah and f_cerah and f2_mendung:
                nkRendah[217]=min(sedang,sejuk,hujan,w_cerah,f_cerah,f2_mendung);

        if sedang and sejuk and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[218]=min(sedang,sejuk,hujan,w_cerah,f_cerah,f2_hujan);

        if sedang and sejuk and hujan and w_cerah and f_mendung and f2_cerah:
                nkRendah[219]=min(sedang,sejuk,hujan,w_cerah,f_mendung,f2_cerah);
        
        if sedang and sejuk and hujan and w_cerah and f_mendung and f2_mendung:
                nkRendah[220]=min(sedang,sejuk,hujan,w_cerah,f_mendung,f2_mendung);
        
        if sedang and sejuk and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[221]=min(sedang,sejuk,hujan,w_cerah,f_mendung,f2_hujan);

        if sedang and sejuk and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[222]=min(sedang,sejuk,hujan,w_cerah,f_hujan,f2_cerah);

        if sedang and sejuk and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[223]=min(sedang,sejuk,hujan,w_cerah,f_hujan,f2_mendung);
        
        if sedang and sejuk and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[224]=min(sedang,sejuk,hujan,w_cerah,f_hujan,f2_hujan);

        if sedang and sejuk and hujan and w_mendung and f_cerah and f2_cerah:
                nkRendah[225]=min(sedang,sejuk,hujan,w_mendung,f_cerah,f2_cerah);

        if sedang and sejuk and hujan and w_mendung and f_cerah and f2_mendung:
                nkRendah[226]=min(sedang,sejuk,hujan,w_mendung,f_cerah,f2_mendung);

        if sedang and sejuk and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[227]=min(sedang,sejuk,hujan,w_mendung,f_cerah,f2_hujan);

        if sedang and sejuk and hujan and w_mendung and f_mendung and f2_cerah:
                nkRendah[228]=min(sedang,sejuk,hujan,w_mendung,f_mendung,f2_cerah);

        if sedang and sejuk and hujan and w_mendung and f_mendung and f2_mendung:
                nkRendah[229]=min(sedang,sejuk,hujan,w_mendung,f_mendung,f2_mendung);

        if sedang and sejuk and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[230]=min(sedang,sejuk,hujan,w_mendung,f_mendung,f2_hujan);

        if sedang and sejuk and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[231]=min(sedang,sejuk,hujan,w_mendung,f_hujan,f2_cerah);

        if sedang and sejuk and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[232]=min(sedang,sejuk,hujan,w_mendung,f_hujan,f2_mendung);

        if sedang and sejuk and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[233]=min(sedang,sejuk,hujan,w_mendung,f_hujan,f2_hujan);

        if sedang and sejuk and hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[234]=min(sedang,sejuk,hujan,w_hujan,f_cerah,f2_cerah);

        if sedang and sejuk and hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[235]=min(sedang,sejuk,hujan,w_hujan,f_cerah,f2_mendung);

        if sedang and sejuk and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[236]=min(sedang,sejuk,hujan,w_hujan,f_cerah,f2_hujan);

        if sedang and sejuk and hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[237]=min(sedang,sejuk,hujan,w_hujan,f_mendung,f2_cerah);

        if sedang and sejuk and hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[238]=min(sedang,sejuk,hujan,w_hujan,f_mendung,f2_mendung);

        if sedang and sejuk and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[239]=min(sedang,sejuk,hujan,w_hujan,f_mendung,f2_hujan);

        if sedang and sejuk and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[240]=min(sedang,sejuk,hujan,w_hujan,f_hujan,f2_cerah);

        if sedang and sejuk and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[241]=min(sedang,sejuk,hujan,w_hujan,f_hujan,f2_mendung);

        if sedang and sejuk and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[242]=min(sedang,sejuk,hujan,w_hujan,f_hujan,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[243]=min(sedang,sejuk,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[244]=min(sedang,sejuk,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[245]=min(sedang,sejuk,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[246]=min(sedang,sejuk,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if sedang and sejuk and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[247]=min(sedang,sejuk,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if sedang and sejuk and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[248]=min(sedang,sejuk,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[249]=min(sedang,sejuk,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[250]=min(sedang,sejuk,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if sedang and sejuk and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[251]=min(sedang,sejuk,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[252]=min(sedang,sejuk,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[253]=min(sedang,sejuk,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[254]=min(sedang,sejuk,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[255]=min(sedang,sejuk,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[256]=min(sedang,sejuk,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[257]=min(sedang,sejuk,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[258]=min(sedang,sejuk,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[259]=min(sedang,sejuk,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[260]=min(sedang,sejuk,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkRendah[261]=min(sedang,sejuk,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkRendah[262]=min(sedang,sejuk,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[263]=min(sedang,sejuk,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[264]=min(sedang,sejuk,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkRendah[265]=min(sedang,sejuk,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[266]=min(sedang,sejuk,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if sedang and sejuk and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[267]=min(sedang,sejuk,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if sedang and sejuk and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[268]=min(sedang,sejuk,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if sedang and sejuk and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[269]=min(sedang,sejuk,tdk_hujan,w_hujan,f_hujan,f2_hujan);

        if sedang and dingin and hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[270]=min(sedang,dingin,hujan,w_cerah,f_cerah,f2_cerah);

        if sedang and dingin and hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[271]=min(sedang,dingin,hujan,w_cerah,f_cerah,f2_mendung);

        if sedang and dingin and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[272]=min(sedang,dingin,hujan,w_cerah,f_cerah,f2_hujan);

        if sedang and dingin and hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[273]=min(sedang,dingin,hujan,w_cerah,f_mendung,f2_cerah);
        
        if sedang and dingin and hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[274]=min(sedang,dingin,hujan,w_cerah,f_mendung,f2_mendung);
        
        if sedang and dingin and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[275]=min(sedang,dingin,hujan,w_cerah,f_mendung,f2_hujan);

        if sedang and dingin and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[276]=min(sedang,dingin,hujan,w_cerah,f_hujan,f2_cerah);

        if sedang and dingin and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[277]=min(sedang,dingin,hujan,w_cerah,f_hujan,f2_mendung);
        
        if sedang and dingin and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[278]=min(sedang,dingin,hujan,w_cerah,f_hujan,f2_hujan);

        if sedang and dingin and hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[279]=min(sedang,dingin,hujan,w_mendung,f_cerah,f2_cerah);

        if sedang and dingin and hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[280]=min(sedang,dingin,hujan,w_mendung,f_cerah,f2_mendung);

        if sedang and dingin and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[281]=min(sedang,dingin,hujan,w_mendung,f_cerah,f2_hujan);

        if sedang and dingin and hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[282]=min(sedang,dingin,hujan,w_mendung,f_mendung,f2_cerah);

        if sedang and dingin and hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[283]=min(sedang,dingin,hujan,w_mendung,f_mendung,f2_mendung);

        if sedang and dingin and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[284]=min(sedang,dingin,hujan,w_mendung,f_mendung,f2_hujan);

        if sedang and dingin and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[285]=min(sedang,dingin,hujan,w_mendung,f_hujan,f2_cerah);

        if sedang and dingin and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[286]=min(sedang,dingin,hujan,w_mendung,f_hujan,f2_mendung);

        if sedang and dingin and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[287]=min(sedang,dingin,hujan,w_mendung,f_hujan,f2_hujan);

        if sedang and dingin and hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[288]=min(sedang,dingin,hujan,w_hujan,f_cerah,f2_cerah);

        if sedang and dingin and hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[289]=min(sedang,dingin,hujan,w_hujan,f_cerah,f2_mendung);

        if sedang and dingin and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[290]=min(sedang,dingin,hujan,w_hujan,f_cerah,f2_hujan);

        if sedang and dingin and hujan and w_hujan and f_mendung and f2_cerah:
                nkRendah[291]=min(sedang,dingin,hujan,w_hujan,f_mendung,f2_cerah);

        if sedang and dingin and hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[292]=min(sedang,dingin,hujan,w_hujan,f_mendung,f2_mendung);

        if sedang and dingin and hujan and w_hujan and f_mendung and f2_hujan:
                nkTinggi[293]=min(sedang,dingin,hujan,w_hujan,f_mendung,f2_hujan);

        if sedang and dingin and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[294]=min(sedang,dingin,hujan,w_hujan,f_hujan,f2_cerah);

        if sedang and dingin and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[295]=min(sedang,dingin,hujan,w_hujan,f_hujan,f2_mendung);

        if sedang and dingin and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[296]=min(sedang,dingin,hujan,w_hujan,f_hujan,f2_hujan);

        if sedang and dingin and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[297]=min(sedang,dingin,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if sedang and dingin and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[298]=min(sedang,dingin,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if sedang and dingin and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[299]=min(sedang,dingin,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if sedang and dingin and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[300]=min(sedang,dingin,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if sedang and dingin and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[301]=min(sedang,dingin,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if sedang and dingin and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[302]=min(sedang,dingin,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if sedang and dingin and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[303]=min(sedang,dingin,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if sedang and dingin and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[304]=min(sedang,dingin,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if sedang and dingin and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[305]=min(sedang,dingin,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if sedang and dingin and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[306]=min(sedang,dingin,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if sedang and dingin and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[307]=min(sedang,dingin,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if sedang and dingin and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[308]=min(sedang,dingin,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if sedang and dingin and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[309]=min(sedang,dingin,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if sedang and dingin and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[310]=min(sedang,dingin,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if sedang and dingin and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[311]=min(sedang,dingin,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if sedang and dingin and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[312]=min(sedang,dingin,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if sedang and dingin and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[313]=min(sedang,dingin,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if sedang and dingin and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[314]=min(sedang,dingin,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if sedang and dingin and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[315]=min(sedang,dingin,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if sedang and dingin and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[316]=min(sedang,dingin,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if sedang and dingin and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[317]=min(sedang,dingin,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if sedang and dingin and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[318]=min(sedang,dingin,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if sedang and dingin and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[319]=min(sedang,dingin,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if sedang and dingin and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[320]=min(sedang,dingin,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if sedang and dingin and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[321]=min(sedang,dingin,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if sedang and dingin and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[322]=min(sedang,dingin,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if sedang and dingin and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[323]=min(sedang,dingin,tdk_hujan,w_hujan,f_hujan,f2_hujan);
        
        
        if kering and panas and hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[324]=min(kering,panas,hujan,w_cerah,f_cerah,f2_cerah);

        if kering and panas and hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[325]=min(kering,panas,hujan,w_cerah,f_cerah,f2_mendung);

        if kering and panas and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[326]=min(kering,panas,hujan,w_cerah,f_cerah,f2_hujan);

        if kering and panas and hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[327]=min(kering,panas,hujan,w_cerah,f_mendung,f2_cerah);
        
        if kering and panas and hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[328]=min(kering,panas,hujan,w_cerah,f_mendung,f2_mendung);
        
        if kering and panas and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[329]=min(kering,panas,hujan,w_cerah,f_mendung,f2_hujan);

        if kering and panas and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[330]=min(kering,panas,hujan,w_cerah,f_hujan,f2_cerah);

        if kering and panas and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[331]=min(kering,panas,hujan,w_cerah,f_hujan,f2_mendung);
        
        if kering and panas and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[332]=min(kering,panas,hujan,w_cerah,f_hujan,f2_hujan);

        if kering and panas and hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[333]=min(kering,panas,hujan,w_mendung,f_cerah,f2_cerah);

        if kering and panas and hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[334]=min(kering,panas,hujan,w_mendung,f_cerah,f2_mendung);

        if kering and panas and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[335]=min(kering,panas,hujan,w_mendung,f_cerah,f2_hujan);

        if kering and panas and hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[336]=min(kering,panas,hujan,w_mendung,f_mendung,f2_cerah);

        if kering and panas and hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[337]=min(kering,panas,hujan,w_mendung,f_mendung,f2_mendung);

        if kering and panas and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[338]=min(kering,panas,hujan,w_mendung,f_mendung,f2_hujan);

        if kering and panas and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[339]=min(kering,panas,hujan,w_mendung,f_hujan,f2_cerah);

        if kering and panas and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[340]=min(kering,panas,hujan,w_mendung,f_hujan,f2_mendung);

        if kering and panas and hujan and w_mendung and f_hujan and f2_hujan:
                nkTinggi[341]=min(kering,panas,hujan,w_mendung,f_hujan,f2_hujan);

        if kering and panas and hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[342]=min(kering,panas,hujan,w_hujan,f_cerah,f2_cerah);

        if kering and panas and hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[343]=min(kering,panas,hujan,w_hujan,f_cerah,f2_mendung);

        if kering and panas and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[344]=min(kering,panas,hujan,w_hujan,f_cerah,f2_hujan);

        if kering and panas and hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[345]=min(kering,panas,hujan,w_hujan,f_mendung,f2_cerah);

        if kering and panas and hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[346]=min(kering,panas,hujan,w_hujan,f_mendung,f2_mendung);

        if kering and panas and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[347]=min(kering,panas,hujan,w_hujan,f_mendung,f2_hujan);

        if kering and panas and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[348]=min(kering,panas,hujan,w_hujan,f_hujan,f2_cerah);

        if kering and panas and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[349]=min(kering,panas,hujan,w_hujan,f_hujan,f2_mendung);

        if kering and panas and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[350]=min(kering,panas,hujan,w_hujan,f_hujan,f2_hujan);

        if kering and panas and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[351]=min(kering,panas,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if kering and panas and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[352]=min(kering,panas,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if kering and panas and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[353]=min(kering,panas,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if kering and panas and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[354]=min(kering,panas,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if kering and panas and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[355]=min(kering,panas,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if kering and panas and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[356]=min(kering,panas,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if kering and panas and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[357]=min(kering,panas,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if kering and panas and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[358]=min(kering,panas,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if kering and panas and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[359]=min(kering,panas,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if kering and panas and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[360]=min(kering,panas,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if kering and panas and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[361]=min(kering,panas,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if kering and panas and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[362]=min(kering,panas,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if kering and panas and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[363]=min(kering,panas,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if kering and panas and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[364]=min(kering,panas,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if kering and panas and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[365]=min(kering,panas,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if kering and panas and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[366]=min(kering,panas,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if kering and panas and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[367]=min(kering,panas,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if kering and panas and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[368]=min(kering,panas,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if kering and panas and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[369]=min(kering,panas,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if kering and panas and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[370]=min(kering,panas,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if kering and panas and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[371]=min(kering,panas,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if kering and panas and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[372]=min(kering,panas,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if kering and panas and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[373]=min(kering,panas,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if kering and panas and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[374]=min(kering,panas,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if kering and panas and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[375]=min(kering,panas,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if kering and panas and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[376]=min(kering,panas,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if kering and panas and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[377]=min(kering,panas,tdk_hujan,w_hujan,f_hujan,f2_hujan);
        
        if kering and sejuk and hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[378]=min(kering,sejuk,hujan,w_cerah,f_cerah,f2_cerah);

        if kering and sejuk and hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[379]=min(kering,sejuk,hujan,w_cerah,f_cerah,f2_mendung);

        if kering and sejuk and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[380]=min(kering,sejuk,hujan,w_cerah,f_cerah,f2_hujan);

        if kering and sejuk and hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[381]=min(kering,sejuk,hujan,w_cerah,f_mendung,f2_cerah);
        
        if kering and sejuk and hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[382]=min(kering,sejuk,hujan,w_cerah,f_mendung,f2_mendung);
        
        if kering and sejuk and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[383]=min(kering,sejuk,hujan,w_cerah,f_mendung,f2_hujan);

        if kering and sejuk and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[384]=min(kering,sejuk,hujan,w_cerah,f_hujan,f2_cerah);

        if kering and sejuk and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[385]=min(kering,sejuk,hujan,w_cerah,f_hujan,f2_mendung);
        
        if kering and sejuk and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[386]=min(kering,sejuk,hujan,w_cerah,f_hujan,f2_hujan);

        if kering and sejuk and hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[387]=min(kering,sejuk,hujan,w_mendung,f_cerah,f2_cerah);

        if kering and sejuk and hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[388]=min(kering,sejuk,hujan,w_mendung,f_cerah,f2_mendung);

        if kering and sejuk and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[389]=min(kering,sejuk,hujan,w_mendung,f_cerah,f2_hujan);

        if kering and sejuk and hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[390]=min(kering,sejuk,hujan,w_mendung,f_mendung,f2_cerah);

        if kering and sejuk and hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[391]=min(kering,sejuk,hujan,w_mendung,f_mendung,f2_mendung);

        if kering and sejuk and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[392]=min(kering,sejuk,hujan,w_mendung,f_mendung,f2_hujan);

        if kering and sejuk and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[393]=min(kering,sejuk,hujan,w_mendung,f_hujan,f2_cerah);

        if kering and sejuk and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[394]=min(kering,sejuk,hujan,w_mendung,f_hujan,f2_mendung);

        if kering and sejuk and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[395]=min(kering,sejuk,hujan,w_mendung,f_hujan,f2_hujan);

        if kering and sejuk and hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[396]=min(kering,sejuk,hujan,w_hujan,f_cerah,f2_cerah);

        if kering and sejuk and hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[397]=min(kering,sejuk,hujan,w_hujan,f_cerah,f2_mendung);

        if kering and sejuk and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[398]=min(kering,sejuk,hujan,w_hujan,f_cerah,f2_hujan);

        if kering and sejuk and hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[399]=min(kering,sejuk,hujan,w_hujan,f_mendung,f2_cerah);

        if kering and sejuk and hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[400]=min(kering,sejuk,hujan,w_hujan,f_mendung,f2_mendung);

        if kering and sejuk and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[401]=min(kering,sejuk,hujan,w_hujan,f_mendung,f2_hujan);

        if kering and sejuk and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[402]=min(kering,sejuk,hujan,w_hujan,f_hujan,f2_cerah);

        if kering and sejuk and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[403]=min(kering,sejuk,hujan,w_hujan,f_hujan,f2_mendung);

        if kering and sejuk and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[404]=min(kering,sejuk,hujan,w_hujan,f_hujan,f2_hujan);

        if kering and sejuk and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[405]=min(kering,sejuk,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if kering and sejuk and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[406]=min(kering,sejuk,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if kering and sejuk and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[407]=min(kering,sejuk,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if kering and sejuk and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[408]=min(kering,sejuk,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if kering and sejuk and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[409]=min(kering,sejuk,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if kering and sejuk and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[410]=min(kering,sejuk,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if kering and sejuk and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[411]=min(kering,sejuk,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if kering and sejuk and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[412]=min(kering,sejuk,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if kering and sejuk and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[413]=min(kering,sejuk,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if kering and sejuk and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[414]=min(kering,sejuk,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if kering and sejuk and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[415]=min(kering,sejuk,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if kering and sejuk and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[416]=min(kering,sejuk,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if kering and sejuk and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[417]=min(kering,sejuk,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if kering and sejuk and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[418]=min(kering,sejuk,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if kering and sejuk and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[419]=min(kering,sejuk,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if kering and sejuk and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[420]=min(kering,sejuk,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if kering and sejuk and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[421]=min(kering,sejuk,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if kering and sejuk and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[422]=min(kering,sejuk,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if kering and sejuk and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[423]=min(kering,sejuk,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if kering and sejuk and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[424]=min(kering,sejuk,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if kering and sejuk and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[425]=min(kering,sejuk,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if kering and sejuk and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[426]=min(kering,sejuk,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if kering and sejuk and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[427]=min(kering,sejuk,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if kering and sejuk and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[428]=min(kering,sejuk,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if kering and sejuk and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[429]=min(kering,sejuk,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if kering and sejuk and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[430]=min(kering,sejuk,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if kering and sejuk and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[431]=min(kering,sejuk,tdk_hujan,w_hujan,f_hujan,f2_hujan);

        if kering and dingin and hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[432]=min(kering,dingin,hujan,w_cerah,f_cerah,f2_cerah);

        if kering and dingin and hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[433]=min(kering,dingin,hujan,w_cerah,f_cerah,f2_mendung);

        if kering and dingin and hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[434]=min(kering,dingin,hujan,w_cerah,f_cerah,f2_hujan);

        if kering and dingin and hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[435]=min(kering,dingin,hujan,w_cerah,f_mendung,f2_cerah);
        
        if kering and dingin and hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[436]=min(kering,dingin,hujan,w_cerah,f_mendung,f2_mendung);
        
        if kering and dingin and hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[437]=min(kering,dingin,hujan,w_cerah,f_mendung,f2_hujan);

        if kering and dingin and hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[438]=min(kering,dingin,hujan,w_cerah,f_hujan,f2_cerah);

        if kering and dingin and hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[439]=min(kering,dingin,hujan,w_cerah,f_hujan,f2_mendung);
        
        if kering and dingin and hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[440]=min(kering,dingin,hujan,w_cerah,f_hujan,f2_hujan);

        if kering and dingin and hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[441]=min(kering,dingin,hujan,w_mendung,f_cerah,f2_cerah);

        if kering and dingin and hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[442]=min(kering,dingin,hujan,w_mendung,f_cerah,f2_mendung);

        if kering and dingin and hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[443]=min(kering,dingin,hujan,w_mendung,f_cerah,f2_hujan);

        if kering and dingin and hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[444]=min(kering,dingin,hujan,w_mendung,f_mendung,f2_cerah);

        if kering and dingin and hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[445]=min(kering,dingin,hujan,w_mendung,f_mendung,f2_mendung);

        if kering and dingin and hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[446]=min(kering,dingin,hujan,w_mendung,f_mendung,f2_hujan);

        if kering and dingin and hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[447]=min(kering,dingin,hujan,w_mendung,f_hujan,f2_cerah);

        if kering and dingin and hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[448]=min(kering,dingin,hujan,w_mendung,f_hujan,f2_mendung);

        if kering and dingin and hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[449]=min(kering,dingin,hujan,w_mendung,f_hujan,f2_hujan);

        if kering and dingin and hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[450]=min(kering,dingin,hujan,w_hujan,f_cerah,f2_cerah);

        if kering and dingin and hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[451]=min(kering,dingin,hujan,w_hujan,f_cerah,f2_mendung);

        if kering and dingin and hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[452]=min(kering,dingin,hujan,w_hujan,f_cerah,f2_hujan);

        if kering and dingin and hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[453]=min(kering,dingin,hujan,w_hujan,f_mendung,f2_cerah);

        if kering and dingin and hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[454]=min(kering,dingin,hujan,w_hujan,f_mendung,f2_mendung);

        if kering and dingin and hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[455]=min(kering,dingin,hujan,w_hujan,f_mendung,f2_hujan);

        if kering and dingin and hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[456]=min(kering,dingin,hujan,w_hujan,f_hujan,f2_cerah);

        if kering and dingin and hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[457]=min(kering,dingin,hujan,w_hujan,f_hujan,f2_mendung);

        if kering and dingin and hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[458]=min(kering,dingin,hujan,w_hujan,f_hujan,f2_hujan);

        if kering and dingin and tdk_hujan and w_cerah and f_cerah and f2_cerah:
                nkTinggi[459]=min(kering,dingin,tdk_hujan,w_cerah,f_cerah,f2_cerah);

        if kering and dingin and tdk_hujan and w_cerah and f_cerah and f2_mendung:
                nkTinggi[460]=min(kering,dingin,tdk_hujan,w_cerah,f_cerah,f2_mendung);

        if kering and dingin and tdk_hujan and w_cerah and f_cerah and f2_hujan:
                nkRendah[461]=min(kering,dingin,tdk_hujan,w_cerah,f_cerah,f2_hujan);

        if kering and dingin and tdk_hujan and w_cerah and f_mendung and f2_cerah:
                nkTinggi[462]=min(kering,dingin,tdk_hujan,w_cerah,f_mendung,f2_cerah);
        
        if kering and dingin and tdk_hujan and w_cerah and f_mendung and f2_mendung:
                nkTinggi[463]=min(kering,dingin,tdk_hujan,w_cerah,f_mendung,f2_mendung);
        
        if kering and dingin and tdk_hujan and w_cerah and f_mendung and f2_hujan:
                nkRendah[464]=min(kering,dingin,tdk_hujan,w_cerah,f_mendung,f2_hujan);

        if kering and dingin and tdk_hujan and w_cerah and f_hujan and f2_cerah:
                nkRendah[465]=min(kering,dingin,tdk_hujan,w_cerah,f_hujan,f2_cerah);

        if kering and dingin and tdk_hujan and w_cerah and f_hujan and f2_mendung:
                nkRendah[466]=min(kering,dingin,tdk_hujan,w_cerah,f_hujan,f2_mendung);
        
        if kering and dingin and tdk_hujan and w_cerah and f_hujan and f2_hujan:
                nkRendah[467]=min(kering,dingin,tdk_hujan,w_cerah,f_hujan,f2_hujan);

        if kering and dingin and tdk_hujan and w_mendung and f_cerah and f2_cerah:
                nkTinggi[468]=min(kering,dingin,tdk_hujan,w_mendung,f_cerah,f2_cerah);

        if kering and dingin and tdk_hujan and w_mendung and f_cerah and f2_mendung:
                nkTinggi[469]=min(kering,dingin,tdk_hujan,w_mendung,f_cerah,f2_mendung);

        if kering and dingin and tdk_hujan and w_mendung and f_cerah and f2_hujan:
                nkRendah[470]=min(kering,dingin,tdk_hujan,w_mendung,f_cerah,f2_hujan);

        if kering and dingin and tdk_hujan and w_mendung and f_mendung and f2_cerah:
                nkTinggi[471]=min(kering,dingin,tdk_hujan,w_mendung,f_mendung,f2_cerah);

        if kering and dingin and tdk_hujan and w_mendung and f_mendung and f2_mendung:
                nkTinggi[472]=min(kering,dingin,tdk_hujan,w_mendung,f_mendung,f2_mendung);

        if kering and dingin and tdk_hujan and w_mendung and f_mendung and f2_hujan:
                nkRendah[473]=min(kering,dingin,tdk_hujan,w_mendung,f_mendung,f2_hujan);

        if kering and dingin and tdk_hujan and w_mendung and f_hujan and f2_cerah:
                nkRendah[474]=min(kering,dingin,tdk_hujan,w_mendung,f_hujan,f2_cerah);

        if kering and dingin and tdk_hujan and w_mendung and f_hujan and f2_mendung:
                nkRendah[475]=min(kering,dingin,tdk_hujan,w_mendung,f_hujan,f2_mendung);

        if kering and dingin and tdk_hujan and w_mendung and f_hujan and f2_hujan:
                nkRendah[476]=min(kering,dingin,tdk_hujan,w_mendung,f_hujan,f2_hujan);

        if kering and dingin and tdk_hujan and w_hujan and f_cerah and f2_cerah:
                nkTinggi[477]=min(kering,dingin,tdk_hujan,w_hujan,f_cerah,f2_cerah);

        if kering and dingin and tdk_hujan and w_hujan and f_cerah and f2_mendung:
                nkTinggi[478]=min(kering,dingin,tdk_hujan,w_hujan,f_cerah,f2_mendung);

        if kering and dingin and tdk_hujan and w_hujan and f_cerah and f2_hujan:
                nkRendah[479]=min(kering,dingin,tdk_hujan,w_hujan,f_cerah,f2_hujan);

        if kering and dingin and tdk_hujan and w_hujan and f_mendung and f2_cerah:
                nkTinggi[480]=min(kering,dingin,tdk_hujan,w_hujan,f_mendung,f2_cerah);

        if kering and dingin and tdk_hujan and w_hujan and f_mendung and f2_mendung:
                nkTinggi[481]=min(kering,dingin,tdk_hujan,w_hujan,f_mendung,f2_mendung);

        if kering and dingin and tdk_hujan and w_hujan and f_mendung and f2_hujan:
                nkRendah[482]=min(kering,dingin,tdk_hujan,w_hujan,f_mendung,f2_hujan);

        if kering and dingin and tdk_hujan and w_hujan and f_hujan and f2_cerah:
                nkRendah[483]=min(kering,dingin,tdk_hujan,w_hujan,f_hujan,f2_cerah);

        if kering and dingin and tdk_hujan and w_hujan and f_hujan and f2_mendung:
                nkRendah[484]=min(kering,dingin,tdk_hujan,w_hujan,f_hujan,f2_mendung);

        if kering and dingin and tdk_hujan and w_hujan and f_hujan and f2_hujan:
                nkRendah[485]=min(kering,dingin,tdk_hujan,w_hujan,f_hujan,f2_hujan);
        
        
        #nkRendah.append(5);
        #nkRendah.insert(1,6);
        # print "FUZZY OUTPUT";
        for i in range(486):
                if nkRendah[i]>0:
                        # print "Rule "+str(i+1)+ " Rendah : "+str(nkRendah[i]);
                        if nkRendah[i]>rendah:
                                rendah=nkRendah[i];
                if nkTinggi[i]>0:
                        # print "Rule "+str(i+1)+ " Tinggi : "+str(nkTinggi[i]);
                        if nkTinggi[i]>tinggi:
                                tinggi=nkTinggi[i];

        # if rendah>0:
        #       print "Rendah("+str(rendah)+")";
        # if tinggi>0:
        #       print "Tinggi("+str(tinggi)+")";


        #DEFUZIFIKASI
        #batas
        # print "DEFUZZYFIKASI";
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
                # print str(count) + ":" + str(y[i]);
                i += 1;
        mamdani = mamdani_pembilang/mamdani_penyebut;
        #print "Nilai Kelayakan : "+str(mamdani);
        return mamdani;
