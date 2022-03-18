#!/usr/bin/env python3

import sqlite3
con = sqlite3.connect('invocations.db')
cur = con.cursor()
cur.execute('''CREATE TABLE invocations (gist text, date text)''')
cur.execute("INSERT INTO invocations VALUES ('mattygyk','2022-03-16T16:39:26Z')")
cur.execute("SELECT * FROM invocations WHERE gist = 'mattygyk' ")
print(cur.fetchall())
con.commit()
con.close()