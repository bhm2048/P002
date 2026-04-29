from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/time")
def api_time():
    now = datetime.now()
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "iso": now.isoformat(),
    })


@app.route("/api/echo", methods=["POST"])
def api_echo():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    payload = request.get_json()
    payload["received_at"] = datetime.now().isoformat()
    return jsonify(payload)


if __name__ == "__main__":
    app.run(debug=True)
