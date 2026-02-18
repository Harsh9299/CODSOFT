"""
RAW Camera Feed - No Processing
Just displays the camera feed to verify video is visible
"""
import cv2
import time

print("Opening camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()

print("Camera opened successfully!")
print("Configuring...")

# Use lower resolution for compatibility
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Warming up...")
time.sleep(2)

# Read and check first 5 frames
print("\nChecking first 5 frames:")
for i in range(5):
    ret, frame = cap.read()
    if ret and frame is not None:
        print(f"  Frame {i+1}: OK - Shape: {frame.shape}, Min pixel: {frame.min()}, Max pixel: {frame.max()}")
    else:
        print(f"  Frame {i+1}: FAILED")

print("\nStarting video display... Press 'q' to quit")
print("Look for the 'RAW CAMERA FEED' window")
print("-" * 50)

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print(f"ERROR reading frame {frame_count}")
        break
    
    frame_count += 1
    
    # Calculate FPS
    elapsed = time.time() - start_time
    fps = frame_count / elapsed if elapsed > 0 else 0
    
    # Add text overlays
    cv2.putText(frame, f"RAW CAMERA FEED", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Frame: {frame_count}", (10, 70),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 110),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'q' to quit", (10, 150),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    
    # Show frame
    cv2.imshow('RAW CAMERA FEED', frame)
    
    # Check for 'q' key
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print(f"\nQuitting after {frame_count} frames")
        break

cap.release()
cv2.destroyAllWindows()
print("Done!")
