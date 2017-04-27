from importer import h5py, pd, HDFStore
from extractor import *
from loader import *
from helper import *


def create_football_h5():
    
    """
    Given a dict with leagues, create and return hdf5 file
    """
    
    h5 = h5py.File('oddschecker.h5', 'w')
    football = h5.create_group('football')
    h5.close()
            
    return h5



def print_h5_structure(file):
    
    """
    Prints the structure of given hdf5 file
    """
    
    for sport in file.keys():
        print (sport)
        for country in file[sport]:
            print ('\t' + country)
            for league in file[sport][country]:
                print ('\t\t' + league)
                for table in file[sport][country][league]:
                    print ('\t\t\t' + table)
        print ('\n')

        
        
def add_league_to_football_h5(leagues):    
    
    """
    Adds leagues from {country: league} dict to football h5 file; returns updated h5
    """
    
    h5 = h5py.File('oddschecker.h5', 'r+')
    
    football = h5['football']
    
    for country in leagues.keys():
        for league in leagues[country]:
            football.create_group(country + '/' + league)
    
    h5.close()
    
    return h5



def update_league_in_db(df, country, league):
    
    """
    Update league in database given datafrme, country and league
    """
    
    if country == 'english':
        country = country.replace('english', 'england')
    country = country.replace('other/', '')
    country = country.replace('world/', '')
    league = league.replace('-', '_')

    store = HDFStore('oddschecker.h5')
    try:
        data_h5 = store['football/' + country + '/' + league]
        
        data_updated = pd.concat([data_h5, df], axis = 0)
        data_updated = data_updated.loc[:, ['date', 'fixture', 'kickoff', 'market', 'selection', 'price']]
        data_updated = remove_duplicate_prices(data_updated)
        data_updated.reset_index(drop = True, inplace = True)

        store['football/' + country + '/' + league] = data_updated
    except TypeError:
        pass

    store.close()
    
    
    
def update_db(leagues):

    """
    Update database given dictionary with leagues
    """
    
    from extractor import get_fixtures_from_oddschecker, get_df_for_fixture
    
    for country in leagues:
        for league in leagues[country]:
            
            print(country)
            print('\t' + league)
    
            fixtures = get_fixtures_from_oddschecker(country, league)
            
            df = get_df_for_fixture(fixtures, country, league)

            update_league_in_db(df, country, league)
