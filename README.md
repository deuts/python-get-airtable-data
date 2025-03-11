# Airtable Data Fetcher

A reusable Python function to retrieve data from an Airtable table with pagination, filtering, sorting, and error handling.

## Features

✅ Supports fetching all records with pagination  
✅ Optional filtering based on field values  
✅ Optional sorting by a specific field  
✅ Handles API errors and rate limits with retries  
✅ Uses table ID instead of table name for stability  

## Installation

Before using this script, install the required dependencies:

```sh
pip install pyairtable requests
```

## Usage

### Example: Fetch All Records
```python
from get_airtable_data import fetch_airtable_data

API_KEY = "your_airtable_api_key"
BASE_ID = "your_base_id"
TABLE_ID = "your_table_id"

records = fetch_airtable_data(API_KEY, BASE_ID, TABLE_ID)
print(records)
```

### Example: Fetch with Filters, Sorting, and Record Limit
```python
records = fetch_airtable_data(
    API_KEY, 
    BASE_ID, 
    TABLE_ID, 
    filters={"Status": "Pending"}, 
    sort_by="Due Date", 
    max_records=50
)
```

## Environment Variables (Optional)
Instead of hardcoding credentials, you can use environment variables:

```sh
export AIRTABLE_API_KEY="your_api_key"
export AIRTABLE_BASE_ID="your_base_id"
export AIRTABLE_TABLE_ID="your_table_id"
```

Then, modify your script:

```python
import os
from get_airtable_data import fetch_airtable_data

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")

records = fetch_airtable_data(API_KEY, BASE_ID, TABLE_ID)
```

## Error Handling
The function includes:
- **Retries for network issues and rate limits**
- **Graceful handling of invalid API keys and permissions**
- **Automatic pagination when `max_records` is not set**

## License
This project is licensed under the MIT License.
