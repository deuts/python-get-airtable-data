import time
import pyairtable
from pyairtable import Api
from requests.exceptions import RequestException

def create_record(api_key, base_id, table_id, data):
  """
  Creates a new record in an Airtable table.

  Args:
      api_key (str): Airtable API key.
      base_id (str): Airtable Base ID.
      table_id (str): Airtable Table ID.
      data (dict): Dictionary containing field-value pairs for the new record.

  Returns:
      dict: The created record's details, or None if an error occurs.
  """
  api = Api(api_key)
  table = api.table(base_id, table_id)
  retries = 3
  backoff_factor = 2

  for attempt in range(retries):
    try:
      record = table.create(data)
      return record["fields"]

    except pyairtable.ApiError as e:
      if e.status_code == 401:
        print("Error: Invalid API Key or Base ID. Check your credentials.")
        break
      elif e.status_code == 403:
        print("Error: Insufficient permissions to create records.")
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

  DATA = {"Name": "John Doe", "Email": "john@example.com"}

  result = create_record(API_KEY, BASE_ID, TABLE_ID, DATA)
  print(result)
