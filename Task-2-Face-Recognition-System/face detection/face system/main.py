"""
Real-Time Face Recognition Application
Main entry point for the face recognition system
"""

import cv2
import time
import argparse
from detect import FaceDetector
from recognize import FaceRecognizer
from register import FaceRegistration
from typing import Dict, List


class FaceRecognitionApp:
    """
    Real-time face recognition application
    Combines detection and recognition for live video processing
    """
    
    def __init__(self, camera_index: int = 0, min_confidence: float = 0.9,
                 similarity_threshold: float = 0.6, detection_method: str = 'haar'):
        """
        Initialize the face recognition application
        
        Args:
            camera_index: Camera device index
            min_confidence: Minimum confidence for face detection
            similarity_threshold: Minimum similarity for face recognition
            detection_method: Detection method - 'haar' (faster) or 'mtcnn' (more accurate)
        """
        print("\n" + "="*70)
        print("Face Recognition System - Initialization")
        print("="*70)
        
        # Initialize components
        print(f"\n[INFO] Loading face detector ({detection_method.upper()})...")
        self.detector = FaceDetector(min_confidence=min_confidence, method=detection_method)
        
        print("[INFO] Loading face recognizer...")
        self.recognizer = FaceRecognizer(similarity_threshold=similarity_threshold)
        
        print("[INFO] Initializing registration system...")
        self.registration = FaceRegistration(self.detector, self.recognizer)
        
        self.camera_index = camera_index
        self.running = False
        
        # Performance metrics
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        # Display settings
        self.show_fps = True
        self.show_landmarks = False
        
        # Performance optimization - process every Nth frame
        self.process_every_n_frames = 3  # Process every 3rd frame for speed
        self.current_frame_num = 0
        self.last_detections = []  # Cache last detections
        
        print("\n[INFO] System ready!")
        self._print_controls()
    
    def _print_controls(self):
        """Print keyboard controls"""
        print("\n" + "-"*70)
        print("Keyboard Controls:")
        print("  'q' - Quit application")
        print("  'r' - Register new face")
        print("  'l' - List registered faces")
        print("  'd' - Delete a face from database")
        print("  'f' - Toggle FPS display")
        print("  'k' - Toggle facial keypoints")
        print("  'h' - Show this help")
        print("-"*70 + "\n")
    
    def _calculate_fps(self) -> float:
        """
        Calculate current FPS
        
        Returns:
            Current frames per second
        """
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        
        if elapsed_time > 1.0:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()
        
        return self.fps
    
    def _draw_info_panel(self, frame, detections: List[dict], 
                        recognition_results: Dict):
        """
        Draw information panel on frame
        
        Args:
            frame: Input frame
            detections: List of face detections
            recognition_results: Dictionary of recognition results
        """
        height, width = frame.shape[:2]
        
        # Semi-transparent panel background
        overlay = frame.copy()
        panel_height = 120
        cv2.rectangle(overlay, (0, 0), (width, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Title
        cv2.putText(frame, "Face Recognition System", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Statistics
        stats_y = 60
        cv2.putText(frame, f"Faces Detected: {len(detections)}", (10, stats_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        stats_y += 25
        registered = len(self.recognizer.list_registered_faces())
        cv2.putText(frame, f"Registered: {registered}", (10, stats_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # FPS
        if self.show_fps:
            fps_text = f"FPS: {self.fps:.1f}"
            cv2.putText(frame, fps_text, (width - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Controls hint
        cv2.putText(frame, "Press 'h' for help", (10, stats_y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    def _process_frame(self, frame):
        """
        Process a single frame for face detection and recognition
        
        Args:
            frame: Input video frame
            
        Returns:
            Processed frame with annotations
        """
        # Increment frame counter
        self.current_frame_num += 1
        
        # Only process every Nth frame for performance
        if self.current_frame_num % self.process_every_n_frames == 0:
            # Detect faces
            detections = self.detector.detect_faces(frame)
            self.last_detections = detections  # Cache for next frames
        else:
            # Use cached detections for intermediate frames
            detections = self.last_detections
        
        # Recognition results storage
        recognition_results = {}
        
        # Process each detected face
        for i, detection in enumerate(detections):
            box = detection['box']
            confidence = detection['confidence']
            
            # Extract face region for recognition
            face_region = self.detector.get_face_region(frame, box, padding=20)
            
            # Recognize face
            name, similarity_score = None, 0.0
            if face_region is not None:
                name, similarity_score = self.recognizer.recognize_face(face_region)
            
            # Store result
            recognition_results[i] = {
                'name': name,
                'confidence': similarity_score,
                'box': box
            }
            
            # Draw bounding box and label
            x, y, w, h = box
            
            if name:
                # Recognized face - green box
                color = (0, 255, 0)
                label = f"{name}"
                confidence_text = f"{similarity_score:.1f}%"
            else:
                # Unknown face - red box
                color = (0, 0, 255)
                label = "Unknown"
                confidence_text = f"Det: {confidence:.2f}"
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            
            # Draw label background
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.rectangle(frame, (x, y - 35), (x + label_size[0] + 10, y), color, -1)
            
            # Draw label text
            cv2.putText(frame, label, (x + 5, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Draw confidence/similarity score
            score_y = y + h + 25
            cv2.putText(frame, confidence_text, (x, score_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw facial keypoints (if enabled)
            if self.show_landmarks:
                keypoints = detection['keypoints']
                for key, point in keypoints.items():
                    cv2.circle(frame, point, 3, (0, 255, 255), -1)
        
        # Draw info panel
        self._draw_info_panel(frame, detections, recognition_results)
        
        return frame
    
    def run(self):
        """
        Run the face recognition application
        Main loop for real-time video processing
        """
        print("\n[INFO] Starting camera...")
        
        # Open webcam with DirectShow backend (better for Windows)
        cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("[ERROR] Could not open camera")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Give camera time to initialize and warm up
        print("[INFO] Warming up camera...")
        time.sleep(2)
        
        # Read and discard first few frames (they may be black)
        for _ in range(5):
            cap.read()
        
        print("[INFO] Camera ready. Application running...")
        self.running = True
        
        try:
            while self.running:
                # Read frame
                ret, frame = cap.read()
                
                if not ret or frame is None:
                    print("[WARNING] Failed to read frame")
                    continue
                
                # Verify frame has data
                if frame.size == 0:
                    print("[WARNING] Empty frame received")
                    continue
                
                # Calculate FPS
                self._calculate_fps()
                
                # Process frame
                processed_frame = self._process_frame(frame)
                
                # Verify processed frame
                if processed_frame is None or processed_frame.size == 0:
                    processed_frame = frame
                
                # Display frame
                cv2.imshow('Face Recognition System', processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    # Quit
                    print("\n[INFO] Shutting down...")
                    self.running = False
                
                elif key == ord('r'):
                    # Register new face
                    print("\n[INFO] Entering registration mode...")
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    name = input("Enter person's name: ").strip()
                    if name:
                        self.registration.register_new_face(name, self.camera_index)
                    
                    # Reopen camera
                    cap = cv2.VideoCapture(self.camera_index)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                    print("\n[INFO] Resuming face recognition...")
                
                elif key == ord('l'):
                    # List registered faces
                    registered = self.recognizer.list_registered_faces()
                    print("\n" + "-"*50)
                    print(f"Registered Faces ({len(registered)}):")
                    for i, name in enumerate(registered, 1):
                        samples = len(self.recognizer.face_database[name])
                        print(f"  {i}. {name} ({samples} samples)")
                    print("-"*50)
                
                elif key == ord('d'):
                    # Delete face
                    registered = self.recognizer.list_registered_faces()
                    if registered:
                        print("\n" + "-"*50)
                        print("Registered faces:")
                        for i, name in enumerate(registered, 1):
                            print(f"  {i}. {name}")
                        print("-"*50)
                        name = input("Enter name to delete: ").strip()
                        if name:
                            self.recognizer.delete_face(name)
                    else:
                        print("\n[INFO] No faces registered")
                
                elif key == ord('f'):
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                
                elif key == ord('k'):
                    # Toggle keypoints
                    self.show_landmarks = not self.show_landmarks
                
                elif key == ord('h'):
                    # Show help
                    self._print_controls()
        
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user")
        
        except Exception as e:
            print(f"\n[ERROR] Application error: {e}")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            print("\n[INFO] Application closed")


def main():
    """
    Main entry point
    Parse arguments and start application
    """
    parser = argparse.ArgumentParser(
        description='Real-Time Face Detection and Recognition System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run with default settings
  python main.py --camera 1         # Use camera index 1
  python main.py --threshold 0.7    # Set similarity threshold to 0.7
  
For first-time use:
  1. Run the application
  2. Press 'r' to register faces
  3. After registration, faces will be recognized automatically
        """
    )
    
    parser.add_argument('--camera', type=int, default=0,
                       help='Camera device index (default: 0)')
    
    parser.add_argument('--confidence', type=float, default=0.9,
                       help='Face detection confidence threshold (default: 0.9)')
    
    parser.add_argument('--threshold', type=float, default=0.6,
                       help='Face recognition similarity threshold (default: 0.6)')
    
    parser.add_argument('--method', type=str, default='haar',
                       choices=['haar', 'mtcnn'],
                       help='Face detection method: haar (fast) or mtcnn (accurate) (default: haar)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.confidence < 0.0 or args.confidence > 1.0:
        print("[ERROR] Confidence must be between 0.0 and 1.0")
        return
    
    if args.threshold < 0.0 or args.threshold > 1.0:
        print("[ERROR] Threshold must be between 0.0 and 1.0")
        return
    
    # Create and run application
    app = FaceRecognitionApp(
        camera_index=args.camera,
        min_confidence=args.confidence,
        similarity_threshold=args.threshold,
        detection_method=args.method
    )
    
    app.run()


if __name__ == "__main__":
    main()
