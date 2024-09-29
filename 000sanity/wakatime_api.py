import requests
import json

# Session - Provides Connection Pooling Persistence
session = requests.Session()
# Disable Verification
session.verify = False
# Prevent Tracking
session.trust_env = False

'https://wakatime.com/oauth/authorize?client_id=dmvbPh9nvVZVDoqINRLx0URc&redirect_uri=https://br-code.bcodelabs.com/&response_type=code&namelabSite&publisher_name=BR%20Code&website=https%3A%2F%2Fbcodelabs.com%2F&description=Branden%20van%20Staden%20code%20tracker%2F&scopes=read_stats.languages%2Cread_stats.editors#'

def auth_user():
    url = 'https://wakatime.com/oauth/authorize'

    headers = {
        "Referer": "https://wakatime.com/",
        'Content-Type': 'application/x-www-form-urlencoded',        
    }

    params = {
        'client_id': 'dmvbPh9nvVZVDoqINRLx0URc',
        'response_type': 'code',
        'redirect_uri': 'https://br-code.bcodelabs.com/',    
    }

    response = session.post(url=url, data=params, headers=headers)

    print(response.status_code)
    print(response.text)
    input()
    # print(response.json())

# auth_user()

def generate_token():    
    url = 'https://wakatime.com/oauth/token?client_id=dmvbPh9nvVZVDoqINRLx0URc&client_secret=waka_sec_Vj0nxOOxjl9VWfOTX1wij9jEtejHhVpDRRO5QiHnV1CFLuOnnLXx1IwZB9gfOvDHHQNbfKVfQc8hDnZV&grant_type=authorization_code'
    
    headers = {
    'client_id': 'dmvbPh9nvVZVDoqINRLx0URc',
    'Content-Type': 'application/x-www-form-urlencoded'   
    }
    
    params = {
    'client_id': 'dmvbPh9nvVZVDoqINRLx0URc',
    'code': 'aSAFGNCVdTJP6OduY3t0xXY3ZTsIxfhzczRJPDOZ49Kn6KPdgODiHDP58DU2NY9gPxyhKx7Q8KeCHNFz',
    'client_secret': 'waka_sec_Vj0nxOOxjl9VWfOTX1wij9jEtejHhVpDRRO5QiHnV1CFLuOnnLXx1IwZB9gfOvDHHQNbfKVfQc8hDnZV',
    'grant_type': 'authorization_code',
    'redirect_uri': 'https://br-code.bcodelabs.com/',    
    
    }
    response = requests.post(url=url, data=params, headers=headers)

    print(response.status_code)
    print(response.content)
    input()
    print(response.json())

generate_token()
