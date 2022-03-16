#!/usr/bin/env python3
import requests
import json
#api_url = "https://api.github.com/gists/public"
headers = {'Accept: application/vnd.github.v3+json'}
for api_url in ['https://api.github.com/gists/public']:
    try:
        response = requests.get(api_url)
        response.text
        print(response.json)
    except: 
        print("failed")
    else:
        print(response.status_code)