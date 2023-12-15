from datetime import datetime
from api_nzb_search import api_nzb_search
from nzb_search_db_connection import nzb_search_connection
import tkinter as tk
from tkinter import messagebox
from parameterreader import ParameterReader
from fn_pw_cap import Filename_Password_Capture

param_reader = ParameterReader("config.yaml")

try:
    param_reader.read_file()    
except Exception as e:
    print(f'Problem reading the config file: {e}')

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
    write_to_status(f'Number of records from Database: {cur.rowcount}\n')

    for rw in row:
        try:
            collection_id = cls.get_collection_id(rw[3])
            print(f'0:{rw[0]}, 1:{rw[1]}, 5:{rw[5]}, 3:{rw[3]}, 4:{rw[4]}, Collection ID: {collection_id}')
            date = rw[1].strftime("%m%d")
            series = str(rw[5]).zfill(2) 

            # The following IF statement is to handle the case where there is no password.
            if rw[4] is None:
                nzb_filename = f'{date} {series} {rw[0]}' # Filename where there is NO password.
                write_to_status(f'ID: {rw[0]}, NO PW\n')
            else:
                nzb_filename = f'{date} {series} {rw[0]} {{{{{rw[4]}}}}}' # Filename where there IS no password.
                write_to_status(f'ID: {rw[0]}\n')
            print(f'NZB Filename: {nzb_filename}')

            # The method create_nzb_file resutrns a tuple (success, error)
            success, error = cls.create_nzb_file(collection_id, nzb_filename) 
            row_id = rw[0]
            if not success:
                print(f'Error occurred: {error}')
                sql_update = 'UPDATE movies SET nzb_created=0 WHERE ID=?;' # api_nzb_search_02.sql
                cur.execute(sql_update, (row_id,))
                conn.commit()
            else: 
                sql_update = 'UPDATE movies SET nzb_created=1 WHERE ID=?;' # api_nzb_search_02.sql
                cur.execute(sql_update, (row_id,))
                conn.commit()
            print(f'--------------------------------------------------------------')
        except Exception as e:
            print(f"An error occurred: {e}")
    print(f'--------------------------- E N D ----------------------------')
    cur.close()
    conn.close()
    write_to_status(f'--------------------------- E N D ----------------------------\n')

def submit():
    nzb_date = entry_date.get()
    nzb_series = entry_series.get()
    # messagebox.showinfo("Submitted", f"NZB Date: {nzb_date}\nNZB Series: {nzb_series}")
    main(nzb_date, nzb_series)

def text_capture():
    #capture_date = param_reader.get_parameter("nzb_capture_date")
    #capture_sid = param_reader.get_parameter("nzb_capture_sid")
    capture_date = entry_capture_date.get()
    capture_sid = entry_capture_series.get()
    txt_capture = Filename_Password_Capture(1)
    txt_capture.database_upate(capture_date, capture_sid)
    print(f'Text Capture Completed.')
    write_to_status(f'Text Capture Completed.\n')

def write_to_status(text):
    text_widget.insert(tk.END, text)

root = tk.Tk()
root.configure(padx=10, pady=10)

label_date = tk.Label(root, text="NZB Date:", font=('Arial', 14))
label_date.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry_date = tk.Entry(root, font=('Arial', 14))
entry_date.grid(row=0, column=1, padx=10, pady=10)
entry_date.delete(0, tk.END)  # delete the current value
default_date = param_reader.get_parameter("ui_default_date")
entry_date.insert(0, default_date)  # insert the new value

label_series = tk.Label(root, text="NZB Series:", font=('Arial', 14))
label_series.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry_series = tk.Entry(root, font=('Arial', 14))
entry_series.grid(row=1, column=1, padx=10, pady=10)
entry_series.delete(0, tk.END)  # delete the current value
default_sid = param_reader.get_parameter("ui_default_sid")
entry_series.insert(0, default_sid)  # insert the new value

submit_button = tk.Button(root, text="Submit", command=submit, font=('Arial', 14))
submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# New separator line
separator = tk.Frame(root, height=3, bd=1, relief='sunken')
separator.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

label_capture_date = tk.Label(root, text="Capture Date:", font=('Arial', 14), anchor="w", justify="left")
label_capture_date.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_capture_date = tk.Entry(root, font=('Arial', 14))
entry_capture_date.grid(row=4, column=1, padx=10, pady=10)
default_entry_capture_date = param_reader.get_parameter("nzb_capture_date")
entry_capture_date.delete(0, tk.END)  # delete the current value
entry_capture_date.insert(0, default_entry_capture_date)  # insert the new value

label_capture_sid = tk.Label(root, text="Capture Series:", font=('Arial', 14), anchor="w", justify="left")
label_capture_sid.grid(row=5, column=0, padx=10, pady=10, sticky="w")
entry_capture_series = tk.Entry(root, font=('Arial', 14))
entry_capture_series.grid(row=5, column=1, padx=10, pady=10)
default_entry_capture_series = param_reader.get_parameter("nzb_capture_sid")
entry_capture_series.delete(0, tk.END)  # delete the current value
entry_capture_series.insert(0, default_entry_capture_series)  # insert the new value

capture_button = tk.Button(root, text="Capture", command=text_capture, font=('Arial', 14))
capture_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

text_widget = tk.Text(root, height=10, width=30)
text_widget.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

root.mainloop()