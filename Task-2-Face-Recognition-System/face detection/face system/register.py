"""
Face Registration Module
Handles registration of new faces via webcam
"""

import cv2
import time
from detect import FaceDetector
from recognize import FaceRecognizer
from typing import Optional


class FaceRegistration:
    """
    Handles the process of registering new faces
    Captures multiple samples for better recognition accuracy
    """
    
    def __init__(self, detector: FaceDetector, recognizer: FaceRecognizer,
                 samples_required: int = 5):
        """
        Initialize face registration system
        
        Args:
            detector: Face detector instance
            recognizer: Face recognizer instance
            samples_required: Number of face samples to capture per person
        """
        self.detector = detector
        self.recognizer = recognizer
        self.samples_required = samples_required
        
        print(f"[INFO] Face Registration initialized")
        print(f"[INFO] Samples required per person: {samples_required}")
    
    def register_new_face(self, name: str, camera_index: int = 0) -> bool:
        """
        Register a new face by capturing samples from webcam
        
        Args:
            name: Name/identifier for the person
            camera_index: Camera device index (default: 0)
            
        Returns:
            True if registration successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Registering new face: {name}")
        print(f"{'='*60}")
        
        # Check if name already exists
        if name in self.recognizer.list_registered_faces():
            print(f"[WARNING] '{name}' already registered")
            response = input("Add more samples? (y/n): ").strip().lower()
            if response != 'y':
                return False
        
        # Open webcam with DirectShow backend (better for Windows)
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("[ERROR] Could not open webcam")
            return False
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        samples_captured = 0
        capturing = False
        countdown = 3
        last_capture_time = 0
        capture_interval = 0.5  # Seconds between captures
        
        print("\n[INSTRUCTIONS]")
        print("  - Position your face in the camera frame")
        print("  - Press 's' to start capturing samples")
        print("  - Press 'q' to quit registration")
        print("  - Keep your face visible and vary angles slightly")
        
        try:
            while samples_captured < self.samples_required:
                ret, frame = cap.read()
                
                if not ret:
                    print("[ERROR] Failed to read frame")
                    break
                
                # Create display frame
                display_frame = frame.copy()
                
                # Detect faces
                detections = self.detector.detect_faces(frame)
                
                # Filter to largest face only
                if len(detections) > 0:
                    largest_detection = max(detections, 
                                           key=lambda d: d['box'][2] * d['box'][3])
                    detections = [largest_detection]
                
                # Draw detection box
                if len(detections) > 0:
                    box = detections[0]['box']
                    x, y, w, h = box
                    
                    if capturing:
                        color = (0, 255, 0)  # Green when capturing
                        label = f"Capturing... ({samples_captured}/{self.samples_required})"
                    else:
                        color = (0, 165, 255)  # Orange when ready
                        label = "Press 's' to start"
                    
                    # Draw bounding box
                    cv2.rectangle(display_frame, (x, y), (x + w, y + h), color, 2)
                    
                    # Draw label
                    cv2.putText(display_frame, label, (x, y - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    
                    # Capture samples automatically when started
                    if capturing:
                        current_time = time.time()
                        
                        if current_time - last_capture_time >= capture_interval:
                            # Extract face region
                            face_region = self.detector.get_face_region(frame, box, padding=20)
                            
                            if face_region is not None:
                                # Register the face
                                success = self.recognizer.register_face(name, face_region)
                                
                                if success:
                                    samples_captured += 1
                                    last_capture_time = current_time
                                    print(f"[INFO] Sample {samples_captured}/{self.samples_required} captured")
                                    
                                    # Visual feedback - flash effect
                                    cv2.rectangle(display_frame, (0, 0), 
                                                (display_frame.shape[1], display_frame.shape[0]),
                                                (0, 255, 0), 10)
                else:
                    # No face detected
                    cv2.putText(display_frame, "No face detected", (20, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Display status information
                status_y = 30
                cv2.putText(display_frame, f"Registering: {name}", (20, status_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                status_y += 30
                cv2.putText(display_frame, f"Samples: {samples_captured}/{self.samples_required}",
                           (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Progress bar
                bar_width = 400
                bar_height = 20
                bar_x, bar_y = 20, display_frame.shape[0] - 40
                progress = samples_captured / self.samples_required
                
                # Draw progress bar background
                cv2.rectangle(display_frame, (bar_x, bar_y),
                            (bar_x + bar_width, bar_y + bar_height),
                            (50, 50, 50), -1)
                
                # Draw progress
                cv2.rectangle(display_frame, (bar_x, bar_y),
                            (bar_x + int(bar_width * progress), bar_y + bar_height),
                            (0, 255, 0), -1)
                
                # Progress percentage
                cv2.putText(display_frame, f"{int(progress * 100)}%",
                           (bar_x + bar_width + 10, bar_y + 15),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Show frame
                cv2.imshow('Face Registration', display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('s') and not capturing and len(detections) > 0:
                    capturing = True
                    print("[INFO] Starting capture...")
                elif key == ord('q'):
                    print("\n[INFO] Registration cancelled by user")
                    cap.release()
                    cv2.destroyAllWindows()
                    return False
            
            # Registration complete
            cap.release()
            cv2.destroyAllWindows()
            
            print(f"\n{'='*60}")
            print(f"✓ Registration complete for '{name}'!")
            print(f"✓ Captured {samples_captured} samples")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            cap.release()
            cv2.destroyAllWindows()
            return False
    
    def register_from_image(self, name: str, image_path: str) -> bool:
        """
        Register a face from an image file
        
        Args:
            name: Name/identifier for the person
            image_path: Path to image file
            
        Returns:
            True if registration successful
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"[ERROR] Could not read image: {image_path}")
                return False
            
            # Detect face
            detection = self.detector.detect_largest_face(image)
            
            if detection is None:
                print("[ERROR] No face detected in image")
                return False
            
            # Extract face region
            face_region = self.detector.get_face_region(image, detection['box'], padding=20)
            
            if face_region is None:
                print("[ERROR] Could not extract face region")
                return False
            
            # Register face
            success = self.recognizer.register_face(name, face_region)
            
            if success:
                print(f"[INFO] Successfully registered '{name}' from image")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Image registration failed: {e}")
            return False


