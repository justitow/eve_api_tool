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



def display_num(number):
"""
display_num

Used for printing large values in human-readable format

:param number: represents the number that will be interpereted for the string
:returns: returns a formated and simplified string with a shortened place size attached
"""
    if number >= 1000 and number < 1000000:
        return ("%.2f" % (number/1000)) + ' k' # magic Something, something, two decimals
    if number >= 1000000 and number < 1000000000:
        return ("%.2f" % (number/1000000)) + ' mil'
    if number >= 1000000000:
        return ("%.2f" % (number/1000000000)) + ' bil'
  

def id_to_name(id):
"""
id_to_name

Used to return the string name of an item using a given typeID.
Locates the value within the invTypes table

:param cur: cursor for the sqlite database
:param id: integer value for the typeID of the material
:returns: outputs a string for the item anme
"""
    cur.execute('SELECT typeName FROM SDE.invTypes WHERE typeID=?;', (id,))
    name = cur.fetchall()
    return name[0][0]


def prepare_component_db():
# I kinda want to eliminate this function
"""
prepare_component_db

Standalone function that recreates the table based off of the materials and products

:param cur: Cursor for the sql database
"""
    cur.execute(''' SELECT DISTINCT materialTypeID
                    FROM reaction_materials
                    WHERE materialTypeID NOT IN (
                        SELECT productTypeID
                        FROM reaction_products
                    );''') # the three repetitions are done this way so that there aren't repeat entries
    materials = cur.fetchall()
    cur.execute(''' SELECT DISTINCT productTypeID
                    FROM reaction_products
                    WHERE productTypeID NOT IN (
                        SELECT materialTypeID
                        FROM reaction_materials
                    );''')
    products = cur.fetchall()
    cur.execute(''' SELECT DISTINCT productTypeID
                    FROM reaction_products
                    WHERE productTypeID IN (
                        SELECT materialTypeID
                        FROM reaction_materials
                    );''')
    both = cur.fetchall()
    cur.execute('DELETE FROM reaction_items;')
    cur.execute('BEGIN TRANSACTION;')
    for mat in materials:
        cur.execute('INSERT INTO reaction_items (type_id) VALUES (?)', (mat[0],))
    for prod in products:
        cur.execute('INSERT INTO reaction_items (type_id) VALUES (?)', (prod[0],))
    for prod_mat in both:
        cur.execute('INSERT INTO reaction_items (type_id) VALUES (?)', (prod_mat[0],))
    cur.execute('END TRANSACTION;')


def generate_market_info_requests(input_list, order_string, region):
"""
generate_market_info_requests

Generates the operations that will be requested from the API given a list
of typeids, the type of order, and a regionID

:param input_list: iterable list of the ID's of the items for which information will be requested
:param order_string: can be 'buy', 'sell', or 'both'. Represents the type of order that will be requested
:param region: ID of the region information will be requested from

:returns: returns a list of operations that will be used for the multi-request.
"""
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
    return operations


