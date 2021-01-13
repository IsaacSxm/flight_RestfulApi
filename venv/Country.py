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
            "Country": {
              "description": "Name of country",
              "type": "string",
              "minLength": 3,
              "maxLength": 100
            },
            "AverageTemp": {
              "description": "Average yearly temperature in degree Celsius",
              "type": "number",
              "minimum": -25,
              "maximum": 50
            }
          },
          "required": ["Country","AverageTemp"]
}

class GetAndPost(Resource):
    def get(self):
        conn = db_connect.connect()
        try:
            query = conn.execute("SELECT * FROM CountryAndAvgTemp;")
            result = {'Country': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
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
                        country = request.json['']
                        avgTempCelsius = request.json['']
                        query = conn.execute("insert into CountryAndAvgTemp values('{0}', '{1}')".format(country, avgTempCelsius))
                        return {"Success" : "JSON content posted successfully"}
                post_(self)
                return {"Success": "JSON content posted successfully"}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)

        else:
            try:
                xml_data = request.data
                content_xml = xmltodict.parse(xml_data)
                for content in content_xml:
                    country = content_xml['Countries']['Country']
                    avgTempCelsius = content_xml['Countries']['AvgTempCelsius']
                    query = conn.execute("INSERT INTO CountryAndAvgTemp values ('{0}', '{1}')".format(country, avgTempCelsius))
                return {'Success': 'POST xml content-type successful'}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)

class UpdateCountry(Resource):
    def put(self, Country):
        conn = db_connect()
        if "application/json" in request.headers["Content-Type"]:
            try:
                @expects_json(schema)
                def put_(self):
                    for content in request.json:
                        avgTempCelsius = request.json['AvgTempCelsius']
                        query = conn.execute("UPDATE CountryAndAvgTemp SET avgTempCelsius='{1}' WHERE country='{0}')".format(Country, avgTempCelsius))
                    return {'Success' : 'JSON content-type POST successful'}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)

        else:
            try:
                xml_data = request.data
                content_xml = xmltodict.parse(xml_data)
                for content in content_xml:
                    avgTempCelsius = content_xml['Countries']['AvgTempCelsius']
                    query = conn.execute("UPDATE CountryAndAvgTemp SET avgTempCelsius='{1}' WHERE country='{0}')".format(Country, avgTempCelsius))
                return {'Success': 'XML content-type UPDATE successful'}
            except requests.exceptions.HTTPError as e:
                return SystemError(e)

class DeleteCountry(Resource):
    def delete(self, Country):
        conn = db_connect.connect()
        try:
            query = conn.execute("DELETE FROM CountryAndAvgTemp WHERE country='{0}'".format(Country))
            return {"Status": 'Deleted successfully!!'}
        except Exception as e:
            return {'Error': "Could not perform DELETE"}