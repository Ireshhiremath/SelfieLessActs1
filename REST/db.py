import mysql.connector

mydb2 = mysql.connector.connect(host = "localhost", port = 3306, user = 'selflessact', password = 'password', auth_plugin = 'mysql_native_password')
mycursor2 = mydb2.cursor()
mycursor2.execute("DROP DATABASE IF EXISTS selflessacts1")
mycursor2.execute("CREATE DATABASE selflessacts1")
mydb1 = mysql.connector.connect(host = "localhost", port = 3306, user = 'selflessact', password = 'password', auth_plugin = 'mysql_native_password', database = 'selflessacts1')

mycursor1 = mydb1.cursor()
mycursor1.execute("""DROP TABLE IF EXISTS acts""")
mycursor1.execute("""DROP TABLE IF EXISTS users""")
mycursor1.execute("""DROP TABLE IF EXISTS category""")
mycursor1.execute("""CREATE TABLE users (username VARCHAR(100) PRIMARY KEY, passwd VARCHAR(50), fname VARCHAR(50), lname VARCHAR(50), email VARCHAR(50), phoneno VARCHAR(30), Gender char(1), Age integer, DoB DATE, BloodG VARCHAR(50), Address VARCHAR(300))""")
mycursor1.execute("""CREATE TABLE category (catno integer AUTO_INCREMENT PRIMARY KEY, catname VARCHAR(50))""")
mycursor1.execute("""CREATE TABLE acts (actid integer AUTO_INCREMENT PRIMARY KEY, votes integer, comments VARCHAR(300), caption VARCHAR(300), uname VARCHAR(100), catno1 INTEGER, imgpath VARCHAR(100), times DATETIME,  FOREIGN KEY(uname) REFERENCES users(username), FOREIGN KEY(catno1) REFERENCES category(catno))""")



