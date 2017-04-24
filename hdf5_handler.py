import h5py

def create_football_h5(leagues):
    
    """
    Given a dict with leagues, create and return hdf5 file
    """
    
    file = h5py.File('oddschecker.h5', 'w')
    football = file.create_group('football')
    
    file = h5py.File('oddschecker.h5', 'r+')
    
    for country in leagues.keys():
        for league in leagues[country]:
            football.create_group(country + '/' + league)
            
    return file



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

