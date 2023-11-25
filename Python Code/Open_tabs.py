import sqlite3
from sqlite3 import Error
import webbrowser
import datetime

def create_connection(db_file):

    conn = None

    try:
            conn = sqlite3.connect(db_file)
    except Error as e:
            print(e)

    return conn

def sql_movies_search(conn):

    #Base SQL statement
    global current_date
    global series_id
    global browser_switch

    #Get current date from database
    cur = conn.cursor()
    cur.execute("SELECT param_value FROM app_parameters WHERE ID=1")
    row = cur.fetchone()
    current_date = row[0]
    print("Current Date: " + current_date)

    #Get Current Series ID from database
    cur.execute("SELECT param_value FROM app_parameters WHERE ID=2")
    row = cur.fetchone()
    series_id = row[0]
    print("Current Series ID: " + series_id)

    #Get Browser Switch from database
    cur.execute("SELECT param_value FROM app_parameters WHERE ID=3")
    row = cur.fetchone()
    browser_switch = row[0]
    print("Browser Switch: " + browser_switch)

    str_sql = "SELECT * FROM nzb_search ns WHERE series_id = " + series_id + " AND download_date = '" + current_date + "';"

    return str_sql

def select_all_movies(conn):

    cur = conn.cursor()

    print("SQL: " + sql_movies_search(conn))

    print(current_date)

    cur.execute(sql_movies_search(conn))

    rows = cur.fetchall()

    #text_title = "Bro"

    text_title = "Date: " + current_date + "; Series ID: " + series_id
    print(text_title)

    with open(r"c:\Users\latto\OneDrive\Python\Projects\NZB_Search\Python Code\bro.txt", 'a') as f:
        f.write(text_title + '\n')
        for row in rows:
                print(row[6])
                line_str = row[6] + '\n'
                f.write(line_str)
                if browser_switch == '1':
                    webbrowser.open_new_tab(row[7])
        f.write("\n")
def main():
        database = r"C:\Users\latto\OneDrive\Python\Projects\NZB_Search\SQLite\nzb.db"
        conn = create_connection(database)

        with conn:
            select_all_movies(conn)

if __name__ == '__main__':
    main()

