from flask import Flask, request, jsonify
import tkz

app = Flask(__name__)


@app.get("/search")
def hello_world():
    result = []
    query = request.args.get("q", "")
    if not query:
        return jsonify(result)

    words = tkz.tokenize(query)

    return result
