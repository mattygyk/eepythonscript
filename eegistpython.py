#!/usr/bin/env python3
from xmlrpc.client import _iso8601_format
import requests
import json
import sqlite3
from datetime import datetime

github_user = input("Enter your github user id:")


def db_function(gistuser):
        con = sqlite3.connect('invocations.db')
        cur = con.cursor()
        #query db for previous run of gist user
        cur.execute("SELECT * FROM invocations WHERE gist_user = ? ", (gistuser,))
        gistdata = cur.fetchone()
        print (gistdata)
        today = datetime.now()
        todayFrmt = today.strftime('%Y-%m-%dT%H:%M:%SZ')
        if gistdata is None :
            #Add a record if this is the first time this user has been queried 
            print ("Database Empty for: ", gistuser)
            try:
                gist_insert_query = """INSERT INTO invocations (gist_user, last_date) VALUES (?, ?);"""
                val_data = (gistuser, todayFrmt)
                cur.execute(gist_insert_query, val_data)
                print("Record Inserted:", cur.rowcount )
                con.commit()
            except con.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if con:
                    con.close()
                    print("The SQLite connection is closed")
                    return ("NoDate")
        else:
            print ("Gistuser is:", gistuser )
            print ("Date: ", gistdata[1])
            return todayFrmt 


db_function(github_user)

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

get_gists("cpcdoy")