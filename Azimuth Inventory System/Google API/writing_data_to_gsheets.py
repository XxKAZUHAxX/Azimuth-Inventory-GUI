from Google1 import Create_Service

CLIENT_SECRET_FILE = '../client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_Id = '1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs'
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
worksheet_name = 'DR IN N OUT!'

def update():
    """Overwrites one or more cell(s)"""
    cell_range_insert = 'I10'
    values = [['ROW A', 'ROW B', 'ROW C'], ['Apple', 'Android', 'Ambot']]
    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': values
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_Id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()

def append():
    """Appends one or more cell(s)"""
    data = {"PO Number":{"0":"12345","1":"12345","2":"12345"},"DR Number":{"0":"54321","1":"54321","2":"54321"},"Store":{"0":"Azimuth","1":"Azimuth","2":"Azimuth"},"Brand":{"0":"Kirisun","1":"Kirisun","2":"Kirisun"},"Buying Price":{"0":"5000","1":"5000","2":"5000"},"Model":{"0":"DP-405","1":"DP-405","2":"DP-405"},"Type":{"0":"DMR","1":"DMR","2":"DMR"},"Unit Remarks":{"0":"10","1":"10","2":"10"},"DL Price":{"0":"50000","1":"50000","2":"50000"},"Serial Number":{"0":"1111","1":"2222","2":"3333"},"IMEI 1":{"0":"4444","1":"5555","2":"6666"},"IMEI 2":{"0":"7777","1":"8888","2":"9999"}}
    cell_range_insert = f"A{locate_lastrow()}"
    values = data
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_Id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()

def locate_lastrow():
    """Locates the last row of a given column"""
    last_row = 2
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_Id,
        majorDimension='ROWS',
        range='DR IN N OUT!A2:A'
    ).execute()
    last_row += len(response['values']) - 1
    # print(last_row)
    return last_row

append()