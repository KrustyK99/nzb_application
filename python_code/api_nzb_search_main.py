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

    # Add variable curr_datetime to the status messages.
    curr_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    write_to_status(f'------------------- S T A R T -------------------\n{curr_datetime}\n')
    
    print(f'Number of records from Database: {cur.rowcount}')
    write_to_status(f'Number of records from Database: {cur.rowcount}\n')

    counter = 0 # Counter for number of records processed.
    counter_saved = 0 # Counter for number of files saved.
    for rw in row:
        try:
            collection_id = cls.get_collection_id(rw[3])
            #0:ID, 1:download_date, 2:description, 3:filename, 4:password, 5:series_id, 6:note, 7:nzb_created, 8:nzb_exception, 9:dl_comments, 10:movie_type, 11:movie_url
            print(f'0:{rw[0]}, 1:{rw[1]}, 5:{rw[5]}, 3:{rw[3]}, 4:{rw[4]}, Collection ID: {collection_id}')
            date = rw[1].strftime("%m%d")
            series = str(rw[5]).zfill(2) 

            # The following IF statement is to handle the case where there is no password.
            if rw[4] is None:
                nzb_filename = f'{date} {series} {rw[0]}' # Filename where there is NO password.
                success, error = cls.create_nzb_file(collection_id, nzb_filename) 
                row_id = rw[0]
                if not success:
                    print(f'Error occurred: {error}')
                    sql_update = 'UPDATE movies SET nzb_created=0 WHERE ID=?;' # api_nzb_search_02.sql
                    cur.execute(sql_update, (row_id,))
                    conn.commit()
                    write_to_status(f'  ID: {rw[0]}, Error:{error}\n')
                else: 
                    sql_update = 'UPDATE movies SET nzb_created=1 WHERE ID=?;' # api_nzb_search_02.sql
                    cur.execute(sql_update, (row_id,))
                    conn.commit()
                    counter_saved += 1
                    write_to_status(f'  ID: {rw[0]}, nzb saved!\n')
                print(f'-------------------------------------------------')
                
            else:
                nzb_filename = f'{date} {series} {rw[0]} {{{{{rw[4]}}}}}' # Filename where there IS no password.
                success, error = cls.create_nzb_file(collection_id, nzb_filename)
                row_id = rw[0]
                if not success:
                    print(f'Error occurred: {error}')
                    sql_update = 'UPDATE movies SET nzb_created=0 WHERE ID=?;' # api_nzb_search_02.sql
                    cur.execute(sql_update, (row_id,))
                    conn.commit()
                    write_to_status(f'  ID: {rw[0]}, Error:{error}\n')
                else: 
                    sql_update = 'UPDATE movies SET nzb_created=1 WHERE ID=?;' # api_nzb_search_02.sql
                    cur.execute(sql_update, (row_id,))
                    conn.commit()
                    counter_saved += 1
                    write_to_status(f'  ID: {rw[0]}, nzb saved!\n')
                #write_to_status(f'ID: {rw[0]}\n')
            print(f'NZB Filename: {nzb_filename}')
            print(f'-------------------------------------------------')
        except Exception as e:
            print(f"An error occurred: {e}")
        counter += 1
    
    print(f'{curr_datetime}\n--------------------- E N D ---------------------\n')
    cur.close()
    conn.close()
        
    write_to_status(f'Number of records processed: {counter}\nNumber of files saved: {counter_saved}\n')
    end_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    total_time = datetime.strptime(end_datetime, "%m/%d/%Y %H:%M:%S") - datetime.strptime(curr_datetime, "%m/%d/%Y %H:%M:%S")
    write_to_status(f'Total run time: {total_time}\n')
    write_to_status(f'{end_datetime}\n--------------------- E N D ---------------------\n')

def submit():
    nzb_date = entry_date.get()
    nzb_series = entry_series.get()
    # messagebox.showinfo("Submitted", f"NZB Date: {nzb_date}\nNZB Series: {nzb_series}")
    main(nzb_date, nzb_series)

def text_capture():    
    capture_date = entry_capture_date.get()
    capture_sid = entry_capture_series.get()
    txt_capture = Filename_Password_Capture(1)
    
    # Add variable curr_datetime to the status messages.
    curr_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    write_to_status(f'------------------- S T A R T -------------------\n{curr_datetime}\n')

    # write_to_status box that the text capture is starting and list capture data and series id
    write_to_status(f'Text Capture Starting.\nCapture Date: {capture_date}\nCapture Series: {capture_sid}\n')
    
    try:
        id_list = txt_capture.database_upate(capture_date, capture_sid)
        for key, value in id_list.items():
            if not isinstance(value, tuple):
                write_to_status(f'  {key}: {value}\n')
            else:
                fn = value[0][:7] + "..." if len(value[0]) > 7 else value[0]
                pw = value[1][:7] + "..." if len(value[1]) > 7 else value[1]
                write_to_status(f'  {key}: File: {fn} PW: {pw}\n')
        # write to status the number of records processed
        write_to_status(f'Number of records processed: {len(id_list)}\n')
    except Exception as e:
        print(f'Error updating filename/password: {e}')
        write_to_status(f'Error updating filename/password: {e}\n')
    print(f'Text Capture Completed.')
    write_to_status(f'Text Capture Completed.\n')
    end_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    total_time = datetime.strptime(end_datetime, "%m/%d/%Y %H:%M:%S") - datetime.strptime(curr_datetime, "%m/%d/%Y %H:%M:%S")
    write_to_status(f'Total run time: {total_time}\n')
    write_to_status(f'{curr_datetime}\n--------------------- E N D ---------------------\n')

