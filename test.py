from google.oauth2 import service_account
from googleapiclient.discovery import build

spreadsheet_id = "1fMlqflPJTg9oTuKthrAtgJdKLM124wMcgStw9fwLJ9Q"
# For example:
# spreadsheet_id = "8VaaiCuZ2q09IVndzU54s1RtxQreAxgFNaUPf9su5hK0"

credentials = service_account.Credentials.from_service_account_file(
    "key.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build("sheets", "v4", credentials=credentials)


request = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id, ranges=[], includeGridData=False
)
sheet_props = request.execute()

print(sheet_props)

# Output:
# My New Google Sheets Spreadsheet
