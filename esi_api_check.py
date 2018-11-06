from esipy import EsiApp
from esipy import EsiClient
import ssl
import pickle
import os
from datetime import date, time, datetime, timedelta
import sqlite3
import time
from pyfiglet import figlet_format


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

def id_to_name(cur, id):
    cur.execute('SELECT typeName FROM SDE.invTypes WHERE typeID=?;', (id,))
    name = cur.fetchall()
    return name[0][0]

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
    cur.execute(''' SELECT DISTINCT materialTypeID 
                    FROM reaction_materials 
                    WHERE materialTypeID NOT IN (
                        SELECT DISTINCT productTypeID 
                        FROM reaction_products
                    );''')
    materials=cur.fetchall()
    cur.execute(''' SELECT DISTINCT productTypeID 
                    FROM reaction_products 
                    WHERE productTypeID NOT IN (
                        SELECT materialTypeID 
                        FROM reaction_materials
                    );''')
    products=cur.fetchall()
    cur.execute(''' SELECT DISTINCT materialTypeID 
                    FROM reaction_materials 
                    WHERE materialTypeID IN (
                        SELECT productTypeID 
                        FROM reaction_products
                    );''')
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
    cur.execute("ATTACH DATABASE 'sde.sqlite' AS sde;")
    return cur
    
