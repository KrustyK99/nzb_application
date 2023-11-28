import requests
import json
from nzb_search_db_connection import nzb_search_connection
import datetime

class api_nzb_search:
    """
    This class handles searching the NZB Index API for NZB files.
    """
    def __init__(self):
        """
        Initializes the api_nzb_search class.

        Sets up the API key and request URL, checks the connection to the API server,
        and checks the number of API calls made.
        """
        self.api_key = "f995d8d5732bf73306aedb29a8a844618d0fda48f15b773377fb4e0227300a26"
        self.api_request = "https://api.nzbindex.com/api/v3/?key="

        print('--------------------------------------------')
        
        # Check connection to API Server
        try:
            self.response = requests.get(f'{self.api_request}{self.api_key}')
            print(f'Request: {self.api_request}{self.api_key}')
            print("Request Response Code: " + str(self.response.status_code))
            if self.response.status_code == 200:
                print(f'   Connection is good!')
        except Exception as e:
            print("Can't make connection.")
            print(f"An error of type {type(e).__name__} occurred. Arguments:\n{e.args}")
            raise

        print('--------------------------------------------')

        # Check number of API calls. Note: For free NZB Index account 1000 max per day. Use alternate API Key if limit is reached.
        try:
            date = datetime.date.today().isoformat()
            self.response02 = requests.get(f'https://api.nzbindex.com/api/v3/usage/{date}?key={self.api_key}')
            print(f'https://api.nzbindex.com/api/v3/usage/{date}?key={self.api_key}')
            print(f'Number of API calls: {self.response02.text}')
        except Exception as e:
            print("Something wrong with printing response.")
            print(f"An error of type {type(e).__name__} occurred. Arguments:\n{e.args}")
            raise

        print('--------------------------------------------')
    
    def create_nzb_file(self, collection_id, collection_name): 
        """
        Creates an NZB file for a given collection.

        Parameters:
        collection_id (int): The ID of the collection.
        collection_name (str): The name of the collection.

        Returns:
        None
        """
        if collection_id == 0:
            print(f'Problem with Collection. NZB file NOT saved.')
            return

        request_cmd = f'https://api.nzbindex.com/api/v3/download/?key={self.api_key}&r[]={collection_id}'
        print(f'File download API call: https://api.nzbindex.com/api/v3/download/?key={self.api_key}&r[]={collection_id}')

        response = requests.get(request_cmd)
        print(f'File download API response code: {response.status_code}')
        
        try:
            open_string = fr'C:\Projects\nzb-search\Python Code\api saved files\{collection_name}.nzb'
            print(f'NZB Filename: {open_string}')
            open(open_string, "wb").write(response.content)
            print(f'NZB file saved successfully.')
        except Exception as e:
            print(f'Problem with saving nzb file. Collection ID={collection_id}')
            print(e)
            return
    
    def get_collection_id(self, movie_filename):
        """
        Retrieves the collection ID for a given movie filename.

        This method makes an API call to NZBIndex's search endpoint with the movie filename as the query.
        If a single result is found, it returns the ID of the result. If no results or multiple results are found, it returns 0.

        Parameters:
        movie_filename (str): The filename of the movie to search for.

        Returns:
        int:
        """
        # search_string = 'psaMLqhbq03qrWLR8lYPeaMZJAIIAUJTRLsdvi64Z7adQB1lCon6fjT2fK7b6PiL'
        request_cmd = f'https://api.nzbindex.com/api/v3/search/?key={self.api_key}&q={movie_filename}'

        # print(f'API Search Call: {request_cmd}')

        response = requests.get(request_cmd)

        data = json.loads(response.text)

        try:
            # print(f'JSON ID: {data["results"][0]["id"]}')
            if len(data["results"]) == 1: 
                return data["results"][0]["id"]
            else:
                return 0
        except:
            print(f'Problem parsing json was encountered.')
            return 0

    def json_count(self, filename):
        """
        Counts the number of results for a given filename in the NZBIndex API.

        This method makes an API call to NZBIndex's search endpoint with the filename as the query.
        It then returns the number of results found.

        Parameters:
        filename (str): The filename to search for.

        Returns:
        int: The number of results found. If an error occurs, it will return None.
        """
        request_cmd = f'https://api.nzbindex.com/api/v3/search/?key={self.api_key}&q={filename}'
        print(request_cmd)
        response = requests.get(request_cmd)
        data = json.loads(response.text)

        try:
            # print(f'Number of objects in json:  {len(data["results"])}')
            return len(data["results"])
        except:
            print(f'Problem counting objects in json.')
        
# def main():
#     print(f'--------------------------- S T A R T ----------------------------------')

#     # API Stuff
#     cls = api_nzb_search()
    
#     # Database stuff
#     cls_db_connection = nzb_search_connection(1)
#     conn = cls_db_connection.create_connection()
#     nzb_date = "2022-10-12"
#     nzb_series = 7
#     str_sql = f'SELECT m.ID, m.download_date, m.description, m.filename, m.password, m.series_id, m.note, m.nzb_created, m.nzb_exception, m.dl_comments, m.movie_type, m.movie_url FROM movies m WHERE ((m.download_date="{nzb_date}") AND (m.series_id={nzb_series}) AND (m.nzb_created Is Null) AND (m.nzb_exception Is Null));' # api_nzb_search_01.sql 
#     cur = conn.cursor()
#     cur.execute(str_sql)
#     row = cur.fetchall()
#     print(f'Number of records from Database: {cur.rowcount}')
#     for rw in row:
#         collection_id = cls.get_collection_id(rw[3])
#         print(f'0:{rw[0]}, 1:{rw[1]}, 5:{rw[5]}, 3:{rw[3]}, 4:{rw[4]}, Collection ID: {collection_id}')
#         nzb_filename = f'{rw[0]}-{rw[3]}'
#         cls.create_nzb_file(collection_id, nzb_filename)
#         print(f'--------------------------------------------------------------')
#     cur.close

#     print(f'---------------------------- E N D -----------------------------------')

# if __name__ == '__main__':
#     main()