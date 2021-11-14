import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Jubilant9828!",

)

my_cursor = mydb.cursor()

my_cursor.execute("USE enable-ninja SHOW TABLES")
for db in my_cursor:
    print(db)