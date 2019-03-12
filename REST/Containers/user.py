from flask import Flask, request, json, jsonify
import mysql.connector
#import hashlib
import time
#import base64




#SHA1 : The 160 bit hash function that resembles MD5 hash in working and was discontinued to be used seeing its security vulnerabilities.
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Selflessact'

mydb = mysql.connector.connect(host = "localhost", port = 3306, user = 'root', password = 'sagar', auth_plugin = 'mysql_native_password', database = 'selflessacts2')
mycursor = mydb.cursor()


#Add user
@app.route('/api/v1/users', methods = ['POST'])
def adduser():
    if request.method == 'POST':
        content = request.get_json()
        if(content):
            uname = content['username']
            uname1 = str(uname)
            pass0 =  content['password']
            #pass1 = hashlib.sha1(pass0.encode()).hexdigest()

            sql = "SELECT username FROM users Where username = %s"
            rows = mycursor.execute(sql, (uname1, ))
            rows = mycursor.fetchone()
            jsonify(rows)
            if(rows):
               flg=0
               for i in range(len(rows[0])):
                  if((rows[0])[i]!=uname[i]):
                     flg=1
                     break
               if (flg==0):
                  #user already exist
                  response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')

            else:
                query = "INSERT INTO users (username, password) VALUES(%s,%s)"
                iodata = (uname1,pass0)
                mycursor.execute(query, (iodata))
                mydb.commit()
                response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
                    #user created
        else:
            response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')

    else:
        #return render_template('Index.html'), 405
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response



#Remove User
@app.route('/api/v1/users/<username>', methods = ['DELETE'])
def removeuser(username):
    if request.method == 'DELETE':
        if(username):
            mycursor.execute("""SELECT username FROM users where username = %s""", (username, ))
            n = mycursor.fetchone()
            jsonify(n)
            if(n):
                    flg=0
                    for i in range(len(n[0])):
                        if((n[0])[i]!=username[i]):
                            flg=1
                            break
                    if (flg==0):
                        #user exist - will be deleted
                        mycursor.execute("DELETE FROM acts where username = %s", (username, ))
                        mycursor.execute("DELETE FROM users where username = %s", (username, ))
                        mydb.commit()
                        #return render_template('Index.html'), 200
                        response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
            else:
                #user doesn't exist
                response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
            #return render_template('Index.html'), 200
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
#list all users
@app.route('/api/v1/users',method=['GET'])
def listallusers():
    if request.method=='GET':
        list=mycursor.execute("SELECT * users.username FROM users ")
        list=mycursor.fetchall()
        if(list):
            response=app.response_class(response=json.dumps({'':list}),status=200,mimetype='application/json')
        else:
            response=app.response_class(response=json.dumps({}),status=204,mimetype='application/json')
    else:
        response=app.response_class(response=json.dumps({}),status=405,mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 80)
