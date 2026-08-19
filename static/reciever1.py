import customtkinter as ctk  
import requests             
import threading            
import time                 
import pyautogui            # Requires: pip install pyautogui
from datetime import datetime

# --- CONFIGURATION ---
RENDER_URL = "https://talk-and-type.onrender.com"

# --- PYAUTOGUI AUTOMATION ENGINE ---
def win_type_text(text):
    """ Types text character by character for a 'live' effect. """
    print(f"[ENGINE TRIGGERED] Typing: '{text}'")
    try:
        # Use write() instead of copy/paste for smoother live typing
        pyautogui.write(text, interval=0.01) 
    except Exception as e:
        print(f"!!! Typing Engine Error: {e}")

# --- MAIN APP CLASS ---
class TalkAndTypeReceiver(ctk.CTk):
    def __init__(self):
        super().__init__()

        # WINDOW SETUP
        self.title("Talk & Type Receiver")
        self.geometry("450x470")
        self.resizable(False, False) 
        ctk.set_appearance_mode("system")  
        ctk.set_default_color_theme("dark-blue") 

        # UI ELEMENTS
        self.title_label = ctk.CTkLabel(self, text="TALK & TYPE", font=("Arial", 30, "bold"))
        self.title_label.pack(pady=20)

        self.code_entry = ctk.CTkEntry(self, placeholder_text="Enter 7-Digit Code", width=200, height=35)
        self.code_entry.pack(pady=10)

        self.status_indicator = ctk.CTkLabel(self, text="● OFFLINE", text_color="red", font=("Arial", 14, "bold"))
        self.status_indicator.pack(pady=5)

        self.start_btn = ctk.CTkButton(self, text="Start", command=self.start_thread)
        self.start_btn.pack(pady=15)

        self.log = ctk.CTkTextbox(self, width=400, height=150)
        self.log.pack(pady=10, padx=20)
        self.log.configure(state="disabled")

        self.last_text = ""  

    def start_thread(self):
        room_code = self.code_entry.get().strip()
        if not room_code: return

        self.status_indicator.configure(text="● LIVE", text_color="green")
        self.start_btn.configure(state="disabled", text="Monitoring...")
        threading.Thread(target=self.run_receiver, daemon=True).start()

    def run_receiver(self):
        room_code = self.code_entry.get().strip()
        while True:
            try:
                response = requests.get(f"{RENDER_URL}/get_text", params={'code': room_code}, timeout=5)
                
                if response.status_code == 200:
                    new_text = response.json().get('text')
                    
                    if new_text and new_text != self.last_text:
                        # Find only the new part to avoid re-typing
                        if new_text.startswith(self.last_text):
                            diff = new_text[len(self.last_text):]
                        else:
                            diff = new_text
                        
                        self.last_text = new_text 
                        if diff:
                            win_type_text(diff)
                    
            except Exception as e:
                print(f"Network Error: {e}")

            time.sleep(0.05) # Very fast polling for live feel

    def add_to_log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", f">>> {msg}\n")
        self.log.configure(state="disabled")

if __name__ == "__main__":
    app = TalkAndTypeReceiver()
    app.mainloop()