# from crawler import Crawler
from google_sheets import Google_Sheet
from crawler import Crawler

import pandas as pd
import numpy as np
import time
import sys

def update_row(sheet, metadata): 
    header = sheet.get_header()
    row = {}
    
    for col in header:
        try:
            row[col] = metadata[col]
        except:
            row[col] = ''

    sheet.update_row(list(row.values()))

def score_listing(metadata):

    try:
        try:
            t_rent = float(metadata['Total Rent'])
        except:
            t_rent = float(metadata['Base Rent'])
        score = (t_rent / float(metadata['Living Space'])) / np.sqrt(float(metadata['No Rooms']))
    except Exception as e:
        print(e)
        metadata['Qualified?'] = 'n'
        return metadata

    keys = ['Balcony', 'Has Kitchen', 'Lift', 'Cellar', 'WG Possible']

    for k in keys:
        try:
            if metadata[k] == 'y':
                score -= 0.5
        except:
            continue

    try:
        if 5 < float(metadata['Floor']) < 10:
            score -= 0.5

        if float(metadata['Floor'] )>= 10:
            score -= 1.2
    except:
        pass

    metadata['Qualified?'] = 'y'
    metadata['Score'] = score
    
    if score > 9:
        metadata['Qualified?'] = 'n'
    
    else:
        try:
            if metadata['Balcony'] == 'n':
                metadata['Qualified?'] = 'n'
        except:
            pass
        try:
            if float(metadata['Floor']) > 2 and metadata['Lift'] == 'n':
                metadata['Qualified?'] = 'n'
        except:
            pass

    if score < 6.75:
        metadata['Qualified?'] = 'y'
        try:
            if metadata['WBS'] == 'y':
                metadata['Qualified?'] = 'n'
        except:
            pass

    return metadata

def main():

    sheet = Google_Sheet()
    crawler = Crawler()

    ### get all ids
    ids = sheet.get_all_ids()
    print(len(ids))

    ### get all listings
    shape = 'eW1sX0lzZ2JwQWZ1Qml3Q3BFZ2JCYk5zc0FfQ2ttQWxccWZCbEpvR3pBcU14S2lDYklrTGZDbXFAXGFsQGtAeWNAVmlXekNreUJ7Q314QHlHYU9hT2BAfXRAcmVAe3RAck9RcWBAX1V9XGJ8QHl1QmpLeWFAbF19ZkFyUGd0QXFFeXZAa0tpUnVPeUNvZ0BkSXNgQHJeeWlAZn1Ac1pmZ0B3U2JkQHtjQXF2QHd7QGtMY3hAbUx5RUR9Q2xIe3NAbGdEeVh0YkFvYkBoZEJjTHB4QnRAandAZWJAdkFxcEBmfUBiWWhtQWhcbGdBYGhAYnJBYmJBa3VCaFJ_ZUB1W3JfQmRwQGBWfnRAalJ0T2RjQWVIYmZAdkl0V2hUeEN1S2ZxQ3JoQXFQ'
    listings = crawler.get_listings(shape_id=shape)
    time.sleep(5)

    for listing in listings:

        listing_id = listing.split('/')[-1]
        print(listing_id)

        if listing_id in ids:
            print("Ad %s already processed..." % listing_id)
            continue
       
        ### get ad data
        metadata = crawler.get_ad_data(listing)

        if type(metadata) == bool:
            print("Error fetching metadata...")
            continue
        
        ### check qualification
        metadata = score_listing(metadata)

        if metadata['Qualified?'] == 'y':
            ### contact ad
            # if not metadata['Scout Id'] in ids:
            timestamp, contacted = crawler.contact_ad(listing)
            if contacted:
                metadata['Contacted?'] = 'y'
                print("Ad %s contacted at %s" % (metadata['Scout Id'], timestamp))
            else:
                metadata['Contacted?'] = 'n'
                print("Could not contact ad %s at %s" % (metadata['Scout Id'], timestamp))
            metadata['Contacted At'] = timestamp
        else:
            print("Ad %s not qualified..." % metadata['Scout Id'])

        ### update row
        update_row(sheet, metadata)
        time.sleep(2)

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
    while True:
        try: 
            main()
            time.sleep(60*3)
        except KeyboardInterrupt:
            sys.exit()
        except:
            pass