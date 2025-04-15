import requests
import re


class search:
    
    def  __init__(self,api_key = "AIzaSyDDFuBxcWah6KGuVC8Zde9-ZgNbHARA-L8", cse_id =  "c2d52ba67f1be42df"):
        self.api_key = api_key
        self.cse_id = cse_id

    def optimize_query(self,query: str):
        """
        Optimize the input query by trimming whitespace,
        converting to lowercase, and collapsing multiple spaces.
        """
        optimized = query.strip().lower()
        optimized = re.sub(r'\s+', ' ', optimized)
        return optimized

    def processQuery(self,query: str, num_results = 50):

        """
        Uses Google Custom Search JSON API to fetch the top `num_results`
        for the given query and returns a list of dictionaries.
        
        Each dictionary contains:
            - title: Title of the result.
            - link: URL of the result.
            - snippet: A brief snippet or description.
        """
        optimized_query = self.optimize_query(query)
        results = []
        start_index = 1  # Google Custom Search index starts at 1

        # The API returns a maximum of 10 results per call; loop if more are needed.
        while len(results) < num_results:
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": optimized_query,
                "start": start_index,
            }
            url = "https://www.googleapis.com/customsearch/v1"
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                print("API CALL failed",response)
                return []
            
            data = response.json()
            items = data.get("items", [])
            if not items:
                break
            
            # Append only the desired keys to our results list.
            for item in items:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
            
            # Check if there is a next page available.
            queries = data.get("queries", {})
            if "nextPage" in queries:
                start_index = queries["nextPage"][0]["startIndex"]
            else:
                break

        return results[:num_results]