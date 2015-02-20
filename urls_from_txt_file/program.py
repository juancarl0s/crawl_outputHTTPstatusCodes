from bs4 import BeautifulSoup
import urllib
import re
import csv 

def write_url_and_statusCodes_ToFile(txtBoolean, csvBoolean):
	urls_set = set()
	# urls_file = open("urls.txt", "r")

	# for line in urls_file:
	# 	if line.endswith("/"):
	# 		line = line[:-1] 
	# 	urls_set.add(line)
	# 	print line

	with open("urls.txt", "r") as urls_file:
		for line in urls_file:
			if line.endswith("/"):
				line = line[:-1] 
			urls_set.add(line)

	#write text file
	
	print "Writing to file(s)"
	if txtBoolean:
		statusCodesTXT = open("urls_and_statusCodes.txt", "w")
	if csvBoolean:	
		statusCodesCSV = csv.writer(open("urls_and_statusCodes.csv", "wb"))

	for url in urls_set:
		print "Checking %s" % url
		if txtBoolean:
			statusCodesTXT.write(url + "Status code: %d" % urllib.urlopen(url).code + "\n\n")
		if csvBoolean:
			statusCodesCSV.writerow([url, urllib.urlopen(url).code])

	if txtBoolean:		
		statusCodesTXT.close()	
	print "Done with file(s)"	

	return

selected_option = raw_input("Do you want the results to be writte as a:\n  1)Text file (status_codes.txt).\n  2)CSV file (status_codes.csv).\n  3)Both.\nSelection: ")
if selected_option == "1":
	write_url_and_statusCodes_ToFile(True,False)
elif selected_option == "2":
	write_url_and_statusCodes_ToFile(False,True)
elif selected_option == "3":
	write_url_and_statusCodes_ToFile(True,True)