import requests


class HubspotAPI:
    def __init__(self, token):
        self.apiurl = 'https://api.hubapi.com/crm/v3/objects'
        self.headers = {'Accepts': 'application/json', 'authorization': "Bearer " + token}

    def getDeals(self, limit=5):
        url = self.apiurl + '/deals'
        parameters = {'limit': limit}
        r = requests.get(url, headers=self.headers, params=parameters)
        json_data = r.json()['results']
        return json_data
