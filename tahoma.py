#!flask/bin/python
from tahoma_api import TahomaApi
from tahoma_api import Action
from flask import Flask, jsonify

import json

# Read login data
with open("login_data.json") as login_data:
    login = json.load(login_data)

app = Flask(__name__)
api = TahomaApi(login["userName"], login["userPassword"])
api.get_setup()
devices = api.get_devices()

for deviceURL, value in devices.items():
    print(deviceURL, value.label, value.command_definitions)


@app.route('/execute/<string:label>/<string:command>', methods=['GET'])
def execute(label, command):
    data = {
        "commands": [
            {
                "name": command,
            }
        ]
    }

    for deviceURL, value in devices.items():
        if label == value.label:
            print(deviceURL, value.label, value.command_definitions)
            data['deviceURL'] = deviceURL
            api.apply_actions(label, [Action(data)])
            return jsonify(success=True, message='Device '+label+' found', commad=command)

    return jsonify(success=False,  message='No device found')


if __name__ == '__main__':
    app.run(debug=True)
