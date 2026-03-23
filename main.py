from flask import Flask, render_template, request, jsonify
import random

# Make sure your app is set up like this:
app = Flask(__name__, static_folder='static')

# This dictionary acts as our 'Mailbox' system
# It stores { "7-digit-code": "The spoken text" }
mailboxes = {}

current_code = ""
@app.route('/')
def index():
    # This serves your Talk&Type.html file from the templates folder
    return render_template('index.html')

# DOOR 1: Generates the 7-digit code for the website
@app.route('/generate_code')
def generate_code():
    global current_code  # This tells Python to use the tank on Line 10
    new_code = str(random.randint(1000000, 9999999))
    current_code = new_code # This saves the code for the phone to find later
    mailboxes[new_code] = None
    print(f"New Room Created: {new_code}")
    return jsonify({"code": new_code})
# Add this to your main.py
@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    user_code = data.get('code')
    
    # Check if the code the phone sent matches the one on the screen
    if user_code == current_code:
        return {"status": "success", "message": "Linked!"}, 200
    else:
        return {"status": "error", "message": "Invalid Code"}, 400

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
        # Find where you save the message, then add this:
        pyautogui.write(message, interval=0.05)
        mailboxes[code] = None  # Empty the mailbox after picking it up
        return jsonify({"text": message}), 200
    
    return jsonify({"text": None}), 200

if __name__ == "__main__":
    # This allows Render to handle the connection for the whole world
    app.run(host='0.0.0.0', port=10000)
