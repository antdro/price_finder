# Python 3.6.0 |Anaconda 4.3.1 (64-bit)|

from importer import *
from loader import *

def get_markets_from_oddschecker(url):
	
	"""
	Returns a list with markets available on www.oddschecker.com
	
	URL example: 'https://www.oddschecker.com/football/italy/serie-a/fiorentina-v-inter/betting-markets'
	"""
	
	list_of_markets = []
	bs4 = from_url_to_bs4(url)

	result = re.search('https://www.oddschecker.com/(.*)betting-markets', url)
	link_core = result.group(1)
	link_part = "<a href=\"/" + link_core

	all_links = bs4.find_all(href = True)

	for link in all_links:
		if link_part in str(link):
			market_name = re.search(link_part + "(.*)\">", str(link))
			list_of_markets.append(market_name.group(1))
	
	return list_of_markets
