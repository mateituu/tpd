# Import dependencies

import sqlite3
import os


# Define cache function
def cache_keys(pssh: str, keys: str):
    dbconnection = sqlite3.connect(f"{os.getcwd()}/keys/database.db")
    dbcursor = dbconnection.cursor()
    dbcursor.execute("INSERT or REPLACE INTO database VALUES (?, ?)", (pssh, keys))
    dbconnection.commit()
    dbconnection.close()