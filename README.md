# Airtable Python Scripts

This repository contains Python scripts to interact with Airtable:
- `fetch_records.py` - Retrieve records from an Airtable table.
- `create_record.py` - Insert a new record.
- `modify_record.py` - Update an existing record.
- `delete_record.py` - Remove a record.

Each script includes:
- Error handling for authentication, permissions, rate limits, and network errors.
- Retries with exponential backoff.
- Modular functions for easy reuse.

## Prerequisites

Ensure you have the following:
- Python 3 installed.
- An Airtable API key.
- Your Base ID and Table ID from Airtable.
- Required Python packages installed:

```sh
pip install pyairtable
```

## Configuration

Each script requires an Airtable API key, Base ID, and Table ID. Update the following variables in the script:

```python
API_KEY = "your_airtable_api_key"
BASE_ID = "your_base_id"
TABLE_ID = "your_table_id"
```

## Usage

### Fetch Records

```sh
python fetch_records.py
```

### Create a New Record

```sh
python create_record.py
```

Modify `DATA` in `create_record.py` to match your table fields:

```python
DATA = {"Name": "John Doe", "Email": "john@example.com"}
```

### Modify an Existing Record

```sh
python modify_record.py
```

Update `RECORD_ID` and `UPDATE_DATA` in `modify_record.py`:

```python
RECORD_ID = "rec1234567890"
UPDATE_DATA = {"Status": "Completed"}
```

### Delete a Record

```sh
python delete_record.py
```

Set `RECORD_ID` in `delete_record.py`:

```python
RECORD_ID = "rec1234567890"
```

## Error Handling

- **401 Unauthorized**: Check if your API key is correct.
- **403 Forbidden**: Verify your Airtable account permissions.
- **404 Not Found**: Ensure the record exists.
- **429 Rate Limit**: The script will retry automatically with exponential backoff.
- **Network Errors**: The script will retry up to 3 times.

## More on `fetch_records.py`

### Features

✅ Supports fetching all records with pagination  
✅ Optional filtering based on field values  
✅ Optional sorting by a specific field  
✅ Handles API errors and rate limits with retries  
✅ Uses table ID instead of table name for stability 

#### Example: Fetch All Records
```python
from fetch_records import fetch_airtable_data

API_KEY = "your_airtable_api_key"
BASE_ID = "your_base_id"
TABLE_ID = "your_table_id"

records = fetch_airtable_data(API_KEY, BASE_ID, TABLE_ID)
print(records)
```

#### Example: Fetch with Filters, Sorting, and Record Limit
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

### Environment Variables (Optional)
Instead of hardcoding credentials, you can use environment variables:

```sh
export AIRTABLE_API_KEY="your_api_key"
export AIRTABLE_BASE_ID="your_base_id"
export AIRTABLE_TABLE_ID="your_table_id"
```

Then, modify your script:

```python
import os
from fetch_records import fetch_airtable_data

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")

records = fetch_airtable_data(API_KEY, BASE_ID, TABLE_ID)
```

### Error Handling
The function includes:
- **Retries for network issues and rate limits**
- **Graceful handling of invalid API keys and permissions**
- **Automatic pagination when `max_records` is not set**

## License

This project is open-source under the MIT License.

