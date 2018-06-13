"""Configuration settings for console app using device flow authentication
"""

CLIENT_ID = 'bd3a0357-8ca6-46e3-890a-457c8760fab2'

AUTHORITY_URL = 'https://login.microsoftonline.com/common'
RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'beta'

# This code can be removed after configuring CLIENT_ID and CLIENT_SECRET above.
if 'ENTER_YOUR' in CLIENT_ID:
    print('ERROR: config.py does not contain valid CLIENT_ID.')
    import sys
    sys.exit(1)