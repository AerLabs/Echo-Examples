import requests
import json

url = "https://echo.aerlabs.com/v1/noise"

with open('noise_input.json', 'r') as file:
    data=file.read()

token = input("please input your token")

payload = data
headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer " + token,
    'cache-control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
