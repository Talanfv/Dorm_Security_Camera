import cv2
import os
import time
import smtplib
from email.message import EmailMessage
from deepface import DeepFace

# --- CONFIG ---
BASE_PATH = "training_data"
AUTHORIZED_PEOPLE = [f for f in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, f))]
COOLDOWN_TIME = 10 
MOTION_THRESHOLD = 100000

# --- EMAIL CONFIG ---
SENDER_EMAIL = "YOUR_EMAIL_HERE"
SENDER_PASSWORD = "YOUR_PASSWORD_HERE"
RECEIVER_EMAIL = "YOUR_EMAIL_HERE" # Can be the same

def send_alert(image_path):
    msg = EmailMessage()
    msg['Subject'] = "🚨 DORM INTRUDER ALERT 🚨"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.set_content("Motion detected! Face not recognized. See attached photo.")

    with open(image_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename="intruder.jpg")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            print("📧 Alert email sent successfully!")
    except Exception as e:
        print(f"❌ Email failed: {e}")

# --- MAIN LOOP ---
cap = cv2.VideoCapture(0)
last_scan_time = 0
ret, frame1 = cap.read()
ret, frame2 = cap.read()

print("--- DORM GUARD: FULL SECURITY MODE ---")

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(cv2.GaussianBlur(gray, (5, 5), 0), 20, 255, cv2.THRESH_BINARY)
    
    if cv2.countNonZero(thresh) > MOTION_THRESHOLD and (time.time() - last_scan_time) > COOLDOWN_TIME:
        print("\n🏃 Motion! Scanning...")
        temp_path = "capture.jpg"
        cv2.imwrite(temp_path, frame2)
        
        found_match = False
        try:
            for person in AUTHORIZED_PEOPLE:
                person_folder = os.path.join(BASE_PATH, person)
                for photo_name in os.listdir(person_folder):
                    res = DeepFace.verify(img1_path=temp_path, 
                                          img2_path=os.path.join(person_folder, photo_name),
                                          model_name="Facenet512", enforce_detection=False)
                    if res["verified"] and res["distance"] < 0.25:
                        print(f"✅ Verified: {person}")
                        found_match = True
                        break
                if found_match: break
            
            if not found_match:
                print("🚨 INTRUDER! Sending email...")
                send_alert(temp_path)
            
            last_scan_time = time.time()
        except Exception as e:
            print(f"AI Error: {e}")

    cv2.imshow("Security Feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()