def interactive_registration():
    """
    Interactive CLI for face registration
    """
    print("\n" + "="*60)
    print("Face Registration System")
    print("="*60)
    
    # Initialize components (use Haar for better performance)
    print("\n[INFO] Initializing system...")
    detector = FaceDetector(min_confidence=0.9, method='haar')
    recognizer = FaceRecognizer(similarity_threshold=0.6)
    registration = FaceRegistration(detector, recognizer, samples_required=5)
    
    # Show currently registered faces
    registered = recognizer.list_registered_faces()
    if registered:
        print(f"\n[INFO] Currently registered faces: {', '.join(registered)}")
    else:
        print("\n[INFO] No faces registered yet")
    
    while True:
        print("\n" + "-"*60)
        print("Options:")
        print("  1. Register new face (webcam)")
        print("  2. Register from image file")
        print("  3. List registered faces")
        print("  4. Delete a registered face")
        print("  5. Exit")
        print("-"*60)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            name = input("Enter person's name: ").strip()
            if name:
                registration.register_new_face(name)
            else:
                print("[ERROR] Name cannot be empty")
        
        elif choice == '2':
            name = input("Enter person's name: ").strip()
            image_path = input("Enter image path: ").strip()
            if name and image_path:
                registration.register_from_image(name, image_path)
            else:
                print("[ERROR] Name and image path required")
        
        elif choice == '3':
            stats = recognizer.get_database_stats()
            print(f"\nRegistered Faces: {stats['total_people']}")
            for i, name in enumerate(stats['registered_names'], 1):
                samples = len(recognizer.face_database[name])
                print(f"  {i}. {name} ({samples} samples)")
        
        elif choice == '4':
            name = input("Enter name to delete: ").strip()
            if name:
                recognizer.delete_face(name)
        
        elif choice == '5':
            print("\n[INFO] Exiting registration system")
            break
        
        else:
            print("[ERROR] Invalid choice")


if __name__ == "__main__":
    # Run interactive registration
    interactive_registration()
