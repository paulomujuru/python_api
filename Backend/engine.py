#!/usr/bin/python

"""
Import the needed Python3 packages

"""
from functools import wraps
from secrets import config, db, host, pwd, user

import mysql.connector
from cryptography.fernet import Fernet
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

"""

backend = Define the Flask variable
api = Assign the Flask server as the main endpoint for the API
key = Random byte string
cipher_suite = Fernet is an implementation of symmetric (also known as “secret key”) authenticated cryptography

"""
backend = Flask(__name__)
api = Api(backend)
key = Fernet.generate_key()
cipher_suite = Fernet(key)


"""
Function to Encrypt the User's Password
ciphered_text = In order to encrypt the password, it first needs to be converted to bytes
                Then decode the response and return the encrypted password as String
"""


def encrypted(password):
    ciphered_text = cipher_suite.encrypt(bytes(password, encoding='utf8')).decode("utf-8")
    return ciphered_text


"""
Function to Decrypt the User's Password
uncipher_text = In order to decrypt the password, it first needs to be converted to bytes
                Then decode the response and return the encrypted password as String
"""


def decrypted(password):
    uncipher_text = cipher_suite.decrypt(bytes(password, encoding='utf8')).decode("utf-8")
    return uncipher_text


"""
Construct a decorator for Basic Authentication

auth = Using the request package from Flask we request for authorization
sql = Create the MySQL query
mydb = Use mysql-connector to connect to the database using the config variable defined in the secrets.py 
data = After the query executes fetch the response and return it
if the password passed in using Basic Authentication machtes the user's decrypted password in the database and return Login Successful
else return Login in Required
"""


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        sql = f"SELECT username, password FROM user_login where username='{auth.username}';"
        mydb = mysql.connector.connect(**config)
        mycursor = mydb.cursor()
        mycursor
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        if auth and decrypted(data[0][1]) == auth.password:
            return f(*args, **kwargs)
        return make_response('User not logged in!', 401, {'WWW-Authenicate': 'Basic realm="Login Required"'})
    return decorated 


"""
@auth_required = Apply Basic Autentication to this function

parser = Enables adding and parsing of multiple arguments in the context of a single request
args = Parse the arugment from the request

"""


class Login(Resource):
    @auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str,
                            required=True, help="Username Required!")
        parser.add_argument("password", type=str,
                            required=True, help="Password Required!")
        args = parser.parse_args()
        _username = args["username"]
        _password = args["password"]
        try:
            sql = f"SELECT username, password FROM user_login where username='{_username}';"
            mydb = mysql.connector.connect(**config)
            mycursor = mydb.cursor()
            mycursor
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            if decrypted(data[0][1]) == _password:
                return {"Message": "Login Successful"}, 200
            else:
                return {
                    "message": "Login failed username or password is incorrect."
                }
        except Exception as error:
            return {"error": str(error)}


class Registery(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str,
                            required=True, help="Username Required!")
        parser.add_argument("password", type=str,
                            required=True, help="Password Required!")
        args = parser.parse_args()
        _username = args["username"]
        _password = args["password"]
        sql = f"INSERT INTO user_login (username, password) VALUES {_username, encrypted(_password)}"
        try:
            mydb = mysql.connector.connect(**config)
            mycursor = mydb.cursor()
            mycursor
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()
            return {"Message": "User Registered Successfully",
            "data": {
                "username": _username,
                "password": encrypted(_password)
            }}, 200
        except Exception as error:
            return {"error": str(error)}


class SearchProfiles(Resource):
    def get(self):
        users = {}
        sql = f"SELECT * FROM user_profiles;"
        mydb = mysql.connector.connect(**config)
        mycursor = mydb.cursor()
        mycursor
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        return data

    @auth_required
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("profileid", type=str,
                                required=True, help="profileid is required!")
            args = parser.parse_args()
            _profileid = args["profileid"]
            sql = f"SELECT name, age, favourite_color, favourite_OS from user_profiles where profileid={_profileid};"
            mydb = mysql.connector.connect(**config)
            mycursor = mydb.cursor()
            mycursor
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            return {"data": {
                "name": data[0][0],
                "age": data[0][1],
                "favourite_color": data[0][2],
                "favourite_OS": data[0][3]
            }}
        except Exception as error:
            return {"error": str(error)}


class CreateProfile(Resource):

    @auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True,
                            help="name is required")
        parser.add_argument("age", type=str, required=True,
                            help="age is required")
        parser.add_argument("favourite_color", type=str,
                            required=True, help="favourite_color is required")
        parser.add_argument("favourite_OS", type=str,
                            required=True, help="favourite_OS is required")
        args = parser.parse_args()
        _name = args["name"]
        _age = args["age"]
        _favourite_color = args["favourite_color"]
        _favourite_OS = args["favourite_OS"]
        data = _name, _age, _favourite_color, _favourite_OS
        sql = f"INSERT INTO user_profiles (name, age, favourite_color, favourite_OS) VALUES {data}"
        try:
            mydb = mysql.connector.connect(**config)
            mycursor = mydb.cursor()
            mycursor
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()
            return {"data": data}, 200
        except Exception as error:
            return {"error": str(error)}

    @auth_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("profileid", type=str,
                            required=True, help="profileid is required")
        parser.add_argument("name", type=str, required=False)
        parser.add_argument("age", type=str, required=False)
        parser.add_argument("favourite_color", type=str, required=False)
        parser.add_argument("favourite_OS", type=str, required=False)
        args = parser.parse_args()
        _profileid = args["profileid"]
        _name = args["name"]
        _age = args["age"]
        _favourite_color = args["favourite_color"]
        _favourite_OS = args["favourite_OS"]
        data = _name, _age, _favourite_color, _favourite_OS
        sql = f"UPDATE user_profiles SET name={_name}, age={_age}, favourite_color={_favourite_color}, favourite_OS={_favourite_OS} WHERE profileid={_profileid}"
        try:
            mydb = mysql.connector.connect(**config)
            mycursor = mydb.cursor()
            mycursor
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()
            return {"message": "Profile update successfully"}, 200
        except Exception as error:
            return {"error": str(error)}

"""
Define the Endpoints
"""
api.add_resource(SearchProfiles, "/search/profiles")
api.add_resource(CreateProfile, "/edit/profiles")
api.add_resource(Registery, "/user/register")
api.add_resource(Login, "/user/login")

"""
Run a local instance of Flask
"""
backend.run(host="0.0.0.0", debug=True, port=80)
