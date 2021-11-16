from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

#Create an instance of Flask
app = Flask(__name__)

#Create an instance of MySQL
mysql = MySQL()

#Create an instance of Flask RESTful API
api = Api(app)

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
app.config['MYSQL_DATABASE_DB'] = 'teste'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#Initialize the MySQL extension
mysql.init_app(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/teste")
def hello2():
    return "Aqui e apenas um teste de get!"

@app.route("/teste1", methods=['POST'])
def insertUser():
    try:
        _name = request.json['name']
        _age = request.json['age']
        _city = request.json['city']

        print(_name)
        print(_age)
        print(_city)

        response = jsonify(name=_name, age=_age, city=_city, message='User printed successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Errp ao printar entrada')         
        response.status_code = 400 
    finally:
        return(response)

@app.route("/teste1",  methods=['GET'])    
def getAll():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""select * from otg_demo_users""")
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route("/teste1/<int:user_id>",  methods=['GET'])            
def getById(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select * from otg_demo_users where id = %s',user_id)
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()        

#Get All Users, or Create a new user
class UserList(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from otg_demo_users""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _name = request.json['name']
            _age = request.json['age']
            _city = request.json['city']
            insert_user_cmd = """INSERT INTO otg_demo_users(name, age, city) 
                                VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_name, _age, _city))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            response.status_code = 201
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)
            
#Get a user by id, update or delete user
class User(Resource):
    def get(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from otg_demo_users where id = %s',user_id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _name = request.form['name']
            _age = request.form['age']
            _city = request.form['city']
            update_user_cmd = """update otg_demo_users 
                                 set name=%s, age=%s, city=%s
                                 where id=%s"""
            cursor.execute(update_user_cmd, (_name, _age, _city, user_id))
            conn.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to update user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

    def delete(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from otg_demo_users where id = %s',user_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

#API resource routes
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/user/<int:user_id>', endpoint='user')

if __name__ == "__main__":
    app.run(debug=True)