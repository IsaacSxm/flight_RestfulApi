import Airline
import Airport
import Country
import flight
import json
from simplexml import dumps
from flask import Flask, render_template, jsonify, request, make_response
from flask import Response, Flask
from flask_restful import Resource, Api, Resource, fields
from flask_expects_json import expects_json


app = Flask(__name__)
api = Api(app)
apiAirlines = Api(app)
apiAirports = Api(app)
apiCountry = Api(app)
apiFlight = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
	resp = make_response(json.dumps(data), code)
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

@apiFlight.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'Flights':data}), code)
	resp.headers.extend(headers or {})
	return resp


@app.route('/')
def index():
	return render_template('index.html')

# api.add_resource(Airline.Greet, '/')
apiAirlines.add_resource(Airline.AirlinesSelect, '/airlines/<AIRLINE_ID>')
apiAirlines.add_resource(Airline.Airlines, '/airlines') 	#route to SELECT/POST everything from airlines
api.add_resource(Airline.DeleteAirline, '/airlines/delete/<AIRLINE_ID>') 	#route to DELETE airline
api.add_resource(Airline.UpdateAirline, '/airlines/update/<AIRLINE_ID>') 	#route to UPDATE airline


apiAirports.add_resource(Airport.Airports, '/airports') 	#route to SELECT/POST everything from airports
apiAirports.add_resource(Airport.AirportsSelect, '/airports/<AIRPORT_ID>')
api.add_resource(Airport.DeleteAirport, '/airports/delete/<AIRPORT_ID>') #route to DELETE airport
api.add_resource(Airport.UpdateAirport, '/airports/update/<AIRPORT_ID>') #route to UPDATE airport


apiCountry.add_resource(Country.GetAndPost, '/countries') 	#route to SELECT/POST everything from airports
apiCountry.add_resource(Country.CountrySelect, '/countries/<Country>')
api.add_resource(Country.DeleteCountry, '/countries/delete/<Country>')		#route to DELETE country
api.add_resource(Country.UpdateCountry, '/countries/update/<Country>')		#route to UPDATE country


apiFlight.add_resource(flight.Flight, '/flights')	#route to SELECT/POST everything from flight
apiFlight.add_resource(flight.flightSelect, '/flights/<FLIGHT_NUMBER>')
api.add_resource(flight.DeleteFlight, '/flights/delete/<FLIGHT_NUMBER>')	#route to DELETE flight
api.add_resource(flight.UpdateFlight, '/flights/update/<FLIGHT_NUMBER>')	#route to UPDATE flight

if __name__ == '__main__':
    app.run()