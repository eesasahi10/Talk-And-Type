import requests
import time
import os
import pyautogui  # The "Fingers" of the app

# --- CONFIGURATION ---
# 1. Double-check this matches your Render link!
RENDER_URL = "https://talk-and-type.onrender.com"
ROOM_CODE = "1234"  
POLL_INTERVAL = 1   # Checks every 1 second for faster typing
# ---------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_text():
    # Adding /get_text ensures we talk to the right "door" on Render
    endpoint = f"{RENDER_URL}/get_text"
    params = {'code': ROOM_CODE}
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            # If Render says "Yes, here is the text!"
            if data and data.get('text'):
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
    print("\n[ACTION REQUIRED]: Open Notepad/Word and click inside!")
    print("-" * 44)

    while True:
        new_text = fetch_text()
        if new_text:
            print(f"\n[RECEIVED]: {new_text}")
            
            # This part does the actual typing on your laptop
            pyautogui.write(new_text, interval=0.05) 
            pyautogui.press('enter') 

            print("Waiting for next message...")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
