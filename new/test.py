import dht11 as DT 
sampleFreq = 60

def main():
	while True:
		temp, hum = getdht()
		pass
		logdht(temp, hum)
		time.sleep(sampleFreq)

# ------------ Execute program 
main()