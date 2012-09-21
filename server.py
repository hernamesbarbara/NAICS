from flask import Flask, jsonify
from flask import render_template, request, Response
import json, os
from naics import *

app = Flask(__name__)

@app.route("/naics/all", methods=['GET'])
def naics():
    return Response(json.dumps(fetch_naics()), mimetype="application/json")

@app.route('/naics/<int:code>', methods=['GET'])
def find_one(code):
    return Response(json.dumps(fetch_one(code)), mimetype="application/json")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

