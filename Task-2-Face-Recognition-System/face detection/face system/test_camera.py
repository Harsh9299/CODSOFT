"""
Camera Diagnostic Tool
Checks if camera is accessible and lists available cameras
"""

import cv2
import sys


def test_camera_indices():
    """Test camera indices 0-5 to find available cameras"""
    print("="*60)
    print("Camera Detection Test")
    print("="*60)
    
    available_cameras = []
    
    for index in range(6):
        print(f"\nTesting Camera {index}...", end=" ")
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # Use DirectShow backend
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✓ WORKING (Resolution: {frame.shape[1]}x{frame.shape[0]})")
                available_cameras.append(index)
            else:
                print("✗ Opened but can't read frames")
            cap.release()
        else:
            print("✗ Not available")
    
    print("\n" + "="*60)
    if available_cameras:
        print(f"✓ Found {len(available_cameras)} working camera(s): {available_cameras}")
        print("\nYou can use these cameras with:")
        for cam in available_cameras:
            print(f"  .venv\\Scripts\\python.exe main.py --camera {cam}")
        return True
    else:
        print("✗ No working cameras found!")
        print("\nPossible issues:")
        print("  1. No webcam is connected")
        print("  2. Camera is being used by another application")
        print("  3. Camera driver issues")
        print("  4. Windows Camera privacy settings blocking access")
        print("\nTroubleshooting:")
        print("  - Try opening Windows Camera app to test")
        print("  - Close other apps that might use camera (Teams, Zoom, etc.)")
        print("  - Restart your computer")
        print("  - Check Device Manager for camera status")
        return False


def test_camera_live(camera_index=0):
    """Test camera with live preview"""
    print(f"\n{'='*60}")
    print(f"Live Camera Test (Camera {camera_index})")
    print("Press 'q' to quit")
    print("="*60)
    
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print(f"✗ Could not open camera {camera_index}")
        return False
    
    print("✓ Camera opened successfully")
    print("Opening preview window...")
    
    frame_count = 0
    while frame_count < 300:  # Run for ~10 seconds at 30fps
        ret, frame = cap.read()
        
        if not ret:
            print(f"✗ Failed to read frame {frame_count}")
            break
        
        frame_count += 1
        
        # Add info to frame
        cv2.putText(frame, f"Camera {camera_index} - Frame {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        
        cv2.imshow('Camera Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"✓ Test complete! Processed {frame_count} frames")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("WEBCAM DIAGNOSTIC TOOL")
    print("="*60)
    
    # Test for available cameras
    has_camera = test_camera_indices()
    
    if has_camera:
        print("\n" + "="*60)
        response = input("\nWould you like to test camera with live preview? (y/n): ").strip().lower()
        
        if response == 'y':
            camera_index = input("Enter camera index to test (default 0): ").strip()
            camera_index = int(camera_index) if camera_index.isdigit() else 0
            test_camera_live(camera_index)
    else:
        print("\n" + "="*60)
        print("RECOMMENDATION:")
        print("Since no camera was detected, you can:")
        print("1. Test with image files instead of webcam")
        print("2. Fix your camera hardware/drivers first")
        print("="*60)
    
    print("\n✓ Diagnostic complete!")
