import Rest
import json
from simplexml import dumps
from flask import Flask, jsonify, request, make_response
from flask import Response
from flask_restful import Resource, Api, Resource, fields


app = Flask(__name__)
api = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
	resp = make_response(json.dumps({'response' : data}), code)
	resp.headers.extend(headers or {})
	return resp

@api.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'response' : data}), code)
	resp.headers.extend(headers or {})
	return resp


api.add_resource(Rest.Delete, '/delete/<AIRLINE_ID>') #route to delete based on airline id
api.add_resource(Rest.Updates, '/update/<AIRLINE_ID>') #route to update based on airline id
api.add_resource(Rest.Airlines, '/airlines') #route to select everything from airlines
api.add_resource(Rest.Airports, '/airports') #route to select everything from airports
api.add_resource(Rest.Greet, '/')


if __name__ == '__main__':
    app.run()