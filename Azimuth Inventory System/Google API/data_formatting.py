from Google1 import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = '../client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_Id = '1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs'
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
worksheet_name = 'DR IN N OUT!'
sheet_id = '1072916009'

request_body = {
    'requests': [
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 3519,
                    'endRowIndex': 3524,
                    'startColumnIndex': 8,
                    'endColumnIndex': 10
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {
                            'type': 'CURRENCY',
                            'pattern': '$#,##0'
                        },
                        'backgroundColor': {
                            'red': 120,
                            'green': 60,
                            'blue': 70
                        },
                        'textFormat': {
                            'fontSize': 14,
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(numberFormat,backgroundColor,textFormat)'
            }
        }
    ]
}

response = service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_Id,
    body=request_body
).execute()