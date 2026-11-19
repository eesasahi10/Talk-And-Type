
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from upstash_redis import Redis
import random
import os

app = Flask(__name__)
CORS(app)

# Connect to shared Redis storage
redis = Redis.from_env()

# Temporary connection codes expire after 15 minutes
CODE_TTL = 900


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_code')
def generate_code():
    while True:
        new_code = str(random.randint(1000000, 9999999))

        # Create a unique temporary mailbox
        created = redis.set(
            f"mailbox:{new_code}",
            "",
            ex=CODE_TTL,
            nx=True
        )

        if created:
            print(f"New Room Created: {new_code}")
            return jsonify({"code": new_code})


@app.route('/connect', methods=['POST'])
def connect():
    data = request.get_json(silent=True) or {}
    user_code = str(data.get('code', '')).strip()

    if not user_code:
        return jsonify({
            "status": "error",
            "message": "Missing Code"
        }), 400

    if redis.exists(f"mailbox:{user_code}"):
        return jsonify({
            "status": "success",
            "message": "Linked!"
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid Code"
    }), 400


@app.route('/send_text', methods=['POST'])
def send_text():
    data = request.get_json(silent=True) or {}

    code = str(data.get('code', '')).strip()
    speech = data.get('speech', '')

    key = f"mailbox:{code}"

    if not code or not redis.exists(key):
        return jsonify({
            "status": "error",
            "message": "Invalid Room Code"
        }), 404

    if not isinstance(speech, str):
        return jsonify({
            "status": "error",
            "message": "Invalid speech"
        }), 400

    processed_text = speech.lower()

    replacements = {
        "full stop": ".",
        "period": ".",
        "comma": ",",
        "question mark": "?",
        "exclamation mark": "!",
        "slash": "/",
        "space": " ",
        "open bracket": "(",
        "close bracket": ")",
        "new line": "\n",
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "dash": "-",
        "hyphen": "-",
        "open curly bracket": "{",
        "close curly bracket": "}",
        "star": "*",
        "hash": "#",
        "at the rate of": "@",
        "percentage": "%",
        "colon": ":"
    }

    for word, symbol in replacements.items():
        processed_text = processed_text.replace(word, symbol)

    # Store the text and refresh the mailbox expiration
    redis.set(key, processed_text, ex=CODE_TTL)

    print(f"Room {code} received text: {processed_text}")

    return jsonify({"status": "success"}), 200


@app.route('/get_text')
def get_text():
    code = request.args.get('code', '').strip()

    if not code:
        return jsonify({"text": ""}), 200

    text = redis.get(f"mailbox:{code}")

    if text is None:
        return jsonify({"text": ""}), 200

    return jsonify({"text": text}), 200
