# Real-Time Face Detection and Recognition System

A production-ready Python application for real-time face detection and recognition using MTCNN and FaceNet embeddings. Built as a portfolio project demonstrating computer vision and deep learning capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)

## 🎯 Features

- **Accurate Face Detection**: MTCNN (Multi-task Cascaded Convolutional Networks) for robust face detection
- **Face Recognition**: FaceNet-based 128-dimensional embeddings with cosine similarity matching
- **Real-time Processing**: Live webcam feed processing with FPS display
- **Face Registration**: Easy-to-use interface for registering new faces via webcam or images
- **Confidence Scores**: Display recognition confidence for each detected face
- **Persistent Storage**: Local database for face embeddings using NumPy and Pickle
- **Modular Architecture**: Clean, maintainable code structure suitable for professional portfolios
- **Error Handling**: Graceful error handling throughout the application
- **Interactive Controls**: Keyboard shortcuts for all major functions

## 📁 Project Structure

```
face-recognition-system/
│
├── detect.py          # Face detection using MTCNN
├── recognize.py       # Face recognition with embeddings
├── register.py        # Face registration system
├── main.py           # Main application entry point
├── face_database.pkl # Stored face embeddings (created automatically)
└── README.md         # Documentation
```

## 🔧 Requirements

- Python 3.8 or higher
- Webcam/Camera device

### Python Packages

```
opencv-python
mtcnn
tensorflow
numpy
scikit-learn
```

## 📦 Installation

1. **Clone or download this repository**

2. **Install required packages:**

```bash
pip install opencv-python mtcnn tensorflow numpy scikit-learn
```

3. **Verify installation:**

```bash
python -c "import cv2, mtcnn, tensorflow; print('All packages installed successfully!')"
```

## 🚀 Usage

### Quick Start

Run the main application:

```bash
python main.py
```

### Command Line Arguments

```bash
# Use a different camera
python main.py --camera 1

# Adjust face detection confidence
python main.py --confidence 0.85

# Adjust recognition similarity threshold
python main.py --threshold 0.65

# Combine arguments
python main.py --camera 1 --threshold 0.7
```

### Keyboard Controls

While the application is running:

| Key | Action |
|-----|--------|
| `r` | Register a new face |
| `l` | List all registered faces |
| `d` | Delete a face from database |
| `f` | Toggle FPS display |
| `k` | Toggle facial keypoints overlay |
| `h` | Show help/controls |
| `q` | Quit application |

## 📝 Workflow

### 1. First-Time Setup

1. Run the application: `python main.py`
2. Press `r` to enter registration mode
3. Enter the person's name when prompted
4. Position your face in the camera frame
5. Press `s` to start capturing samples
6. Keep face visible while 5 samples are captured
7. Registration complete!

### 2. Real-Time Recognition

After registration, faces will be automatically recognized:
- **Green boxes**: Recognized faces with name and confidence score
- **Red boxes**: Unknown/unrecognized faces
- **Confidence percentage**: Shows recognition accuracy

### 3. Managing Faces

- Press `l` to view all registered faces
- Press `d` to remove a face from the database
- Re-register a face to add more samples for better accuracy

## 🧩 Module Overview

### detect.py - Face Detection

Contains the `FaceDetector` class using MTCNN:

```python
from detect import FaceDetector

detector = FaceDetector(min_confidence=0.9)
detections = detector.detect_faces(image)
```

**Key Features:**
- MTCNN-based face detection
- Facial landmark detection (eyes, nose, mouth)
- Bounding box extraction
- Visualization utilities

### recognize.py - Face Recognition

Contains the `FaceRecognizer` class for face embeddings:

```python
from recognize import FaceRecognizer

recognizer = FaceRecognizer(similarity_threshold=0.6)
name, confidence = recognizer.recognize_face(face_image)
```

**Key Features:**
- 128-dimensional face embeddings using FaceNet architecture
- Cosine similarity for face matching
- Persistent database storage
- Support for multiple samples per person

### register.py - Face Registration

Contains the `FaceRegistration` class:

```python
from register import FaceRegistration

registration = FaceRegistration(detector, recognizer)
registration.register_new_face(name="John Doe")
```

**Key Features:**
- Interactive webcam-based registration
- Automatic sample capture
- Visual feedback and progress tracking
- Image file registration support

### main.py - Main Application

The complete real-time face recognition system:

```python
python main.py
```

**Key Features:**
- Real-time video processing
- Integrated detection and recognition
- Interactive user interface
- Performance metrics (FPS)

## 🎓 Technical Details

### Face Detection Pipeline

