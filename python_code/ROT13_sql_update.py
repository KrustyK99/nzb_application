import mariadb
import sys
from ROT13_Converter import ROT13_Converter

class ROT13_update:
    def __init__(self,int_begin_id, int_end_id):
        self.int_begin_id = int_begin_id
        self.int_end_id = int_end_id
        self.sql_str = "UPDATE movies_dev SET filename=CONCAT(filename, char(13), char(10), 'Another Line.') WHERE ID=;"

        # self.conn = self.make_connection()
    
    def make_connection(self):
        # Connect to MariaDB Platform
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
    
    def make_updates(self):
        # Instantiate ROT13 Converter
        cls_rot13 = ROT13_Converter()

        # Create database cursor
        cur = self.conn.cursor()

        # Set the counter so we know which row to start updating from.
        i = self.int_begin_id

        # Loop over the database row as set by int_begin_id and int_end_id
        while i <= self.int_end_id:
            # Get Value to encode.
            str_sql_01 = ("SELECT filename FROM movies_dev where id=" + str(i))
            cur.execute(str_sql_01)
            row = cur.fetchone()
            encoded_string = cls_rot13.ROT13_convert(row[0],1) #Encode the string using ROT13_Converter class.

            # Update fields with encoded value
            self.sql_str = ("UPDATE movies_dev SET filename='" + encoded_string + "'WHERE ID=" + str(i) + ";")
            print(str(i) + ") String:" + row[0] + "; ROT13:" + encoded_string)
            cur.execute(self.sql_str)
            self.conn.commit()
            i = i+1

def main():
    print("<< MAIN START >>")
    # Get Cursor
    cls = ROT13_update(376,584)
    conn = cls.make_connection()
    cls.make_updates()
    # cur = conn.cursor()
    # cur.execute(cls.sql_str)
    # conn.commit()

    print("<< MAIN END >>")
    # print("Number of rows: " + str(cur.rowcount))
    # print("SQL: " + cls.sql_str)

if __name__ == '__main__':
    main()