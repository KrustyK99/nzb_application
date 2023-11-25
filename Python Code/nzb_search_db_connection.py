import mariadb
import sys
import sqlite3
from sqlite3 import Error

class nzb_search_connection:
    
    def __init__(self, db_type):
        self.db_type = db_type

        if self.db_type == 1:
            self.db_type_desc = "mariaDB"
        elif self.db_type == 2:
            self.db_type_desc = "SQLit"
        elif self.db_type == 3:
            self.db_type_desc = "Business"            
        elif self.db_type == 4:
            self.db_type_desc = "Business-sandbox"
        else:
            print("NZB Search: Unrecognized database type.")
            self.db_type_desc = "< NZB Search: Unrecognized DB Type >"

    def create_connection(self):
        if self.db_type == 1:
            try:
                self.conn = mariadb.connect(
                user="linc_dev",
                password="D0gP1L3$1lv8rB1g",
                host="192.168.2.252",
                port=3307,
                database="nzb_search_dev")
                return self.conn
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)
        elif self.db_type == 2:
            db_file = r"C:\Users\latto\OneDrive\Python\Projects\NZB_Search\SQLite\nzb.db"
            self.conn = None
            try:
                self.conn = sqlite3.connect(db_file)
            except Error as e:
                    print(e)
            return self.conn
        elif self.db_type == 3:
            try:
                self.conn = mariadb.connect(
                user="linc_dev",
                password="D0gP1L3$1lv8rB1g",
                host="192.168.2.252",
                port=3307,
                database="Business")
                return self.conn
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)
        elif self.db_type == 4:
            try:
                self.conn = mariadb.connect(
                user="linc_dev",
                password="D0gP1L3$1lv8rB1g",
                host="192.168.2.252",
                port=3307,
                database="Business-sandbox")
                return self.conn
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

def main():
    print("<< MAIN START >>")
    cls = nzb_search_connection(1)
    conn = cls.create_connection()
    cur = conn.cursor()
    cur.execute("select * from movies where id<50;")
    row = cur.fetchall()
    print(cur.rowcount)
    print("<< MAIN END >>")

if __name__ == '__main__':
    main()