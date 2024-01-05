import json
import datetime
from python_code.nzb_search_db_connection import nzb_search_connection

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

class JSONExportImport:
    def __init__(self, database_type=5):
        #self.cls = nzb_search_connection(database_type)
        pass

    def _execute_query(self, conn, query, params=None):
        pass

    def json_export(self, query="select * from movies where ID >= 5000;", database_type=1):
        """
        Export the results of a query to a json file
        
        Args:
            query (str): The query to execute
            database_type (int): The database type to connect to
            1 = nzb search
            2 = sqlite
            3 = Business
            4 = Business-sandbox
            5 = nzb search test
            6 = nzb search (empty)
            7 = nzb search test (pymysql)

        Returns:
            None
        """
        cls = nzb_search_connection(database_type)
        with cls.create_connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()   
            print(f'Number of rows: {len(rows)}')

            columns = [desc[0] for desc in cur.description]
            dict_rows = [dict(zip(columns, row)) for row in rows]

            with open('output.json', 'w') as f:
                json.dump(dict_rows, f, cls=DateTimeEncoder, indent=4)

        print(f'File written: output.json')

    def json_import(self, filename='output.json', database_type=7, reset_auto_increment=False):
        """
        Import a json file into the database
        
        Args:
            filename (str): The filename to import
            reset_auto_increment (bool): Whether to reset the auto increment value
            
        Returns:
            None
        """
        cls = nzb_search_connection(database_type)

        with open(filename) as f:
            data = json.load(f)
        
        with cls.create_connection() as conn:
            cur = conn.cursor()
            if reset_auto_increment:
                cur.execute("ALTER TABLE movies AUTO_INCREMENT = 1;")
            
            query = "insert into movies (download_date, description, filename, password, series_id, note, nzb_created, nzb_exception, dl_comments, movie_type, movie_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            values = [
            (row['download_date'], row['description'], row['filename'], row['password'], row['series_id'], row['note'], row['nzb_created'], row['nzb_exception'], row['dl_comments'], row['movie_type'], row['movie_url'])
            for row in data
            ]
            
            print(f'Number of rows: {len(values)}')

            cur.executemany(query, values)
            conn.commit()

def main():
    cls = JSONExportImport()
    #cls.json_export(query="select * from movies where ID >= 5000;", database_type=1)
    cls.json_import(database_type=7, reset_auto_increment=True )

if __name__ == "__main__":
    main()