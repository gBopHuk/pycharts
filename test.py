import preparam


valup = High[i] - Open[i]
valdo = Open[i] - Low[i]

if valup > valdo : 
	 val[i]=valdo
else val[i]=valup

getval = min(val[:start])