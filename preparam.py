import sys

filename = sys.argv[1]
csvf = open(filename.decode('utf-8')
i=0

for line in csv.readlines():
	sline = line.split(',')
	dtime[i] = sline[0]+' '+sline[1]
	fopen[i],fhigh[i],flow[i],fclose[i]=float(sline[2]),\
									float(sline[3]),\
									float(sline[4]),\
									float(sline[5])
	i++
