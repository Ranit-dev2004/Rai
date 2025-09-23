from deepface import DeepFace
import cv2
from rai_voice import speak

ALLOWED_PERSON = "Ranit Saha"
DB_PATH = "faces_db/"

def identity_detector():
    speak("Starting identity verification...")

    cap = cv2.VideoCapture(0)
    authorized = False

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to capture video.")
            break

        try:
            verification = DeepFace.find(frame, db_path=DB_PATH, enforce_detection=False)
            
            if len(verification) > 0:
                identity = ALLOWED_PERSON
                if not authorized:
                    speak(f"Identity verified: {identity}. You are allowed.")
                    authorized = True
                    break  # ✅ exit the loop once verified
            else:
                identity = "Unknown"
                if authorized:
                    speak("Identity mismatch — locking system.")
                    authorized = False

            cv2.putText(frame, f"Identity: {identity}", (20,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2, cv2.LINE_AA)
            cv2.imshow('RAI Identity Detector', frame)

            if cv2.waitKey(500) & 0xFF == ord('q'):
                break

        except Exception as e:
            print("Error:", e)
            speak("No face detected — access blocked.")
            authorized = False
            if cv2.waitKey(2000) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    speak("Identity detector stopped.")
