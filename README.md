This is a Python script that uses a webcam to guard my dorm room. It detects motion, checks if the person's face is in my "allowed" list, and sends me an email if it sees an intruder.

How it works:
Motion Sensor: It stays on standby until it sees movement (saves CPU/power).

Face ID: It compares the person to photos I saved of me and my roommates.

Alerts: If it doesn't recognize the face, it snaps a photo and emails it to me instantly.

Stuff you need:
Python * A Webcam (I used a Logitech Brio 100)

Libraries: opencv-python and deepface

Setup:
Put photos of people you know in the training_data folder. Each person gets their own folder (e.g., training_data/Talan/).

Open the script and put your email and Gmail App Password in the config section.

Run it and leave the camera pointed at the door.

Why I made this:
I originally tried using Microsoft Azure for the AI, but they have a lot of restrictions now. I switched to a local library called DeepFace so the AI runs entirely on my own gaming PC. It’s faster, free, and more private.