def fetch_market_data():
"""
fetch_market_data

If the data stored in the database is older than 1hr, the program polls the API for the market data

:param cur: Cursor for the sqlite program.sqlite database
"""
    cur.execute('SELECT date_pulled FROM market_info LIMIT 1;')
    last_polled = datetime.strptime(cur.fetchall()[0][0], '%Y-%m-%d %H:%M:%S') # processes the datetime from the database into python obj
    difference = datetime.today() - last_polled
    if difference.total_seconds()//60 < 60: # if the data is less than an hour old
        print('Market data is ' + str(difference.seconds//60) + ' minutes old')
        return
    
    print('Stale market data, requesting from the API')
    # generate the typeid's of the materials and products, divided based on use
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

    
    results = None #initialize results variable
    print('starting request')
    if len(operations) > 1: # if there is less than one request, multi_request fails
        results = api.client.multi_request(operations) # multi-threaded api request
    else:
        results = api.client.request(operations[0])
    #print(results)
    insert_market_info(results, cur) # process the responses into the database    

    

def initialize_database():
"""
initialize_database

Creates the cursor that will be used throughout the program to interface with the sqlite databases
Automatically attaches the sde database.

:returns: Cursor object for interfacing with the sde.
"""
    con = sqlite3.connect('./program.sqlite')
    con.isolation_level = None
    cur = con.cursor()
    cur.execute("ATTACH DATABASE 'sde.sqlite' AS sde;")
    return cur

    

def insert_market_info(results, cur):
"""
insert_market_info

Takes results from the API query and inserts them into the database.

:param results: List of the request/response tuples returned from the multi-request function
:param cur: Cur for the sqlite database
"""
    print('inserting')
    cur.execute("DELETE FROM market_info;") # clear all market data
    cur.execute('BEGIN TRANSACTION;')
    for swagger_object in results:
        for order in swagger_object[1].data:
            cur.execute("INSERT OR IGNORE INTO market_info (duration, issued, is_buy_order, location_id, min_volume, order_id, price, range, system_id, type_id, volume_remain, volume_total, date_pulled) VALUES (?,datetime(?),?,?,?,?,?,?,?,?,?,?,DATETIME('now', 'localtime'));", 
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
    cur.execute(''' DELETE FROM market_info
                    WHERE system_id IN (
                        SELECT DISTINCT system_id
                        FROM market_info
                        JOIN SDE.mapSolarSystems ON solarSystemID=system_id
                        WHERE security<.5
                    );''') # remove market entries in lowsec
                    
     

def retrieve_partitioned_material_ids(mode):
"""
retrieve_partitioned_material_ids

Used for evaluating reactions while preserving the order of chain reactions
Gets a list of the materials/products for a given stage. 
Stage is broken into non-involved, first step, middle step, and final step

:param cur: cursor for the sqlite database
:param mode: Tuple for deciding which stage we are looking at. Tuple values can be "==" or "!="
:returns: Returns a list of the reactionID's for the mode
"""
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
                                );'''
    cur.execute(sql_reaction_id_string)
    reactionIDs =  cur.fetchall()

    
    return reactionIDs



def buy_cost_evaluator(type_id):
'''
buy_cost_evaluator

Finds the average buy price for the first $min_material orders
This value is stored in the reaction_items table in the buy_cost column

:param cur: cursor for the sqlite database
:param type_id: type_id for the material being evaluated

'''
    cur.execute('''SELECT price, volume_remain, rowid AS market_rowid
                   FROM market_info
                   WHERE type_id=?
                   AND is_buy_order=0
                   ORDER BY price ASC;''', (type_id,) ) #gathers orders, sorted by cheapness
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
                        
        if total_volume >= min_material: # when the min_material is reached, stops polling through the orders
            break
    if total_volume != 0: # it can be zero when there aren't any orders found for the object
        table_cost = total_cost/total_volume
    else:
        table_cost = None # makes it be NULL, wonder if this has any effect later on in the program?
    cur.execute('UPDATE reaction_items SET buy_cost=? WHERE type_id=?', (table_cost, type_id))
    


def self_production_cost_evaluator(reactionID): # this should be the one that checks if it is cheaper to self-produce
"""
self_production_cost_evaluator

Evaluates the how much it would be to produce one unit of product. This information gets stored in reaction_items
This checks for the cost of buying the material vs producing the material yourself.
The values for these checked are each columns in reaction_items. 
This function is called for each of the "modes" calculated for all of the reactions.

:param cur: cursor for sqlite database
:param reactionID: single typeID for evaluation
"""
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
        cur.execute(''' SELECT buy_cost, production_cost
                        FROM reaction_items
                        WHERE type_id=?;''', (material_id,))
        price = cur.fetchall()
        buy_cost = price[0][0]
        production_cost = price[0][1]
        if buy_cost is None: # this means no buy orders were found for a material. Common for drugs
            continue
        if production_cost is not None and not always_buy: # the always_buy is a parameter for if we are evaluating subcomponents
            cost = min(buy_cost, production_cost)
            reaction_subtotal += cost*material_count
        else: #this means that there is no production_cost for the material (hydrogen blocks and stuff)
            reaction_subtotal += buy_cost*material_count
            
    reaction_total = reaction_subtotal/product_count #get the price per material 
 
    cur.execute('UPDATE reaction_items SET production_cost=? WHERE type_id=?;', (reaction_total, product_id))

 
def find_material_buy_prices():
"""
find_material_buy_prices

Finds all of the material_id's and sends them to the buy_cost_evaluator function

:param cur: cursor for the sqlite database
"""   
    cur.execute('UPDATE market_info SET marked_for_buy=0;')
    cur.execute('SELECT materialTypeID from reaction_materials;')
    materialIDs = cur.fetchall()
    cur.execute('BEGIN TRANSACTION;')
    for materialID in materialIDs:
        buy_cost_evaluator(materialID[0])
    cur.execute('END TRANSACTION;')



def partition_and_evaluate_reaction_costs():
"""
partition_and_evaluate_reaction_costs

Seperates the reactions into the modes based on if they have materials that are also products. 
Gets the reaction_id's and then sends the type_id's to the self_production_cost_evaluator one at
a time to calculate the values.

:param cur: cursor for the sqlite database

"""    
    modes = (('=', '=',), ('=', '!=',), ('!=', '!=',), ('!=', '=',)) 
    best_price = {}
    
    for mode in modes:
        reactionIDs = retrieve_partitioned_material_ids(mode)
        cur.execute('BEGIN TRANSACTION;')
        for reactionID in reactionIDs:
            self_production_cost_evaluator(reactionID[0])
        cur.execute('END TRANSACTION;')


def fetch_market_history():
"""
fetch_market_history

Queries the market_history infomation from the API. Stores it in the market_history table.
Only active for The Forge

:param cur: cursor for the sqlite database
"""
    cur.execute(''' SELECT materialTypeID
                    FROM reaction_materials
                    UNION
                    SELECT productTypeID
                    FROM reaction_products;''')
    reaction_types = cur.fetchall()
    print('fetching market history')
    operations = []
    #regions = [10000002, 10000042, 10000043, 10000032]
    #for region in regions:
    for input_id in reaction_types:
        operations.append(
            api.app.op['get_markets_region_id_history'](
                region_id=10000002,
                type_id=input_id[0],
            ) 
        )
        
    results = api.client.multi_request(operations)
    cur.execute('DELETE FROM market_history;')
    cur.execute('BEGIN TRANSACTION;')
    for operation in operations:
        for response in operation[1].data:
            # print(operation[0].query[1])
            # print(response)
            cur.execute(''' INSERT INTO market_history (
                            average,
                            history_date,
                            highest,
                            lowest,
                            order_count,
                            volume,
                            type_id)
                            VALUES (?,DATE(?),?,?,?,?,?);''',(
                        response['average'],
                        str(response['date']),
                        response['highest'],
                        response['lowest'],
                        response['order_count'],
                        response['volume'],
                        operation[0].query[1][1])
                        )
            
          
            
    cur.execute('END TRANSACTION;')



def evaluate_sell_price(product_id):
"""
evaluate_sell_price
"""
    cur.execute(''' SELECT price, volume_remain, rowid
                    FROM market_info
                    WHERE is_buy_order=1
                    AND type_id=?
                    ORDER BY price DESC;''', (product_id,))
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
    cur.execute('UPDATE reaction_items SET sell_cost=? WHERE type_id=?', (total_price, product_id))
   
def find_product_sell_prices():
    cur.execute('SELECT productTypeID FROM reaction_products;')
    products_query = cur.fetchall()
    
    cur.execute('BEGIN TRANSACTION;')
    for query in products_query:
        evaluate_sell_price(query[0])
    cur.execute('END TRANSACTION;')

def evaluate_reaction_margins():
    cur.execute('DELETE FROM reaction_margins;')
    cur.execute('SELECT productTypeID, quantity  FROM reaction_products;')
    products_query = cur.fetchall()

    cur.execute('BEGIN TRANSACTION;')
    for query in products_query:
        productID = query[0]
        product_count = query[1]
        cur.execute(''' SELECT production_cost, sell_cost
                        FROM reaction_items
                        WHERE type_id = ?;''', (productID,))
        cost_query = cur.fetchall()
        production_cost = cost_query[0][0]
        sell_cost = cost_query[0][1]
        margin = 0
        
        margin = sell_cost - production_cost
        
        cur.execute(''' INSERT INTO reaction_margins 
                        (product_type_id, obtain_price, sell_price, margin)
                        VALUES (?,?,?,?);''',
                        (productID, production_cost*product_count, sell_cost*product_count, margin*product_count))
    cur.execute('END TRANSACTION;')

def find_recipe(product_id):
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
    print(id_to_name(product_id), '\n')
    print('*--------------------------------------------------*')
    for material in materials:
        materialID = material[0]
        materialQuantity = material[1]

        cur.execute(''' SELECT production_cost, buy_cost
                        FROM reaction_items
                        WHERE type_id=?;''', (materialID,))
        mat_cost = cur.fetchall()
        material_production_cost = mat_cost[0][0]
        material_buy_cost = mat_cost[0][1]
        
        print(id_to_name(materialID), 'x' + str(materialQuantity), mat_cost)
        if (not always_buy) and (material_buy_cost is not None) and (material_production_cost is not None) and (material_production_cost < material_buy_cost):
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

                cur.execute(''' SELECT buy_cost
                                FROM reaction_items
                                WHERE type_id=?;''', (sub_materialID,))
                sub_mat_cost = cur.fetchall()
                sub_material_cost = sub_mat_cost[0][0]
                print('    ', id_to_name(sub_materialID), 'x' + str(sub_materialQuantity), sub_mat_cost)
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
        print(' ', id_to_name(item), 'x' + str(recipe[item]))
    print('')
    return recipe

def refresh_margin_display(top_margins):
    menu_index = 0
    for response in top_margins:
        product_type_id = response[0]
        margin = response[1]
        obtain_price = response[2]
        sell_price = response[3]
        print(str(menu_index+1) + ".)", display_num(margin) ,'with', id_to_name(product_type_id), display_num(sell_price) , '-', display_num(obtain_price), "ROI:", "%.2f"%((sell_price-obtain_price)/obtain_price*100) + "%")
        menu_index += 1
    return input('choice ("e" to exit): ')
    
def find_purchase_details(recipe, current_type_id):
    total_count = int(input('How many reactions will be taking place? '))
    print(recipe)
    volumes = {}
    volume_by_market = {}
    for material in recipe:
        print(' ', id_to_name(material), 'x', recipe[material]*total_count)
        cur.execute(''' SELECT volume
                        FROM SDE.invTypes
                        WHERE typeID=?''', (material,))
        volume = cur.fetchall()[0][0]
        print('   ', 'Volume:', volume)
        print('   ', 'Total Volume:', volume*recipe[material]*total_count)
        cur.execute(''' SELECT solarSystemName, SUM(price*volume_remain)/SUM(volume_remain), SUM(volume_remain), security
                        FROM market_info
                        JOIN SDE.mapSolarSystems ON system_id=solarSystemID
                        WHERE marked_for_buy=1
                        AND type_id=?
                        GROUP by system_id
                        ORDER BY SUM(price*volume_remain)/SUM(volume_remain) ASC''', (material,))
        markets = cur.fetchall()
        for market in markets:
            print('   ', market[0], market[1], 'isk', 'total available:', market[2])
            
        
            
    cur.execute(''' SELECT obtain_price, margin
                    FROM reaction_margins
                    WHERE product_type_id=?;''', (current_type_id,))
    query = cur.fetchall()
    input_isk = query[0][0]
    margin = query[0][1]
    
    total_input = input_isk*total_count
    total_net_profit = margin*total_count
    
    print('invested isk:', display_num(total_input))
    print('total profits:', display_num(total_net_profit))
    print('')
    return total_count
    
def display_top_margins():
    cur.execute(''' SELECT product_type_id, margin, obtain_price, sell_price
                    FROM reaction_margins
                    WHERE margin > 0
                    ORDER BY margin DESC;''')
    top_margins = cur.fetchall()

    response = refresh_margin_display(top_margins)

    while response != 'e':
        #try:
            response = int(response)
            response -= 1
            if response >= 0 and response < len(top_margins):
                print('Retrieving recipe for', id_to_name(top_margins[response][0]) + "." )
                print('')
                print('')
                recipe = find_recipe(top_margins[response][0])
                current_type_id = top_margins[response][0]
            else:
                print('Error: too high')
            response = input('choice ("e" to exit): ')
            if response == 'b':
                find_purchase_details(recipe, current_type_id)
                response = input('choice: ')
                continue
        #except: 
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
always_buy = 0
cur = initialize_database()

if __name__=="__main__":
    print('welcome to zombocom')
    
    fetch_market_data()
    # fetch_market_history()
    prepare_component_db()
    find_material_buy_prices()
    partition_and_evaluate_reaction_costs()
    find_product_sell_prices()
    evaluate_reaction_margins()
    display_top_margins()

    #print(results)