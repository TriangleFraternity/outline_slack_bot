import requests
import json
from flask import Flask, request
app = Flask(__name__)


@app.route('/action', methods=['GET', 'POST'])
def handle_action():
    payload = json.loads(request.form['payload'])
    app.logger.debug(payload)

    response_url = payload['response_url']
    reply_data = {
            "text": "It's 80 degrees right now.",
            "response_type": "in_channel"
            }
    r = requests.post(response_url, json=reply_data)
    app.logger.debug(r.status_code)
    return 'Hello, World!'

app.run(debug=True, host='0.0.0.0', port=80)
