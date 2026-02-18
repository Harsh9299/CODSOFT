"""
Face Detection Module
Supports both MTCNN and Haar Cascade detection methods
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

try:
    from mtcnn import MTCNN
    MTCNN_AVAILABLE = True
except ImportError:
    MTCNN_AVAILABLE = False


class FaceDetector:
    """
    Face detector supporting multiple detection methods
    - MTCNN: More accurate but slower
    - Haar Cascade: Faster and more reliable on CPU
    """
    
    def __init__(self, min_confidence: float = 0.9, method: str = 'haar'):
        """
        Initialize the face detector
        
        Args:
            min_confidence: Minimum confidence threshold for detection (0.0 to 1.0)
            method: Detection method - 'mtcnn' or 'haar' (default: 'haar')
        """
        self.method = method.lower()
        self.min_confidence = min_confidence
        
        if self.method == 'mtcnn':
            if not MTCNN_AVAILABLE:
                print("[WARNING] MTCNN not available, falling back to Haar Cascade")
                self.method = 'haar'
            else:
                try:
                    self.detector = MTCNN()
                    print(f"[INFO] MTCNN Face Detector initialized (min confidence: {min_confidence})")
                except Exception as e:
                    print(f"[ERROR] Failed to initialize MTCNN: {e}")
                    print("[INFO] Falling back to Haar Cascade")
                    self.method = 'haar'
        
        if self.method == 'haar':
            # Load Haar Cascade classifier
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            print(f"[INFO] Haar Cascade Face Detector initialized")
    
    def detect_faces(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces in an image
        
        Args:
            image: Input image in BGR format (OpenCV format)
            
        Returns:
            List of dictionaries containing face detection results
            Each dict contains: 'box', 'confidence', 'keypoints' (for MTCNN)
        """
        try:
            if self.method == 'mtcnn':
                return self._detect_mtcnn(image)
            else:
                return self._detect_haar(image)
                
        except Exception as e:
            print(f"[ERROR] Face detection failed: {e}")
            return []
    
    def _detect_mtcnn(self, image: np.ndarray) -> List[dict]:
        """Detect faces using MTCNN"""
        # Convert BGR to RGB (MTCNN expects RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        detections = self.detector.detect_faces(rgb_image)
        
        # Filter by confidence threshold
        filtered_detections = [
            det for det in detections 
            if det['confidence'] >= self.min_confidence
        ]
        
        return filtered_detections
    
    def _detect_haar(self, image: np.ndarray) -> List[dict]:
        """Detect faces using Haar Cascade"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Convert to MTCNN-like format for compatibility
        detections = []
        for (x, y, w, h) in faces:
            detection = {
                'box': [x, y, w, h],
                'confidence': 1.0,  # Haar doesn't provide confidence
                'keypoints': {
                    'left_eye': (x + w//4, y + h//3),
                    'right_eye': (x + 3*w//4, y + h//3),
                    'nose': (x + w//2, y + h//2),
                    'mouth_left': (x + w//3, y + 2*h//3),
                    'mouth_right': (x + 2*w//3, y + 2*h//3)
                }
            }
            detections.append(detection)
        
        return detections
    
    def get_face_region(self, image: np.ndarray, box: List[int], 
                        padding: int = 20) -> Optional[np.ndarray]:
        """
        Extract face region from image with padding
        
        Args:
            image: Input image
            box: Bounding box [x, y, width, height]
            padding: Padding around face in pixels
            
        Returns:
            Cropped face image or None if extraction fails
        """
        try:
            x, y, w, h = box
            height, width = image.shape[:2]
            
            # Add padding and ensure within image boundaries
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(width, x + w + padding)
            y2 = min(height, y + h + padding)
            
            # Extract face region
            face = image[y1:y2, x1:x2]
            
            return face if face.size > 0 else None
            
        except Exception as e:
            print(f"[ERROR] Face extraction failed: {e}")
            return None
    
    def draw_detections(self, image: np.ndarray, detections: List[dict], 
                       label: str = None, confidence: float = None) -> np.ndarray:
        """
        Draw bounding boxes and labels on detected faces
        
        Args:
            image: Input image
            detections: List of face detections
            label: Optional label to display (e.g., person's name)
            confidence: Optional confidence score to display
            
        Returns:
            Image with drawn annotations
        """
        output = image.copy()
        
        for detection in detections:
            box = detection['box']
            det_confidence = detection['confidence']
            x, y, w, h = box
            
            # Determine color based on recognition
            color = (0, 255, 0) if label else (255, 0, 0)  # Green if recognized, Blue otherwise
            
            # Draw bounding box
            cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
            
            # Prepare text label
            if label:
                text = f"{label}"
                if confidence is not None:
                    text += f" ({confidence:.2f}%)"
            else:
                text = f"Face ({det_confidence:.2f})"
            
            # Draw label background
            (text_width, text_height), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                output, 
                (x, y - text_height - 10), 
                (x + text_width, y), 
                color, 
                -1
            )
            
            # Draw text
            cv2.putText(
                output, 
                text, 
                (x, y - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, 
                (255, 255, 255), 
                2
            )
            
            # Draw facial keypoints (optional)
            keypoints = detection['keypoints']
            for key, point in keypoints.items():
                cv2.circle(output, point, 2, (0, 255, 255), 2)
        
        return output
    
    def detect_largest_face(self, image: np.ndarray) -> Optional[dict]:
        """
        Detect and return only the largest face in the image
        Useful for registration where we expect one person
        
        Args:
            image: Input image
            
        Returns:
            Detection dict for largest face or None
        """
        detections = self.detect_faces(image)
        
        if not detections:
            return None
        
        # Find largest face by area
        largest = max(detections, key=lambda d: d['box'][2] * d['box'][3])
        return largest


# Utility function for quick face detection
def detect_faces_simple(image_path: str, min_confidence: float = 0.9) -> List[dict]:
    """
    Simple function to detect faces from an image file
    
    Args:
        image_path: Path to image file
        min_confidence: Minimum confidence threshold
        
    Returns:
        List of face detections
    """
    try:
        detector = FaceDetector(min_confidence)
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"[ERROR] Could not read image: {image_path}")
            return []
        
        return detector.detect_faces(image)
        
    except Exception as e:
        print(f"[ERROR] Detection failed: {e}")
        return []


if __name__ == "__main__":
    # Test the face detector
    print("Face Detection Module - Test Mode")
    print("-" * 50)
    
    # Initialize detector (Haar Cascade by default for better performance)
    detector = FaceDetector(min_confidence=0.9, method='haar')
    
    # Test with webcam
    print("\n[INFO] Testing with webcam... Press 'q' to quit")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces
            detections = detector.detect_faces(frame)
            
            # Draw detections
            output = detector.draw_detections(frame, detections)
            
            # Display info
            cv2.putText(
                output, 
                f"Faces detected: {len(detections)}", 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (0, 255, 0), 
                2
            )
            
            cv2.imshow('Face Detection Test', output)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Test completed")
