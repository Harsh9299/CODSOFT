"""
Diagnostic Face Recognition App - Shows what's happening
"""
import cv2
import time
from detect import FaceDetector
from recognize import FaceRecognizer

print("\n" + "="*70)
print("Diagnostic Mode - Face Recognition")
print("="*70)

# Initialize
print("\n[1/5] Loading face detector...")
detector = FaceDetector(min_confidence=0.9)

print("[2/5] Loading face recognizer...")
recognizer = FaceRecognizer(similarity_threshold=0.6)

print("[3/5] Opening camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Could not open camera!")
    exit()

print("[4/5] Configuring camera...")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("[5/5] Warming up camera...")
time.sleep(2)

# Discard first frames
for i in range(10):
    ret, frame = cap.read()
    print(f"  Warmup frame {i+1}: ret={ret}, frame={'OK' if frame is not None else 'NULL'}", end="")
    if frame is not None:
        print(f", shape={frame.shape}")
    else:
        print()

print("\n" + "="*70)
print("Starting main loop... Press 'q' to quit")
print("="*70)

frame_num = 0
detect_every = 3

try:
    while True:
        ret, frame = cap.read()
        frame_num += 1
        
        if not ret or frame is None:
            print(f"Frame {frame_num}: FAILED to read")
            continue
        
        # Only detect every N frames
        if frame_num % detect_every == 0:
            detections = detector.detect_faces(frame)
            print(f"Frame {frame_num}: Detected {len(detections)} faces")
            
            # Draw detections
            output = detector.draw_detections(frame, detections)
        else:
            output = frame.copy()
        
        # Add info overlay
        cv2.putText(output, f"Frame: {frame_num}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(output, "Press 'q' to quit", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        
        cv2.imshow('Diagnostic Face Recognition', output)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nQuitting...")
            break

except KeyboardInterrupt:
    print("\nInterrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup complete")
