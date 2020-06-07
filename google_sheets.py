import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

import numpy as np
import pandas as pd

class Google_Sheet():

    def __init__(self):

        self.header = ['Online Since',
                    'Scout Id',
                    'Regio3',
                    'Regio2',
                    'Street',
                    'House Number',
                    'Zip Code',
                    'Link',
                    'Picture',
                    'Base Rent',
                    'Total Rent',
                    'No Rooms',
                    'Living Space',
                    'Floor',
                    'Number Of Floors',
                    'Lift',
                    'Balcony',
                    'Has Kitchen',
                    'Cellar',
                    'Garden',
                    'Pets Allowed',
                    'WG Possible',
                    'WBS',
                    'Energy Efficiency Class',
                    'Heating Type',
                    'Heating Costs',
                    'Type Of Flat',
                    'Year Constructed',
                    'Newly Const',
                    'Condition',
                    'Interior Qual',
                    'Last Refurbish',
                    'Pricetrend',
                    'Pricetrendbuy',
                    'Pricetrendrent',
                    'Contacted?',
                    'Contacted At'
                    ]

        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'drive_credentials.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/1bCCV49QH8z4cD4GuNP_A9M3oow1DCOJznZwNf_QTWmQ")
        self.sheet = wks.worksheet("contacted")

    def update_row(self, row):
        # date = str(datetime.utcnow())
        # processed_images.append_row([processed_date, keywords])
        self.sheet.append_row(row)

    def get_all_ids(self):
        return self.sheet.col_values(2)[1:]

    def get_all_area(self):
        return self.sheet.col_values(21)

    def get_header(self):
        return self.sheet.row_values(1)

    def update_header(self, header=None):
        if not header:
            header = self.header
        n_cols = len(header)
        last_cell = gspread.utils.rowcol_to_a1(1, n_cols)
        self.sheet.update("A1:" + last_cell, [header])