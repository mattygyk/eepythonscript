#!/usr/bin/env python3
import requests
import json
import sqlite3
import pandas as pd
import argparse
from tabulate import tabulate
from datetime import datetime

#Set user inputs and epoch Date
github_user = input("Enter your github user id: -> ")
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest = "reportOveride", default = "no")
args = parser.parse_args()
epochFmt = datetime(1970, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ')

#Function to if there has been a run previously for a user.
def db_function(gistuser):
        con = sqlite3.connect('invocations.db')
        cur = con.cursor()
        #query db for previous run of gist user
        cur.execute("SELECT * FROM invocations WHERE gist_user = ? ", (gistuser,))
        gistData = cur.fetchone()
        nowFmt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        if gistData is None :
            #Add a record if this is the first time this user has been queried 
            try:
                gist_insert_query = """INSERT INTO invocations (gist_user, last_date) VALUES (?, ?);"""
                val_data = (gistuser, nowFmt)
                cur.execute(gist_insert_query, val_data)
                con.commit()
                con.close()
                return epochFmt
            except con.Error as error:
                print("Failed to insert data into sqlite table", error)
        else:
            #If user already exists update the last_date to now and retgurn the previous runs date.
            gist_update_query = """UPDATE invocations SET last_date = ? WHERE gist_user = ? ;"""
            val_data = (nowFmt, gistuser)
            cur.execute(gist_update_query, val_data)
            con.commit()
            con.close()
            return gistData[1]


def get_gists(guser):
    api_url = f"https://api.github.com/users/{guser}/gists"
    headers = {"Accept" : "application/json"}
    todayFrmt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    # Check for overide setting. If yes return formatted epcoh date. This will set the date to check from regardless of results from db_function function.
    if args.reportOveride == "no":
       gistUserDate = db_function(guser)
    else:
       gistUserDate = epochFmt
    gistUserDateFmt = pd.to_datetime(gistUserDate)
    try:
        response = requests.get(api_url, headers=headers)
        rspJ = response.json()
        length = len(rspJ)
        count_records = 0
        #Build a dataframe of lists for each record returned from the api
        resultsDataset = pd.DataFrame(columns=['FILENAME', 'CREATION_DATE', 'GIST API INFO URL'])
        for i in rspJ:
            rspDict=dict(i)
            pdData = []
            createdDate = (rspDict.get('created_at'))
            createdDateFmt = pd.to_datetime(createdDate)
            if createdDateFmt > gistUserDateFmt :
                gUrl=(rspDict.get('url'))
                files=(rspDict.get('files'))
                filesdata=list(files.values())[0]
                fileName = (filesdata.get('filename'))
                createDateRefromatted = createdDateFmt.strftime("%Y-%m-%d  %H:%M:%S")
                pdData = [fileName, createDateRefromatted, gUrl]
                resultsDataset.loc[len(resultsDataset)] = pdData
                count_records += 1
        if count_records == 0:
            print ("Nothing new to report")
            print ("If you want to overide the date and produce a full report re-run this script with -f yes flag")
        else:
            print(tabulate(resultsDataset, showindex=False, headers=resultsDataset.columns))
            print ("Number of records reported = ", count_records)
    except:
        print("Github User "+guser+" does not exist !")

get_gists(github_user)