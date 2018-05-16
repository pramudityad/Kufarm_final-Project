import rule_py as fuzzy

soil	= 70
rain	= 230
temp	= 29
hum		= 70
ow_code = 1
wu_code = 1

NK = fuzzy.calculate(soil,rain,temp,hum,ow_code,wu_code)
print (NK)