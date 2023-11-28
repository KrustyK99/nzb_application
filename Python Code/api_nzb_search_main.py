from api_nzb_search import api_nzb_search
from nzb_search_db_connection import nzb_search_connection
import tkinter as tk
from tkinter import messagebox

def main(nzb_date, nzb_series):
    # API Stuff
    cls = api_nzb_search()
    
    # Database stuff
    cls_db_connection = nzb_search_connection(1)
    conn = cls_db_connection.create_connection()
    #nzb_date = "2022-10-12"
    #nzb_series = 7
    str_sql = 'SELECT m.ID, m.download_date, m.description, m.filename, m.password, m.series_id, m.note, m.nzb_created, m.nzb_exception, m.dl_comments, m.movie_type, m.movie_url FROM movies m WHERE ((m.download_date=?) AND (m.series_id=?) AND (m.nzb_created Is Null) AND (m.nzb_exception Is Null));' # api_nzb_search_01.sql 
    cur = conn.cursor()
    cur.execute(str_sql, (nzb_date, nzb_series))
    row = cur.fetchall()
    print(f'Number of records from Database: {cur.rowcount}')
    for rw in row:
        try:
            collection_id = cls.get_collection_id(rw[3])
            print(f'0:{rw[0]}, 1:{rw[1]}, 5:{rw[5]}, 3:{rw[3]}, 4:{rw[4]}, Collection ID: {collection_id}')
            nzb_filename = f'{rw[0]}-{rw[3]}'
            cls.create_nzb_file(collection_id, nzb_filename)
            print(f'--------------------------------------------------------------')
        except Exception as e:
            print(f"An error occurred: {e}")
    cur.close()
    conn.close()

def submit():
    nzb_date = entry_date.get()
    nzb_series = entry_series.get()
    messagebox.showinfo("Submitted", f"NZB Date: {nzb_date}\nNZB Series: {nzb_series}")

root = tk.Tk()

label_date = tk.Label(root, text="Enter NZB Date:")
label_date.pack()

entry_date = tk.Entry(root)
entry_date.pack()

label_series = tk.Label(root, text="Enter NZB Series:")
label_series.pack()

entry_series = tk.Entry(root)
entry_series.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()