import pytest
import requests_mock
from api_nzb_search import api_nzb_search

def test_api_nzb_search():
    with requests_mock.Mocker() as m:
        # Mock the API responses
        m.get('https://api.nzbindex.com/api/v3/?key=f995d8d5732bf73306aedb29a8a844618d0fda48f15b773377fb4e0227300a26', status_code=200)
        m.get('https://api.nzbindex.com/api/v3/usage/2022-10-12?key=f995d8d5732bf73306aedb29a8a844618d0fda48f15b773377fb4e0227300a26', text='500')

        # Initialize the class
        api = api_nzb_search()

        # Check the API key
        assert api.api_key == "f995d8d5732bf73306aedb29a8a844618d0fda48f15b773377fb4e0227300a26"

        # Check the API request URL
        assert api.api_request == "https://api.nzbindex.com/api/v3/?key="

        # Check the number of API calls
        assert api.response02.text == '500'

        # Test the create_nzb_file method
        # You'll need to replace this with a real test, depending on what the method does
        # assert api.create_nzb_file('123', 'test') is None