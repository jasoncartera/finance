 #!/usr/bin/env python
 
import sqlite3
import datetime 
import calendar 

conn = sqlite3.connect('finance.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Finance (id INTEGER PRIMARY KEY, date DATE, time NUMERIC
             ,cost FLOAT, item TEXT, cat_id INTEGER, detail_id INTEGER, location_id INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Income (id INTEGER PRIMARY KEY, date DATE, time NUMERIC, value FLOAT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Rent (id INTEGER PRIMARY KEY, date DATE, time NUMERIC, value FLOAT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Categories (id INTEGER PRIMARY KEY, category TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Details (id INTEGER PRIMARY KEY, detail TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Location (id INTEGER PRIMARY KEY, location TEXT UNIQUE)''')

#code for listing each cat
#SELECT Finance.item, Finance.cost, Location.location FROM Finance JOIN Location on Finance.location_id = Location.id WHERE cat_id = 1

print("Enter read, write, income, or rent. \n \
If reading choose from: \n \
1. sum all \n \
2. print all \n \
3. sum dates \n \
4. sum by month \n \
5. print sum by dates \n \
6. sum by category \n \
7. sum all months")
    
prompt = input('>>> ')

def WriteIncome():
    time = str(datetime.datetime.now().time() )
    date = datetime.date.today()
    value = input('Enter Income: ').rstrip()
    cur.execute('''INSERT INTO Income (date, time, value) VALUES ( ?, ?, ? )''', (date, time, value) )
    conn.commit()
         
#write data 
def WriteData():         
    time = str( datetime.datetime.now().time() )
    date = datetime.date.today()
    item = input('Enter item: ').rstrip()
    if len(item) < 1:
        print("No item entered")
    else:
        cost = input('Enter amount of item: ')
        print([i for i in cur.execute('''SELECT location FROM Location''')])
        location = input('Enter location: ').rstrip()
        print([i for i in cur.execute('''SELECT category FROM Categories''')])
        cat = input('Enter category of item: ').rstrip()
        print([i for i in cur.execute('''SELECT detail FROM Details''')])
        detail = input('Enter detail: ').rstrip()
        
        cur.execute('''INSERT OR IGNORE INTO Categories (category) VALUES ( ? )''', ( cat,) )
        cur.execute('''INSERT OR IGNORE INTO Details (detail) VALUES ( ? )''', ( detail, ) )
        cur.execute('''INSERT OR IGNORE INTO Location (location) VALUES ( ? )''', (location, ) )
        cur.execute('''SELECT id FROM Categories WHERE category = ( ? )''', ( cat, ) )
        cat_id = cur.fetchone()[0]
        cur.execute('''SELECT id FROM Details WHERE detail = ( ? )''', ( detail, ) )
        detail_id = cur.fetchone()[0]
        cur.execute('''SELECT id FROM Location WHERE location = ( ? )''', (location, ) )
        location_id = cur.fetchone()[0]
        cur.execute('''INSERT INTO Finance (date, time, cost, item, cat_id, detail_id, location_id) VALUES ( ?, ?, ?, ?, ?, ?, ?)''', 
                    ( date, time, cost, item, cat_id, detail_id, location_id) )
              
        conn.commit()
            

#read functions
        
def SumAll():
    sql_total = cur.execute('SELECT sum(cost) FROM Finance')
    for i in sql_total:
        print('Total sum is: ',i[0])


def PrintAll():     
    sql_data = '''SELECT Finance.date, Finance.cost, Finance.item, Categories.category, Details.detail, Location.location
                    FROM Finance JOIN Categories JOIN Details JOIN Location ON Finance.cat_id = Categories.id AND Finance.detail_id = Details.id
                     Finance.location_id = Location.id  '''              
    for item in cur.execute(sql_data):
        print(item[0], '|', item[1], '|', item[2], '|', item[3], '|', item[4], '|', item[5], '|', item[6])


def PrintSumDates():
    sql = "SELECT date, SUM(cost) FROM finance GROUP BY date"
    for item in cur.execute(sql):
        print(item[0],':',item[1])
        
def SumByDates():
    usrDate = input('Enter date MDY: ')
    usrEnd = input('Enter date MDY: ')
    fd = datetime.datetime.strptime(usrDate, "%m%d%y").date()
    ed = datetime.datetime.strptime(usrEnd, "%m%d%y").date()
    spent_sql = "SELECT cost FROM Finance WHERE date BETWEEN (?) AND (?)"
    date_price = [t[0] for t in cur.execute(spent_sql, (fd, ed))]
    print('Total costs from',fd.strftime('%b %d'),'to',ed.strftime('%b %d')+':', sum(date_price))


def SumByMonth():
    yyyymm = input('Enter yyyymm: ')
    month_sql = '''SELECT Categories.category, SUM(Finance.cost) FROM Finance JOIN Categories ON Finance.cat_id = Categories.id 
                WHERE strftime('%Y%m',date) = ( ? ) GROUP BY cat_id'''
    sum_total = cur.execute(month_sql,(yyyymm,))
    cost_list = list()
    for category in sum_total:
        cost_list.append(category[1])
        print(category[0], category[1])
    print('Total sum for', yyyymm,'is', sum(cost_list))
  
def SumAllMonths():
    yyyy = input('Enter yyyy: ')
    sql = '''SELECT strftime('%m', date) as valMonth, 
    SUM(cost) as valTotalMonth 
    FROM Finance 
    WHERE strftime('%Y', date) = (?) GROUP BY valMonth'''
    for month in cur.execute(sql, (yyyy,)):
        print(month[0], month[1])

def SumByCategory():
    sql = "SELECT Categories.category, sum(Finance.cost) FROM Finance JOIN Categories ON Finance.cat_id = Categories.id GROUP BY cat_id"
    for item in cur.execute(sql):
        print(item[0],':',item[1])
    
while prompt == 'write':
    WriteData()
    prompt = input('Next action? ')
    if prompt == 'exit':
        break
    
while prompt == 'income':
    WriteIncome()
    prompt = input('Next action? ')
        
while prompt == 'read':
    action = input('Execute: ')
    if action == '1':
        SumAll()
    elif action == 'write':
        WriteData()
    elif action == '2':
        PrintAll()    
    elif action == '3': 
        SumByDates()
    elif action == '4':
        SumByMonth()
    elif action == '5':
        PrintSumDates()    
    elif action == '6':
        SumByCategory()
    elif action == '7':
        SumAllMonths()          
    else :        
        break

            
cur.close()
        
   








