"""
Training endpoints for AI/ML models.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

# Import training modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'ai-ml', 'training'))

try:
    from model_trainer import ModelTrainer
    TRAINING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Training modules not available: {e}")
    TRAINING_AVAILABLE = False

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/train-models")
async def train_models(
    background_tasks: BackgroundTasks,
    force_retrain: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Train AI/ML recommendation models.
    
    Args:
        force_retrain: Force retraining even if models are recent
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict: Training results
    """
    if not TRAINING_AVAILABLE:
        raise HTTPException(
            status_code=501, 
            detail="Training functionality not available. Please check AI/ML dependencies."
        )
    
    # Check if user is admin/superuser
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can train models"
        )
    
    try:
        # Initialize trainer
        trainer = ModelTrainer(db)
        
        # Start training in background
        background_tasks.add_task(trainer.train_all_models)
        
        return {
            "message": "Model training started in background",
            "status": "started",
            "force_retrain": force_retrain,
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error(f"Error starting model training: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start model training: {str(e)}"
        )


@router.post("/retrain-models")
async def retrain_models(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Retrain models if needed (checks if models are outdated).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict: Retraining results
    """
    if not TRAINING_AVAILABLE:
        raise HTTPException(
            status_code=501, 
            detail="Training functionality not available. Please check AI/ML dependencies."
        )
    
    # Check if user is admin/superuser
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can retrain models"
        )
    
    try:
        # Initialize trainer
        trainer = ModelTrainer(db)
        
        # Check if retraining is needed and start if necessary
        background_tasks.add_task(trainer.retrain_models)
        
        return {
            "message": "Model retraining check started in background",
            "status": "started",
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error(f"Error starting model retraining: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start model retraining: {str(e)}"
        )


@router.get("/model-status")
async def get_model_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get status of trained models.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict: Model status information
    """
    if not TRAINING_AVAILABLE:
        raise HTTPException(
            status_code=501, 
            detail="Training functionality not available. Please check AI/ML dependencies."
        )
    
    try:
        # Check model files
        models_dir = "ai-ml/models"
        model_files = {
            "content_based_model": os.path.exists(os.path.join(models_dir, "content_based_model.pkl")),
            "content_based_metadata": os.path.exists(os.path.join(models_dir, "content_based_metadata.json"))
        }
        
        # Read metadata if available
        metadata = {}
        metadata_path = os.path.join(models_dir, "content_based_metadata.json")
        if os.path.exists(metadata_path):
            try:
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            except Exception as e:
                logger.warning(f"Error reading metadata: {e}")
        
        return {
            "model_files": model_files,
            "metadata": metadata,
            "training_available": TRAINING_AVAILABLE,
            "models_directory": models_dir
        }
        
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model status: {str(e)}"
        )


@router.post("/prepare-training-data")
async def prepare_training_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Prepare training data from database.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict: Training data preparation results
    """
    if not TRAINING_AVAILABLE:
        raise HTTPException(
            status_code=501, 
            detail="Training functionality not available. Please check AI/ML dependencies."
        )
    
    # Check if user is admin/superuser
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can prepare training data"
        )
    
    try:
        # Initialize trainer
        trainer = ModelTrainer(db)
        
        # Prepare training data
        training_data = trainer.prepare_training_data()
        
        return {
            "message": "Training data prepared successfully",
            "data_summary": training_data.get("metadata", {}),
            "data_file": "Saved to ai-ml/data/ directory"
        }
        
    except Exception as e:
        logger.error(f"Error preparing training data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to prepare training data: {str(e)}"
        )
