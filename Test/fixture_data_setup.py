import pytest
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, insert, delete, Date, Text

class DatabaseFixture:
    def __init__(self, engine_url):
        self.engine = create_engine(engine_url)
        self.metadata = MetaData()
        self.test_table = Table(
            'movies',
            self.metadata,
            Column('ID', Integer, primary_key=True),
            Column('download_date', Date),
            Column('description', String(1000)),
            Column('filename', String(500)),
            Column('password', String(500)),
            Column('series_id', Integer),
            Column('note', Text),
            Column('nzb_created', Integer),
            Column('nzb_exception', Integer),
            Column('dl_comments', Text),
            Column('movie_type', Integer),
            Column('movie_url', String(250))
        )
        self.metadata.create_all(self.engine)

    def insert_data(self, data):
        with self.engine.connect() as connection:
            connection.execute(insert(self.test_table), data)

    def delete_data(self):
        with self.engine.connect() as connection:
            connection.execute(delete(self.test_table))

@pytest.fixture
def db_fixture():
    fixture = DatabaseFixture('mysql+pymysql://linc_dev:D0gP1L3$1lv8rB1g@192.168.2.252/nzb_search_test')

    # Insert test data
    fixture.insert_data([{'ID': 1, 'description': 'Test Description'}, {'filename': '<Test Filename>', 'password': '<Test Password>'}])

    yield fixture

    # Clean up test data
    fixture.delete_data()

def main():
    print(f'Testing.')

if __name__ == '__main__':
    main()