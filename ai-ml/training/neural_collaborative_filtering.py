"""
Neural Collaborative Filtering implementation for advanced course recommendations.
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import logging
from typing import Dict, List, Tuple, Optional
import pickle
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class CourseInteractionDataset(Dataset):
    """Dataset class for course interactions."""
    
    def __init__(self, user_ids: np.ndarray, course_ids: np.ndarray, ratings: np.ndarray):
        self.user_ids = torch.LongTensor(user_ids)
        self.course_ids = torch.LongTensor(course_ids)
        self.ratings = torch.FloatTensor(ratings)
    
    def __len__(self):
        return len(self.user_ids)
    
    def __getitem__(self, idx):
        return {
            'user_id': self.user_ids[idx],
            'course_id': self.course_ids[idx],
            'rating': self.ratings[idx]
        }


class NeuralCollaborativeFiltering(nn.Module):
    """
    Neural Collaborative Filtering model for course recommendations.
    
    This model uses deep learning to learn complex user-item interactions
    and provides more accurate recommendations than traditional methods.
    """
    
    def __init__(self, num_users: int, num_courses: int, embedding_dim: int = 64, 
                 hidden_dims: List[int] = [128, 64, 32], dropout_rate: float = 0.2):
        super(NeuralCollaborativeFiltering, self).__init__()
        
        self.num_users = num_users
        self.num_courses = num_courses
        self.embedding_dim = embedding_dim
        
        # User and course embeddings
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.course_embedding = nn.Embedding(num_courses, embedding_dim)
        
        # Neural network layers
        layers = []
        input_dim = embedding_dim * 2  # Concatenated user and course embeddings
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_dim),
                nn.Dropout(dropout_rate)
            ])
            input_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(input_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.network = nn.Sequential(*layers)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize model weights."""
        nn.init.normal_(self.user_embedding.weight, std=0.01)
        nn.init.normal_(self.course_embedding.weight, std=0.01)
        
        for layer in self.network:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)
                nn.init.constant_(layer.bias, 0)
    
    def forward(self, user_ids: torch.Tensor, course_ids: torch.Tensor) -> torch.Tensor:
        """Forward pass of the model."""
        # Get embeddings
        user_emb = self.user_embedding(user_ids)
        course_emb = self.course_embedding(course_ids)
        
        # Concatenate embeddings
        concat_emb = torch.cat([user_emb, course_emb], dim=1)
        
        # Pass through network
        output = self.network(concat_emb)
        
        return output.squeeze()


class NeuralCFTrainer:
    """Trainer class for Neural Collaborative Filtering model."""
    
    def __init__(self, model: NeuralCollaborativeFiltering, device: str = 'cpu'):
        self.model = model
        self.device = device
        self.model.to(device)
        
        # Loss and optimizer
        self.criterion = nn.BCELoss()
        self.optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', patience=5, factor=0.5
        )
    
    def train_epoch(self, dataloader: DataLoader) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for batch in dataloader:
            user_ids = batch['user_id'].to(self.device)
            course_ids = batch['course_id'].to(self.device)
            ratings = batch['rating'].to(self.device)
            
            # Forward pass
            predictions = self.model(user_ids, course_ids)
            loss = self.criterion(predictions, ratings)
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        return total_loss / num_batches
    
    def validate(self, dataloader: DataLoader) -> float:
        """Validate the model."""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in dataloader:
                user_ids = batch['user_id'].to(self.device)
                course_ids = batch['course_id'].to(self.device)
                ratings = batch['rating'].to(self.device)
                
                predictions = self.model(user_ids, course_ids)
                loss = self.criterion(predictions, ratings)
                
                total_loss += loss.item()
                num_batches += 1
        
        return total_loss / num_batches
    
    def train(self, train_loader: DataLoader, val_loader: DataLoader, 
              epochs: int = 50, patience: int = 10) -> Dict:
        """Train the model with early stopping."""
        best_val_loss = float('inf')
        patience_counter = 0
        train_losses = []
        val_losses = []
        
        for epoch in range(epochs):
            # Train
            train_loss = self.train_epoch(train_loader)
            train_losses.append(train_loss)
            
            # Validate
            val_loss = self.validate(val_loader)
            val_losses.append(val_loss)
            
            # Learning rate scheduling
            self.scheduler.step(val_loss)
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # Save best model
                self.save_model('best_model.pth')
            else:
                patience_counter += 1
            
            if patience_counter >= patience:
                logger.info(f"Early stopping at epoch {epoch + 1}")
                break
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
        
        return {
            'train_losses': train_losses,
            'val_losses': val_losses,
            'best_val_loss': best_val_loss,
            'epochs_trained': epoch + 1
        }
    
    def save_model(self, filepath: str):
        """Save the trained model."""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_config': {
                'num_users': self.model.num_users,
                'num_courses': self.model.num_courses,
                'embedding_dim': self.model.embedding_dim
            }
        }, filepath)
    
    def load_model(self, filepath: str):
        """Load a trained model."""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        return checkpoint['model_config']


