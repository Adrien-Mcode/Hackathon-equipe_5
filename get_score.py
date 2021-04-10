import pandas
import requests

data = {
    "password": "Ensae06CPdist"
}

response = requests.post("https://51.159.6.59:8798/metrics/", json=data, verify=False)
body = response.json()
df = pandas.DataFrame(body)
df[df.project == "tgtg"].sort_values('value')
print(df)