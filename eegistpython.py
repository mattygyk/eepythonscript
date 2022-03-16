#!/usr/bin/env python3
import requests
import json
#api_url = "https://api.github.com/gists/public"
headers = {"Accept" : "application/json"}
for api_url in ['https://api.github.com/gists/public']:
    try:
        response = requests.get(api_url, headers=headers)
        response.text
        data = response.json()
        print(data)
    except: 
        print("failed")
    else:
        print(response.status_code)