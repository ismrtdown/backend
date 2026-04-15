import requests

url = "https://backend-09gi.onrender.com/report"

payloads = [
    {
        "station_code": "CC3"
    },
    {
        "station_code": "CC4"
    },
    {
        "station_code": "CC5"
    },
    {
        "station_code": "CE1"
    },
    {
        "station_code": "CE2"
    },
]
"""

payloads = [
    {
        "station_code": "NE3"
    },
    {
        "station_code": "NE5"
    },
    {
        "station_code": "NE7"
    },
]
"""

for x in payloads:
    for _ in range(10):
        print(requests.post(url, json=x, headers={"Content-Type": "application/json"}))
