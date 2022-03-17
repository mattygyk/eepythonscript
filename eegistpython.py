#!/usr/bin/env python3
import requests
import json
import sqlite3

def db_function(gistuser):
          con = sqlite3.connect('invocations.db')
          con.row_factory = sqlite3.Row
          cur = con.cursor()
          #query db for previious run of gist user
          cur.execute("SELECT * FROM invocations WHERE gist = 'mabongogyk' ")
          gistdata = cur.fetchone()
          print (gistdata)
          if gistdata == "None" :
              print ("Database Empty for: ", gistuser )
          else:
              print ("Gistuser is:", gistuser )

mattty = db_function("mattygyk")

# #api_url = "https://api.github.com/gists/public"
# headers = {"Accept" : "application/json"}
# for api_url in ['https://api.github.com/gists/public']:
#     try:
#         response = requests.get(api_url, headers=headers)
#         response.text
#         data = response.json()
#         print(data)
#     except: 
#         print("failed")
#     else:
#         print(response.status_code)
