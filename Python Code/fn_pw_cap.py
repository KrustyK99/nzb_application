import re
from nzb_search_db_connection import nzb_search_connection
from parameterreader import ParameterReader

conn = None  # Declare conn as a global variable 

class Filename_Password_Capture:
    def __init__(self, db_type):
        """
        Initializes a new instance of the Filename_Password_Capture class.

        Parameters:
            db_type (int): The type of database to connect to.
            nzb_id (int): The ID of the record to process.

        Raises:
            RuntimeError: If the file cannot be read.
        """
        self.db_type = db_type
        self.conn = nzb_search_connection(db_type).create_connection()        
    
    def capture_filename_password02(self, nzb_id):
        self.nzb_id = nzb_id
        self.pr = ParameterReader("config.yaml")
        self.pr.read_file()
        self.re_patthern = self.pr.get_parameter("re_pattern")
        self.str_sql = 'SELECT m.ID, m.note FROM movies m WHERE (m.ID=?);'
        self.cur = self.conn.cursor()
        self.cur.execute(self.str_sql, (self.nzb_id,))
        self.row = self.cur.fetchall()
        self.note = self.row[0][1]

        # Initialize filename and password as not found
        self.nzb_filename = "<No Filename Found>"
        self.nzb_password = "<No Password Found>"

        # If note is None, return the default filename and password
        if self.note is None:
            return self.nzb_filename, self.nzb_password

        # Split the note into lines and process each line
        for line in self.note.split('\n'):
            self.match = re.search(self.re_patthern, line)
            if self.match:
                if self.match.group(1) == "File Name":
                    self.nzb_filename = self.match.group(2).replace('\r','')
                elif self.match.group(1) == "File Pass":
                    self.nzb_password = self.match.group(2).replace('\r','')

        return self.nzb_filename, self.nzb_password

    def database_upate(self, nzb_date, nzb_series):
        """
        Updates the database with the filename and password.

        Parameters:
            nzb_date (str): The date the nzb was added to the database.
            nzb_series (str): The series the nzb is associated with.

        Raises:
            RuntimeError: If the file cannot be read.
        """
        self.nzb_date = nzb_date
        self.nzb_series = nzb_series
        self.str_sql = 'SELECT m.ID, m.filename, m.password, m.note FROM movies m WHERE (m.download_date=?) AND (m.series_id=?);'
        self.cur = self.conn.cursor()
        self.cur.execute(self.str_sql, (self.nzb_date, self.nzb_series))
        self.row = self.cur.fetchall()
        print(f'Number of rows: {len(self.row)}')

        rw_dict = {}  # Dictionary to store rw[0] as key and fn, pw as values

        for rw in self.row:
            # Check to see if filename and password not empty
            if rw[3] is None:
                rw_dict[rw[0]] = "No note"
            else:
                if rw[1] is None and rw[2] is None:
                    self.str_sql_update = 'UPDATE movies SET filename=?, password=? WHERE (ID=?);'
                    fn = self.capture_filename_password02(rw[0])[0]
                    pw = self.capture_filename_password02(rw[0])[1]

                    self.cur.execute(self.str_sql_update, (fn, pw, rw[0]))
                    self.conn.commit()

                    rw_dict[rw[0]] = (fn, pw)  # Add rw[0] as key and fn, pw as values to the dictionary
                else:
                    rw_dict[rw[0]] = "Existing values"  # Add rw[0] as key and "Existing values" as value to the dictionary

        self.conn.close()

        return rw_dict  # Return the dictionary with rw[0] as key and fn, pw as values or "Existing values"

if __name__ == "__main__":
    try:
        cls = Filename_Password_Capture(1)
        pr = ParameterReader("config.yaml")
        pr.read_file()
        #print(f'cls.db_type: {cls.db_type}')
        #nzb_filename, nzb_password = cls.capture_filename_password()
        #print(f'Filename, Password: {nzb_filename}, {nzb_password}')
        cls.database_upate(pr.get_parameter("nzb_capture_date"), pr.get_parameter("nzb_capture_sid"))
    except Exception as e:
        print(f'Error: {e}')
