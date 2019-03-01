from flask import Flask, render_template, request, json, jsonify
import mysql.connector
import hashlib

#SHA1 : The 160 bit hash function that resembles MD5 hash in working and was discontinued to be used seeing its security vulnerabilities.
app = Flask(__name__, static_url_path='/static')

mydb = mysql.connector.connect(host = "localhost", port = 3306, user = 'root', password = 'sagar', auth_plugin = 'mysql_native_password', database = 'test')
mycursor = mydb.cursor()

#Home page
@app.route('/')
def index():
    return render_template('Index.html'), 200

#Add user
@app.route('/api/v1/users', methods = ['POST'])
def adduser():
    if request.method == 'POST':
        content = request.get_json()
        uname = content['username']
        uname1 = str(uname) 
        pass0 =  content['password']
        pass1 = hashlib.sha1(pass0.encode())
        pass2 = str(pass1)
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
                #return render_template('Index.html'), 405
                response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
                
        else:
            query = "INSERT INTO users (username, password) VALUES(%s,%s)"
            iodata = (uname1,pass2)
            mycursor.execute(query, (iodata))
            mydb.commit()
            response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
            #return render_template('Index.html'), 201
            #user created              
            
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
                        #mycursor.execute("DELETE FROM acts where uname = %s", (username, ))
                        mycursor.execute("DELETE FROM users where username = %s", (username, ))
                        mydb.commit()
                        #return render_template('Index.html'), 200
                        response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
            else:
                #user doesn't exist
                response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')     
            return response
            #return render_template('Index.html'), 200
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')        

#list all categories
@app.route('/api/v1/categories', methods = ['GET'])
def listallcat():
    if request.method == 'GET':
        #cat = mycursor.execute("SELECT category.catname, COUNT(acts.actid) FROM acts,category Group By acts.catno1")
        cat = mycursor.execute("SELECT catname FROM category")
        cat = mycursor.fetchall()
        if(cat):
            return jsonify(cat),200
            '''
            cat1 = {}
            for row in cat
                for key in cursor.description
                    cat1.append({key[0]: value for value in row})
            '''
            #return render_template('Signup.html'), 200 #204
        else:  
            response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
            #return render_template('Signup.html'), 200 #204
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response            

#Add a category
@app.route('/api/v1/categories', methods = ['POST'])
def addcat():
    if request.method == 'POST':
        content = request.get_json()
        cat = content['categoryName']
        cat3 = "INSERT INTO category (catname) VALUES(%s)"
        mycursor.execute(cat3, (cat, ))
        mydb.commit()
        response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
        #return render_template('Signup.html'), 201
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response         

#Remove a category
@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def removeacat(categoryName):
    if request.method == 'DELETE':
        if(categoryName):
            mycursor.execute("SELECT catname FROM category where catname = %s", (categoryName, ))
            n = mycursor.fetchone()
            jsonify(n)
            if(n):
                flg=0
                for i in range(len(n[0])):
                    if((n[0])[i]!=categoryName[i]):
                        flg=1
                        break
                if(flg==0):
                    cat = mycursor.execute("SELECT catno FROM category where catname = %s", (categoryName, ))
                    cat = mycursor.fetchall()
                    #jsonify(cat)
                    mycursor.execute("DELETE FROM acts where catno1 in (Select catno From category WHERE catname = %s)", (categoryName, ))
                    mycursor.execute("DELETE FROM category where catname = %s", (categoryName, ))
                    
                    mydb.commit()
                    response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
                    #return render_template('Signup.html'), 201
            else:
    
                response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')                
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response    
    #return render_template('Signup.html'), 200

#List acts of categories(<100)
@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def listactscat(categoryName):
    if request.method == 'GET':
        if(categoryName):
            cat3 = mycursor.execute("SELECT * FROM acts,category WHERE acts.catno1 = category.catno AND category.catname = %s ORDER BY times DESC", (categoryName, ))
            cat3 = mycursor.fetchall()
            #jsonify(cat3)
            #print(cat3)
            if(cat3):
                cat4 = mycursor.execute("SELECT COUNT(*) FROM acts,category WHERE acts.catno1 = category.catno AND category.catname = %s ", (categoryName, ))
                cat4 = mycursor.fetchone()
                if(cat4[0] > 100):                          ##Error
                    response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
                else:    
                    cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat3]        
                    response = app.response_class(response=json.dumps({'':cat1}), status=200, mimetype='application/json')
                    #return render_template('Signup.html'), 200 #204
            else:  
                response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                #return render_template('Signup.html'), 200 #204
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response 
    #return render_template('Signup.html'), 200 #204,413

