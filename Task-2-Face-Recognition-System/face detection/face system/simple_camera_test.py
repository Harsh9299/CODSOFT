"""
Simple camera feed test
"""
import cv2
import time

print("Opening camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Give camera time to initialize
time.sleep(2)

print("Camera opened:", cap.isOpened())

if cap.isOpened():
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Starting video feed... Press 'q' to quit")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if ret:
            frame_count += 1
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Simple Camera Test', frame)
        else:
            print(f"Failed to read frame {frame_count}")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("Test complete")
