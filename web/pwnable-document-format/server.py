#!/usr/bin/env python3
from flask import Flask, send_file, request, make_response

app = Flask(__name__)

PDF_PATH = "./exploit.pdf"

# Utility to add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = request.headers.get(
        "Access-Control-Request-Headers", "Content-Type, Authorization"
    )
    response.headers["Access-Control-Max-Age"] = "3600"
    return response

# Preflight handler (OPTIONS)
@app.route("/exploit.pdf", methods=["OPTIONS"])
def options_file():
    resp = make_response("", 204)
    return resp

# Actual file-serving route
@app.route("/exploit.pdf", methods=["GET"])
def get_file():
    return send_file(PDF_PATH, mimetype="application/pdf", as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
