from Google1 import Create_Service
import pandas as pd
from pprint import pprint

class Create_Instance():
    def __init__(self):
        CLIENT_SECRET_FILE = 'client_secret.json'
        API_SERVICE_NAME = 'sheets'
        API_VERSION = 'v4'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.spreadsheet_Id = '1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs'
        self.service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
        self.start()

    def start(self):
        self.range = 'DR IN N OUT!A2:A'
        dr_in_n_out_spreadsheet = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_Id, majorDimension='ROWS',
                                                            range='DR IN N OUT!A2:AQ').execute()
        models_spreadsheet = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_Id, majorDimension='ROWS',
                                                            range='INVENTORY!A1:B').execute()
        dealer_spreadsheet = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_Id, majorDimension='ROWS',
                                                            range='DEALER LIST!A1:A').execute()
        columns1, data1 = dr_in_n_out_spreadsheet['values'][0], dr_in_n_out_spreadsheet['values'][1:]
        columns2, data2 = models_spreadsheet['values'][0], models_spreadsheet['values'][1:]
        data3 = dealer_spreadsheet['values']
        self.dr_in_n_out_df = pd.DataFrame(data1, columns=columns1)
        self.inventory_df = pd.DataFrame(data2, columns=columns2)
        self.dealers_df = pd.DataFrame(data3)
        self._all_models_dict = {'DMR':[], 'POC':[], 'ACCESSORIES':[], 'PARTS':[], 'OTHERS':[]}

        for item in set([type for type in self.inventory_df['TYPES'] if type != '' and type != None]):
            self._all_models_dict[item] = [model for i, model in enumerate(self.inventory_df["ITEMS"]) if self.inventory_df["TYPES"][i] == item]
        # print(self._all_models_dict.keys())
        # pprint(self._all_models_dict)
        # print(self.inventory_df['ITEMS'])
        # print(self.dealers_df)


if __name__ == '__main__':
    instance = Create_Instance()