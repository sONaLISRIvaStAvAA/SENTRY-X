# SENTRY-X
SENTRY-X is a real-time surveillance system that integrates Arduino-based embedded hardware with Python-based software intelligence to detect, verify, and respond to potential intrusions.
The system follows a closed-loop architecture, where software verification can actively influence and override hardware alert decisions.
🧠 System Overview
🔧 Hardware Components

Arduino (UNO/Nano compatible)

Ultrasonic sensor (distance-based detection)

RGB LED (system state indication)

Buzzer (intrusion alert)

16×2 LCD with potentiometer-based contrast control

LCD backlight powered via resistor for night visibility

🧩 Circuit Design

Complete circuit designed and simulated using Tinkercad

Potentiometer used for LCD contrast stabilization

Proper current limiting applied for LCD backlight

💻 Software Components

Python-based GUI using Tkinter

Live video stream using OpenCV

Face verification using reference image comparison

Audio alerts via Pygame

Serial communication using PySerial

🔁 Closed-Loop Operation

Arduino detects presence or intrusion via ultrasonic sensor

Python GUI activates camera and verification process

If an authorized person is detected, Python sends a verification signal to Arduino

Arduino resets alert state and returns to SAFE mode

This prevents false alarms and enables intelligent decision-making.

🛠️ Technologies Used

Arduino (C/C++)

Python

OpenCV

Tkinter

PySerial

Pygame

Tinkercad

📷 Demo & Circuit

🎥 Project demo video

🧩 Tinkercad circuit diagram included

🚀 Future Enhancements

ML-based face recognition

Cloud-based logging and alerts

Mobile notifications

Multi-user authentication
