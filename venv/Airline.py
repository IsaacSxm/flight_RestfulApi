from flask import request, Response
from flask_restful import Resource, Api, Resource, fields
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
from http import HTTPStatus
from flask_expects_json import expects_json
import xml.etree.ElementTree as ET

db_connect = create_engine('sqlite:///C:/sqlite3/Flights_db.db')

schema = {
         "type": "object",
         "properties": {
             "airline_id": {
                 "description": "This is a unique identifier for the name of the airline",
                 "type": "string",
                 "minLength": 2,
                 "maxLength": 2
             },
             "airline": {
                 "description": "This is the name of the airline",
                 "type": "string"
             }
         },
         "required": ["airline_id", "airline"]
     }

class Greet(Resource):
    def get(self):
        return {'message': 'Hello, Welcome to flight restful API. XML and JSON headers.'}

class Airlines(Resource):
    def get(self):
        conn = db_connect.connect()
        try:
            query = conn.execute("SELECT * FROM airlines;")
            result = {'Airlines': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return result
        except Exception as e:
            return {'Error' : 'Could not perform GET request'}


    # @expects_json(schema)
    def post(self):
        conn = db_connect.connect()
        if "application/json" in request.headers["Content-Type"]:
            print(request.json)
            airline_Id = request.json['airline_id']
            airline = request.json['airline']
            query = conn.execute("insert into airlines values('{0}', '{1}')".format(airline_Id, airline))
            return {'status': 'success'}

        # elif "application/xml" in request.xml["Content-Type"]:




        # except Exception as e:
        #     return {'Error' : "Could not perform POST"}


class Updates(Resource):
    @expects_json(schema)
    def put(self, AIRLINE_ID):
        conn = db_connect.connect()
        try:
            airline = request.json['airline']
            query = "UPDATE airlines SET airline='{1}' WHERE airline_id ='{0}'".format(AIRLINE_ID, airline)
            conn.execute(query)
            return {"Good": 'success'}
        except Exception as e:
            return {'Error' : "Could not UPDATE"}


class Delete(Resource):
    def delete(self, AIRLINE_ID):
        conn = db_connect.connect()
        try:
            query = conn.execute("DELETE FROM airlines WHERE airline_id='{0}' ".format(AIRLINE_ID))
            # resp = 'Deleted successfully!!'
            # resp.status_code = 200
            return {"Status": 'Deleted successfully!!'}
        except Exception as e:
            return {'Error' : "Could not perform DELETE"}

