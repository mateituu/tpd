# Import dependencies

import os
import sqlite3


# Check to see if the database already exists, if not create a keys folder, and create the database.
def database_check():
    # Check to see if the "keys" directory exists, if not creates it
    if "keys" not in os.listdir(os.getcwd()):
        os.makedirs('keys')

    # Check to see if a database exists in keys directory, if not create it
    if not os.path.isfile(f"{os.getcwd()}/keys/database.db"):
        print(f"Creating database.\n")
        dbconnection = sqlite3.connect(f"{os.getcwd()}/keys/database.db")
        dbcursor = dbconnection.cursor()
        dbcursor.execute('CREATE TABLE IF NOT EXISTS "DATABASE" ( "pssh" TEXT, "keys" TEXT, PRIMARY KEY("pssh") )')
        dbconnection.close()