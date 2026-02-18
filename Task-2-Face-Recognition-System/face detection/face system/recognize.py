"""
Face Recognition Module using FaceNet Embeddings
Handles face embedding generation and recognition via cosine similarity
"""

import os
import pickle
import numpy as np
import cv2
from typing import Dict, Tuple, Optional, List
from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import load_model
import tensorflow as tf


class FaceRecognizer:
    """
    Face recognition system using FaceNet embeddings (128-d vectors)
    Uses cosine similarity for face matching
    """
    
    def __init__(self, database_path: str = "face_database.pkl", 
                 similarity_threshold: float = 0.6):
        """
        Initialize the face recognizer
        
        Args:
            database_path: Path to save/load face embeddings database
            similarity_threshold: Minimum similarity score for recognition (0.0 to 1.0)
        """
        self.database_path = database_path
        self.similarity_threshold = similarity_threshold
        self.face_database = {}  # {name: [embeddings]}
        self.normalizer = Normalizer(norm='l2')  # L2 normalization for embeddings
        
        # Load or create FaceNet model
        self.model = self._load_facenet_model()
        
        # Load existing database
        self.load_database()
        
        print(f"[INFO] Face Recognizer initialized")
        print(f"[INFO] Similarity threshold: {similarity_threshold}")
        print(f"[INFO] Registered faces: {len(self.face_database)}")
    
    def _load_facenet_model(self):
        """
        Load FaceNet model for generating embeddings
        Uses a pre-trained model or creates embedding extractor
        
        Returns:
            Loaded model
        """
        model_path = "facenet_keras.h5"
        
        try:
            # Try to load existing model
            if os.path.exists(model_path):
                print(f"[INFO] Loading FaceNet model from {model_path}")
                model = load_model(model_path, compile=False)
                return model
            else:
                # Create a simple embedding model using transfer learning
                # In production, download a pre-trained FaceNet model
                print("[INFO] Creating embedding model...")
                model = self._create_embedding_model()
                return model
                
        except Exception as e:
            print(f"[WARNING] Could not load FaceNet model: {e}")
            print("[INFO] Using fallback embedding model")
            return self._create_embedding_model()
    
    def _create_embedding_model(self):
        """
        Create a simple embedding model using MobileNetV2 as backbone
        For production, replace with actual FaceNet model
        
        Returns:
            Keras model that outputs 128-d embeddings
        """
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
        from tensorflow.keras.models import Model
        
        # Input layer for 160x160 RGB images (FaceNet standard)
        input_layer = Input(shape=(160, 160, 3))
        
        # Use MobileNetV2 as feature extractor
        base_model = MobileNetV2(
            input_shape=(160, 160, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False
        
        # Build embedding model
        x = base_model(input_layer)
        x = GlobalAveragePooling2D()(x)
        x = Dense(256, activation='relu')(x)
        embeddings = Dense(128, activation=None, name='embeddings')(x)  # 128-d embeddings
        
        model = Model(inputs=input_layer, outputs=embeddings)
        
        print("[INFO] Embedding model created (128-d output)")
        return model
    
    def preprocess_face(self, face_image: np.ndarray) -> np.ndarray:
        """
        Preprocess face image for embedding extraction
        
        Args:
            face_image: Input face image (BGR format)
            
        Returns:
            Preprocessed image ready for model input
        """
        try:
            # Resize to FaceNet input size (160x160)
            face_resized = cv2.resize(face_image, (160, 160))
            
            # Convert BGR to RGB
            face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values to [0, 1]
            face_normalized = face_rgb.astype('float32') / 255.0
            
            # Expand dimensions for batch processing
            face_batch = np.expand_dims(face_normalized, axis=0)
            
            return face_batch
            
        except Exception as e:
            print(f"[ERROR] Face preprocessing failed: {e}")
            return None
    
    def get_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Generate 128-d embedding vector for a face
        
        Args:
            face_image: Input face image (BGR format)
            
        Returns:
            Normalized 128-d embedding vector or None
        """
        try:
            # Preprocess face
            face_batch = self.preprocess_face(face_image)
            if face_batch is None:
                return None
            
            # Generate embedding
            embedding = self.model.predict(face_batch, verbose=0)
            
            # L2 normalize the embedding
            embedding_normalized = self.normalizer.transform(embedding)
            
            return embedding_normalized[0]
            
        except Exception as e:
            print(f"[ERROR] Embedding generation failed: {e}")
            return None
    
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0.0 to 1.0, higher is more similar)
        """
        # Cosine similarity = dot product of normalized vectors
        similarity = np.dot(embedding1, embedding2)
        
        # Convert to [0, 1] range (from [-1, 1])
        similarity = (similarity + 1) / 2
        
        return float(similarity)
    
    def register_face(self, name: str, face_image: np.ndarray) -> bool:
        """
        Register a new face in the database
        
        Args:
            name: Name/identifier for the person
            face_image: Face image to register
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Generate embedding
            embedding = self.get_embedding(face_image)
            
            if embedding is None:
                print(f"[ERROR] Could not generate embedding for {name}")
                return False
            
            # Add to database (support multiple embeddings per person)
            if name not in self.face_database:
                self.face_database[name] = []
            
            self.face_database[name].append(embedding)
            
            print(f"[INFO] Registered face for '{name}' (total samples: {len(self.face_database[name])})")
            
            # Save database
            self.save_database()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Face registration failed: {e}")
            return False
    
    def recognize_face(self, face_image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Recognize a face by comparing against database
        
        Args:
            face_image: Input face image
            
        Returns:
            Tuple of (name, confidence_score) or (None, 0.0) if no match
        """
        try:
            # Check if database is empty
            if not self.face_database:
                return None, 0.0
            
            # Generate embedding for input face
            query_embedding = self.get_embedding(face_image)
            
            if query_embedding is None:
                return None, 0.0
            
            # Compare with all registered faces
            best_match_name = None
            best_match_score = 0.0
            
            for name, embeddings_list in self.face_database.items():
                # Calculate similarity with each embedding of this person
                similarities = [
                    self.cosine_similarity(query_embedding, emb) 
                    for emb in embeddings_list
                ]
                
                # Take the maximum similarity (best match)
                max_similarity = max(similarities)
                
                # Update best match if this is better
                if max_similarity > best_match_score:
                    best_match_score = max_similarity
                    best_match_name = name
            
            # Check if best match exceeds threshold
            if best_match_score >= self.similarity_threshold:
                confidence_pct = best_match_score * 100
                return best_match_name, confidence_pct
            else:
                return None, 0.0
                
        except Exception as e:
            print(f"[ERROR] Face recognition failed: {e}")
            return None, 0.0
    
    def save_database(self):
        """Save face embeddings database to disk"""
        try:
            with open(self.database_path, 'wb') as f:
                pickle.dump(self.face_database, f)
            print(f"[INFO] Database saved to {self.database_path}")
        except Exception as e:
            print(f"[ERROR] Could not save database: {e}")
    
    def load_database(self):
        """Load face embeddings database from disk"""
        try:
            if os.path.exists(self.database_path):
                with open(self.database_path, 'rb') as f:
                    self.face_database = pickle.load(f)
                print(f"[INFO] Loaded {len(self.face_database)} faces from database")
            else:
                print("[INFO] No existing database found, starting fresh")
        except Exception as e:
            print(f"[ERROR] Could not load database: {e}")
            self.face_database = {}
    
    def delete_face(self, name: str) -> bool:
        """
        Delete a registered face from database
        
        Args:
            name: Name of person to delete
            
        Returns:
            True if deleted, False if not found
        """
        if name in self.face_database:
            del self.face_database[name]
            self.save_database()
            print(f"[INFO] Deleted '{name}' from database")
            return True
        else:
            print(f"[WARNING] '{name}' not found in database")
            return False
    
    def list_registered_faces(self) -> List[str]:
        """
        Get list of all registered face names
        
        Returns:
            List of registered names
        """
        return list(self.face_database.keys())
    
    def get_database_stats(self) -> Dict:
        """
        Get statistics about the face database
        
        Returns:
            Dictionary with database statistics
        """
        stats = {
            'total_people': len(self.face_database),
            'total_embeddings': sum(len(embs) for embs in self.face_database.values()),
            'registered_names': list(self.face_database.keys())
        }
        return stats


if __name__ == "__main__":
    # Test the face recognizer
    print("Face Recognition Module - Test Mode")
    print("-" * 50)
    
    # Initialize recognizer
    recognizer = FaceRecognizer(similarity_threshold=0.6)
    
    # Display database stats
    stats = recognizer.get_database_stats()
    print(f"\nDatabase Statistics:")
    print(f"  Total people: {stats['total_people']}")
    print(f"  Total embeddings: {stats['total_embeddings']}")
    print(f"  Registered: {stats['registered_names']}")
    
    print("\n[INFO] Recognition module ready for use")
