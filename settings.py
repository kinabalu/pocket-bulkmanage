API_URL = 'https://getpocket.com'

# User must define a CONSUMER_KEY
CONSUMER_KEY = None

# Define if you've already authorized so no oauth shuffle necessary again
ACCESS_TOKEN = None

# Load custom development settings overrides
try:
    from local_settings import *
except:
    pass