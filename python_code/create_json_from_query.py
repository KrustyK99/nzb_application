import json
import datetime
from python_code.nzb_search_db_connection import nzb_search_connection

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

def main():
    cls = nzb_search_connection(1)
    with cls.create_connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from movies where ID >= 5418;")
        rows = cur.fetchall()
        print(f'Number of rows: {len(rows)}')

        # Convert rows to list of dictionaries
        columns = [desc[0] for desc in cur.description]
        dict_rows = [dict(zip(columns, row)) for row in rows]

        # Write to JSON file
        with open('output.json', 'w') as f:
            json.dump(dict_rows, f, cls=DateTimeEncoder)

# function to import json file into database table
def import_json_to_table(filename='output.json', database_type=5):
    """
    Import json file into database table

    Parameters
    ----------
    filename : str
        Filename of json file to import

    database_type : int
        Database type to use for connection
        1 = nzb database
        2 = SQLite
        3 = Business database
        4 = Business (Sandbox) database
        5 = nzb_search test database (default)
        6 = nzb_search empty database

    Returns
    -------
    None
    """
    # Create connection: The following creates a connection to the test database
    cls = nzb_search_connection(database_type)
    with cls.create_connection() as conn:
        cur = conn.cursor()
        with open(filename) as f:
            data = json.load(f)
        for row in data:
            print(f'row: {row}')
            #cur.execute("insert into movies (download_date, description, filename, password, series_id, note, nzb_created, nzb_exception, dl_comments, movie_type, movie_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row['download_date'], row['description'], row['filename'], row['password'], row['series_id'], row['note'], row['nzb_created'], row['nzb_exception'], row['dl_comments'], row['movie_type'], row['movie_url'])
            cur.execute("insert into movies (download_date, description, filename, password, series_id, note, nzb_created, nzb_exception, dl_comments, movie_type, movie_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['download_date'], row['description'], row['filename'], row['password'], row['series_id'], row['note'], row['nzb_created'], row['nzb_exception'], row['dl_comments'], row['movie_type'], row['movie_url']))
        conn.commit()


import_json_to_table()

#if __name__ == "__main__":
#    main()

