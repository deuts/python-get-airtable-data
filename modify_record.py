import time
import pyairtable
from pyairtable import Api
from requests.exceptions import RequestException

def modify_record(api_key, base_id, table_id, record_id, data):
  """
  Updates an existing record in an Airtable table.

  Args:
      api_key (str): Airtable API key.
      base_id (str): Airtable Base ID.
      table_id (str): Airtable Table ID.
      record_id (str): The ID of the record to update.
      data (dict): Dictionary of fields to update.

  Returns:
      dict: The updated record's details, or None if an error occurs.
  """
  api = Api(api_key)
  table = api.table(base_id, table_id)
  retries = 3
  backoff_factor = 2

  for attempt in range(retries):
    try:
      record = table.update(record_id, data)
      return record["fields"]

    except pyairtable.ApiError as e:
      if e.status_code == 401:
        print("Error: Invalid API Key or Base ID. Check your credentials.")
        break
      elif e.status_code == 403:
        print("Error: Insufficient permissions to modify records.")
        break
      elif e.status_code == 404:
        print("Error: Record not found.")
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

  return None  # Return None if all retries fail

# Example Usage
if __name__ == "__main__":
  API_KEY = "your_airtable_api_key"
  BASE_ID = "your_base_id"
  TABLE_ID = "your_table_id"

  RECORD_ID = "rec1234567890"
  UPDATE_DATA = {"Status": "Completed"}

  result = modify_record(API_KEY, BASE_ID, TABLE_ID, RECORD_ID, UPDATE_DATA)
  print(result)
