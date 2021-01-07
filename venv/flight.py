import Airline
import Airport
import json
from simplexml import dumps
from flask import Flask, jsonify, request, make_response
from flask import Response, Flask
from flask_restful import Resource, Api, Resource, fields
from flask_expects_json import expects_json

app = Flask(__name__)
api = Api(app)


@api.representation('application/json')
def output_json(data, code, headers=None):
	resp = make_response(json.dumps({' ' : data}), code)
	resp.headers.extend(headers or {})
	return resp

@api.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({' ' : data}), code)
	resp.headers.extend(headers or {})
	return resp


api.add_resource(Airline.Delete, '/delete/<AIRLINE_ID>') #route to delete based on airline id
api.add_resource(Airline.Updates, '/update/<AIRLINE_ID>') #route to update based on airline id
api.add_resource(Airline.Airlines, '/airlines') #route to select everything from airlines
# api.app.validate('AirlinesSchema', 'titile')
api.add_resource(Airport.Airports, '/airports') #route to select everything from airports
api.add_resource(Airline.Greet, '/')
# @app.validate('AirlinesSchema', 'title')


if __name__ == '__main__':
    app.run()