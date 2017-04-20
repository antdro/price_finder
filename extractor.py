# Python 3.6.0 |Anaconda 4.3.1 (64-bit)|

from importer import *
from loader import *
import datetime



def get_markets_from_oddschecker(url):
	
	"""
	Returns a list with markets available on www.oddschecker.com
	
	URL example: 'https://www.oddschecker.com/football/italy/serie-a/fiorentina-v-inter/betting-markets'
	"""
	if "/betting-markets" not in url:
			raise ValueError("URL is invalid. \nURL example: 'https://www.oddschecker.com/football/italy/serie-a/fiorentina-v-inter				/betting-markets'")
        
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



def get_best_prices_for_market(url):

	"""
	Given URL, returns dictionary with selections and prices for correcponding fixture and market
	"""

	bs4 = from_url_to_bs4(url)
	best_odds = bs4.findAll(class_ = "add-to-bet-basket")
	selections = []
	prices = []
	prices_dict = {}

	for record in best_odds:
		selection = record['data-name']    
		price_string = record['data-ng-click']
		price = re.search("(.*), (.*), (.*)\)", price_string).group(3)
		selections.append(selection)
		prices.append(price) 

	prices_dict["selection"] = selections
	prices_dict["price"] = prices
	
	return prices_dict



def get_kick_off(url):
    
    """
    Given URL, returns fixture's kick-off date and time as a string
    """
    
    bs4 = from_url_to_bs4(url)
    source = str(bs4)
    kick_off_string = re.search("startDate\":\"(\d\d\d\d-\d\d-\d\dT\d\d:\d\d)", source)
    kick_off = kick_off_string.group(1).replace('T', " ")
    
    return kick_off



def parse_football_url(url):

    """
    Given URL, returns a dictionary with market attributes
    """

    football_url_pattern = "https://(.*)/(.*)/(.*)/(.*)/(.*)/(.*)"
    result = re.search(football_url_pattern, url)

    market_attrs = {}

    market_attrs["website"] = [result.group(1)]
    market_attrs["sport"] = [result.group(2)]
    market_attrs["country"] = [result.group(3)]
    market_attrs["league"] = [result.group(4)]
    market_attrs["fixture"] = [result.group(5)]
    market_attrs["market"] = [result.group(6)]

    return market_attrs



def get_df_for_market(url):

    """
    Given URL, returns dataframe with market attributes and prices
    """

    prices_dict = get_best_prices_for_market(url)
    df_prices = pd.DataFrame(prices_dict)

    market_attrs = parse_football_url(url)
    kick_off = get_kick_off(url)
    date = get_current_date()
    market_attrs["kickoff"] = [kick_off]
    market_attrs["date"] = [date]
    df_market_attrs = pd.DataFrame(market_attrs)

    number_of_prices = len(prices_dict['price'])
    df = df_market_attrs
    for number in range(number_of_prices - 1):
        df = pd.concat([df, df_market_attrs])
    df.index = list(range(number_of_prices)) 

    dataframe = pd.concat([df, df_prices], axis = 1)
    dataframe = dataframe.loc[:, ['date', 'website', 'sport','fixture', 'country','league','market', 'selection' ,'price','kickoff']]

    return dataframe