#list # acts of a category
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def listnoactscat(categoryName):
    if request.method == 'GET':
        if(categoryName):
            mycursor.execute("SELECT category.catname, COUNT(acts.actid) FROM acts,category WHERE category.catname = %s Group By acts.catno1", (categoryName, ))
            cat8 = mycursor.fetchall()
            if(cat8):
                return cat8
                cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat8]
                response = app.response_class(response=json.dumps({'':cat1}), status=200, mimetype='application/json')
                #return render_template('Signup.html'), 200 #204
            else:  
                response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                #return render_template('Signup.html'), 200 #204
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 200 #204

#return # acts for a category in given range
@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', methods = ['GET'])

def noactcatrange(categoryName):
    if request.method == 'GET':
        startRange = request.args['start']
        endRange = request.args['end']
        #startRange = int(startRange)
        #endRange = int(endRange)
        print('HI')
        if(categoryName, (startRange >= 1), endRange):
            cnt = mycursor.execute("SELECT COUNT(*) FROM acts WHERE acts.catno1 = category.catno AND category.catname = %s", (categoryName, ))
            cnt = mycursor.fetchone()
            #cnt = jsonify(cnt)
            if(cnt[0] <= endRange):
                cat6 = mycursor.execute("SELECT * FROM acts WHERE acts.catno1 = category.catno AND category.catname = %s GROUP BY catno1 HAVING COUNT(*) >= %s AND COUNT(*) <= %s ORDER BY times DESC", (categoryName, startRange, endRange, ))
                cat6 = mycursor.fetchall()
                if(cat6):   
                    cat7 = [dict(zip([key1[0] for key1 in mycursor.description], row1)) for row1 in cat6]        
                    response = app.response_class(response=json.dumps({'':cat7}), status=200, mimetype='application/json')
                        #return render_template('Signup.html'), 200 #204
                else:  
                    response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                    #return render_template('Signup.html'), 200 #204
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 200 #204,413

#Upvote an Act
@app.route('/api/v1/acts/upvote', methods = ['POST'])
def upvoteact():
    if request.method == 'POST':
        content1 = request.get_json()
        actid = int(content1['actid'])
        mycursor.execute("SELECT votes FROM acts WHERE actid = %s", (actid, ))
        n = mycursor.fetchone()
        if(n):
            votes = n[0] + 1
            votes = int(votes)
            cat4 = "UPDATE acts SET votes = %s WHERE actid = %s"
            mycursor.execute(cat4, (votes, actid, ))
            mydb.commit()
            response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
        else:
            response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
           
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response    

#Remove an act
@app.route('/api/v1/acts/<actid>', methods = ['DELETE'])
def removeact(actid):
    if request.method == 'DELETE':
        actid = int(actid)
        mycursor.execute("SELECT actid FROM acts WHERE actid = %s", (actid, ))
        id = mycursor.fetchone()
        
        if(id[0] == actid):
            mycursor.execute("DELETE FROM acts where actid = %s", (actid, ))
            mydb.commit()
            response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
        else:
            response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
           
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 200

#Upload an Act
@app.route('/api/v1/acts', methods = ['POST'])
def uploadact():
    if request.method == 'POST':
        content = request.get_json()
        cat = content['categoryName']
        
        cat3 = "INSERT INTO acts (votes,comments,caption,uname,catno1,imgpath,times) VALUES(%s)"
        #mycursor.execute(cat3, (0, '',caption,,cat6,'',''))
        #mydb.commit()
        response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
        #return render_template('Signup.html'), 201
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 201




if __name__ == '__main__':
    app.run(host='127.0.0.1', port= 5000)
  
