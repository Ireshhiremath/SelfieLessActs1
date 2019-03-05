import mysql.connector

mydb2 = mysql.connector.connect(host = "localhost", port = 3306, user = 'root', password = 'Dell.N5559', auth_plugin = 'mysql_native_password')
mycursor2 = mydb2.cursor()
mycursor2.execute("DROP DATABASE IF EXISTS selflessacts2")
mycursor2.execute("CREATE DATABASE selflessacts2")
mydb1 = mysql.connector.connect(host = "localhost", port = 3306, user = 'root', password = 'Dell.N5559', auth_plugin = 'mysql_native_password', database = 'selflessacts2')

mycursor1 = mydb1.cursor()
mycursor1.execute("""DROP TABLE IF EXISTS acts""")
mycursor1.execute("""DROP TABLE IF EXISTS users""")
mycursor1.execute("""DROP TABLE IF EXISTS category""")
mycursor1.execute("""CREATE TABLE users (username VARCHAR(100) PRIMARY KEY, password VARCHAR(50))""")
mycursor1.execute("""CREATE TABLE category (catno integer AUTO_INCREMENT PRIMARY KEY, categoryName VARCHAR(50))""")
mycursor1.execute("""CREATE TABLE acts (actid integer AUTO_INCREMENT PRIMARY KEY, votes integer DEFAULT 0, comments VARCHAR(300), caption VARCHAR(300), username VARCHAR(100), catno1 INTEGER, imgB64 BLOB, timestamp DATETIME,  FOREIGN KEY(username) REFERENCES users(username), FOREIGN KEY(catno1) REFERENCES category(catno))""")


