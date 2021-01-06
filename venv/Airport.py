from flask import request
from flask_restful import Resource, Api, Resource, fields
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
from http import HTTPStatus
from flask_expects_json import expects_json

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
  "required": ["airport_id","airport_name", "city", "state", "country"]
}

class Airports(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT airport_id, airport_name, city, country, latitude, longitude FROM airports;")
        result = {'Airports': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result

    @expects_json(schema)
    def post(self):
        conn = db_connect.connect()
        print(request.json)
        airport_id = request.json['airport_id']
        airport_name = request.json['airport_name']
        city = request.json['city']
        state = request.json['state']
        country = request.json['country']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        query = conn.execute("INSERT INTO airports values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(airport_id, airport_name, city, state, country, latitude, longitude))
        return {'status': 'success'}

class Update(Resource):
    @expects_json(schema)
    def put(self, AIRPORT_ID):
        conn = db_connect.connect()
        airport_name = request.json['airport_name']
        city = request.json['city']
        state = request.json['state']
        country = request.json['country']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        query = "UPDATE airports SET airport_name='{1}','{2}', '{3}', '{4}', '{5}', '{6}' WHERE airport_id = '{0}'".format(airport_id, airport_name, city, state, country, latitude, longitude)
        conn.execute(query)
        return {'status': 'success'}

class Delete(Resource):
    def delete(self, AIRPORT_ID):
        conn = db_connect.connect()
        query = conn.execute("DELETE FROM airports WHERE airport_id='0'".format(AIRPORT_ID))
        return {'status': 'Deleted'}
