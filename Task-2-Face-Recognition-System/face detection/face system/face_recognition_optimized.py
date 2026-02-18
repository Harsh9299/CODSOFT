"""
Optimized Face Recognition System
Lightweight version for better performance
"""

import cv2
import time
import numpy as np
from detect import FaceDetector
from recognize import FaceRecognizer

print("\n" + "="*70)
print("Face Recognition System - Optimized Version")
print("="*70)

# Initialize with lower settings for performance
print("\n[INFO] Loading face detector...")
detector = FaceDetector(min_confidence=0.9)

print("[INFO] Loading face recognizer...")
recognizer = FaceRecognizer(similarity_threshold=0.6)

print("[INFO] Opening camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("[ERROR] Could not open camera")
    exit()

# Use moderate resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("[INFO] Warming up camera...")
time.sleep(1)

# Discard first few frames
for _ in range(5):
    cap.read()

print("\n" + "="*70)
print("CONTROLS:")
print("  'q' - Quit")
print("  'r' - Register new face")
print("  'l' - List registered faces")
print("="*70)
print("\n[INFO] Starting... Look for the window!")

# Performance settings
process_every = 5  # Only process every 5th frame for speed
frame_num = 0
last_detections = []
fps_start = time.time()
fps_counter = 0
current_fps = 0

try:
    while True:
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("[WARNING] Failed to read frame")
            continue
        
        frame_num += 1
        fps_counter += 1
        
        # Calculate FPS
        if time.time() - fps_start >= 1.0:
            current_fps = fps_counter / (time.time() - fps_start)
            fps_counter = 0
            fps_start = time.time()
        
        # Only run detection periodically
        if frame_num % process_every == 0:
            try:
                detections = detector.detect_faces(frame)
                last_detections = detections
                
                # Process each face
                for detection in detections:
                    box = detection['box']
                    x, y, w, h = box
                    
                    # Extract and recognize face
                    face_region = detector.get_face_region(frame, box, padding=20)
                    if face_region is not None:
                        name, confidence = recognizer.recognize_face(face_region)
                        
                        # Draw box and label
                        if name:
                            color = (0, 255, 0)  # Green for recognized
                            label = f"{name} ({confidence:.0f}%)"
                        else:
                            color = (0, 0, 255)  # Red for unknown
                            label = "Unknown"
                        
                        # Draw bounding box
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        
                        # Draw label background
                        cv2.rectangle(frame, (x, y-30), (x+200, y), color, -1)
                        cv2.putText(frame, label, (x+5, y-8),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            except Exception as e:
                print(f"[WARNING] Detection error: {str(e)[:50]}")
        else:
            # Draw cached detections on non-processing frames
            for detection in last_detections:
                box = detection['box']
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        
        # Add info panel
        panel_height = 100
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (640, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        
        # Display info
        cv2.putText(frame, "FACE RECOGNITION SYSTEM", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(frame, f"Faces: {len(last_detections)}", (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(frame, "Press 'q' to quit, 'r' to register", (140, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Show frame
        cv2.imshow('Face Recognition System', frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n[INFO] Quitting...")
            break
        elif key == ord('r'):
            print("\n[INFO] Press 'q' in this window first, then register")
        elif key == ord('l'):
            registered = recognizer.list_registered_faces()
            print(f"\n[INFO] Registered faces: {registered if registered else 'None'}")

except KeyboardInterrupt:
    print("\n[INFO] Interrupted by user")
except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Cleanup complete")