class NeuralCFRecommendationEngine:
    """Neural Collaborative Filtering recommendation engine."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.user_encoder = LabelEncoder()
        self.course_encoder = LabelEncoder()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def prepare_data(self, interactions_df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare data for training."""
        # Encode user and course IDs
        user_ids = self.user_encoder.fit_transform(interactions_df['user_id'])
        course_ids = self.course_encoder.fit_transform(interactions_df['course_id'])
        
        # Normalize ratings to 0-1 range
        ratings = interactions_df['rating'].values / 5.0
        
        return user_ids, course_ids, ratings
    
    def train_model(self, interactions_df: pd.DataFrame, test_size: float = 0.2, 
                   epochs: int = 50) -> Dict:
        """Train the Neural CF model."""
        logger.info("Preparing data for Neural CF training...")
        
        # Prepare data
        user_ids, course_ids, ratings = self.prepare_data(interactions_df)
        
        # Split data
        train_user_ids, val_user_ids, train_course_ids, val_course_ids, train_ratings, val_ratings = train_test_split(
            user_ids, course_ids, ratings, test_size=test_size, random_state=42
        )
        
        # Create datasets
        train_dataset = CourseInteractionDataset(train_user_ids, train_course_ids, train_ratings)
        val_dataset = CourseInteractionDataset(val_user_ids, val_course_ids, val_ratings)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=1024, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=1024, shuffle=False)
        
        # Initialize model
        num_users = len(self.user_encoder.classes_)
        num_courses = len(self.course_encoder.classes_)
        
        self.model = NeuralCollaborativeFiltering(
            num_users=num_users,
            num_courses=num_courses,
            embedding_dim=64,
            hidden_dims=[128, 64, 32],
            dropout_rate=0.2
        )
        
        # Train model
        trainer = NeuralCFTrainer(self.model, self.device)
        training_results = trainer.train(train_loader, val_loader, epochs=epochs)
        
        # Save encoders
        self.save_encoders()
        
        logger.info(f"Neural CF training completed. Best validation loss: {training_results['best_val_loss']:.4f}")
        
        return training_results
    
    def get_recommendations(self, user_id: int, num_recommendations: int = 10, 
                          exclude_courses: List[int] = None) -> List[Tuple[int, float]]:
        """Get recommendations for a user."""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        self.model.eval()
        
        # Encode user ID
        try:
            encoded_user_id = self.user_encoder.transform([user_id])[0]
        except ValueError:
            # User not in training data, return empty recommendations
            return []
        
        # Get all course IDs
        all_course_ids = self.course_encoder.classes_
        
        # Exclude courses if specified
        if exclude_courses:
            exclude_encoded = []
            for course_id in exclude_courses:
                try:
                    encoded_course_id = self.course_encoder.transform([course_id])[0]
                    exclude_encoded.append(encoded_course_id)
                except ValueError:
                    continue
            all_course_ids = [cid for cid in all_course_ids if cid not in exclude_encoded]
        
        # Predict ratings for all courses
        user_tensor = torch.LongTensor([encoded_user_id] * len(all_course_ids)).to(self.device)
        course_tensor = torch.LongTensor(all_course_ids).to(self.device)
        
        with torch.no_grad():
            predictions = self.model(user_tensor, course_tensor)
        
        # Get top recommendations
        predictions_cpu = predictions.cpu().numpy()
        course_scores = list(zip(all_course_ids, predictions_cpu))
        course_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Decode course IDs and return top recommendations
        recommendations = []
        for encoded_course_id, score in course_scores[:num_recommendations]:
            original_course_id = self.course_encoder.inverse_transform([encoded_course_id])[0]
            recommendations.append((original_course_id, float(score)))
        
        return recommendations
    
    def save_model(self, model_path: str):
        """Save the complete model and encoders."""
        if self.model is None:
            raise ValueError("No model to save")
        
        # Save model
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_config': {
                'num_users': self.model.num_users,
                'num_courses': self.model.num_courses,
                'embedding_dim': self.model.embedding_dim
            }
        }, model_path)
        
        # Save encoders
        encoder_path = model_path.replace('.pth', '_encoders.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump({
                'user_encoder': self.user_encoder,
                'course_encoder': self.course_encoder
            }, f)
        
        logger.info(f"Model saved to {model_path}")
    
    def load_model(self, model_path: str):
        """Load the complete model and encoders."""
        # Load model
        checkpoint = torch.load(model_path, map_location=self.device)
        
        self.model = NeuralCollaborativeFiltering(**checkpoint['model_config'])
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.to(self.device)
        
        # Load encoders
        encoder_path = model_path.replace('.pth', '_encoders.pkl')
        with open(encoder_path, 'rb') as f:
            encoders = pickle.load(f)
            self.user_encoder = encoders['user_encoder']
            self.course_encoder = encoders['course_encoder']
        
        logger.info(f"Model loaded from {model_path}")
    
    def save_encoders(self):
        """Save encoders separately."""
        encoder_path = os.path.join('ai-ml', 'models', 'neural_cf_encoders.pkl')
        os.makedirs(os.path.dirname(encoder_path), exist_ok=True)
        
        with open(encoder_path, 'wb') as f:
            pickle.dump({
                'user_encoder': self.user_encoder,
                'course_encoder': self.course_encoder
            }, f)
