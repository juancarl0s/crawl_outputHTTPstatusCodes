from bs4 import BeautifulSoup
import urllib
import re
import csv 

def open_all_links_in_this_page(urlGiven):
	#This value is the maximun number of URLs the set can hold, if not set and the site tested is big enough the recursion will reach a limit and the program breaks
	if len(urls_set)<500:
		if urlGiven.endswith("/"):
			urlGiven = urlGiven[:-1]
		urlGiven_html = urllib.urlopen(urlGiven)

		#beautifulsoup is forced to use lxml
		urlGiven_html_bt = BeautifulSoup(urlGiven_html.read(), "lxml")
		#I find all 'a' tags
		allLinksInPage_dict = urlGiven_html_bt.findAll('a')

		#Loop over all links I can fin in the page I am on right now
		for key in allLinksInPage_dict:

			url_to_test = key['href']
			url_to_add_to_set = ""	
			#If the link is a relative URL, handle the case
			if len(url_to_test)>0 and ( url_to_test[0] == "/" ):
				url_to_add_to_set = urlGiven + url_to_test
			#Check that the link to test is in the scope given by the user
			if bool(re.search( r'(.*)'+ domainGivenByUser + r'(.*)', url_to_test, re.DOTALL)) and (url_to_test not in urls_set):
					url_to_add_to_set = url_to_test
					urls_set.add(url_to_add_to_set)
	return

def writeToFile(txtBoolean, csvBoolean):
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
	
domainGivenByUser = raw_input('Enter the domain (i.e.: mysite.dev): ')

urlGivenByUser = raw_input('Enter url of page that contains all links you want to open (i.e.: http://mysite.dev/something): ')
print "I'm working now..."

urls_set = set()

open_all_links_in_this_page(urlGivenByUser)

selected_option = raw_input("Do you want the results to be writte as a:\n  1)Text file (status_codes.txt).\n  2)CSV file (status_codes.csv).\n  3)Both.\nSelection: ")
if selected_option == "1":
	writeToFile(True,False)
elif selected_option == "2":
	writeToFile(False,True)
elif selected_option == "3":
	writeToFile(True,True)