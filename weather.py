import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

#API_TOKEN can be set different, is used for Postman 

API_TOKEN = "parsifal"

app = Flask(__name__)
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def home_page():
    return "<p><h2>KMA L2: Python Saas.</h2></p>"


@app.route(
    "/weather/api/history",
    methods=["POST"],
)

def weather_endpoint():

    json_data = request.get_json()
    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)
    token = json_data.get("token")
    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    date = ""
    if json_data.get("date"):
        date = json_data.get("date")

    location = ""
    if json_data.get("location"):
        location = json_data.get("location")

    requester_name = ""
    if json_data.get("requester_name"):
        requester_name = json_data.get("requester_name")

    #---------------------------------------------------------------------------------------------

    url = "https://visual-crossing-weather.p.rapidapi.com/history"

    querystring = {
                "startDateTime": date+"T15:00:00",
                "aggregateHours":"24",
                "location": location,
                "unitGroup":"metric",
                "contentType":"json",
                }

    headers = {
        
#In order to get Key and Host values you have to register at link below
#https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather/
        
    "X-RapidAPI-Key": , 
    "X-RapidAPI-Host": 
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_dict = response.json()

    date_now = dt.datetime.now().isoformat()

    temp_dict = response_dict['locations']

    dict_ = {
    "requester_name" : requester_name,
    "timestamp" : date_now,
    "location" : temp_dict[querystring['location']]['id'],
    "date": temp_dict[querystring["location"]]["values"][0]['datetimeStr'].split('T')[0],
    "wheather":
        {
        "temp_c_max" : temp_dict[querystring['location']]["values"][0]["maxt"],
        "temp_c" : temp_dict[querystring['location']]["values"][0]["temp"],
        "temp_c_min" : temp_dict[querystring['location']]["values"][0]["mint"],
        "wind_kph" : temp_dict[querystring['location']]["values"][0]["wspd"],
        "pressure_mb" : temp_dict[querystring['location']]["values"][0]["sealevelpressure"],
        "humidity" : temp_dict[querystring['location']]["values"][0]["humidity"],
        "weathertype" : temp_dict[querystring['location']]["values"][0]["weathertype"],
        "visibility" : temp_dict[querystring['location']]["values"][0]["visibility"],
        "cloudcover" : temp_dict[querystring['location']]["values"][0]["cloudcover"]
        }
    }
    return dict_

