from flask import jsonify, make_response
import json
import os

class FileHelper:
    def get_response_message():
        message = jsonify({"message": "from server data added!"})
        response = make_response(message, 201)
        response.headers["Content-Type"] = "application/json"
        return response
    
    def read_dummy_file():
        if os.path.exists('./static/dummyData.json'):
            with open('./static/dummyData.json') as dummyFile:
                data = json.load(dummyFile)
            return data or []
        return []
    
    def write_dummy_file(currentData, newData):
        with open('./static/dummyData.json', 'w') as dummyFile:
            currentData.append(newData)
            json.dump(currentData, dummyFile)