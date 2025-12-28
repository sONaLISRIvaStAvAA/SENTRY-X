import tkinter as tk
from PIL import Image, ImageTk
import cv2
import serial
import time
import pygame
import numpy as np
import os


# ---------- SERIAL ----------
ser = serial.Serial('COM10', 9600, timeout=1)
time.sleep(2)

# ---------- SOUND ----------
pygame.mixer.init()
presence_sound = pygame.mixer.Sound("presence.wav")
alert_sound = pygame.mixer.Sound("alert.wav")

# ---------- LOAD KNOWN IMAGES ----------
def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(path)
    return cv2.resize(img, (200, 200))

known1 = load_image("known1.jpg")
known2 = load_image("known2.jpg")

# ---------- MATCH ----------
def is_match(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (200, 200))
    d1 = np.mean(cv2.absdiff(gray, known1))
    d2 = np.mean(cv2.absdiff(gray, known2))
    return d1 < 40 or d2 < 40

# ---------- UI ----------
root = tk.Tk()
root.title("INTRUDER SYSTEM")
root.geometry("1000x600")
bg_img = Image.open("background.jpg").resize((1000, 600))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()

status = tk.Label(
    root, text="SYSTEM ARMED",
    fg="lime", bg="black",
    font=("Consolas", 30, "bold")
)
status.pack(pady=20)

camera_label = tk.Label(root, bg="black")
camera_label.place(x=700, y=50)   # default position (top-right)

result_label = tk.Label(
    root, bg="black",
    font=("Consolas", 26, "bold")
)
result_label.pack(pady=20)

# ---------- GLOBALS ----------
cap = None
verified = False
alert_played = False
presence_active = False
current_state = "SAFE"

# ---------- CAMERA ----------
def start_camera():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            cap = cv2.VideoCapture(1)

def update_camera():
    global verified, alert_played

    if cap is not None:
        ret, frame = cap.read()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((250, 180))
            imgtk = ImageTk.PhotoImage(img)

            camera_label.configure(image=imgtk)
            camera_label.image = imgtk  # keep reference

            if not verified:
                if is_match(frame):
                    verified = True
                    result_label.config(text="✔ VERIFIED", fg="lime")
                    ser.write(b'V')  # tell Arduino verified
                else:
                    result_label.config(text="❌ NOT VERIFIED", fg="red")
                    if not alert_played:
                        alert_sound.play()
                        alert_played = True
                    status.config(text="INTRUSION ALERT", fg="white")

    root.after(30, update_camera)

# ---------- PRESENCE ----------
def start_presence():
    global presence_active, verified, alert_played

    if presence_active:
        return

    presence_active = True
    verified = False
    alert_played = False

    presence_sound.play()
    status.config(text="PRESENCE DETECTED", fg="yellow")
    result_label.config(text="")

    # move camera slightly inward if you want later
    # camera_label.place(x=550, y=120)

    start_camera()

# ---------- SHUTDOWN ----------
def shutdown_camera():
    global cap, presence_active
    if cap:
        cap.release()
        cap = None
    presence_active = False
    camera_label.config(image="")

# ---------- SERIAL ----------
def check_serial():
    global current_state

    if ser.in_waiting:
        data = ser.readline().decode(errors="ignore").strip()

        if data != current_state:
            current_state = data

            if data == "SAFE":
                shutdown_camera()
                status.config(text="SYSTEM ARMED", fg="lime")
                result_label.config(text="")

            elif data == "PRESENCE":
                start_presence()

            elif data == "ALERT" and not verified:
                status.config(text="INTRUSION ALERT", fg="white")

    root.after(100, check_serial)

# ---------- START ----------
check_serial()
update_camera()
root.mainloop()
