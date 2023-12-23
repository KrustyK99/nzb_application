import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from python_code.api_nzb_search import api_nzb_search
from python_code.nzb_search_db_connection import nzb_search_connection
from python_code.parameterreader import ParameterReader
from python_code.fn_pw_cap import Filename_Password_Capture


class NZBApplication:
    def __init__(self):
        self.param_reader = ParameterReader("config.yaml")

        try:
            self.param_reader.read_file()    
        except Exception as e:
            print(f'Problem reading the config file: {e}')

        self.root = tk.Tk()
        self.root.title("NZB Application")
        # root.iconbitmap("path/to/icon.ico")  # Replace "path/to/icon.ico" with the actual path to your icon file

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        # Add frame to holder title and icon
        self.frame_title = tk.Frame(self.root, bg="light blue", highlightthickness=2, highlightbackground="green")
        self.frame_title.grid(row=0, column=0, padx=10, pady=(10,5), sticky="nsew")
        self.frame_title.grid_columnconfigure(0, weight=1)
        # frame_title.grid_columnconfigure(1, weight=1)
        self.frame_title.grid_rowconfigure(0, weight=1)


        # Frame for nzb date and series
        self.frame_nzb = tk.Frame(self.root, bg="light blue")
        self.frame_nzb.grid(row=1, column=0, padx=10, pady=(10,5), sticky="nsew")
        self.frame_nzb.grid_columnconfigure(0, weight=1)
        self.frame_nzb.grid_columnconfigure(1, weight=1)
        self.frame_nzb.grid_rowconfigure(0, weight=1)

        # Frame for filename and password capture
        self.frame_capture = tk.Frame(self.root, bg="light green")
        self.frame_capture.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.frame_capture.grid_columnconfigure(0, weight=1)
        self.frame_capture.grid_columnconfigure(1, weight=1)
        self.frame_capture.grid_rowconfigure(0, weight=1)

        # Frame for status messages
        self.frame_status = tk.Frame(self.root, bg="#D8BFD8")
        self.frame_status.grid(row=3, column=0, padx=10, pady=(5,10), sticky="nsew")
        self.frame_status.grid_columnconfigure(0, weight=1)
        self.frame_status.grid_rowconfigure(0, weight=1)

        # Add label to title frame
        self.lable_title = tk.Label(self.frame_title, text="NZB Application", font=('Verdana', 16), bg="light blue", justify="center")
        self.lable_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Label: NZB Date
        self.label_date = tk.Label(self.frame_nzb, text="NZB Date:", font=('Arial', 14), bg="light blue")
        self.label_date.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Entry: NZB Date
        self.entry_date = tk.Entry(self.frame_nzb, font=('Arial', 14))
        self.entry_date.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_date.delete(0, tk.END)  # delete the current value
        self.default_date = self.param_reader.get_parameter("ui_default_date")
        self.entry_date.insert(0, self.default_date)  # insert the new value

        # Label: NZB Series
        self.label_series = tk.Label(self.frame_nzb, text="NZB Series:", font=('Arial', 14), bg="light blue")
        self.label_series.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # Entry: NZB Series
        self.entry_series = tk.Entry(self.frame_nzb, font=('Arial', 14))
        self.entry_series.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_series.delete(0, tk.END)  # delete the current value
        default_sid = self.param_reader.get_parameter("ui_default_sid")
        self.entry_series.insert(0, default_sid)  # insert the new value
        # NZB Submit button
        self.submit_button = tk.Button(self.frame_nzb, text="Submit", command=self.submit, font=('Arial', 14))
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # New separator line
        self.separator = tk.Frame(self.root, height=3, bd=1, relief='sunken')
        self.separator.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Label: Capture Date
        self.label_capture_date = tk.Label(self.frame_capture, text="Capture Date:", font=('Arial', 14), anchor="w", justify="left", bg="light green")
        self.label_capture_date.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        # Entry: Capture Date
        self.entry_capture_date = tk.Entry(self.frame_capture, font=('Arial', 14))
        self.entry_capture_date.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        self.default_entry_capture_date = self.param_reader.get_parameter("nzb_capture_date")
        self.entry_capture_date.delete(0, tk.END)  # delete the current value
        self.entry_capture_date.insert(0, self.default_entry_capture_date)  # insert the new value

        # Label: Capture Series
        self.label_capture_sid = tk.Label(self.frame_capture, text="Capture Series:", font=('Arial', 14), anchor="w", justify="left", bg="light green")
        self.label_capture_sid.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        # Entry: Capture Series
        self.entry_capture_series = tk.Entry(self.frame_capture, font=('Arial', 14))
        self.entry_capture_series.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
        self.default_entry_capture_series = self.param_reader.get_parameter("nzb_capture_sid")
        self.entry_capture_series.delete(0, tk.END)  # delete the current value
        self.entry_capture_series.insert(0, self.default_entry_capture_series)  # insert the new value
        # Button: Capture Filename and Password
        self.capture_button = tk.Button(self.frame_capture, text="Capture", command=self.text_capture, font=('Arial', 14))
        self.capture_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Add label to status frame
        self.label_status = tk.Label(self.frame_status, text="Status Messages", font=('Arial', 12), bg="#D8BFD8")
        self.label_status.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        # Scrollbar widget for text_widget
        self.scrollbar = tk.Scrollbar(self.frame_status)
        self.scrollbar.grid(row=1, column=2, padx=(0,10), pady=(6,10), sticky='ns')

        # Text Widget to show status messages so user can see what is happening.
        self.text_widget = tk.Text(self.frame_status, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.text_widget.grid(row=1, column=0, columnspan=1, padx=(10,0), pady=(5,10), sticky='nsew')

        # Configure the Scrollbar to scroll the Text widget
        self.scrollbar.config(command=self.text_widget.yview)

        # Add button below the text widget to clear the text widget's contents
        self.button_clear = tk.Button(self.frame_status, text="Clear", command=lambda: self.text_widget.delete(1.0, tk.END), font=('Arial', 14))
        self.button_clear.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def nzb_main(self, nzb_date, nzb_series):
        # API Stuff
        cls = api_nzb_search()
        
        # Database stuff (see class (nzb_search_connection) for db_type values and descriptions)
            # 1 = mariaDB
            # 2 = SQLite
            # 3 = Business
            # 4 = Business-sandbox
        db_type = self.param_reader.get_parameter("database_type")

        cls_db_connection = nzb_search_connection(db_type)
        conn = cls_db_connection.create_connection()
        str_sql = 'SELECT m.ID, m.download_date, m.description, m.filename, m.password, m.series_id, m.note, m.nzb_created, m.nzb_exception, m.dl_comments, m.movie_type, m.movie_url FROM movies m WHERE ((m.download_date=?) AND (m.series_id=?) AND (m.nzb_created Is Null) AND (m.nzb_exception Is Null));' # api_nzb_search_01.sql 
        cur = conn.cursor()
        cur.execute(str_sql, (nzb_date, nzb_series))
        row = cur.fetchall()

        # Add variable curr_datetime to the status messages.
        curr_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.write_to_status(f'------------------- S T A R T -------------------\n{curr_datetime}\n')
        
        print(f'Number of records from Database: {cur.rowcount}')
        self.write_to_status(f'Number of records from Database: {cur.rowcount}\n')

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
                        self.write_to_status(f'  ID: {rw[0]}, Error:{error}\n')
                    else: 
                        sql_update = 'UPDATE movies SET nzb_created=1 WHERE ID=?;' # api_nzb_search_02.sql
                        cur.execute(sql_update, (row_id,))
                        conn.commit()
                        counter_saved += 1
                        self.write_to_status(f'  ID: {rw[0]}, nzb saved!\n')
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
                        self.write_to_status(f'  ID: {rw[0]}, Error:{error}\n')
                    else: 
                        sql_update = 'UPDATE movies SET nzb_created=1 WHERE ID=?;' # api_nzb_search_02.sql
                        cur.execute(sql_update, (row_id,))
                        conn.commit()
                        counter_saved += 1
                        self.write_to_status(f'  ID: {rw[0]}, nzb saved!\n')
                    #write_to_status(f'ID: {rw[0]}\n')
                print(f'NZB Filename: {nzb_filename}')
                print(f'-------------------------------------------------')
            except Exception as e:
                print(f"An error occurred: {e}")
            counter += 1
        
        print(f'{curr_datetime}\n--------------------- E N D ---------------------\n')
        cur.close()
        conn.close()
        
        self.write_to_status(f'Number of records processed: {counter}\nNumber of files saved: {counter_saved}\n')
        end_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        total_time = datetime.strptime(end_datetime, "%m/%d/%Y %H:%M:%S") - datetime.strptime(curr_datetime, "%m/%d/%Y %H:%M:%S")
        self.write_to_status(f'Total run time: {total_time}\n')
        self.write_to_status(f'{end_datetime}\n--------------------- E N D ---------------------\n')

    def submit(self):
        nzb_date = self.entry_date.get()
        nzb_series = self.entry_series.get()
        self.nzb_main(nzb_date, nzb_series)

    def text_capture(self):    
        capture_date = self.entry_capture_date.get()
        capture_sid = self.entry_capture_series.get()
        txt_capture = Filename_Password_Capture(1)
        
        # Add variable curr_datetime to the status messages.
        curr_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.write_to_status(f'------------------- S T A R T -------------------\n{curr_datetime}\n')

        # write_to_status box that the text capture is starting and list capture data and series id
        self.write_to_status(f'Text Capture Starting.\nCapture Date: {capture_date}\nCapture Series: {capture_sid}\n')
        
        try:
            id_list = txt_capture.database_upate(capture_date, capture_sid)
            for key, value in id_list.items():
                if not isinstance(value, tuple):
                    self.write_to_status(f'  {key}: {value}\n')
                else:
                    fn = value[0][:7] + "..." if len(value[0]) > 7 else value[0]
                    pw = value[1][:7] + "..." if len(value[1]) > 7 else value[1]
                    self.write_to_status(f'  {key}: File: {fn} PW: {pw}\n')
            # write to status the number of records processed
            self.write_to_status(f'Number of records processed: {len(id_list)}\n')
        except Exception as e:
            print(f'Error updating filename/password: {e}')
            self.write_to_status(f'Error updating filename/password: {e}\n')
        print(f'Text Capture Completed.')
        self.write_to_status(f'Text Capture Completed.\n')
        end_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        total_time = datetime.strptime(end_datetime, "%m/%d/%Y %H:%M:%S") - datetime.strptime(curr_datetime, "%m/%d/%Y %H:%M:%S")
        self.write_to_status(f'Total run time: {total_time}\n')
        self.write_to_status(f'{curr_datetime}\n--------------------- E N D ---------------------\n')

    def write_to_status(self,text):
        self.text_widget.insert(tk.END, text)
        # write text to app_log.md file

        file_path = self.param_reader.get_parameter("log_file_location")
        filename = self.param_reader.get_parameter("log_file_name")
        full_filename = os.path.join(file_path, filename)
        try:
            with open(full_filename, 'a') as f:
                f.write(text)
        except IOError as e:
            print(f"Error opening log file {full_filename}: {e}")

    def run(self):
        self.root.mainloop()

def main():
    app = NZBApplication()
    app.run()

if __name__ == "__main__":
    main()