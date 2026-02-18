"""
Quick Start Guide - Face Recognition System
Run this script to get started quickly
"""

import sys
import subprocess


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70)


def check_installation():
    """Check if all required packages are installed"""
    print_header("Checking Installation")
    
    packages = {
        'cv2': 'opencv-python',
        'mtcnn': 'mtcnn',
        'tensorflow': 'tensorflow',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn'
    }
    
    missing = []
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✓ {package} - installed")
        except ImportError:
            print(f"✗ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\n[ERROR] Missing packages: {', '.join(missing)}")
        print("\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n✓ All packages installed successfully!")
    return True


def test_camera():
    """Test if camera is accessible"""
    print_header("Testing Camera")
    
    try:
        import cv2
        
        print("Attempting to open camera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Camera 0 not accessible")
            print("Try different camera indices: 1, 2, etc.")
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            print(f"✓ Camera working! Frame shape: {frame.shape}")
            return True
        else:
            print("✗ Could not read frame from camera")
            return False
            
    except Exception as e:
        print(f"✗ Error testing camera: {e}")
        return False


def quick_demo():
    """Run quick face detection demo"""
    print_header("Quick Face Detection Demo")
    
    try:
        from detect import FaceDetector
        import cv2
        
        print("\nInitializing face detector...")
        detector = FaceDetector(min_confidence=0.9)
        
        print("Opening camera... Press 'q' to quit")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("[ERROR] Could not open camera")
            return
        
        frames_processed = 0
        faces_detected = 0
        
        while frames_processed < 100:  # Run for ~3 seconds at 30fps
            ret, frame = cap.read()
            if not ret:
                break
            
            detections = detector.detect_faces(frame)
            output = detector.draw_detections(frame, detections)
            
            frames_processed += 1
            faces_detected += len(detections)
            
            cv2.putText(output, "Quick Demo - Press 'q' to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Face Detection Demo', output)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✓ Demo complete!")
        print(f"  Frames processed: {frames_processed}")
        print(f"  Total faces detected: {faces_detected}")
        
    except Exception as e:
        print(f"✗ Demo failed: {e}")


def main():
    """Main quick start function"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    Face Detection & Recognition System - Quick Start         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("\nThis script will help you get started with the face recognition system.")
    
    # Step 1: Check installation
    if not check_installation():
        print("\n[!] Please install missing packages first.")
        return
    
    input("\nPress Enter to continue to camera test...")
    
    # Step 2: Test camera
    if not test_camera():
        print("\n[!] Camera test failed. Please check your camera connection.")
        print("    You can still proceed, but the application won't work without a camera.")
    
    input("\nPress Enter to run quick face detection demo...")
    
    # Step 3: Quick demo
    quick_demo()
    
    # Step 4: Next steps
    print_header("Next Steps")
    print("""
1. REGISTER FACES:
   Run: python register.py
   Or press 'r' in main application
   
2. START RECOGNITION:
   Run: python main.py
   
3. KEYBOARD CONTROLS (in main application):
   - 'r' : Register new face
   - 'l' : List registered faces
   - 'd' : Delete a face
   - 'f' : Toggle FPS display
   - 'h' : Show help
   - 'q' : Quit

4. COMMAND LINE OPTIONS:
   python main.py --camera 1          # Use different camera
   python main.py --threshold 0.7     # Adjust recognition threshold
   
5. READ DOCUMENTATION:
   See README.md for complete documentation
    """)
    
    print("\n" + "="*70)
    print("Ready to start? Run: python main.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
