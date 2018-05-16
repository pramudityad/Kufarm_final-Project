import rule_py as fuzzy

soil	= 145
rain	= 220
temp	= 30
hum		= 75
ow_code = 2
wu_code = 1

NK = fuzzy.calculate(soil,rain,temp,hum,ow_code,wu_code)
print (NK)