# Python 3.6.0 |Anaconda 4.3.1 (64-bit)|

from importer import *

def from_url_to_bs4(url):
	
	"""
	Provided a url returns a BeautifulSoup object with url's content
	"""

	source = urllib.request.urlopen(url).read()
	return bs(source, "lxml")