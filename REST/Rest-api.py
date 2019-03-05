from flask import Flask, render_template, request, json, jsonify
import mysql.connector
import hashlib
import time
import base64

#SHA1 : The 160 bit hash function that resembles MD5 hash in working and was discontinued to be used seeing its security vulnerabilities.
app = Flask(__name__,template_folder='template')

mydb = mysql.connector.connect(host = "localhost", port = 3306, user = 'root', password = 'root', auth_plugin = 'mysql_native_password', database = 'selflessacts1')
mycursor = mydb.cursor()

#Home page
@app.route('/')
def index():
    #print("hello")
    return render_template('Index.html'), 200

#Add user
@app.route('/api/v1/users', methods = ['POST'])
def adduser():
    if request.method == 'POST':
        content = request.get_json()
        uname = content['username']
        uname1 = str(uname) 
        pass0 =  content['passwd']
        pass1 = hashlib.sha1(pass0.encode())
        #pass1 = sha1_crypt.encrypt(pass0)
        bg =  content['BloodG']
        email1 =  content['email']
        phono =  content['phoneno']
        gen =  content['Gender']
        dob =  content['DoB']
        age =  content['Age']
        fname1 =  content['fname']
        lname1 =  content['lname']
        add1 =  content['Address']         
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
            query = "INSERT INTO users(username, passwd, fname, lname, email, phoneno, Gender, Age, DoB, BloodG, Address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			
            iodata = (uname1,str(pass1),fname1,lname1,email1,phono,gen,age,dob,bg,add1)
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
                        mycursor.execute("DELETE FROM acts where uname = %s", (username, ))
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
        cat = content['catname']
        cat3 = "INSERT INTO category (catname) VALUES(%s)"
        mycursor.execute(cat3, (cat, ))
        mydb.commit()
        response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
        #return render_template('Signup.html'), 201
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response         

#Remove a category
@app.route('/api/v1/categories/<catname>', methods = ['DELETE'])
def removeacat(catname):
    if request.method == 'DELETE':
        if(catname):
            mycursor.execute("SELECT catname FROM category where catname = %s", (catname, ))
            n = mycursor.fetchone()
            jsonify(n)
            if(n):
                flg=0
                for i in range(len(n[0])):
                    if((n[0])[i]!=catname[i]):
                        flg=1
                        break
                if(flg==0):
                    cat = mycursor.execute("SELECT catno FROM category where catname = %s", (catname, ))
                    cat = mycursor.fetchall()
                    #jsonify(cat)
                    mycursor.execute("DELETE FROM acts where catno1 in (Select catno From category WHERE catname = %s)", (catname, ))
                    mycursor.execute("DELETE FROM category where catname = %s", (catname, ))
                    
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
@app.route('/api/v1/categories/<catname>/acts/', methods = ['GET'])
def listactscat(catname):
    if request.method == 'GET':
        if(catname):
            cat3 = mycursor.execute("SELECT * FROM acts,category WHERE acts.catno1 = category.catno AND category.catname = %s ORDER BY times DESC", (catname, ))
            cat3 = mycursor.fetchall()
            #jsonify(cat3)
            #print(cat3)
            cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat3]
	    print(cat1)
            if(cat3):
                cat4 = mycursor.execute("SELECT COUNT(*) FROM acts,category WHERE acts.catno1 = category.catno AND category.catname = %s ", (catname, ))
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
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response 
    #return render_template('Signup.html'), 200 #204,413

#list # acts of a category #work on this and
@app.route('/api/v1/categories/<catname>/acts/size', methods = ['GET'])
def listnoactscat(catname):
    if request.method == 'GET':
        if(catname):
            mycursor.execute("SELECT catname, COUNT(a.actid) as actids FROM acts as a,category WHERE catname = %s and a.catno1=catno Group By a.catno1", (catname, ))
            cat8 = mycursor.fetchall()
            if(cat8):
		cat1 = [dict(zip([key[0] for key in mycursor.description], row)) for row in cat8]
		#print(cat1)	
		#response = app.response_class(response=json.dumps({'':cat8}), status=200, mimetype='application/json')	
		response = app.response_class(response=json.dumps({'':cat1}), status=200, mimetype='application/json')
		#print(cat8)  		
		return response              
		#return render_template('Signup.html'), 200 #204
            else:  
                response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                #return render_template('Signup.html'), 200 #204 
    else:
        response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
    #return render_template('Signup.html'), 200 #204

#return # acts for a category in given range # This one
@app.route('/api/v1/categories/<catname>/acts', methods = ['GET'])
def noactcatrange(catname):
    if request.method == 'GET':
        startRange = request.args['start']
        endRange = request.args['end']
        #startRange = int(startRange)
        #endRange = int(endRange)
        if(catname, (int(startRange) >= 1), endRange):
            cnt = mycursor.execute("SELECT COUNT(*) FROM acts,category WHERE acts.catno1 = category.catno AND category.catname = %s", (catname, ))
            cnt = mycursor.fetchone()
            #cnt = jsonify(cnt)
            
            if((int(endRange) <= cnt[0])):
                cat6 = mycursor.execute("SELECT * FROM acts,category WHERE category.catno = acts.catno1 AND category.catname = %s ORDER BY times DESC", (catname, ))
                cat6 = mycursor.fetchall()
                if(cat6):
                    cat7 = [dict(zip([key1[0] for key1 in mycursor.description], row1)) for row1 in cat6]        
                    cat10=[]
                    for i in range((int(startRange)-1), (int(endRange))):
                        cat10.append(cat7[i]) 
                        print(cat7[i])
                    response = app.response_class(response=json.dumps({'':cat10}), status=200, mimetype='application/json')
                            #return render_template('Signup.html'), 200 #204
                else:  
                    response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json') 
                        #return render_template('Signup.html'), 200 #204
            else:
                response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
        else:
            response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')                
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
        data=request.get_json()
        time1 = time.strptime(data['time'], '%Y-%m-%d:%H-%M-%S')
	#print(time1)        
	uname2 = data['uname']
        actid = data['actid']
        caption = data['caption']
	comments = data['comments']
        catname = data['catname']
        imgB64 = data['image']
        #image = request.files['imgB64']  
        #image_string = base64.b64encode(image.read())
        cat6 = mycursor.execute("SELECT catno FROM category WHERE catname = %s", (catname, ))
        cat6 = mycursor.fetchone()
        if cat6 is not None :
            cat12 = mycursor.execute("SELECT actid FROM acts WHERE actid = %s", (actid, ))
            cat12 = mycursor.fetchone()
            if(cat12 is None):
                cat3 = "INSERT INTO acts (actid,caption,comments,uname,catno1,imgpath,times) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(cat3, (int(actid),str(caption),str(comments),str(uname2),int(cat6[0]),str(imgB64),time1))
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




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)
  
