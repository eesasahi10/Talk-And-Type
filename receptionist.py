import requests
import time
import os

# --- CONFIGURATION ---
# Replace this with your actual Render URL tomorrow!
RENDER_URL = "https://talk-and-type.onrender.com"
ROOM_CODE = "1234"  # Make sure this matches what you type in the app
POLL_INTERVAL = 2   # Checks for new text every 2 seconds
# ---------------------

def clear_screen():
    # Keeps the terminal clean and professional
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_text():
    params = {'code': ROOM_CODE}
    try:
        response = requests.get(RENDER_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('text'):
                return data['text']
        return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def main():
    clear_screen()
    print("--- Talk&Type Receptionist (Global Mode) ---")
    print(f"Connected to: {RENDER_URL}")
    print(f"Monitoring Room: {ROOM_CODE}")
    print("Waiting for dictation...")
    print("-" * 44)

    while True:
        new_text = fetch_text()
        if new_text:
            # When text arrives, it prints it and stays on screen
            print(f"\n[RECEIVED]: {new_text}")
            print("\nWaiting for next message...")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
