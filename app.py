from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Set your Ngrok base URL here
NGROK_BASE_URL = "https://9239-2401-4900-1c55-3cdd-79bd-663c-2ed0-5704.ngrok-free.app"

@app.route('/<path:endpoint>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(endpoint):
    # Construct the target URL
    target_url = f"{NGROK_BASE_URL}/{endpoint}"

    # Forward the request
    try:
        # Use the appropriate HTTP method
        if request.method == "GET":
            response = requests.get(target_url, params=request.args)
        elif request.method == "POST":
            response = requests.post(target_url, json=request.json, headers=request.headers)
        elif request.method == "PUT":
            response = requests.put(target_url, json=request.json, headers=request.headers)
        elif request.method == "DELETE":
            response = requests.delete(target_url, headers=request.headers)
        elif request.method == "PATCH":
            response = requests.patch(target_url, json=request.json, headers=request.headers)
        else:
            return jsonify({"error": "Unsupported HTTP method"}), 405

        # Return the response from the Ngrok service
        return (response.content, response.status_code, response.headers.items())

    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the Ngrok service", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port=8080)
