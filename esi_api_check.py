from esipy import EsiApp
from esipy import EsiClient
import ssl
import pickle
import os
from datetime import date, time, datetime, timedelta
import sqlite3
import time

########## DOES WEIRD STUFF DON'T REMOVE ###########################################
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification 
    ssl._create_default_https_context = _create_unverified_https_context


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
########################################################################


def generate_market_info_requests(input_list, order_string, region):
    operations = []
    for input_id in input_list:
        operations.append(
            api.app.op['get_markets_region_id_orders'](
                region_id=region,
                page=1,
                order_type=order_string,
                type_id=input_id[0],
            )
        )
        '''
        res = api.client.head(operation)
        if res.status==200:
            number_of_pages = res.header['X-Pages'][0]
            if number_of_pages > 1:
                print("wweeeeooooweeeeeeooooo")
            for page in range(1, number_of_pages+1):
                operations.append(
                    api.app.op['get_markets_region_id_orders'](
                        region_id=10000002,
                        page=page,
                        order_type=order_string,
                        type_id=input_id[0],
                    )
                )
        '''
    return operations
def to_sql_datetime(in_date):
    outstring = str(in_date.year)+'-'+str(in_date.month)+'-'+str(in_date.day)+' '+str(in_date.hour)+':'+str(in_date.minute) + ':' + str(in_date.second) 
    return outstring
def fetch_market_data(cur):
    cur.execute("SELECT DISTINCT materialTypeID FROM reaction_materials WHERE materialTypeID NOT IN (SELECT materialTypeID FROM reaction_materials WHERE materialTypeID IN (SELECT productTypeID FROM reaction_products))")
    materials=cur.fetchall()
    cur.execute("SELECT DISTINCT productTypeID FROM reaction_products WHERE productTypeID NOT IN (SELECT materialTypeID FROM reaction_materials WHERE materialTypeID IN (SELECT productTypeID FROM reaction_products))")
    products=cur.fetchall()
    cur.execute("SELECT DISTINCT materialTypeID FROM reaction_materials WHERE materialTypeID IN (SELECT productTypeID FROM reaction_products)")
    both = cur.fetchall()
    
    operations = []
    regions = [10000002, 10000042, 10000043, 10000032]
    for region in regions:
        operations += generate_market_info_requests(materials, 'sell', region)
        operations += generate_market_info_requests(products, 'buy', region)
        operations += generate_market_info_requests(both, 'all', region)

    
    results = None
    print('starting request')
    if len(operations) > 1:
        results = api.client.multi_request(operations)
    else:
        results = api.client.request(operations[0])
    #print(results)
    insert_market_info(results, cur)    
#def fetch_market_history(
    
def initialize_database():
    con = sqlite3.connect('./program.sqlite')
    con.isolation_level = None
    cur = con.cursor()
    cur.execute("ATTACH DATABASE 'sde.sqlite' AS sde")
    return cur
    
def insert_market_info(results, cur):
    print('inserting')
    cur.execute("DELETE FROM market_info")
    cur.execute('BEGIN TRANSACTION')
    for swagger_object in results:
        for order in swagger_object[1].data:
            cur.execute('INSERT OR IGNORE INTO market_info (duration, issued, is_buy_order, location_id, min_volume, order_id, price, range, system_id, type_id, volume_remain, volume_total) VALUES (?,datetime(?),?,?,?,?,?,?,?,?,?,?)', 
            (order['duration'],
             str(order['issued']),
             order['is_buy_order'],
             order['location_id'],
             order['min_volume'],
             order['order_id'],
             order['price'],
             order['range'],
             order['system_id'],
             order['type_id'],
             order['volume_remain'],
             order['volume_total']))
    cur.execute('COMMIT')
             
 
def chunks(data, rows=10000):
    for i in range(0, len(data), rows):
        yield data[i:i+rows]

class API:
    def __init__(self):
        self.esi_app = EsiApp()
        
        last_opened = os.path.getmtime('./app.p')
        last_opened = datetime.fromtimestamp(last_opened)
        
        difference = datetime.today() - last_opened
        self.app = None
        if difference.days > 1:
            print('Old swagger information, reinitializing app')
            self.app = self.esi_app.get_latest_swagger
            with open('app.p', 'wb') as handle:
                pickle.dump(self.app, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open('app.p', 'rb') as handle:
                self.app = pickle.load(handle)
   
        self.client = EsiClient(
            retry_requests=True,
            headers={'User-Agent': 'Something'},
            raw_body_only=False,
            )
        

# I want this as a global each time the program is run.        
api = API() #if the swagger information is older than a day, it will re-request it from the server

if __name__=="__main__":
    
    #esi_app, app, client = initialize_api_handlers()
    
    #api = API()
    
    cur = initialize_database()
    
    fetch_market_data(cur)
    
    
    print('working')
    #print(results)