def insert_market_info(results, cur):
    print('inserting')
    cur.execute("DELETE FROM market_info;")
    cur.execute('BEGIN TRANSACTION;')
    for swagger_object in results:
        for order in swagger_object[1].data:
            cur.execute('INSERT OR IGNORE INTO market_info (duration, issued, is_buy_order, location_id, min_volume, order_id, price, range, system_id, type_id, volume_remain, volume_total) VALUES (?,datetime(?),?,?,?,?,?,?,?,?,?,?);', 
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
    cur.execute('END TRANSACTION;')
             
 
def chunks(data, rows=10000):
    for i in range(0, len(data), rows):
        yield data[i:i+rows]
        
def retrieve_partitioned_material_ids(cur, mode):
    sql_reaction_id_string = '''SELECT invt.typeID --, invt.typeName
                                FROM SDE.industryActivity actv
                                JOIN SDE.invTypes invt ON invt.typeID=actv.typeID
                                WHERE actv.activityID=11
                                AND 0 '''+mode[0]+''' (
                                    SELECT COUNT(*) 
                                    FROM (
                                        SELECT * 
                                        FROM reaction_materials mats 
                                        WHERE mats.typeid=actv.typeid
                                        AND mats.materialTypeID IN (
                                            SELECT productTypeID
                                            FROM reaction_products
                                        )
                                    )
                                )
                                AND 0 '''+mode[1]+''' (
                                    SELECT COUNT(*) 
                                    FROM (
                                        SELECT * 
                                        FROM reaction_products prod 
                                        WHERE prod.typeid=actv.typeid
                                        AND prod.productTypeID IN (
                                            SELECT materialTypeID
                                            FROM reaction_materials
                                        )
                                    )
                                )'''
    cur.execute(sql_reaction_id_string + ';')
    reactionIDs =  cur.fetchall()

    cur.execute(''' SELECT DISTINCT materialTypeID
                    FROM reaction_materials
                    WHERE typeID IN ( ''' 
                    + sql_reaction_id_string + 
                ''') AND materialTypeID NOT IN
                        (SELECT type_id 
                        FROM material_cost
                        WHERE self_produced=0);''')
    materialIDs = cur.fetchall()

    return reactionIDs, materialIDs
 
def buy_cost_evaluator(cur, type_id):
    cur.execute('''SELECT price, volume_remain, rowid AS market_rowid
                   FROM market_info
                   WHERE type_id=?
                   AND is_buy_order=0
                   ORDER BY price ASC;''', (type_id,) )
    market_orders = cur.fetchall()
    total_volume = 0
    total_cost = 0
    selected_orders = []
    for market_order in market_orders:
        price = market_order[0]
        volume_remain = market_order[1]
        market_rowid = market_order[2]
        
        total_volume += volume_remain
        total_cost += volume_remain*price
        
        cur.execute(''' UPDATE market_info
                        SET marked_for_buy=1
                        WHERE rowID=?;''', (market_rowid,))
                        
        if total_volume >= min_material:
            break
    # print(id_to_name(cur, type_id))
    if total_volume != 0:
        table_cost = total_cost/total_volume
    else:
        table_cost = None

       
    cur.execute('INSERT INTO material_COST (type_id, cost, time, self_produced) VALUES (?, ?, ?, ?);', (type_id, table_cost, 0, 0))
    
def self_production_cost_evaluator(cur, reactionID): # this should be the one that checks if it is cheaper to self-produce
    cur.execute(''' SELECT DISTINCT materialTypeID, quantity
                    FROM reaction_materials
                    WHERE typeID=?;''', (reactionID,))
    materials_list = cur.fetchall()
    cur.execute(''' SELECT DISTINCT productTypeID, quantity
                    FROM reaction_products
                    WHERE typeID=?;''', (reactionID,))
    product_list = cur.fetchall()
    product_id = product_list[0][0]
    product_count = product_list[0][1] 
    
    reaction_subtotal = 0
    for material_row in materials_list:
        material_id = material_row[0]
        material_count = material_row[1]
        cur.execute(''' SELECT MIN(cost)
                        FROM material_cost
                        WHERE type_id=?;''', (material_id,))
        price = cur.fetchall()
        price = price[0][0]
        if price is not None:
            reaction_subtotal += price*material_count
        else:
            print('When evaluating production costs, no orders found for: ', id_to_name(cur, material_id))
        
    reaction_total = reaction_subtotal/product_count
    
    cur.execute('SELECT time FROM industryActivity WHERE typeID=?;', (reactionID,))
    time = cur.fetchall()
    time = time[0][0]
 
    cur.execute('INSERT INTO material_cost (type_id, cost, time, self_produced) VALUES (?,?,?,?);', (product_id, reaction_total, time, 1))
    
def partition_and_evaluate_reaction_costs(cur):
    modes = (('=', '=',), ('=', '!=',), ('!=', '!=',), ('!=', '=',))
    best_price = {}
    cur.execute('DELETE FROM material_cost;')
    cur.execute('UPDATE market_info SET marked_for_buy=0;')
    cur.execute(''' SELECT DISTINCT materialTypeID
                    FROM reaction_materials
                    WHERE materialTypeID IN(
                        SELECT productTypeID
                        FROM reaction_products
                    );''')
    shared_materials = cur.fetchall() # this can be used to check if a material is used as a product
    for mode in modes:
        reactionIDs, materialIDs = retrieve_partitioned_material_ids(cur, mode)
        cur.execute('BEGIN TRANSACTION;')
        for materialID in materialIDs:
            buy_cost_evaluator(cur, materialID[0])
        cur.execute('END TRANSACTION;')
        cur.execute('BEGIN TRANSACTION;')
        for reactionID in reactionIDs:
            self_production_cost_evaluator(cur, reactionID[0])
        cur.execute('END TRANSACTION;')
                
def evaluate_reaction_profits(cur):
    cur.execute('DELETE FROM product_gross;')
    cur.execute('SELECT productTypeID FROM reaction_products;')
    products_query = cur.fetchall()
    
    cur.execute('BEGIN TRANSACTION;')
    for query in products_query:
        productID = query[0]
        cur.execute(''' SELECT price, volume_remain, rowid
                        FROM market_info
                        WHERE is_buy_order=1
                        AND type_id=?
                        ORDER BY price DESC;''', (productID,))
        market_orders = cur.fetchall()
        
        total_volume = 0
        subtotal_price = 0
        
        for order in market_orders:
            price = order[0]
            volume = order[1]
            order_rowid = order[2]
            
            total_volume += volume
            subtotal_price += volume*price
            
            cur.execute(''' UPDATE market_info
                            SET marked_for_buy=1
                            WHERE rowid=?;''', (order_rowid,))
            
            if total_volume >= min_product:
                break
        total_price = subtotal_price/total_volume
        cur.execute('INSERT INTO product_gross (sell_price, type_id) VALUES (?,?);', (total_price, productID))
    cur.execute('END TRANSACTION;')

def evaluate_reaction_margins(cur):
    cur.execute('DELETE FROM reaction_margins;')
    cur.execute('SELECT productTypeID, quantity  FROM reaction_products;')
    products_query = cur.fetchall()

    cur.execute('BEGIN TRANSACTION;')
    for query in products_query:
        productID = query[0]
        product_count = query[1]
        cur.execute(''' SELECT MIN(cost)
                        FROM material_cost
                        WHERE type_id = ?;''', (productID,))
        cost_query = cur.fetchall()
        product_investment = cost_query[0][0]
        cur.execute(''' SELECT sell_price
                        FROM product_gross
                        WHERE type_id = ?;''', (productID,))
        gross_query = cur.fetchall()
        product_gross = gross_query[0][0]
        margin = product_gross - product_investment
        cur.execute(''' INSERT INTO reaction_margins 
                        (product_type_id, obtain_price, sell_price, margin)
                        VALUES (?,?,?,?);''',
                        (productID, product_investment*product_count, product_gross*product_count, margin*product_count))
    cur.execute('END TRANSACTION;')

def find_recipe(cur, product_id):
    cur.execute(''' SELECT typeID
                    FROM reaction_products
                    WHERE productTypeID=?;''', (product_id,))
    reactionTypeID = cur.fetchall()[0][0]
    cur.execute(''' SELECT materialTypeID, quantity
                    FROM reaction_materials
                    WHERE typeID=?;''', (reactionTypeID,))
    materials = cur.fetchall()
    recipe = {}
    print('')
    print(figlet_format(str(product_id), font='starwars'))
    print(id_to_name(cur, product_id), '\n')
    print('*--------------------------------------------------*')
    for material in materials:
        materialID = material[0]
        materialQuantity = material[1]

        cur.execute(''' SELECT MIN(COST), self_produced
                        FROM material_cost
                        WHERE type_id=?;''', (materialID,))
        mat_cost = cur.fetchall()
        material_cost = mat_cost[0][0]
        material_self_produced = mat_cost[0][1]
        print(id_to_name(cur,materialID), 'x' + str(materialQuantity), mat_cost)
        if material_self_produced:
            cur.execute(''' SELECT typeID
                            FROM reaction_products
                            WHERE productTypeID=?;''', (materialID,))
            subreactionTypeID = cur.fetchall()[0][0]
            cur.execute(''' SELECT materialTypeID, quantity
                            FROM reaction_materials
                            WHERE typeID=?;''', (subreactionTypeID,))
            sub_materials = cur.fetchall()
            for sub_material in sub_materials:
                sub_materialID = sub_material[0]
                sub_materialQuantity = sub_material[1]

                cur.execute(''' SELECT MIN(COST), self_produced
                                FROM material_cost
                                WHERE type_id=?;''', (sub_materialID,))
                sub_mat_cost = cur.fetchall()
                sub_material_cost = sub_mat_cost[0][0]
                sub_material_self_prodcued = sub_mat_cost[0][0]
                print('    ', id_to_name(cur, sub_materialID), 'x' + str(sub_materialQuantity), sub_mat_cost)
                if sub_materialID not in recipe:
                    recipe[sub_materialID] = sub_materialQuantity*materialQuantity
                else:
                    recipe[sub_materialID] += sub_materialQuantity*materialQuantity
        else:
            if materialID not in recipe:
                recipe[materialID] = materialQuantity
            else:
                recipe[materialID] += materialQuantity
        print('*--------------------------------------------------*')
    #print(recipe)
    print('total:')
    for item in recipe:
        print(' ', id_to_name(cur, item), 'x' + str(recipe[item]))
    print('')

def refresh_margin_display(top_margins):
    menu_index = 0
    for response in top_margins:
        product_type_id = response[0]
        margin = response[1]
        obtain_price = response[2]
        sell_price = response[3]
        print(str(menu_index+1) + ".)", "%.2f" % (margin/1000000) + 'm with', id_to_name(cur, product_type_id), "%.2f" % (sell_price/1000000) +  'm -', "%.2f"% (obtain_price/1000000) + 'm', "ROI:", "%.2f"%(sell_price/obtain_price*100) + "%")
        menu_index += 1
    return input('choice ("e" to exit): ')

def display_top_margins(cur):
    cur.execute(''' SELECT product_type_id, margin, obtain_price, sell_price
                    FROM reaction_margins
                    WHERE margin > 0
                    ORDER BY margin DESC;''')
    top_margins = cur.fetchall()

    response = refresh_margin_display(top_margins)

    while response != 'e':
        try:
            response = int(response)
            response -= 1
            if response >= 0 and response < len(top_margins):
                print('Retrieving recipe for', id_to_name(cur, top_margins[response][0]) + "." )
                print('')
                print('')
                find_recipe(cur, top_margins[response][0])
            else:
                print('Error: too high')
            response = input('choice ("e" to exit): ')
        except: 
            if response == 'r':
                response = refresh_margin_display(top_margins)
                continue
            print('Error: value must be a number')
            response = input('choice ("e" to exit): ')


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
min_material = 100000
min_product = 100000

if __name__=="__main__":
    cur = initialize_database()
    
    # fetch_market_data(cur)
    partition_and_evaluate_reaction_costs(cur)
    evaluate_reaction_profits(cur)
    evaluate_reaction_margins(cur)

    display_top_margins(cur)

    #print(results)