from plotly.offline import plot
import sqlite3
#import matplotlib.pyplot as plt
import datetime

conn = sqlite3.connect('finance.sqlite')
cur = conn.cursor()


#Matplotlib function
def MatPlot():
    cat_sql = "SELECT id, category FROM categories"
    print 'Categories:'
    for item in cur.execute(cat_sql):
        print item[0], item[1]
    cat = raw_input('Enter category: ')
    if cat == 'all':
        sql = "SELECT date, SUM(cost) FROM finance WHERE cat_id != 1 GROUP BY date"
    else:
        sql = "SELECT date, SUM(cost) FROM finance WHERE cat_id != 1 and cat_id = ( ? ) GROUP BY date"
    for x in cur.execute(sql, (cat,) ):
        dates.append(x[0])
    sums = [y[1] for y in cur.execute(sql, (cat,) )]

    dates = dates
    x = range(len(sums))
    y = sums
    plt.plot(x, y)
    plt.xticks(x, dates)
    plt.show()



def GraphAll():
    cat_sql = "SELECT id, category FROM categories"
    print 'Categories:'
    for item in cur.execute(cat_sql):
        print item[0], item[1]
    cat = raw_input('Enter category: ')
    if cat == 'all':
        #selects everything but income and sums each date
        sql = "SELECT date, SUM(cost) FROM finance WHERE cat_id != 1 GROUP BY date"
        date = [d[0] for d in cur.execute(sql)]
        sums = [i[1] for i in cur.execute(sql)]
    else:
        #selects individual categories and plots daily spending
        sql = "SELECT date, sum(cost) FROM finance WHERE cat_id = ( ? ) GROUP BY date"
        date = [d[0] for d in cur.execute(sql, (cat,) )]
        sums = [i[1] for i in cur.execute(sql, (cat,) )]
    plot([{"x": date, "y": sums}])

    
def GraphByDate():
    cat_sql = "SELECT id, category FROM categories"
    print 'Categories:'
    for item in cur.execute(cat_sql):
        print item[0], item[1]
    usrDate = raw_input('Enter date MDY: ')
    usrAdd = int(raw_input('Enter Days: '))
    fd = datetime.datetime.strptime(usrDate, "%m%d%y").date()
    dateadd = fd + datetime.timedelta(days=usrAdd)    
    cat = raw_input('Enter category: ')
    if cat == 'all':
        sql = "SELECT date, SUM(cost) FROM Finance WHERE cat_id != 1 AND date BETWEEN (?) AND (?) GROUP BY date"
        date = [d[0] for d in cur.execute(sql, (fd, dateadd) )]
        sums = [i[1] for i in cur.execute(sql, (fd, dateadd) )]
    else:
        sql = "SELECT date, cost FROM Finance WHERE cat_id = ( ? ) AND date BETWEEN (?) AND (?)"
        date = [d[0] for d in cur.execute(sql, (cat, fd, dateadd) )]
        sums = [i[1] for i in cur.execute(sql, (cat, fd, dateadd) )]
    
    plot([{"x": date, "y": sums}])
    
def GraphByItem():
    ex_sql = "SELECT item, sum(cost) FROM Finance GROUP BY item"
    item = [i[0] for i in cur.execute(ex_sql)]
    cost = [i[1] for i in cur.execute(ex_sql)]
    
    plot([{"x": item, "y": cost}])
    
def GraphByCategory():
    ex_sql = '''SELECT Categories.category, sum(Finance.cost) FROM Finance JOIN Categories
                ON Finance.cat_id = Categories.id GROUP BY Finance.cat_id'''
    category = [i[0] for i in cur.execute(ex_sql)]
    cost = [i[1] for i in cur.execute(ex_sql)]
    
    plot([{"x": category, "y": cost}])

print '''Choose one of the following:
         1. Graph by category
         2. Graph all 
         3. Graph by date
         4. Graph by item'''
         

prompt = raw_input('Enter r: ')
while prompt == "r":
    action = raw_input('Execute: ')
    if action == '1':
        GraphByCategory()
    elif action == '2':   
        GraphAll()
    elif action == '3':
        GraphByDate()    
    elif action == '4': 
        GraphByItem() 
    else:
        print 'Goodbye!'
        break