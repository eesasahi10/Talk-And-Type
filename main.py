from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# This dictionary acts as our 'Mailbox' system
# It stores { "7-digit-code": "The spoken text" }
mailboxes = {}

@app.route('/')
def index():
    # This serves your Talk&Type.html file from the templates folder
    return render_template('Talk&Type.html')

# DOOR 1: Generates the 7-digit code for the website
@app.route('/generate_code')
def generate_code():
    new_code = str(random.randint(1000000, 9999999))
    mailboxes[new_code] = None # Create an empty mailbox for this code
    print(f"New Room Created: {new_code}")
    return jsonify({"code": new_code})

# DOOR 2: The Phone calls this to "Drop Off" the text
@app.route('/send_text', methods=['POST'])
def send_text():
    data = request.json
    code = data.get('code')
    speech = data.get('speech')
    
    if code in mailboxes:
        mailboxes[code] = speech
        print(f"Room {code} received text: {speech}")
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error", "message": "Invalid Room Code"}), 404

# DOOR 3: The Laptop calls this to "Pick Up" the text
@app.route('/get_text')
def get_text():
    code = request.args.get('code')
    if code in mailboxes and mailboxes[code] is not None:
        message = mailboxes[code]
        mailboxes[code] = None  # Empty the mailbox after picking it up
        return jsonify({"text": message}), 200
    
    return jsonify({"text": None}), 200

if __name__ == "__main__":
    # This allows Render to handle the connection for the whole world
    app.run(host='0.0.0.0', port=10000)