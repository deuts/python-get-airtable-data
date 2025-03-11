import time
import pyairtable
from pyairtable import Api
from pyairtable.formulas import match
from requests.exceptions import RequestException

def fetch_airtable_data(api_key, base_id, table_id, filters=None, sort_by=None, max_records=None):
  """
  Fetches data from an Airtable table with pagination, error handling, and retries.

  Args:
      api_key (str): Airtable API key.
      base_id (str): Airtable Base ID.
      table_id (str): Airtable Table ID.
      filters (dict, optional): Dictionary of field-value pairs to filter data.
      sort_by (str, optional): Field name to sort by.
      max_records (int, optional): Maximum number of records to retrieve.

  Returns:
      list: A list of records (each record is a dictionary).
  """
  api = Api(api_key)
  table = api.table(base_id, table_id)
  retries = 3
  backoff_factor = 2

  for attempt in range(retries):
    try:
      params = {}
      if filters:
        params["formula"] = match(filters)
      if sort_by:
        params["sort"] = [{ "field": sort_by, "direction": "asc" }]
      
      # Fetch all records with pagination or limit
      records = table.all(**params) if not max_records else table.all(limit=max_records, **params)

      return [record["fields"] for record in records]

    except pyairtable.ApiError as e:
      if e.status_code == 401:
        print("Error: Invalid API Key or Base ID. Check your credentials.")
        break
      elif e.status_code == 403:
        print("Error: Insufficient permissions to access this table.")
        break
      elif e.status_code == 429:
        wait_time = (backoff_factor ** attempt)
        print(f"Rate limit reached. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
      else:
        print(f"Airtable API error: {e}")
        break

    except RequestException as e:
      print(f"Network error: {e}. Retrying...")
      time.sleep(backoff_factor ** attempt)

  return []  # Return an empty list if all retries fail

# Example Usage:
if __name__ == "__main__":
  API_KEY = "your_airtable_api_key"
  BASE_ID = "your_base_id"
  TABLE_ID = "your_table_id"

  FILTERS = {"Status": "Pending"}  # Set to None if no filters are needed
  SORT_BY = "Due Date"  # Set to None if sorting is not needed
  MAX_RECORDS = 50  # Set to None to fetch all records

  results = fetch_airtable_data(API_KEY, BASE_ID, TABLE_ID, filters=FILTERS, sort_by=SORT_BY, max_records=MAX_RECORDS)
  print(results)
