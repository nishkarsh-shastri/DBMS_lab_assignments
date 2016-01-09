from bs4 import BeautifulSoup
import requests
from requests.exceptions import ProxyError

def get_request(url):
	while(True):
		try:
			r = requests.get(url)
			break
		except ProxyError:
			continue
	return r

post_offices = []

def get_post_offices(url):
	r = get_request(url)
	# print("Yahan toh pohoch gaya")
	data = r.text
	# print (data)
	soup = BeautifulSoup(data)
	table = soup.find_all('table')[5]


	# print (table)
	district = []
	for tr in table.find_all('tr'):
		if( tr.td.contents[0].text != 'District'):
			district.append([tr.td.a['href'][(tr.td.a['href'].index('p'))-1:],tr.td.next_sibling.contents[0]])
			# print((tr.td.a['href'][(tr.td.a['href'].index('p'))-1:],tr.td.next_sibling.contents[0]))

	url = url[:url.index('/p')]
	# print (url)
	
	# sub table
	for d in district:
		# crawl row by row
		r = get_request(url+d[0])
		data = r.text
		soup = BeautifulSoup(data)
		#get the table and add post offices
		table = soup.find_all('table')[5]
		# print(table)
		for tr in table.find_all('tr'):
			td = tr.find_all('td')
			if td[1].contents[0].text != 'Pincode ':
				print(td[0].contents[0].text+','+td[1].contents[0].text[:-1]+','+td[2].text+','+td[3].text)
				post_offices.append([td[0].contents[0].text,td[1].contents[0].text[:-1],td[2].text,td[3].text])

def main():
	filename = "input.txt"
	url = ''
	for url in open(filename):
		r = get_request(url)
	soup = BeautifulSoup(r.text)
	table = soup.find_all('table')[5]
	states = []
	# print (table)
	for tr in table.find_all('tr'):
		td = tr.find_all('td')
		# print(td[0].a['href'][8:],td[1].a['href'][8:])
		states.append(td[0].a['href'][8:])
		states.append(td[1].a['href'][8:])

	url = url[:url.index('/p')]
	# print(url)
	for state in states:
		get_post_offices(url+state)

if __name__ == '__main__':
	main()