def write_to_status(text):
    text_widget.insert(tk.END, text)
    # write text to app_log.md file
    with open('app_log.md', 'a') as f:
        f.write(text)

root = tk.Tk()
root.title("NZB Application")
# root.iconbitmap("path/to/icon.ico")  # Replace "path/to/icon.ico" with the actual path to your icon file

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Add frame to holder title and icon
frame_title = tk.Frame(root, bg="light blue", highlightthickness=2, highlightbackground="green")
frame_title.grid(row=0, column=0, padx=10, pady=(10,5), sticky="nsew")
frame_title.grid_columnconfigure(0, weight=1)
# frame_title.grid_columnconfigure(1, weight=1)
frame_title.grid_rowconfigure(0, weight=1)


# Frame for nzb date and series
frame_nzb = tk.Frame(root, bg="light blue")
frame_nzb.grid(row=1, column=0, padx=10, pady=(10,5), sticky="nsew")
frame_nzb.grid_columnconfigure(0, weight=1)
frame_nzb.grid_columnconfigure(1, weight=1)
frame_nzb.grid_rowconfigure(0, weight=1)

# Frame for filename and password capture
frame_capture = tk.Frame(root, bg="light green")
frame_capture.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
frame_capture.grid_columnconfigure(0, weight=1)
frame_capture.grid_columnconfigure(1, weight=1)
frame_capture.grid_rowconfigure(0, weight=1)

# Frame for status messages
frame_status = tk.Frame(root, bg="#D8BFD8")
frame_status.grid(row=3, column=0, padx=10, pady=(5,10), sticky="nsew")
frame_status.grid_columnconfigure(0, weight=1)
frame_status.grid_rowconfigure(0, weight=1)

# Add label to title frame
label_title = tk.Label(frame_title, text="NZB Application", font=('Verdana', 16), bg="light blue", justify="center")
label_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Label: NZB Date
label_date = tk.Label(frame_nzb, text="NZB Date:", font=('Arial', 14), bg="light blue")
label_date.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# Entry: NZB Date
entry_date = tk.Entry(frame_nzb, font=('Arial', 14))
entry_date.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
entry_date.delete(0, tk.END)  # delete the current value
default_date = param_reader.get_parameter("ui_default_date")
entry_date.insert(0, default_date)  # insert the new value

# Label: NZB Series
label_series = tk.Label(frame_nzb, text="NZB Series:", font=('Arial', 14), bg="light blue")
label_series.grid(row=1, column=0, padx=10, pady=10, sticky="w")
# Entry: NZB Series
entry_series = tk.Entry(frame_nzb, font=('Arial', 14))
entry_series.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
entry_series.delete(0, tk.END)  # delete the current value
default_sid = param_reader.get_parameter("ui_default_sid")
entry_series.insert(0, default_sid)  # insert the new value
# NZB Submit button
submit_button = tk.Button(frame_nzb, text="Submit", command=submit, font=('Arial', 14))
submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# New separator line
separator = tk.Frame(root, height=3, bd=1, relief='sunken')
separator.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# Label: Capture Date
label_capture_date = tk.Label(frame_capture, text="Capture Date:", font=('Arial', 14), anchor="w", justify="left", bg="light green")
label_capture_date.grid(row=4, column=0, padx=10, pady=10, sticky="w")
# Entry: Capture Date
entry_capture_date = tk.Entry(frame_capture, font=('Arial', 14))
entry_capture_date.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
default_entry_capture_date = param_reader.get_parameter("nzb_capture_date")
entry_capture_date.delete(0, tk.END)  # delete the current value
entry_capture_date.insert(0, default_entry_capture_date)  # insert the new value

# Label: Capture Series
label_capture_sid = tk.Label(frame_capture, text="Capture Series:", font=('Arial', 14), anchor="w", justify="left", bg="light green")
label_capture_sid.grid(row=5, column=0, padx=10, pady=10, sticky="w")
# Entry: Capture Series
entry_capture_series = tk.Entry(frame_capture, font=('Arial', 14))
entry_capture_series.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
default_entry_capture_series = param_reader.get_parameter("nzb_capture_sid")
entry_capture_series.delete(0, tk.END)  # delete the current value
entry_capture_series.insert(0, default_entry_capture_series)  # insert the new value
# Button: Capture Filename and Password
capture_button = tk.Button(frame_capture, text="Capture", command=text_capture, font=('Arial', 14))
capture_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Add label to status frame
label_status = tk.Label(frame_status, text="Status Messages", font=('Arial', 12), bg="#D8BFD8")
label_status.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

# Scrollbar widget for text_widget
scrollbar = tk.Scrollbar(frame_status)
scrollbar.grid(row=1, column=2, padx=(0,10), pady=(6,10), sticky='ns')

# Text Widget to show status messages so user can see what is happening.
text_widget = tk.Text(frame_status, height=15, width=50, yscrollcommand=scrollbar.set)
text_widget.grid(row=1, column=0, columnspan=1, padx=(10,0), pady=(5,10), sticky='nsew')

# Configure the Scrollbar to scroll the Text widget
scrollbar.config(command=text_widget.yview)

# Add button below the text widget to clear the text widget's contents
button_clear = tk.Button(frame_status, text="Clear", command=lambda: text_widget.delete(1.0, tk.END), font=('Arial', 14))
button_clear.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()