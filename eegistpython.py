#!/usr/bin/env python3
import requests
import json
import sqlite3

def db_function(gistuser):
          con = sqlite3.connect('invocations.db')
          con.row_factory = sqlite3.Row
          cur = con.cursor()
          #query db for previious run of gist user
          cur.execute("SELECT * FROM invocations WHERE gist = 'mattygyk' ")
          gistdata = cur.fetchone()
          print (gistdata)
          if gistdata is None :
              print ("Database Empty for: ", gistuser )
          else:
              print ("Gistuser is:", gistuser )
              print ("Date: ", gistdata[1])

db_function("mattygyk")

def get_gists(guser):
    api_url = f"https://api.github.com/users/{guser}/gists"
    headers = {"Accept" : "application/json"}
    #for api_url in ['https://api.github.com/gists/public']:
    try:
        response = requests.get(api_url, headers=headers)
        response.text
        jsonResponse = response.json()
#        print(jsonResponse)
        responseDict = jsonResponse[0]
        print (responseDict['created_at'])
    except: 
        print("failed")
    else:
        print(response.status_code)

get_gists("mattygyk")