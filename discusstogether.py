import os
import slack

from flask import Flask, session, request, g, json, make_response, render_template, redirect

VERSION = '0.1'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'useless_secret'

@app.route('/slack/event', methods=['POST'])
def receive_slack_event():
    """
	Sample message:

    {
        "token": "one-long-verification-token",
        "team_id": "T061EG9R6",
        "api_app_id": "A0PNCHHK2",
        "event": {
            "type": "message",
            "channel": "D024BE91L",
            "user": "U2147483697",
            "text": "Hello hello can you hear me?",
            "ts": "1355517523.000005",
            "event_ts": "1355517523.000005",
            "channel_type": "im"
        },
        "type": "event_callback",
        "authed_teams": [
            "T061EG9R6"
        ],
        "event_id": "Ev0PV52K21",
        "event_time": 1355517523
    }
    """
    msg = request.get_json()

    if 'challenge' in msg:
        return make_response(json.jsonify(challenge=msg['challenge']), 200)

    event_obj = msg.get('event')
    resp = {"happened": "nothing"}

    if event_obj['user'] == "UMXQK1TF0": # ID of him
        print(msg)
        client = slack.WebClient(token=os.environ.get('SLACK_API_TOKEN'))
        chat = event_obj['text']
        resp = client.chat_postMessage(channel='#development', text=chat)

    return make_response("OK", 200)

if __name__ == "__main__":
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

