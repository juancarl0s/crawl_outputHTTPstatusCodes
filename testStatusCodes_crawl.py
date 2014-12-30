from bs4 import BeautifulSoup
import urllib
import re
import csv 

def crawl_around(urlGiven, n):
	if n<500:
		#if n>10:
		# return
		#print "Begins testing %d:" %n + urlGiven
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

		#if the page I'm on right now is not in the ones I've alread checked, I recursively call the procedure again
		if urlGiven not in urls_set:
			crawl_around(urlGiven, n+1)
	return

def writeToFile(txtBoolean, csvBoolean):
	#write text file
	if txtBoolean:
		print "Writing to TXT file..."
		statusCodesTXT = open("status_codes.txt", "w")
		for url in urls_set:
			statusCodesTXT.write(url + " : %d\n" % urllib.urlopen(url).code)
		print "Done with the TXT file!"	
	#write csv file
	if csvBoolean:		
		print "Writing to CSV file..."
		statusCodesCSV = csv.writer(open("status_codes.csv", "wb"))
		for url in urls_set:
			statusCodesCSV.writerow([url, urllib.urlopen(url).code])
		print "Done with the CSV file!"	
	return

domainGivenByUser = raw_input('Enter the domain (i.e.: mysite.dev): ')

urlGivenByUser = raw_input('Enter url to start spider and test status codes (i.e.: http://mysite.dev/something): ')
print "Crawling..."

urls_set = set()

crawl_around(urlGivenByUser, 0)

selected_option = raw_input("Do you want the results to be writte as a:\n  1)Text file (status_codes.txt).\n  2)CSV file (status_codes.csv).\n  3)Both.\nSelection: ")
if selected_option == "1":
	writeToFile(True,False)
elif selected_option == "2":
	writeToFile(False,True)
elif selected_option == "3":
	writeToFile(True,True)