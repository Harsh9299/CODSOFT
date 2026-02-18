# 🎯 Face Detection and Recognition System

## 📌 Project Overview

This project is a production-ready real-time Face Detection and Recognition system developed using Python. It combines classical computer vision techniques and deep learning models to accurately detect and recognize faces.

The system supports user registration, real-time recognition, and maintains a persistent local face database.

---

## 🟢 Face Detection

### Dual Detection Methods
- **Haar Cascade** – Fast and optimized for real-time performance (25–30 FPS)
- **MTCNN** – Deep learning-based detector with high accuracy and facial landmark detection
- Automatic fallback mechanism for improved robustness
- Real-time frame processing and optimization

---

## 🟢 Face Recognition

- **FaceNet Embeddings** – Generates 128-dimensional facial feature vectors
- **Cosine Similarity Matching** – Used for accurate identity comparison
- Confidence score displayed during recognition
- Persistent local database using NumPy and Pickle

---

## 🖥 User Interface

- Live webcam feed with annotated face bounding boxes
- Color-coded recognition:
  - 🟢 Green → Recognized
  - 🔴 Red → Unknown
- Keyboard-based interactive controls
- Live FPS counter
- Multi-face detection and recognition support

---

## ⚙ Core Functionality

### 1️⃣ Face Detection Pipeline
- Captures video from webcam (DirectShow backend for Windows)
- Processes frames using selected detection method
- Identifies facial regions using bounding boxes
- Extracts facial landmarks (eyes, nose, mouth)

### 2️⃣ Face Recognition Pipeline
- Resizes faces to 160×160
- Normalizes input
- Generates 128-d embeddings using FaceNet
- Applies L2 normalization
- Compares embeddings using cosine similarity
- Recognition threshold: 0.6 (configurable)

### 3️⃣ Face Registration System
- Webcam-based user enrollment
- Captures multiple samples per user
- Real-time progress feedback
- Stores embeddings locally

---

## 🛠 Technical Specifications

- Input Resolution: 640×480 (optimized) / 1280×720 (optional)
- Processing Speed:
  - Haar Cascade: 25–30 FPS
