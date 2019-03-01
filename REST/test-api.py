
from flask import Flask, request, jsonify,json
import pymysql
import time
import base64

app = Flask(__name__)
con=pymysql.connect(host="localhost", user="root", password="sagar", db="test",
 cursorclass=pymysql.cursors.DictCursor)
cur=con.cursor()

@app.route('/api/v1/users', methods=['POST'])
def add_user():
    data=request.get_json()

    usn=data['username']

    pwd=data['password']
    def is_sha1(pwd_str):
    	if len(pwd_str) != 40:
    		return False
    	try:
    		sha_int = int(pwd_str, 16)
    	except ValueError:
    		return False
    	return True
    cur.execute("SELECT COUNT(*) FROM users where usn=%s", usn)
    n=cur.fetchone()['COUNT(*)']
    if(is_sha1(pwd) and n==0):
    	query = ("INSERT INTO users VALUES (%s, %s)")
    	input_data=(usn, pwd)
    	cur.execute(query, input_data)
    	con.commit()
    	response = app.response_class(response=json.dumps({}),
                                  status=201,
                                  mimetype='application/json')
    elif(n!=0 or not(is_sha1(pwd))):
    	response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
    return response
     

@app.route('/api/v1/users/<usn>', methods=['DELETE'])
def rem_user(usn):
	cur.execute("SELECT COUNT(*) FROM users where usn=%s", usn)
	n=cur.fetchone()['COUNT(*)']
	if(n==0):
		response = app.response_class(response=json.dumps({}),
                                  status=405,
                                  mimetype='application/json')
	else:
		cur.execute("DELETE FROM users where usn=%s", usn)
		response = app.response_class(response=json.dumps({}),
                                  status=200,
                                  mimetype='application/json')
		con.commit()
	return response


@app.route('/api/v1/categories', methods=['GET'])
def list_categories():
	cur.execute("SELECT * FROM users")
	res=cur.fetchall()
	ret=dict()
	for row in res:
		ret[row['username']]=row['password']
	return jsonify(ret)

@app.route('/api/v1/categories', methods=['POST'])
def add_category():
	data=request.get_json()
	for category in data:
		cur.execute("SELECT COUNT(*) FROM categories where category=%s", category)
		n=cur.fetchone()['COUNT(*)']
		if(n==0):
			query = ("INSERT INTO categories VALUES (%s)")
			input_data=(category)
			cur.execute(query, input_data)
			con.commit()
			response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
		elif(n!=0):
			response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
	
	return response

@app.route('/api/v1/acts', methods=['POST'])
def upload_act():
	data=request.get_json()
	
	try:
		time.strptime(data['timestamp'], '%d-%m-%Y %S-%M-%H')
	except ValueError:
		response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
		print("alan0")
		return response
	
	cur.execute("SELECT COUNT(*) FROM acts where actId=(%s)", data['actId'])
	n=cur.fetchone()['COUNT(*)']
	if(n!=0):
		response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
		print("alan1")
		return response

	cur.execute("SELECT COUNT(*) FROM users where usn=(%s)", data['username'])
	n=cur.fetchone()['COUNT(*)']
	if(n==0):
		response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
		print("alan2")
		return response

	def isBase64(s):
		try:
			return base64.b64encode(base64.b64decode(s)) == s
		except Exception:
			return False
	"""
	if(not isBase64(data['imgB64'])):
		response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
		print("alan3")
		return response
	"""
	if(len(data)!=6):
		response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
		print("alan4")
		return response

	cur.execute("SELECT COUNT(*) FROM categories WHERE category=(%s)", data['categoryName'])
	n=cur.fetchone()['COUNT(*)']
	if(n==0):
		response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
		print("alan5")
		return response
	
	query = ("INSERT INTO acts VALUES (%s,%s,%Y-%m-%d %H:%M:%S,%s,%s,%s,%d)")
	"""
	query = ("INSERT INTO acts VALUES (%s,%s,'1970-01-02 00:02:00',%s,%s,%s,0)")
	"""

	d=data['timestamp'][0:2]
	m=data['timestamp'][3:5]
	y=data['timestamp'][6:10]
	s=data['timestamp'][11:13]
	mi=data['timestamp'][14:16]
	h=data['timestamp'][17:19]
	input_data=(data['actId'], data['username'],y,m,d,h,mi,s  ,data['caption'], data['categoryName'], data['imgB64'],"0")
	cur.execute(query, input_data)
	con.commit()
	response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
	return response


if __name__ == '__main__':
	app.run(host='127.0.0.1' , port=5000)
