# Python 3.6.0 |Anaconda 4.3.1 (64-bit)|

from importer import *
from loader import *
import datetime
from helper import *


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

    market_attrs["fixture"] = result.group(5)
    market_attrs["market"] = result.group(6)

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
    
    if number_of_prices > 0:
        df = df_market_attrs
        for number in range(number_of_prices - 1):
            df = pd.concat([df, df_market_attrs])

        df.index = list(range(number_of_prices)) 
        
        dataframe = pd.concat([df, df_prices], axis = 1)
        dataframe = dataframe.loc[:, ['date', 'fixture','kickoff', 'market', 'selection' ,'price']]
    else:
        dataframe = pd.DataFrame(columns = ['date', 'fixture', 'kickoff', 'market', 'selection' ,'price'])
        
    return dataframe



def get_fixtures_from_oddschecker(country, league):
    
    """
    Given country and league, returns a list of fixtures
    """
    
    url_league = 'https://www.oddschecker.com/football/' + country + '/' + league + '/'
    url_core = url_league.replace('https://www.oddschecker.com', "")

    bs4 = from_url_to_bs4(url_league)
    all_fixtures = []

    all_fixtures_links = bs4.find_all(class_ = "button btn-1-small", href = True)
    for fixture_link in all_fixtures_links[:-1]:
        pattern = url_core + "(.*)" + "/winner"
        all_fixtures.append((re.search(pattern, str(fixture_link)).group(1)))
        
    return all_fixtures



def get_df_for_fixture(fixtures, country, league):
    
    url_football = 'https://www.oddschecker.com/football/'
    first_fixture = True
    
    for fixture in fixtures:
                
        url_fixture = url_football + country + '/' + league + '/' + fixture + '/'
        url_markets = url_fixture + 'betting-markets'
    
        all_markets = get_markets_from_oddschecker(url_markets)
        
        if first_fixture:
            url_market = url_fixture + all_markets[0]
            df = get_df_for_market(url_market)
            all_markets = all_markets[1:]
            first_fixture = False
            
        for market in all_markets:
            url_temp = url_fixture + market
            df_temp = get_df_for_market(url_temp)
            df = pd.concat([df, df_temp])
        df.reset_index(drop = True, inplace = True)
        
    return df
