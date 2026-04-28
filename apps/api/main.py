from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get("/search")
def hello_world():
    result = []
    query = request.args.get("q", "")
    if not query:
        return jsonify(result)

    return result
