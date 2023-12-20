import os
import sqlite3
from sqlite3 import Error
import nzb_search
from nzb_search_db_connection import nzb_search_connection


class create_directories:
    
    def create_connection(self):
            self.cls_db_connection = nzb_search_connection(1)
            self.db_file = r"C:\Users\latto\OneDrive\Python\Projects\NZB_Search\SQLite\nzb.db"
            self.conn = None
            try:
                    #self.conn = sqlite3.connect(self.db_file)
                    self.conn = self.cls_db_connection.create_connection()
            except Error as e:
                    print(e)
            return self.conn
    
    def create_directory(self):
        folder_root_path = r"C:\Users\latto\Downloads"
        cur = self.conn.cursor()
        str_sql = r"SELECT ID, date_format(download_date, '%y%m%d'), series_id  FROM new_save_directories WHERE create_flag = 1;"
        # DATE_FORMAT('2014-04-01', '%M %e %Y');
        cur.execute(str_sql)
        rows = cur.fetchall()
        for row in rows:
            #folder_name = row[1] + " 0" + str(row[2])
            folder_name = row[1] + self.add_leading_zero(str(row[2]))
            full_folder_name = folder_root_path + chr(92) + folder_name
            print("        " + full_folder_name)
            os.mkdir(full_folder_name)
        print("    Folders created.")

    def remove_dashes(self):
        str_sql = "UPDATE new_save_directories SET download_date = REPLACE (SUBSTRING(download_date,3), '-','');"
        cur = self.conn.cursor()
        cur.execute(str_sql)
        self.conn.commit()
        print("    Dashes and leading text removed.")

    def add_leading_zero(self, series_id_text):
        if len(series_id_text) == 1:
            folder_series_id = " 0" + str(series_id_text)
        else:
            folder_series_id = " " + str(series_id_text)

        return folder_series_id
       
def main():

    print("<< MAIN START >>")

    cls = create_directories()

    cls.create_connection()
    cls.create_directory()

    print("<< MAIN END >>")

if __name__ == '__main__':
    main()