import h5py

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