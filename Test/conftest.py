import pytest
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, insert, delete, Date, Text
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import select, desc

class DatabaseFixture:
    def __init__(self, engine_url):
        self.engine = create_engine(engine_url)
        self.conn = self.engine.connect()        
        self.metadata = MetaData()
        self.table = Table('movies', self.metadata, autoload_with=self.engine)
        
    def insert_data(self, data):
        self.conn.execute(insert(self.table), data)
        self.conn.commit()

    def delete_data(self):
        self.conn.execute(delete(self.table))
        self.conn.commit()

    def create_session_connection(self):
        return self.conn
    
    def close_and_dispose(self):
        self.conn.close()
        self.engine.dispose()

    def reset_id(self):
        with self.engine.begin() as connection:
            connection.execute(text("ALTER TABLE {} AUTO_INCREMENT = 1;".format(self.table.name)))


@pytest.fixture
def db_fixture():
    engine = DatabaseFixture('mysql+pymysql://linc_dev:D0gP1L3$1lv8rB1g@192.168.2.252:3307/nzb_search_test')

    engine.delete_data()
    engine.reset_id()

    engine.insert_data([
        {'download_date': '2026-01-01', 'description': 'Test Description 01', 'filename': 'Test Filename', 'password': 'Test Password', 'series_id': 1, 'note': 'Test Note', 'nzb_created': 1, 'nzb_exception': 1, 'dl_comments': 'Test Comments', 'movie_type': 1, 'movie_url': 'Test URL'},
        {'download_date': '2026-01-01', 'description': 'Test Description 02', 'filename': 'Test Filename', 'password': 'Test Password', 'series_id': 1, 'note': 'Test Note', 'nzb_created': 1, 'nzb_exception': 1, 'dl_comments': 'Test Comments', 'movie_type': 1, 'movie_url': 'Test URL'}    ])

    connection = engine.create_session_connection()
    #print(engine.table.columns.keys())
    stmt = select('*').select_from(engine.table).order_by(desc(engine.table.c.ID)).limit(10)
    result = connection.execute(stmt)
    rows = result.fetchall()
    print(f'Number of rows: {len(rows)}')
    for row in rows:
        print(f'row: {row}')
    
    #test_value = rows[0]

    yield engine.conn

    
    engine.conn.close()
    engine.close_and_dispose()

    # Create a transaction to roll back after the test        
    # connection = engine.connect()
    # transaction = connection.begin()
    # session = Session(bind=connection)

    # Create temporary table here...

    # yield session  # yield the session instead of the engine

    # After the test, rollback the transaction and close the connection
    #transaction.rollback()
    #connection.close()

def main():
    print(f'Testing.')
    cls = DatabaseFixture('mysql+pymysql://linc_dev:D0gP1L3$1lv8rB1g@localhost:3307/nzb_search_test')
    cls.close_and_dispose()

if __name__ == '__main__':
    main()