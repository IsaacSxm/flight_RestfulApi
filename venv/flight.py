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
            "year": {
              "description": "This is a unique identifier for the name of the airline",
              "type": "integer",
              "default": 2015
            },
            "month": {
              "description": "This is the name of the airline",
              "type": "integer",
              "minimum":1,
              "maximum": 12
            },
            "day": {
              "description": "Day of particular flight",
              "type": "integer",
              "minimum": 1,
              "maximum": 31
            },
            "Airline": {
              "description": "This is the airline identifier.",
              "type": "string",
              "minLength": 2,
              "maxLength": 2

            },
            "Flight_number": {
              "description": "Flight number.",
              "type": "integer",
              "minLength": 3,
              "maxLength": 4
            },
            "Tail_number": {
              "description": "This represents the tail number.",
              "type": "string",
              "minLength": 6,
              "maxLength": 6
            },
            "Origin_airport": {
              "description": "This shows the airport code name of where the flight departed",
              "type": "string",
              "minLength": 3,
              "maxLength": 3
            },
            "Destination_country": {
              "description": "This shows the destination country of the flight",
              "type": "string"
            }
          },
          "required": ["year", "month", "day", "Airline", "Flight_number", "Origin_airport", "Destination_country"]
}

class Flight(Resource):
    def get(self):
        conn = db_connect.connect()
        try:
            query = conn.execute("SELECT * FROM flights;")
            result = {'Flight': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return result
        except Exception as e:
          return {'Error': 'Could not perform GET request'}

    def post(self):
      conn = db_connect.connect()
      if "application/json" in request.headers["Content-Type"]:
        try:
          @expects_json(schema)
          def post_(self):
              for content in request.json:
                  year = request.json['YEAR']
                  month = request.json['MONTH']
                  day = request.json['DAY']
                  day_of_week = request.json['DAY_OF_WEEK']
                  airline = request.json['AIRLINE']
                  flight_number = request.json['FLIGHT_NUMBER']
                  tail_number = request.json['TAIL_NUMBER']
                  origin_airport = request.json['ORIGIN_AIRPORT']
                  destination_country = request.json['DESTINATION_COUNTRY']
                  query = conn.execute("INSERT INTO flights values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(year, month, day, day_of_week, airline, flight_number, tail_number, origin_airport, destination_country))
                  return {"Success": "JSON content POST successful"}
              post_(self)
              return {"Success": "JSON content POST successful"}
        except requests.exceptions.HTTPError as e:
          return SystemError(e)

      else:
          try:
            xml_data = request.data
            content_xml = xmltodict.parse(xml_data)
            for content in content_xml:
                year = content_xml['Flights']['Flight']['YEAR']
                month = content_xml['Flights']['Flight']['MONTH']
                day = content_xml['Flights']['Flight']['DAY']
                day_of_week = content_xml['Flights']['Flight']['DAY_OF_WEEK']
                airline = content_xml['Flights']['Flight']['AIRLINE']
                flight_number = content_xml['Flights']['Flight']['FLIGHT_NUMBER']
                tail_number = content_xml['Flights']['Flight']['TAIL_NUMBER']
                origin_airport = content_xml['Flights']['Flight']['ORIGIN_AIRPORT']
                destination_country = content_xml['Flights']['Flight']['DESTINATION_COUNTRY']
                query = conn.execute("INSERT INTO flights values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(year, month, day, day_of_week, airline, flight_number, tail_number, origin_airport, destination_country))
            return {'Success' : 'POST xml content-type successful'}
          except requests.exceptions.HTTPError as e:
            return SystemExit(e)

class UpdateFlight(Resource):

  def put(self, FLIGHT_NUMBER):
      conn = db_connect.connect()
      if "application/json" in request.headers["Content-Type"]:
          try:
              @expects_json(schema)
              def put_(self):
                  for content in request.json:
                      year = request.json['YEAR']
                      month = request.json['MONTH']
                      day = request.json['DAY']
                      day_of_week = request.json['DAY_OF_WEEK']
                      airline = request.json['AIRLINE']
                      flight_number = request.json['FLIGHT_NUMBER']
                      tail_number = request.json['TAIL_NUMBER']
                      origin_airport = request.json['ORIGIN_AIRPORT']
                      destination_country = request.json['DESTINATION_COUNTRY']
                      query = conn.execute("UPDATE flights SET year='{1}', month='{2}', day='{3}', day_of_week='{4}', airline='{5}', flight_number='{6}', tail_number='{7}', origin_airport='{8}', destination_country='{9}')".format(year, month, day, day_of_week, airline, flight_number, tail_number, origin_airport, destination_country))
                      return {"Success": "JSON content PUT/UPDATE successful"}
              put_(self)
              return {"Success": "JSON content PUT/UPDATE successful"}
          except requests.exceptions.HTTPError as e:
              return SystemError(e)

      else:
          try:
             xml_data = request.data
             content_xml = xmltodict.parse(xml_data)
             for content in content_xml:
                  year = content_xml['Flights']['Flight']['YEAR']
                  month = content_xml['Flights']['Flight']['MONTH']
                  day = content_xml['Flights']['Flight']['DAY']
                  day_of_week = content_xml['Flights']['Flight']['DAY_OF_WEEK']
                  airline = content_xml['Flights']['Flight']['AIRLINE']
                  flight_number = content_xml['Flights']['Flight']['FLIGHT_NUMBER']
                  tail_number = content_xml['Flights']['Flight']['TAIL_NUMBER']
                  origin_airport = content_xml['Flights']['Flight']['ORIGIN_AIRPORT']
                  destination_country = content_xml['Flights']['Flight']['DESTINATION_COUNTRY']
                  query = conn.execute("UPDATE flights SET year='{1}', month='{2}', day='{3}', day_of_week='{4}', airline='{5}', flight_number='{6}', tail_number='{7}', origin_airport='{8}', destination_country='{9}')".format(year, month, day, day_of_week, airline, flight_number, tail_number, origin_airport, destination_country))
             return {"Success": "JSON content PUT/UPDATE successful"}
          except requests.exceptions.HTTPError as e:
            return SystemError(e)

class DeleteFlight(Resource):
  def delete(self, FLIGHT_NUMBER):
    conn - db_connect.connect()
    try:
      query = conn.execute("DELETE FROM flights WHERE FLIGHT_NUMBER='{0}'".format(FLIGHT_NUMBER))
      return {"Status" : 'Deleted successfully!!'}
    except Exception as e:
      return {'Error': "Could not perform DELETE"}