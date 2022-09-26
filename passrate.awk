BEGIN {
	failcount = 0;
	totalcount = 0;
	honscount = 0;
	START_DMC = 3632;
	END_DMC = 3841;
	START_SSMC = 3882;
	END_SSMC = 4097;
	fromreg = START_DMC;
	uptoreg = 10000;
}

{
	if ($1 < uptoreg && $1 > fromreg){
		if ($3 == "F") failcount++;
		if ($5 != "" && $5 != " ") honscount++;
		totalcount++;
	}
}

END {
	print "Failed: " (failcount/totalcount)*100 "%";
	print "Hons: " honscount;
}
