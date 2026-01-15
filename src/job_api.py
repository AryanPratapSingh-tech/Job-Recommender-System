from apify_client import ApifyClient
import os
from dotenv import load_dotenv 

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))



#Method to fetch linkedIn Jobs
def fetch_LinkedIn_Jobs(search_query, location = "India", rows=60):

  run_input = {
    "title" : search_query,
    "location" : location,
    "rows" : rows,
    "proxy": {
      "useApifyProxy": True,
      "apifyProxyGroups": ["RESIDENTIAL"]
    }
  }

  run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
  jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
  return jobs
  



def fetch_Naukari_Jobs(search_query, location="India", rows=60):

  run_input = {
    "keyword": search_query,
    "maxJobs": 60,
    "freshness": "all",
    "sortBy": "relevance",
    "experience" : "all",
  }

  run = apify_client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)
  jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
  return jobs