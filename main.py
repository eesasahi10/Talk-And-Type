from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__, static_folder='static')

# Stores { "7-digit-code": "The spoken text" }
mailboxes = {}
current_code = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code')
def generate_code():
    global current_code  
    new_code = str(random.randint(1000000, 9999999))
    current_code = new_code 
    mailboxes[new_code] = "" # Initialize as blank string instead of None
    print(f"New Room Created: {new_code}")
    return jsonify({"code": new_code})

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    user_code = data.get('code')
    if user_code == current_code:
        return {"status": "success", "message": "Linked!"}, 200
    else:
        return {"status": "error", "message": "Invalid Code"}, 400

@app.route('/send_text', methods=['POST'])
def send_text():
    data = request.json
    code = data.get('code')
    speech = data.get('speech')
    
    if code in mailboxes:
        processed_text = speech.lower()
        processed_text = processed_text.replace("full stop" or "period", ".")
        processed_text = processed_text.replace("comma", ",")
        processed_text = processed_text.replace("question mark", "?")
        processed_text = processed_text.replace("exclamation mark", "!")
        processed_text = processed_text.replace("slash", "/")
        processed_text = processed_text.replace("space", " ")
        processed_text = processed_text.replace("open bracket", "(")
        processed_text = processed_text.replace("close bracket", ")")
        processed_text = processed_text.replace("new line", "\n")

        mailboxes[code] = processed_text
        print(f"Room {code} received text: {mailboxes[code]}")
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error", "message": "Invalid Room Code"}), 404

# FIXED DOOR 3: Hold the text, don't delete it instantly so the laptop engine can see it clearly!
@app.route('/get_text')
def get_text():
    code = request.args.get('code')
    if code in mailboxes:
        return jsonify({"text": mailboxes[code]}), 200
    return jsonify({"text": ""}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
