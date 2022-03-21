#!/usr/bin/env python3
import re
import requests
import json
import sqlite3
import pandas as pd
import argparse
from datetime import datetime

github_user = input("Enter your github user id: -> ")
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest = "reportOveride", default = "no")
args = parser.parse_args()

epochFmt = datetime(1970, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ')

def db_function(gistuser):
        con = sqlite3.connect('invocations.db')
        cur = con.cursor()
        #query db for previous run of gist user
        cur.execute("SELECT * FROM invocations WHERE gist_user = ? ", (gistuser,))
        gistData = cur.fetchone()
#        print (gistData)
#        epochFmt = datetime(1970, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ')
        nowFmt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        if gistData is None :
            #Add a record if this is the first time this user has been queried 
 #           print ("Database Empty for: ", gistuser)
            try:
                gist_insert_query = """INSERT INTO invocations (gist_user, last_date) VALUES (?, ?);"""
                val_data = (gistuser, nowFmt)
                cur.execute(gist_insert_query, val_data)
#                print("Record Inserted:", cur.rowcount )
                con.commit()
                con.close()
                return epochFmt
            except con.Error as error:
                print("Failed to insert data into sqlite table", error)
        else:
            gist_update_query = """UPDATE invocations SET last_date = ? WHERE gist_user = ? ;"""
            val_data = (nowFmt, gistuser)
            cur.execute(gist_update_query, val_data)
            con.commit()
            con.close()
#            print ("Gistuser is:", gistuser )
#            print ("Date: ", gistDate)
            return gistData[1]


# mydate = db_function(github_user)
# print ("mydate: ", mydate )

def get_gists(guser):
    api_url = f"https://api.github.com/users/{guser}/gists"
    headers = {"Accept" : "application/json"}
    todayFrmt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    if args.reportOveride == "no":
       gistUserDate = db_function(guser)
    else:
       gistUserDate = epochFmt
    # print ("Date from the funcition = ", gistUserDate)
    # print ("The datatype of the gistuserdata = ", type(gistUserDate))
    # gistUserDateFmt = datetime.strptime(gistUserDate, '%Y-%m-%dT%H:%M:%SZ')
    gistUserDateFmt = pd.to_datetime(gistUserDate)
    # print ("gistUserDataFmt = ", gistUserDateFmt)
    # print ("The datatype of the gistuserdataFMT = ", type(gistUserDateFmt))
    pdDataDS = pd.DataFrame(columns=['URL', 'CREATION_DATE', 'URL'])
    try:
        response = requests.get(api_url, headers=headers)
        rspJ = response.json()
        length = len(rspJ)
        count_records = 0
#        resultsDataset = []
        resultsDataset = pd.DataFrame(columns=['FILENAME', 'CREATION_DATE', 'URL'])
        for i in rspJ:
            rspDict=dict(i)
            pdData = []
            createdDate = (rspDict.get('created_at'))
            # createdDateFmt = datetime.strptime(createdDate, '%Y-%m-%dT%H:%M:%SZ')
            createdDateFmt = pd.to_datetime(createdDate)
            # print ("The datatype of createddate = ", type(createdDate)) 
            # print ("The datatype of createddateFMT = ", type(createdDateFmt)) 
            # print ("Created Date Fmt: ",  createdDateFmt)
            if createdDateFmt > gistUserDateFmt :
                # print ("Type= :", type(rspDict)) 
#                print ("URL= : ", rspDict.get('url'), rspDict.get('created_at'))
                gUrl=(rspDict.get('url'))
                files=(rspDict.get('files'))
                filesdata=list(files.values())[0]
                fileName = (filesdata.get('filename'))
                print ("File Name : ", fileName, "Creation Date : ", createdDate, "URL :", gUrl)
                pdData = [fileName, createdDate, gUrl]
                print ("lentgh: ", len(pdData))
                resultsDataset.loc[len(resultsDataset)] = pdData

#                print ("FILESDATA ", filesdata)
#                print ("FILENAME; ", filesdata.get('filename'))
                
                count_records += 1
        print (resultsDataset)
        if count_records == 0:
            print ("Nothing new to report")
            print ("If you want to overide the date and produce a full report re-run this script with -f yes flag")
        else:
            print ("Number of records reported = ", count_records)
    except:
        print("failed for some reason")

get_gists(github_user)