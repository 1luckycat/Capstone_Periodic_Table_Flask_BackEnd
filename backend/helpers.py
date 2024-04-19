import json
import decimal
import requests
import requests_cache
import os

requests_cache.install_cache('element_cache', backend='sqlite')


def get_table():
     # url = "https://periodictable.p.rapidapi.com/"
     url = "https://periodic-table-api.p.rapidapi.com/getAllElements"

     # headers = {
	#      "X-RapidAPI-Key": os.environ.get('api_key'),
	#      "X-RapidAPI-Host": "periodictable.p.rapidapi.com"
     # }
     headers = {
          "X-RapidAPI-Key": os.environ.get('api_key'),
          "X-RapidAPI-Host": "periodic-table-api.p.rapidapi.com"
     }

     response = requests.get(url, headers=headers)

     if response.status_code == 200:
          return response.json()
     else:
          print(f"Error fetching data: {response.status_code}")
          return None



class JSONEncoder(json.JSONEncoder):
     def default(self, obj):
          if isinstance(obj, decimal.Decimal):
               return str(obj)
          return json.JSONEncoder(JSONEncoder, self).default(obj)