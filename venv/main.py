import Airline
import Airport
import Country
import json
from simplexml import dumps
from flask import Flask, jsonify, request, make_response
from flask import Response, Flask
from http import HTTPStatus
from flask_restful import Resource, Api, Resource, fields
from flask_expects_json import expects_json
import xml.etree.ElementTree as ET

app = Flask(__name__)
api = Api(app)
apiAirlines = Api(app)
apiAirports = Api(app)
apiCountry = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
	resp = make_response(json.dumps({'Airports ':data}), code)
	resp.headers.extend(headers or {})
	return resp


@apiAirlines.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'Airlines':data}), code)
	resp.headers.extend(headers or {})
	return resp

@apiAirports.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'Airports':data}), code)
	resp.headers.extend(headers or {})
	return resp

@apiCountry.representation('application/xml')
def output_xml(data, code, headers=None):
    resp = make_response(dumps({'Countries':data}), code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(Airline.Greet, '/')
apiAirlines.add_resource(Airline.Airlines, '/airlines') #route to SELECT/POST everything from airlines
api.add_resource(Airline.DeleteAirline, '/airlines/delete/<AIRLINE_ID>') #route to DELETE based on airline id
api.add_resource(Airline.UpdateAirline, '/airlines/update/<AIRLINE_ID>') #route to UPDATE based on airline id


apiAirports.add_resource(Airport.Airports, '/airports') #route to SELECT/POST everything from airports
api.add_resource(Airport.DeleteAirport, '/airports/delete/<AIRPORT_ID>') #route to DELETE based on airport id
api.add_resource(Airport.UpdateAirport, '/airports/update/<AIRPORT_ID>') #route to UPDATE based on airport id


apiCountry.add_resource(Country.GetAndPost, '/countries') #route to SELECT/POST everything from airports
api.add_resource(Country.DeleteCountry, '/countries/delete/<Country>')
api.add_resource(Country.UpdateCountry, '/countries/update/<Country>')

if __name__ == '__main__':
    app.run()