1. **Input**: Video frame from webcam (BGR format)
2. **Conversion**: BGR → RGB for MTCNN
3. **Detection**: MTCNN detects faces and landmarks
4. **Filtering**: Apply confidence threshold
5. **Output**: Bounding boxes and keypoints

### Face Recognition Pipeline

1. **Input**: Detected face region
2. **Preprocessing**: Resize to 160×160, normalize
3. **Embedding**: Generate 128-d vector via FaceNet
4. **Normalization**: L2 normalize embedding
5. **Comparison**: Cosine similarity with database
6. **Decision**: Match if similarity > threshold

### Similarity Calculation

The system uses **cosine similarity** to compare face embeddings:

```
similarity = (dot(embedding1, embedding2) + 1) / 2
```

This produces a score between 0 (completely different) and 1 (identical).

## ⚙️ Configuration

### Adjusting Detection Sensitivity

In `detect.py`, modify `min_confidence`:

```python
detector = FaceDetector(min_confidence=0.9)  # Higher = stricter (default: 0.9)
```

### Adjusting Recognition Threshold

In `recognize.py`, modify `similarity_threshold`:

```python
recognizer = FaceRecognizer(similarity_threshold=0.6)  # Higher = stricter (default: 0.6)
```

**Recommended values:**
- **High security**: 0.7 - 0.8 (may reject valid faces)
- **Balanced**: 0.6 - 0.7 (recommended)
- **Lenient**: 0.5 - 0.6 (may accept similar faces)

### Registration Samples

In `register.py`, modify `samples_required`:

```python
registration = FaceRegistration(
    detector, 
    recognizer, 
    samples_required=5  # More samples = better accuracy
)
```

## 🐛 Troubleshooting

### Camera Not Opening

```
[ERROR] Could not open webcam
```

**Solution**: Change camera index
```bash
python main.py --camera 0  # Try 0, 1, 2, etc.
```

### No Face Detected

**Possible causes:**
- Poor lighting conditions
- Face too far from camera
- Face partially occluded
- Low detection confidence

**Solutions:**
- Improve lighting
- Move closer to camera
- Ensure face is fully visible
- Lower confidence threshold: `--confidence 0.8`

### Recognition Not Working

**Possible causes:**
- No faces registered
- Low similarity threshold
- Insufficient registration samples
- Pose/lighting variation

**Solutions:**
- Register faces first (press `r`)
- Lower threshold: `--threshold 0.5`
- Register more samples per person
- Register with varied poses/lighting

### Slow Performance

**Solutions:**
- Reduce camera resolution in code
- Close other applications
- Use faster hardware
- Consider GPU acceleration for TensorFlow

## 🔬 Testing Individual Modules

### Test Face Detection Only

```bash
python detect.py
```

This opens webcam and shows detected faces with bounding boxes.

### Test Face Recognition Module

```bash
python recognize.py
```

This displays database statistics.

### Test Registration System

```bash
python register.py
```

This opens an interactive CLI for face registration.

## 📊 Performance

Typical performance on modern hardware:
- **FPS**: 15-30 (depends on CPU/GPU)
- **Detection Time**: 50-150ms per frame
- **Recognition Time**: 20-50ms per face
- **Total Latency**: < 200ms

## 🔒 Privacy & Security

- All face data is stored **locally** on your machine
- No data is sent to external servers
- Database file (`face_database.pkl`) contains only embeddings, not images
- Delete database file to remove all face data

## 🎨 Customization Ideas

1. **Add voice announcements** when faces are recognized
2. **Log recognition events** with timestamps
3. **Anti-spoofing** with liveness detection
4. **Multiple camera support** for different angles
5. **Web interface** using Flask/FastAPI
6. **Mobile app integration** via API
7. **Export recognition logs** to CSV/JSON

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MTCNN**: Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks
- **FaceNet**: A Unified Embedding for Face Recognition and Clustering
- **OpenCV**: Computer vision library
- **TensorFlow/Keras**: Deep learning framework

## 📧 Contact

For questions or feedback about this project:
- Create an issue in the repository
- Contact: [Your Email/LinkedIn]

## 🏆 Portfolio Note

This project demonstrates:
- ✅ Deep learning integration (TensorFlow/Keras)
- ✅ Computer vision (OpenCV, MTCNN)
- ✅ Real-time video processing
- ✅ Clean, modular code architecture
- ✅ Error handling and robustness
- ✅ User interface design
- ✅ Database management
- ✅ Professional documentation

Perfect for AI/ML internship applications in computer vision and deep learning roles!

---

**Built with ❤️ for AI/ML Portfolio**

*Last Updated: February 2026*
