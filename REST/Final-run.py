from flask import Flask, request, json, jsonify
import mysql.connector
#import hashlib
import time
#import base64

#SHA1 : The 160 bit hash function that resembles MD5 hash in working and was discontinued to be used seeing its security vulnerabilities.
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Selflessact'

mydb = mysql.connector.connect(host = "localhost", port = 3306, user = 'root', password = 'root', auth_plugin = 'mysql_native_password', database = 'selflessacts3')
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

#Add a category
@app.route('/api/v1/categories', methods = ['POST'])
def addcat():
    if request.method == 'POST':
        content = request.get_json()
        #cat = str(cat[0])
	#print(cat)
        cat = content['categoryName']
	print(cat)        
	mycursor.execute("SELECT categoryName FROM category WHERE categoryName = %s", (cat, ))
        n = mycursor.fetchone()
        if(n):
            response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
        else:
            cat3 = "INSERT INTO category (categoryName) VALUES(%s)"
            mycursor.execute(cat3, (cat, ))
            mydb.commit()
            response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
            
        #return render_template('Signup.html'), 201
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response         



#list all categories
@app.route('/api/v1/categories', methods = ['GET'])
def listallcat():
    if request.method == 'GET':
        cat = mycursor.execute("SELECT category.categoryName FROM category ORDER BY category.categoryName")
        cat = mycursor.fetchall()
        if(cat):
            response = app.response_class(response=json.dumps({'':cat}), status=200, mimetype='application/json')
            #return render_template("home.html", listcat=cat)
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

#Remove a category
@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def removeacat(categoryName):
    if request.method == 'DELETE':
        if(categoryName):
            mycursor.execute("SELECT categoryName FROM category where categoryName = %s", (categoryName, ))
            n = mycursor.fetchone()
            jsonify(n)
	    print(n)
            if(n):
                flg=0
                for i in range(len(n[0])):
                    if((n[0])[i]!=categoryName[i]):
                        flg=1
                        break
                if(flg==0):
                    #cat = mycursor.execute("SELECT catno FROM category where catname = %s", (categoryName, ))
                    #cat = mycursor.fetchall()
                    #jsonify(cat)
                    mycursor.execute("DELETE FROM acts where catno1 in (Select catno From category WHERE categoryName = %s)", (categoryName, ))
                    mycursor.execute("DELETE FROM category where categoryName = %s", (categoryName, ))
                    
                    mydb.commit()
                    response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
                    #return render_template('Signup.html'), 201
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
        data=request.get_json()
        time1 = time.strptime(data['timestamp'], '%d-%m-%Y:%S-%M-%H')
        uname2 = data['username']
	comments = data['comments']
        actid = data['actid']
        caption = data['caption']
        catname = data['categoryName']
        imgB64 = data['imgB64']
        #image = request.files['imgB64']  
        #image_string = base64.b64encode(image.read())
        cat6 = mycursor.execute("SELECT catno FROM category WHERE categoryName = %s", (catname, ))
        cat6 = mycursor.fetchone()
        cat15 = mycursor.execute("SELECT username FROM users WHERE username = %s", (uname2, ))
        cat15 = mycursor.fetchone()
        if(cat6 is not None and cat15 is not None):
            cat12 = mycursor.execute("SELECT actid FROM acts WHERE actid = %s", (actid, ))
            cat12 = mycursor.fetchone()
            if(cat12 is None):
                cat3 = "INSERT INTO acts (actid,caption,comments,username,catno1,imgB64,timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(cat3, (int(actid),caption,comments,uname2,int(cat6[0]),imgB64,time1))
                mydb.commit()
                response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
                #return render_template('Signup.html'), 201
            else:
                response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
        else:
            response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 201




#List acts of categories(<100)
@app.route('/api/v1/categories/<categoryName>/acts/', methods = ['GET'])
def listactscat(categoryName):
    if request.method == 'GET':
        if(len(request.args)==0):
            if(categoryName):
                cat3 = mycursor.execute("SELECT actid, username, DATE_FORMAT(timestamp, '%d-%m-%Y:%S-%M-%H') as timestamp, caption, votes, CONVERT(imgB64 USING utf8) as imgB64 FROM acts,category WHERE acts.catno1 = category.catno AND category.categoryName = %s ORDER BY timestamp DESC", (categoryName, ))
                cat3 = mycursor.fetchall()
                #jsonify(cat3)
                #print(cat3)
                cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat3]
                if(cat3):
                    cat4 = mycursor.execute("SELECT COUNT(*) FROM acts,category WHERE acts.catno1 = category.catno AND category.categoryName = %s ", (categoryName, ))
                    cat4 = mycursor.fetchone()
                    if(cat4[0] > 100):                          ##Error
                        response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
                    else:    
                        #cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat3]        
                        response = app.response_class(response=json.dumps({'':cat1}), status=200, mimetype='application/json')
                        #return render_template('Signup.html'), 200 #204
                else:  
                    response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                    #return render_template('Signup.html'), 200 #204 
        else:
            startRange = request.args['start']
            endRange = request.args['end']
            if(categoryName, (int(startRange) >= 1), (int(endRange) <= 100)):
                cnt = mycursor.execute("SELECT COUNT(*) FROM acts,category WHERE acts.catno1 = category.catno AND category.categoryName = %s", (categoryName, ))
                cnt = mycursor.fetchone()
            #cnt = jsonify(cnt)
                if(cnt[0]!=0):
                    if((int(endRange) <= cnt[0])):
                        cat6 = mycursor.execute("SELECT actid, username, DATE_FORMAT(timestamp, '%d-%m-%Y:%S-%M-%H') as timestamp, caption, votes, CONVERT(imgB64 USING utf8) as imgB64 FROM acts,category WHERE category.catno = acts.catno1 AND category.categoryName = %s ORDER BY timestamp DESC", (categoryName, ))
                        cat6 = mycursor.fetchall()
                        if(cat6):
                            cat7 = [dict(zip([key1[0] for key1 in mycursor.description], row1)) for row1 in cat6]        
                            cat10=[]
                            for i in range((int(startRange)-1), (int(endRange))):
                                cat10.append(cat7[i]) 
                            response = app.response_class(response=json.dumps({'':cat10}), status=200, mimetype='application/json')
                            return response
                                    #return render_template('Signup.html'), 200 #204
                        else:  
                            response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
                            return response
                                #return render_template('Signup.html'), 200 #204
                    else:
                        response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
                        return response   ######
                else:
                    response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
            else:
                response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
                return response
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response 
    #return render_template('Signup.html'), 200 #204,413

#list # acts of a category
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def listnoactscat(categoryName):
    if request.method == 'GET':
        if(categoryName):
            mycursor.execute("SELECT COUNT(acts.actid) FROM acts,category WHERE acts.catno1=category.catno AND category.categoryName = %s", (categoryName, ))
            cat8 = mycursor.fetchall()
            if(cat8):
                response = app.response_class(response=json.dumps({'':cat8}), status=200, mimetype='application/json')
                #cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat8]
                #response = app.response_class(response=json.dumps({'':cat1}), status=200, mimetype='application/json')
                #return render_template('Signup.html'), 200 #204
            else:  
                response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                #return render_template('Signup.html'), 200 #204
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 200 #204

#return # acts for a category in given range
#@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])


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
        id1 = mycursor.fetchone()
        
        if(id1[0] == actid):
            mycursor.execute("DELETE FROM acts where actid = %s", (actid, ))
            mydb.commit()
            response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
        else:
            response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
           
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 200




if __name__ == '__main__':    
    app.run(host='127.0.0.1', port= 5000 , debug=True)
