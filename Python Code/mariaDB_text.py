# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="linc_dev",
        password="D0gP1L3$1lv8rB1g",
        host="192.168.2.252",
        port=3307,
        database="nzb_search_dev"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("select * from movies;")

row = cur.fetchall()

print("Cursor created.")
print("Number of rows: " + str(cur.rowcount))

