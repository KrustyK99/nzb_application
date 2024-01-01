import pytest

try:
    exit_code = pytest.main([
            "-v", 
            "Test/test_database.py::TestConnection::test_nzb_search_conn",
            "Test/test_database.py::TestConnection::test_nzb_search_sql",
            "Test/test_database.py::TestConnection::test_nzb_search_test_conn",
            "Test/test_database.py::TestConnection::test_nzb_search_test_sql"
            ])
    if exit_code == 0:
        print(f'PyTest exit code: {exit_code} (pytest executed tests as expected)')
    else:
        print(f'PyTest exit code: {exit_code} (pytest encounted an issue)')
        
except Exception as e:
    print(f'An error occurred while running the tests: {e}')