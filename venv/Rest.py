from flask import request
from flask_restful import Resource, Api, Resource, fields
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
from http import HTTPStatus

db_connect = create_engine('sqlite:///C:/sqlite3/Flights_db.db')

class Greet(Resource):
    def get(self):
        return {'message': 'Hello, Welcome to flight restful API. XML and JSON headers.'}

class Airlines(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM airlines;")
        result = {'Airlines': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        airline_Id = request.json['AIRLINE_ID']
        airline = request.json['AIRLINE']
        query = conn.execute("insert into airlines values('{0}', '{1}')".format(airline_Id, airline))
        return {'status' : 'success'}

class Updates(Resource):
    def put(self, AIRLINE_ID):
        conn = db_connect.connect()
        # airline_Id = request.json['AIRLINE_ID']
        # airline = request.json['AIRLINE']
        query = "UPDATE airlines SET airline=%s WHERE airline_id =%s"
        data = (_airline, _airline_Id)
        # %str(airline_Id).format(airline))
        conn.execute(query, data)
        return {"Good" : 'success'}

        # TODO: make sure to fix  Updates

class Delete(Resource):
    def delete(self, AIRLINE_ID):
        conn = db_connect.connect()
        query = conn.execute("DELETE FROM airlines WHERE AIRLINE_ID='{0}' ".format(AIRLINE_ID))
        resp = jsonify('Deleted successfully!')
        resp.status_code = 200
        return resp



class Airports(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT airport_id, airport_name, city, country, latitude, longitude FROM airports;")
        result = {'Airports': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result