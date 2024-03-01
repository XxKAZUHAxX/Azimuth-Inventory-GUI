from Google1 import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = '../client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

# URL = r'https://docs.google.com/spreadsheets/d/1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs/edit?pli=1#gid=1072916009'
# df = pd.read_csv(URL)

# print(dir(service))
# print(dir(service.spreadsheets))

spreadsheet_Id = '1cTvm237Krvm6Mo5G5vs7yR15_KXAM4iiKX614SKyVKs'
mySpreadsheet = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_Id,
    majorDimension='ROWS',
    range='DR IN N OUT!A2:AQ3522'
).execute()

columns = mySpreadsheet['values'][0]
data = mySpreadsheet['values'][1:]
df = pd.DataFrame(data, columns=columns)
# print(df)

# print(df['MODEL'])

DMRs, POCs, ACCESSORIES, PARTS, OTHERS = [], [], [], [], []
for i, model in enumerate(df['MODEL']):
    if df['TYPE'][i] == 'DMR':
        DMRs.append(model)
    elif df['TYPE'][i] == 'POC':
        POCs.append(model)
    elif df['TYPE'][i] == 'ACCESSORIES':
        ACCESSORIES.append(model)
    elif df['TYPE'][i] == 'PARTS':
        PARTS.append(model)
    elif df['TYPE'][i] == 'OTHERS':
        OTHERS.append(model)

dmr_set = sorted(set(DMRs))
poc_set = sorted(set(POCs))
accessories_set = sorted(set(ACCESSORIES))
parts_set = sorted(set(PARTS))
others_set = sorted(set(OTHERS))

dmr_df = pd.DataFrame(dmr_set)
poc_df = pd.DataFrame(poc_set)
accessories_df = pd.DataFrame(accessories_set)
parts_df = pd.DataFrame(parts_set)
others_df = pd.DataFrame(others_set)

# all_models = pd.concat([dmr_df, poc_df, accessories_df, parts_df, others_df], axis=1)
# all_models.columns = ['DMR', 'POC', 'ACCESSORIES', 'PARTS', 'OTHERS']
# print(all_models)
#
# all_models.to_excel('output.xlsx', index=False)

# count = df['MODEL'].value_counts()['T60']
# print(count)

# for i, model in enumerate(dmr_df.values.flatten()):
#     count = df['MODEL'].value_counts()[model]
#     print(f"{model} : {count}")
#
# print('\n\n\n')
#
# for i, model in enumerate(dmr_df.values.flatten()):
#     count = len(df[df['MODEL'] == model])
#     print(f"{model} : {count}")

# myData = pd.DataFrame.from_dict(mySpreadsheet['values'])
# print(myData)
serials = {}
for i, model in enumerate(dmr_df.values.flatten()):
    # serials = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
    # print(f"{model} : {serials}")
    # serial_no = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]
    serials[model] = [df['SERIAL NO.'][j] for j, item in enumerate(df['MODEL']) if item == model]

# print(', '.join(serials))
model = 'DP405 - 136'
print(', '.join(serials[model]))

# print(myData[1].tolist())