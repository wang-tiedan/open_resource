import csv
import sqlite3

# open the connection to the database
# conn = sqlite3.connect('polar_bear_data.db')
conn = sqlite3.connect('Planning_Applications_Decisions.db')
cur = conn.cursor()

# drop the data from the table so that if we rerun the file, we don't repeat values
conn.execute('DROP TABLE IF EXISTS ID_table')
print("table dropped successfully")
# create table again
conn.execute('CREATE TABLE ID_table (Feature_ID varchar(255), DateCode varchar(255), Measurement varchar(255), Value INTEGER, by_Development_Type varchar(255))')
print("table created successfully")

conn.execute('DROP TABLE IF EXISTS category')
print("table dropped successfully")
# create the category table again  
conn.execute('CREATE TABLE category (ID INTEGER PRIMARY KEY AUTOINCREMENT, Feature_ID varchar(255), DateCode varchar(255), Value INTEGER, by_category varchar(255))')
print("table created successfully")
conn.commit()

# open the file to read it into the database
with open('open_resource_data/ID_table.csv', newline='') as f:
    reader = csv.reader(f, delimiter=",")
    next(reader) # skip the header line
    for row in reader:
        print(row)

        Feature_ID = row[0]
        DateCode = row[1]
        Measurement = row[2]
        Value = int(row[4])
        by_Development_Type = row[5]
      
        cur.execute('INSERT INTO ID_table VALUES (?,?,?,?,?)', (Feature_ID, DateCode, Measurement, Value, by_Development_Type))
        conn.commit()
print("data parsed successfully")

total_row = 0
success_row = 0
failed_row = 0
# open the file to read it into the database
with open('open_resource_data/category.csv', newline='') as f:
    reader = csv.reader(f, delimiter=",")
    next(reader) # skip the header line
    print('start to work on the category table')
    for row in reader:
        total_row += 1
        print(row)
        # check if the row starts with empty string (avoid reading empty lines after the data)
        if row[0]: 
            try:
              Feature_ID = row[1]
              print('Feature ID', Feature_ID)
              # link between two tables
              cur.execute('SELECT * from ID_table WHERE Feature_ID=?', (Feature_ID,))
              temp_row = cur.fetchall() #temp_row is a tuple, and not an array, so need first item from first item
              print('temp_row', temp_row)
              featured_ID = temp_row[0][0]
              print('featured_ID', featured_ID)
              DateCode = row[2]
              print('DateCode', DateCode)
              Value = int(row[5])
              print('Value', Value)
              by_category = row[6]
              print('by_category', by_category)

              # print(temperature)
              cur.execute('INSERT INTO category (Feature_ID, DateCode, Value, by_category) VALUES ( ?,?,?,?)', (featured_ID, DateCode, Value, by_category))
              conn.commit()
              success_row += 1
            except Exception as e: # if there are missing values, go to the next row
              # pass
              print("Exception occur, please check your datasets.")
              failed_row += 1
        else: # stop reading when reaching empty lines.
            break
            failed_row += 1


print("data parsed successfully")
print("Total: " + str(total_row))
print("success: " + str(success_row))
print("failed_row: " + str(failed_row))


conn.close()