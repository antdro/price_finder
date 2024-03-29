# Python 3.6.0 |Anaconda 4.3.1 (64-bit)|

from importer import pd
from datetime import datetime

def get_current_date():

    """
    Returns current date and time in the same format as in get_kick_off()
    """
    
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")
    
    return date



def remove_duplicate_prices(df):

    """
    Remove duplicate prices from dataframe
    """
    
    df.drop_duplicates(subset = ['fixture', 'kickoff', 'market', 'selection'], inplace = True)
    
    return df