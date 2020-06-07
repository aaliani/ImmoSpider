# from crawler import Crawler
from google_sheets import Google_Sheet
from crawler import Crawler

import pandas as pd

def update_row(sheet, metadata): 
    header = sheet.get_header()
    row = {}
    
    for col in header:
        try:
            row[col] = metadata[col]
        except:
            row[col] = ''

    sheet.update_row(list(row.values()))

def is_qualified(metadata):
    try:
        balcony = metadata['Balcony']
    except:
        balcony = 'n'
    return True if balcony == 'y' else False

def main():

    sheet = Google_Sheet()
    crawler = Crawler()

    ### get all ids
    ids = sheet.get_all_ids()
    print(ids)

    ### get all listings
    listings = crawler.get_listings()

    for listing in listings:

        ### get ad data
        metadata = crawler.get_ad_data(listing)

        if type(metadata) == bool:
            print("Error fetching metadata...")
            continue
        
        if metadata['Scout Id'] in ids:
            print("Ad %s already processed..." % metadata['Scout Id'])
            continue

        ### check qualification
        qualified = is_qualified(metadata)

        if qualified:
            ### contact ad
            timestamp, contacted = crawler.contact_ad(listing)
            metadata['Contacted?'] = 'y' if contacted else 'n'
            metadata['Contacted At'] = timestamp

        ### update row
        update_row(sheet, metadata)

    crawler.close_crawler()

    # my_crawler = Crawler()

    # listings = my_crawler.get_listings(ads_since="2020-05-20T17:44:48", price_max=600)

    # print(listings)


    # ids = sheet.get_index()
    # print(ids)


    # fname = 'apartments.csv' #'/home/aqeel/Dev/ImmoSpider/apartments.csv'
    # df = pd.read_csv(fname)
    # # df
    # # link = 'https://www.immobilienscout24.de/expose/114467257' #df.url[5]

    # rand = np.random.choice(df.url, 10)

    # cols = df.columns
    # newcols = ['total_floors', 'heating_type', 'efficiency_class', 'year_constructed', 'score', 'contacted', 'date_contacted']

    # df = df.reindex(columns = np.concatenate([cols, newcols]))

    # list(df.rent + df.extra_costs)
    # df.columns


    # dcols = ['address', 'area', 'balcony', 'cellar', 'contact_name',
    #     'district', 'elevator', 'extra_costs',
    #     'kitchen', 'rent',
    #     'rooms', 'sqm', 'wg', 'score']

    # for row in df.iterrows():
    #     lst = list(row[1])
    #     lst = [str(val) for val in lst]
    #     sheet.update_row(lst)

if __name__ == '__main__':
    main()