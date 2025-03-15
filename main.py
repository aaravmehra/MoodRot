import cv2
import time
import pyautogui
import mediapipe as mp
from deepface import DeepFace
import threading
import os
import random
import customtkinter as ctk
from PIL import Image, ImageTk


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

config = {
    "speak_interval": 10,
    "running": True
}

sentences = [
   "imagine no maidens",
    "you are NOT activating ur balkan rage",
    "no huzz for you dawg",
    "L + ratio + cope",
    "stay on copium blud",
    "ur not HIM lil bro",
    "even caseoh won't try to eat you",
    "yeah you little twink stay on character.ai"
    "suck suck suck suck suck suck suck"`
    "icl u pmo gng"
    "no one will not even date you as a femboy"
    "bruzz ur not pulling thr huzz"
]

mood_sensitivity = {
    "happy": 0.4,
    "neutral": 0.8,
    "sad": 0.9,
    "angry": 1.2,
    "fear": 0.69,
    "disgust": 0.6,
    "surprise": 0.9
}

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

current_mood = "Neutral"

def adjust_mouse_sensitivity(mood):
    sensitivity = mood_sensitivity.get(mood, 0.3)
    x, y = pyautogui.position()
    for _ in range(5):
        pyautogui.moveTo(x, y, duration=sensitivity)

def detect_mood():
    global current_mood
    ret, frame = cap.read()
    if not ret:
        return "neutral"
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        adjust_mouse_sensitivity(emotion)
        current_mood = emotion.capitalize()
        mood_label.configure(text=f"Mood: {current_mood}")  
        return emotion
    except:
        return "neutral"

def mood_loop():
    while config["running"]:
        detect_mood()
        time.sleep(5)

def show_sentence_popup():
    """ Opens a separate styled pop-up window to display a sentence. """
    sentence = random.choice(sentences)

    popup = ctk.CTkToplevel(root)
    popup.title("Message")
    popup.geometry("500x250")
    popup.configure(fg_color="#2B2B2B")
    popup.attributes("-topmost", True) 

    sentence_label = ctk.CTkLabel(
        popup, text=sentence, font=("Arial", 24, "bold"), wraplength=450, text_color="white"
    )
    sentence_label.pack(expand=True, pady=50)

    
    root.after(config["speak_interval"] * 1000, show_sentence_popup)

def update_webcam():
    """ Captures frames from webcam and updates the UI. """
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam_label.configure(image=imgtk)
        webcam_label.imgtk = imgtk
    root.after(20, update_webcam)

def quit_program():
    config["running"] = False
    cap.release()
    cv2.destroyAllWindows()
    root.quit()

def save_settings():
    """ Saves the new interval when the Save button is clicked. """
    config["speak_interval"] = int(interval_slider.get())
    slider_label.configure(text=f"Message Interval: {config['speak_interval']} sec")


ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Mood-Based Cursor Sensitivity")
root.geometry("600x650")
root.configure(fg_color="#1E1E1E")  


header_label = ctk.CTkLabel(root, text="Mood-Based Cursor Sensitivity", font=("Arial", 18, "bold"), text_color="white")
header_label.pack(pady=10)


webcam_label = ctk.CTkLabel(root, text="")  
webcam_label.pack(pady=10)


mood_label = ctk.CTkLabel(root, text="Mood: Neutral", font=("Arial", 16, "bold"), text_color="lightblue")
mood_label.pack(pady=10)


slider_label = ctk.CTkLabel(root, text=f"Message Interval: {config['speak_interval']} sec", font=("Arial", 14), text_color="white")
slider_label.pack(pady=5)


interval_slider = ctk.CTkSlider(root, from_=10, to=600)
interval_slider.set(config["speak_interval"])
interval_slider.pack(pady=10)


save_button = ctk.CTkButton(root, text="Save", command=save_settings, fg_color="#007ACC") 
save_button.pack(pady=10)


quit_button = ctk.CTkButton(root, text="Quit", command=quit_program, fg_color="red")
quit_button.pack(pady=10)

threading.Thread(target=mood_loop, daemon=True).start()
root.after(config["speak_interval"] * 1000, show_sentence_popup)
update_webcam()
root.mainloop()
