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

# @app.route('/delete/<String:AIRLINE_ID>')
# def delete_airline(AIRLINE_ID):
#     conn = db_connect.connect()
#     query = conn.execute("DELETE FROM airlines WHERE airline_id=%s ", (airline_id,))
#     return "Success"
api.add_resource(Rest.Delete, '/delete/<AIRLINE_ID>')
api.add_resource(Rest.Updates, '/update')
api.add_resource(Rest.Airlines, '/airlines')
api.add_resource(Rest.Airports, '/airports')
api.add_resource(Rest.Greet, '/')


if __name__ == '__main__':
    app.run()