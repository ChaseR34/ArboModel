import requests

params = {
    "scientificName": "Zenaida macroura"
}

api_url = 'https://api.gbif.org/v1/occurrence/search/'


r = requests.get(api_url, params=params)

print(r.text)