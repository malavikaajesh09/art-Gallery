import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", 
    database="art_gallery",
    port=3307

)

cursor = db.cursor()
# mysql -u root -p --port=3307