"""
Face Recognition with Haar Cascade Detection
More reliable and faster than MTCNN
"""

import cv2
import time
import numpy as np
from recognize import FaceRecognizer

class HaarFaceDetector:
    """Face detector using Haar Cascades (faster, more reliable)"""
    
    def __init__(self):
        # Load pre-trained Haar Cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        print("[INFO] Haar Cascade Face Detector loaded")
    
    def detect_faces(self, image):
        """Detect faces using Haar Cascade"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def get_face_region(self, image, box, padding=20):
        """Extract face region"""
        x, y, w, h = box
        height, width = image.shape[:2]
        
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(width, x + w + padding)
        y2 = min(height, y + h + padding)
        
        return image[y1:y2, x1:x2]


print("\n" + "="*70)
print("Face Recognition System - Haar Cascade Version")
print("="*70)

# Initialize
print("\n[INFO] Loading components...")
detector = HaarFaceDetector()
recognizer = FaceRecognizer(similarity_threshold=0.6)

print("[INFO] Opening camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("[ERROR] Could not open camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

print("[INFO] Warming up...")
time.sleep(1)
for _ in range(5):
    cap.read()

print("\n" + "="*70)
print("RUNNING - Press 'q' to quit, 'r' to register faces")
print("="*70 + "\n")

# Performance tracking
fps_start = time.time()
fps_counter = 0
current_fps = 0
process_every = 3  # Process every 3rd frame
frame_num = 0
last_faces = []

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            continue
        
        frame_num += 1
        fps_counter += 1
        
        # Calculate FPS
        if time.time() - fps_start >= 1.0:
            current_fps = fps_counter / (time.time() - fps_start)
            fps_counter = 0
            fps_start = time.time()
        
        # Detect faces periodically
        if frame_num % process_every == 0:
            faces = detector.detect_faces(frame)
            last_faces = faces
        else:
            faces = last_faces
        
        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract face for recognition
            face_region = detector.get_face_region(frame, (x, y, w, h), padding=20)
            
            if face_region is not None and face_region.size > 0:
                # Recognize face
                name, confidence = recognizer.recognize_face(face_region)
                
                # Draw box and label
                if name:
                    color = (0, 255, 0)  # Green for recognized
                    label = f"{name} ({confidence:.0f}%)"
                else:
                    color = (0, 0, 255)  # Red for unknown
                    label = "Unknown"
                
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                
                # Draw label background
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                cv2.rectangle(frame, (x, y-35), (x+text_w+10, y), color, -1)
                cv2.putText(frame, label, (x+5, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Info panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (640, 90), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        cv2.putText(frame, "FACE RECOGNITION SYSTEM", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {current_fps:.1f} | Faces: {len(faces)} | Registered: {len(recognizer.list_registered_faces())}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, "Press 'q' to quit", (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Display
        cv2.imshow('Face Recognition System', frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n[INFO] Quitting...")
            break
        elif key == ord('r'):
            cap.release()
            cv2.destroyAllWindows()
            
            # Registration
            from register import FaceRegistration
            registration = FaceRegistration(detector, recognizer, samples_required=5)
            name = input("\nEnter person's name: ").strip()
            if name:
                registration.register_new_face(name, 0)
            
            # Reopen camera
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print("\n[INFO] Resuming...")

except KeyboardInterrupt:
    print("\n[INFO] Interrupted")
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Done!")
