from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SCOPES = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_SPREADSHEET_ID = '1bCCV49QH8z4cD4GuNP_A9M3oow1DCOJznZwNf_QTWmQ'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # # Call the Sheets API
    sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                             range=SAMPLE_RANGE_NAME).execute()
    # values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))

    fname = 'apartments.csv' #'/home/aqeel/Dev/ImmoSpider/apartments.csv'
    df = pd.read_csv(fname)
    # df
    # link = 'https://www.immobilienscout24.de/expose/114467257' #df.url[5]

    rand = np.random.choice(df.url, 10)

    cols = df.columns
    newcols = ['total_floors', 'heating_type', 'efficiency_class', 'year_constructed', 'score', 'contacted', 'date_contacted']

    df = df.reindex(columns = np.concatenate([cols, newcols]))

    list(df.rent + df.extra_costs)
    df.columns


    dcols = ['address', 'area', 'balcony', 'cellar', 'contact_name',
        'district', 'elevator', 'extra_costs',
        'kitchen', 'rent',
        'rooms', 'sqm', 'wg', 'score']

    for row in df.iterrows():
        sheet.append_row(list(row[1]))

if __name__ == '__main__':
    main()