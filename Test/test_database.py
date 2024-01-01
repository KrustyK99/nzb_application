from python_code.nzb_search_db_connection import nzb_search_connection

class TestConnection:
    def test_nzb_search_conn(self):
        db = nzb_search_connection(1)
        with db.create_connection() as conn:
            assert conn is not None

    def test_nzb_search_sql(self):
        db = nzb_search_connection(1)
        with db.create_connection() as conn:
            # execute a simple sql statement to make sure the connection is good
            cur = conn.cursor()
            cur.execute("SELECT * FROM movies LIMIT 1;")
            row = cur.fetchall()
            assert row is not None
            assert len(row) == 1

    def test_business_conn(self):
        db = nzb_search_connection(3)
        with db.create_connection() as conn:
            assert conn is not None

    def test_business_sql(self):
        db = nzb_search_connection(3)
        with db.create_connection() as conn:
            # execute a simple sql statement to make sure the connection is good
            cur = conn.cursor()
            cur.execute("SELECT * FROM Expenses LIMIT 1;")
            row = cur.fetchall()
            assert row is not None
            assert len(row) == 1

    def test_business_sandbox_conn(self):
        db = nzb_search_connection(4)
        with db.create_connection() as conn:
            assert conn is not None

    def test_business_sandbox_sql(self):
        db = nzb_search_connection(4)
        with db.create_connection() as conn:
            # execute a simple sql statement to make sure the connection is good
            cur = conn.cursor()
            cur.execute("SELECT * FROM Expenses LIMIT 1;")
            row = cur.fetchall()
            assert row is not None
            assert len(row) == 1

    def test_nzb_search_test_conn(self):
        db = nzb_search_connection(5)
        with db.create_connection() as conn:
            assert conn is not None
    
    def test_nzb_search_test_sql(self):
        db = nzb_search_connection(5)
        with db.create_connection() as conn:
            # execute a simple sql statement to make sure the connection is good
            cur = conn.cursor()
            cur.execute("SELECT * FROM movies LIMIT 1;")
            row = cur.fetchall()
            assert row is not None
            assert len(row) == 1
