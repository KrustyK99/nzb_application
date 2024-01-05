from python_code.fn_pw_cap import Filename_Password_Capture
from sqlalchemy import text

class TestFN:
    def test_capture_filename_password02(self, db_fixture):
        #test_conn = db_fixture
        #fn = Filename_Password_Capture(1, conn)
        #with db_fixture as conn:
            # add code to execute select query using conn
        conn = db_fixture
        sql = text("select description from movies order by id desc limit 10;")
        result = conn.execute(sql)
        rows = result.fetchall()
        test_value = rows[0]

        assert conn is not None
        assert len(rows) > 0
        #assert test_value[0] == 'Test Description'