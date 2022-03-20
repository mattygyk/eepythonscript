#!/usr/bin/env python3

import sqlite3
con = sqlite3.connect('invocations.db')
cur = con.cursor()
#cur.execute('''CREATE TABLE invocations (gist_user text, last_date text)''')
#cur.execute("INSERT INTO invocations VALUES ('mattygyk','2022-03-16T16:39:26Z')")
#cur.execute("SELECT * FROM invocations WHERE gist_user = 'mattygyk' ")
cur.execute("SELECT * FROM invocations ")
print(cur.fetchall())
con.commit()
con.close()