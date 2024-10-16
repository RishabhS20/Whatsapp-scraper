import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError
import time

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)
# sheet_id = "1hWaUquZDw2eMABKm52jXJ_P2qfF3Cxteiyyjysvxe_o"
sheet_id = "1FYEs3hyJppB79oPxQnKVksoKejFQ-0M9-bC0yLqGP_c"
sheet = client.open_by_key(sheet_id)


def update_multiple_values(data_list, sheet_name, has_serial_numbers, chunk_size=10, sleep_time=2):
    
    workbook = sheet.worksheet(sheet_name)

    if has_serial_numbers:
        # Find the next empty row in column B (column 2) if the sheet has serial numbers
        column_b_values = workbook.col_values(2)  # Get all values in column B
        next_empty_row = len(column_b_values) + 1  # Find the next empty row in column B
        start_column = 2  # Start filling from column B
    else:
        # Find the next empty row across the entire sheet if there are no serial numbers
        all_values = workbook.get_all_values()  # Get all values from the sheet
        next_empty_row = len(all_values) + 1  # Find the next empty row in the entire sheet
        start_column = 1  # Start filling from column A (first column)

    # Break the data_list into smaller chunks
    for i in range(0, len(data_list), chunk_size):
        # Get the chunk of data to update
        chunk = data_list[i:i+chunk_size]

        # Prepare the range of cells to update, starting from the next empty row
        start_row = next_empty_row + i
        end_row = start_row + len(chunk) - 1
        num_columns = len(chunk[0])  # Assuming all rows have the same number of columns

        # Dynamically calculate the start and end cells
        start_cell = f'{chr(65 + start_column - 1)}{start_row}'
        end_cell = f'{chr(65 + start_column - 1 + num_columns - 1)}{end_row}'
        range_to_update = f'{start_cell}:{end_cell}'

        # Retry logic to handle API errors
        retry_count = 0
        success = False
        while not success and retry_count < 5:  # Retry up to 5 times
            try:
                # Perform the batch update for the current chunk
                print("Successfully Enters Try")
                workbook.update(range_to_update, chunk)
                print(f"Successfully updated rows {start_row} to {end_row}")
                success = True
            except APIError as e:
                # Handle API errors (e.g., rate limit exceeded)
                print(f"APIError encountered: {e}. Retrying...")
                retry_count += 1
                time.sleep(2 ** retry_count)  # Exponential backoff Algorithm

        # Sleep after each chunk to avoid hitting rate limits
        time.sleep(sleep_time)

    print("Update completed.")






    