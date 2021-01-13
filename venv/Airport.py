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
            "airport_id": {
                "description": "This is a unique identifier for the name of the airport",
                "type": "string",
                "minLength": 3,
                "maxLength": 3
            },
            "airport_name": {
                "description": "This is the internationally recognized name of the airport",
                "type": "string"
            },
             "city": {
                "description": "City where the airport is located",
                "type":"string",

            },
            "state": {
                "description": "State where the airport is located",
                "type": "string",
                "minLength": 2,
                "maxLength": 2
            },
            "country": {
                "description": "Country of the airport",
                "type": "string"
            },
            "latitude": {
                "description": "Geographical coordinate of the airport",
                "type": "number"
            },
            "longitude": {
                "description": "Geographical coordinate of the airport",
                "type": "number"
            }
        },
        "required": ["airport_id","airport_name", "city", "state", "country", "latitude", "longitude"]
}

class Airports(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM airports;")
        result = {'Airport': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result


    def post(self):
        conn = db_connect.connect()
        if "application/json" in request.headers["Content-Type"]:
            try:
                @expects_json(schema)
                def post_(self):
                    for content in request.json:
                        airport_id = request.json['airport_id']
                        airport_name = request.json['airport_name']
                        city = request.json['city']
                        state = request.json['state']
                        country = request.json['country']
                        latitude = request.json['latitude']
                        longitude = request.json['longitude']
                        query = conn.execute("insert into airports values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(airport_id, airport_name, city, state, country, latitude, longitude))
                        return {"Success" : "JSON content posted successfully"}
                post_(self)
                return {"Success" : "JSON content-type POST successfull"}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)

        else:
            try:
                xml_data = request.data
                content_xml = xmltodict.parse(xml_data)
                for content in content_xml:
                    airport_id = content_xml['Airports']['Airport']['AIRPORT_ID']
                    airport_name = content_xml['Airports']['Airport']['AIRPORT_NAME']
                    city = content_xml['Airports']['Airport']['CITY']
                    state = content_xml['Airports']['Airport']['STATE']
                    country = content_xml['Airports']['Airport']['COUNTRY']
                    latitude = content_xml['Airports']['Airport']['LATITUDE']
                    longitude = content_xml['Airports']['Airport']['LONGITUDE']
                    query = conn.execute("INSERT INTO airports values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(airport_id, airport_name, city, state, country, latitude, longitude))
                return {'Success' : 'XML content-type POST successful'}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)



class UpdateAirport(Resource):

    def put(self, AIRPORT_ID):
        conn = db_connect.connect()
        if "application/json" in request.headers["Content-Type"]:
            try:
                @expects_json(schema)
                def put_(self):
                    for content in request.json:
                        airport_name = request.json['airport_name']
                        city = request.json['city']
                        state = request.json['state']
                        country = request.json['country']
                        latitude = request.json['latitude']
                        longitude = request.json['longitude']
                        query = "UPDATE airports SET airport_name='{1}',city='{2}',state='{3}', country='{4}',latitude= '{5}',longitude= '{6}' WHERE airport_id = '{0}'".format(AIRPORT_ID, airport_name, city, state, country, latitude, longitude)
                        conn.execute(query)
                put_(self)
                return {'Suceess': 'JSON content-type UPDATE successful'}
            except requests.exceptions.HTTPError as e:
                return {SystemError(e)}

        else:
            try:
                xml_data = request.data
                content_xml = xmltodict.parse(xml_data)
                for content in content_xml:
                    airport_name = content_xml['Airports']['Airport']['AIRPORT_NAME']
                    city = content_xml['Airports']['Airport']['CITY']
                    state = content_xml['Airports']['Airport']['STATE']
                    country = content_xml['Airports']['Airport']['COUNTRY']
                    latitude = content_xml['Airports']['Airport']['LATITUDE']
                    longitude = content_xml['Airports']['Airport']['LONGITUDE']
                    query = "UPDATE airports SET airport_name='{1}',city='{2}',state='{3}', country='{4}',latitude= '{5}',longitude= '{6}' WHERE airport_id = '{0}'".format(AIRPORT_ID, airport_name, city, state, country, latitude, longitude)
                    conn.execute(query)
                return {'Success' : 'XML content-type UPDATE successful'}

            except requests.exceptions.HTTPError as e:
                return {SystemError(e)}

class DeleteAirport(Resource):
    def delete(self, AIRPORT_ID):
        conn = db_connect.connect()
        try:
            query = conn.execute("DELETE FROM airports WHERE airport_id='{0}'".format(AIRPORT_ID))
            return {'Status': 'Deleted successfully!!'}
        except Exception as e:
            return {'Error' : "Could not perform DELETE"}
