############################
##Developer: Denis Morozov##
##Date: 21 February 2019  ##
##Software: Python 3.6    ##
############################	

from lxml import html
import lxml, lxml.html
import datetime, os, time, requests

def generate_startURL(pageNumber):
	start_URL = r'https://www.thegazette.co.uk/insolvency/notice?sort-by=latest-date&categorycode=G305010100+G305010200+G305010300+G305010400+G405010004+G305010500+-2&location-distance-1=1&service=insolvency&numberOfLocationSearches=1&results-page-size=100&results-page={}'.format(pageNumber)
	return start_URL

def requesting_response(reQuest):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	response = requests.get(reQuest, headers = headers)
	tree = html.fromstring(response.text)
	return tree

def create_row(company_type, publication_date, company_number, notice_code, main_text):
	row  =	str(company_type).replace(',', '').replace('\n', '').replace('\r', '') + ',' + \
			str(publication_date).replace(',', '').replace('\n', '').replace('\r', '') + ',' + \
			str(company_number).replace(',', '').replace('\n', '').replace('\r', '') + ',' + \
			str(notice_code).replace(',', '').replace('\n', '').replace('\r', '') + ',' + \
			str(main_text).replace(',', '').replace('\n', '').replace('\r', '') + ',' + '\n'
	return row

def writeOutput(row, output, backup):

	if (row not in backup) or (row.startswith('company_type,')):
		output.write(row)

def parse(parseURL):

	response = requesting_response('https://www.thegazette.co.uk' + parseURL)
	main_txt = response.xpath('//*[contains(@data-gazettes, "Notice")]//text()')
	string = ''
	
	for sentence in main_txt:
		string = string + sentence.replace('\n', ' ').replace('\r', ' ').replace('  ', ' ').replace(',', ' ').strip()

	try: a = response.xpath('//*[@id="main_content"]/div/div[1]/div[1]/section/div/dl/dd[1]/text()')[0].strip() #company type code
	except: a = ''

	try: b = response.xpath('//*[@id="main_content"]/div/div[1]/div[1]/section/div/dl/dd[3]/time/text()')[0].strip() #publication time stamp
	except:
		try: b = response.xpath('//*[@id="main_content"]/div/div[1]/div[1]/section/div/dl/dd[3]/text()')[0].strip()
		except: b = ''

	try: c = response.xpath('//*[@id="main_content"]/div/div[1]/div[1]/section/div/dl/dd[6]/a/text()')[0].strip() #company number
	except: c = ''

	try: d = response.xpath('//*[@id="main_content"]/div/div[1]/div[1]/section/div/dl/dd[7]/text()')[0].strip()
	except: d = ''

	return a, b, c, d, string

def parse_details(parseURL, output, backup, temporary, computerDate):
	
	mainTree = requesting_response(parseURL)

	webURLs = mainTree.xpath('//*[@id="search-results"]/div/article/div/header/h3/a/@href')
	webDates = mainTree.xpath('//*[@id="search-results"]/div/article/div/dl/dd/time/text()')

	for i in range(len(webURLs)):
		webDate = webDates[i]
		webURL = webURLs[i]

		if webDate == computerDate:
			if webURL not in temporary:
				print ('\tScrapping ' + str(webURL))
				ctype, ptimestamp, cnumber, ncode, text = parse(webURL)
				row = create_row(ctype, ptimestamp, cnumber, ncode, text)
				writeOutput(row, output, backup)
				temporary.append(webURL)

		else: break

def time_countDown(timer):
	while timer:
		mins, secs = divmod(timer, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print (timeformat, end = '\r')
		time.sleep(1)
		timer = timer - 1

def backup_data(input_, output_):
	for i in range(len(input_)):
		if not input_[i].startswith('company_type,'):
			output_.write(input_[i])



def starting_run():

	temporary = []

	computerTime = (datetime.datetime.now()).strftime("%H:%M")

	if 'backup.csv' not in os.listdir(os.getcwd()):
		backup = open('backup.csv', 'w', encoding = 'UTF-8')
		backup.write(('company_type, publication_date, company_number, notice_code, main_text\n'))
		backup.close()

	while computerTime < '13:30':

		computerDate  = (datetime.datetime.now()).strftime("%d %B %Y")
		
		output = open('output.csv', 'w', encoding = 'UTF-8')
		backup = open('backup.csv', 'r', encoding = 'UTF-8').readlines()

		headers = create_row('company_type,', 'publication_date,', 'company_number,', 'notice_code,', 'main_text')
		writeOutput(headers, output, backup)

		start_URL = generate_startURL(1)
		print ('Starting to check and scrape data:')
		parse_details(start_URL, output, backup, temporary, computerDate)
		output.close()

		output = open('output.csv', 'r', encoding = 'UTF-8').readlines()
		backup = open('backup.csv', 'a', encoding = 'UTF-8')

		print ('Preparing to backup data')		
		backup_data(output, backup)
		backup.close()

		print ('Sleep mode activated')
		time_countDown(1200)

		computerTime = (datetime.datetime.now()).strftime("%H:%M")


starting_run()
