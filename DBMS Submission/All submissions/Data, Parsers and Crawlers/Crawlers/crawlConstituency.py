import sys 
import requests 
import lxml.html 
	
class constituency(object):
	"""docstring for constituency"""
	def __init__(self):
		self.assemblyConstituency = []
		self.centreConstituency = []
		state = ""
	
def refineString(s):
	no_digits = []
	for i in s:
	    if not i.isdigit():
	        no_digits.append(i)
	result = ''.join(no_digits)
	result = result.split('(',1)[0]
	result.strip()
	return result

#def refineString2(s):
	

def getlokSabhaData():
	hxs = lxml.html.document_fromstring(requests.get("http://en.wikipedia.org/wiki/List_of_constituencies_of_the_Lok_Sabha").content)
	states = []
	states=hxs.xpath(".//*[@id='mw-content-text']/h3/span[1]/a/text()")
	print states 
	centre = []
	for tableNo in range(3,39):
		#print ""
		print "state :" + states[tableNo-3]
		try:
			dataConstituencies = []
			s = ".//*[@id='mw-content-text']/table[{}]/tr/td[2]/a/text()".format(tableNo)
			dataConstituencies = hxs.xpath(s)					# gets us the constituency
			print "constituencies:"
			print dataConstituencies

			for i in range(1,len(dataConstituencies)+1):
				centre.append((states[tableNo-3],dataConstituencies[i]))

		except:
			print "Table {} not found".format(tableNo)
	f = open("centreData.txt","w")
	for t in centre:
		s = t[0]+","+t[1]+"\n"
		print s
		f.write(s.encode('utf8'))	
	##print refineString(" sdfa 123.")

if __name__ == "__main__":
	getlokSabhaData()