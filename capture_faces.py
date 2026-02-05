import cv2
import os

# 1. Choose who you are photographing right now
NAME = "Matthew"  # Change this to "Myles" when it's his turn
folder = f"training_data/{NAME}"

if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(0)

# Setting to 720p as we discussed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print(f"--- PHOTO BOOTH FOR: {NAME} ---")
print("Press 's' to take a photo. Press 'q' to finish.")

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Training Photos", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        img_path = os.path.join(folder, f"{NAME}_{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Saved: {img_path}")
        count += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()