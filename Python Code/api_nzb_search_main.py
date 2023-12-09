from datetime import datetime
from api_nzb_search import api_nzb_search
from nzb_search_db_connection import nzb_search_connection
import tkinter as tk
from tkinter import messagebox
from parameterreader import ParameterReader

param_reader = ParameterReader("config.yaml")
param_reader.read_file()

def main(nzb_date, nzb_series):
    # API Stuff
    cls = api_nzb_search()
       
    # Database stuff (see class (nzb_search_connection) for db_type values and descriptions)
        # 1 = mariaDB
        # 2 = SQLite
        # 3 = Business
        # 4 = Business-sandbox
    db_type = param_reader.get_parameter("database_type")

    cls_db_connection = nzb_search_connection(db_type)
    conn = cls_db_connection.create_connection()
    str_sql = 'SELECT m.ID, m.download_date, m.description, m.filename, m.password, m.series_id, m.note, m.nzb_created, m.nzb_exception, m.dl_comments, m.movie_type, m.movie_url FROM movies m WHERE ((m.download_date=?) AND (m.series_id=?) AND (m.nzb_created Is Null) AND (m.nzb_exception Is Null));' # api_nzb_search_01.sql 
    cur = conn.cursor()
    cur.execute(str_sql, (nzb_date, nzb_series))
    row = cur.fetchall()
    print(f'Number of records from Database: {cur.rowcount}')
    for rw in row:
        try:
            collection_id = cls.get_collection_id(rw[3])
            print(f'0:{rw[0]}, 1:{rw[1]}, 5:{rw[5]}, 3:{rw[3]}, 4:{rw[4]}, Collection ID: {collection_id}')
            date = rw[1].strftime("%m%d")
            series = str(rw[5]).zfill(2)
            if rw[4] is None:
                nzb_filename = f'{date} {series} {rw[0]}'
            else:
                nzb_filename = f'{date} {series} {rw[0]} {{{{{rw[4]}}}}}'
            row_id = rw[0]
            print(f'NZB Filename: {nzb_filename}')
            cls.create_nzb_file(collection_id, nzb_filename)
            sql_update = 'UPDATE movies SET nzb_created=1 WHERE ID=?;' # api_nzb_search_02.sql
            cur.execute(sql_update, (row_id,))
            conn.commit()
            print(f'--------------------------------------------------------------')
        except Exception as e:
            print(f"An error occurred: {e}")
    print(f'--------------------------- E N D ----------------------------')
    cur.close()
    conn.close()

def submit():
    nzb_date = entry_date.get()
    nzb_series = entry_series.get()
    # messagebox.showinfo("Submitted", f"NZB Date: {nzb_date}\nNZB Series: {nzb_series}")
    main(nzb_date, nzb_series)

root = tk.Tk()
root.configure(padx=10, pady=10)

label_date = tk.Label(root, text="Enter NZB Date:", font=('Arial', 14))
label_date.grid(row=0, column=0, padx=10, pady=10)

entry_date = tk.Entry(root, font=('Arial', 14))
entry_date.grid(row=0, column=1, padx=10, pady=10)
entry_date.delete(0, tk.END)  # delete the current value
default_date = param_reader.get_parameter("ui_default_date")
entry_date.insert(0, default_date)  # insert the new value

label_series = tk.Label(root, text="Enter NZB Series:", font=('Arial', 14))
label_series.grid(row=1, column=0, padx=10, pady=10)

entry_series = tk.Entry(root, font=('Arial', 14))
entry_series.grid(row=1, column=1, padx=10, pady=10)
entry_series.delete(0, tk.END)  # delete the current value
default_sid = param_reader.get_parameter("ui_default_sid")
entry_series.insert(0, default_sid)  # insert the new value

submit_button = tk.Button(root, text="Submit", command=submit, font=('Arial', 14))
submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()