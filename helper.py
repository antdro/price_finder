# Python 3.6.0 |Anaconda 4.3.1 (64-bit)|

import datetime

def get_current_date():
	
	"""
	Returns current date and time in the same format as in get_kick_off()
	"""
	
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M")
	
	return date