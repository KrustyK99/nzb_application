from datetime import date
import sqlite3
import webbrowser
from sqlite3 import Error
from nzb_constants import nzb_constants
from nzb_search_db_connection import nzb_search_connection

class nzb_search_helper:
    
    def __init__(self):

        cls_constants = nzb_constants()

        self.cls_db_connection = nzb_search_connection(1)

        self.conn = self.cls_db_connection.create_connection()

        #Constants
        self.app_current_date_id = cls_constants.nzb_date_pid
        self.app_series_id = cls_constants.nzb_series_pid
        self.app_browser_open_switch_id = cls_constants.nzb_browser_switch_pid
        self.app_database_path_id = cls_constants.nzb_app_database_path_pid
        self.app_text_log_path_id = cls_constants.nzb_app_text_log_path_pid

        self.app_current_date_value = self.get_app_parameters(self.app_current_date_id)
        self.app_series_value = self.get_app_parameters(self.app_series_id)
        self.app_browser_open_switch_value = self.get_app_parameters(self.app_browser_open_switch_id)
        self.app_database_path_value = self.get_app_parameters( self.app_database_path_id)
        self.app_text_log_path_value = self.get_app_parameters(self.app_text_log_path_id)

        self.sql_movies_02 = "SELECT z.ID, z.download_date, z.series_id, z.description, z.filename, z.password, z.nzb_address, z.Link, z.nzb_exception FROM nzb_search_dev.nzb_search z WHERE series_id = " + str(self.app_series_value) + " AND nzb_exception IS NULL AND download_date = '" + self.app_current_date_value + "';"
        self.sql_movies = "SELECT z.ID, z.download_date, z.series_id, z.description, z.filename, z.password, z.nzb_address, z.Link, z.nzb_exception FROM nzb_search z WHERE series_id = " + str(self.app_series_value) + " AND nzb_exception IS NULL AND download_date = '" + self.app_current_date_value + "' AND nzb_created IS NULL;"
    
    def create_connection(self, db_file):
        self.db_file = db_file
        self.conn = None
        try:
                self.conn = self.cls_db_connection.create_connection()
        except Error as e:
                print(e)
        return self.conn
    
    def get_app_parameters(self, app_parameter_id):
        cur = self.conn.cursor()
        str_sql = "SELECT param_value FROM app_parameters WHERE ID=" + str(app_parameter_id)
        cur.execute(str_sql)
        row = cur.fetchone()
        self.app_parameter_value = row[0]
        return self.app_parameter_value
    
    def select_all_movies(self):
        cur = self.conn.cursor()
        cur.execute(self.sql_movies)
        print("SQL to get valid movies: " + self.sql_movies)
        rows = cur.fetchall()
        text_title = "Run Date: " + str(date.today()) + "; NZB Date: " + self.app_current_date_value + "; Series ID: " + self.app_series_value
        print(text_title)
        with open(self.app_text_log_path_value, 'a') as f:
            f.write(text_title + '\n')
            i = 0
            for row in rows:
                    try:
                        line_str = row[7] + '\n'
                        f.write(line_str)
                    except:
                        f.write(str(row[0]) + ") Problem with buidling hyperlink" + '\n')

                    if self.app_browser_open_switch_value == '1':
                        try:
                            webbrowser.open_new_tab(row[6])
                            print("    Filename: " + row[4])
                            i = i + 1
                        except:
                            print("    Something went wrong with ID: " + str(row[0]))
            f.write("Number of file(s): " + str(i))
            f.write("\n\n")

def main():
    cls = nzb_search_helper()
    print("Current App Date ([ID], [Value]): " + str(cls.app_current_date_id) + ", " + cls.app_current_date_value)
    print("Series ID ([ID], [Value]): " + str(cls.app_series_id) + ", " + cls.app_series_value)
    print("Browser Tab Open Switch ([ID], [Value]): " + str(cls.app_browser_open_switch_id) + ", " + cls.app_browser_open_switch_value)
    print("Database Path ([ID], [Value]): " + str(cls.app_database_path_id) + ", " + cls.app_database_path_value)
    print("Text Log Path ([ID], [Value]): " + str(cls.app_text_log_path_id)+ ", " + cls.app_text_log_path_value)
    print("Movies SQL ([ID], [Value]): " + cls.sql_movies)
    cls.select_all_movies()

if __name__ == '__main__':
    main()