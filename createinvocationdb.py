#!/usr/bin/env python3

import sqlite3
con = sqlite3.connect('invocations.db')
cur = con.cursor()
cur.execute('''CREATE TABLE invocations (gist texdt, date text)''')
con.commit()
con.close()