import Airline
import Airport
import Country
import flight
import json
import pandas
import matplotlib.pyplot as plt, mpld3
from simplexml import dumps
from flask import Flask, render_template, jsonify, request, make_response
from flask import Response, Flask
from flask_restful import Resource, Api, Resource, fields
from flask_expects_json import expects_json
from sqlalchemy import create_engine

#Change this path
db_connect = create_engine('sqlite:///C:/sqlite3/Flights_db.db')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
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


# This end point visualises data by plotting a bar graph
@app.route('/')
def index():
	df = pandas.read_sql("SELECT AIRLINE, AvgTempCelsius, COUNT(AIRLINE) FROM flights INNER JOIN CountryAndAvgTemp ON CountryAndAvgTemp.DESTINATION_COUNTRY = flights.DESTINATION_COUNTRY GROUP BY AvgTempCelsius having count(AIRLINE) > 10", db_connect)
	plots = df.plot.bar(x="AIRLINE", y="AvgTempCelsius" )
	fig = plots.figure
	fig.savefig('static/my_plot.png')
	plt.show()
	return render_template('index.html')


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

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