import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Fetch Ngrok URL from the environment variable
NGROK_BASE_URL = os.getenv("NGROK_BASE_URL")

@app.route('/<path:endpoint>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(endpoint):
    if not NGROK_BASE_URL:
        return jsonify({"error": "NGROK_BASE_URL is not set"}), 500

    target_url = f"{NGROK_BASE_URL}/{endpoint}"

    # Copy headers and add Ngrok host explicitly
    headers = dict(request.headers)
    headers["Host"] = NGROK_BASE_URL.replace("https://", "").replace("http://", "")

    try:
        if request.method == "GET":
            response = requests.get(target_url, params=request.args, headers=headers)
        elif request.method == "POST":
            response = requests.post(target_url, json=request.json, headers=headers)
        elif request.method == "PUT":
            response = requests.put(target_url, json=request.json, headers=headers)
        elif request.method == "DELETE":
            response = requests.delete(target_url, headers=headers)
        elif request.method == "PATCH":
            response = requests.patch(target_url, json=request.json, headers=headers)
        else:
            return jsonify({"error": "Unsupported HTTP method"}), 405

        return (response.content, response.status_code, response.headers.items())

    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the Ngrok service", "details": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
