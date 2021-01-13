from flask import request, Response
import requests
from flask_restful import Resource, Api, Resource
from sqlalchemy import create_engine
from flask_expects_json import expects_json
import xmltodict


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
            result = {'Airline': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return result
        except Exception as e:
            return {'Error' : 'Could not perform GET request'}


    def post(self):
        conn = db_connect.connect()
        if "application/json" in request.headers["Content-Type"]:
            try:
                @expects_json(schema)
                def post_(self):
                    for content in request.json:
                        airline_Id = request.json['airline_id']
                        airline = request.json['airline']
                        query = conn.execute("insert into airlines values('{0}', '{1}')".format(airline_Id, airline))
                        return {"Success" : "JSON content posted successfully"}
                post_(self)
                return {"Success": "JSON content POST successful"}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)

        else:
            try:
                xml_data = request.data
                content_xml = xmltodict.parse(xml_data)
                for content in content_xml:
                    airline_Id = content_xml['Airline']['AIRLINE_ID']
                    airline = content_xml['Airline']['AIRLINE']
                    query = conn.execute("insert into airlines values('{0}', '{1}')".format(airline_Id, airline))
                return {'Success' : 'POST xml content-type successful'}
            except requests.exceptions.HTTPError as e:
                raise SystemExit(e)


class UpdateAirline(Resource):

    def put(self, AIRLINE_ID):
        conn = db_connect.connect()
        if "application/json" in request.headers["Content-Type"]:
            try:
                @expects_json(schema)
                def put_(self):
                    for content in request.json:
                        airline = request.json['airline']
                        query = "UPDATE airlines SET airline='{1}' WHERE airline_id ='{0}'".format(AIRLINE_ID, airline)
                        conn.execute(query)
                        # return {"Good": 'success'}
                put_(self)
                return {"Success": 'JSON content-type POST successful'}
            except requests.exceptions.HTTPError as e:
                raise SystemExit(e)

        else:
            try:
                xml_data = request.data
                content_xml = xmltodict.parse(xml_data)
                for content in content_xml:
                    airline = content_xml['Airline']['AIRLINE']
                    query = conn.execute("UPDATE airlines SET airline='{1}' WHERE airline_id ='{0}' ".format(AIRLINE_ID, airline))
                return {'Success' : 'XML content-type UPDATE successful'}
            except requests.exceptions.HTTPError as e:
                raise SystemExit(e)


class DeleteAirline(Resource):
    def delete(self, AIRLINE_ID):
        conn = db_connect.connect()
        try:
            query = conn.execute("DELETE FROM airlines WHERE airline_id='{0}' ".format(AIRLINE_ID))
            return {"Status": 'Deleted successfully!!'}
        except Exception as e:
            return {'Error' : "Could not perform DELETE"}

