from flask import Flask, jsonify
from flask import render_template, request, Response
import json, os
import parser

app = Flask(__name__)

@app.route("/naics/all", methods=['GET'])
def naics():
    with open('./data/naics07.json', 'r') as f:
        data = json.loads(f.read())

    return Response(json.dumps(data), mimetype="application/json")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
