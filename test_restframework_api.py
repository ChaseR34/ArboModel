import requests

url = "http://localhost:8000/api/v1/weather/"
headers = {
    "GET":"/api/v1/weather/ HTTP/1.1",
    "Host":"127.0.0.1:8000",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Authorization": "Token 3c30ccb4255e7861e2e3803034f1050718c72e65",
    "Origin": "http://localhost:8080",
    "DNT": "1",
    "Referer": "http://localhost:8080/"
}
# r = requests.get(url)
r = requests.get(url, headers=headers)
print("printing stuff")
print(r.headers)
print(r.url)
print(r.status_code)
print(r.text)
print(r.raw)