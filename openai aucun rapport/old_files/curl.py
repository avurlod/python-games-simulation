import requests

API_URL = "https://api.havenondemand.com/1/api/async/recognizelicenseplates/v1"

data = {
    "url": "https://www.havenondemand.com/sample-content/videos/gb-plates.mp4",
    "source_location": "GB",
    "apikey": "695e513c-xxxx-xxxx-a666-xxxxxxxxxx"
 }

response = requests.post(API_URL, data)
print(response.json())
