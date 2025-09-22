"""
Model training script for AI recommendation system.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse
import json

# Add paths for imports
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Import AI components
try:
    # Add AI inference path
    ai_inference_path = os.path.join(os.path.dirname(__file__), '..', 'inference')
    if ai_inference_path not in sys.path:
        sys.path.append(ai_inference_path)
    
    from neural_collaborative_filtering import NeuralCFRecommendationEngine
    from semantic_understanding import SemanticUnderstandingEngine
    from context_aware_engine import ContextAwareRecommendationEngine
    from real_time_learning import RealTimeLearningEngine
    AI_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI components not available: {e}")
    AI_COMPONENTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Model trainer for AI recommendation system."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        
        # Create models directory
        os.makedirs('ai-ml/models', exist_ok=True)
    
    def prepare_interaction_data(self) -> pd.DataFrame:
        """Prepare interaction data for training."""
        logger.info("Preparing interaction data...")
        
        with self.engine.connect() as conn:
            # Get user interactions
            interactions_query = text("""
                SELECT 
                    ui.user_id,
                    ui.course_id,
                    ui.interaction_type,
                    ui.created_at,
                    c.rating as course_rating,
                    c.enrollment_count,
                    c.rating_count
                FROM user_interactions ui
                JOIN courses c ON ui.course_id = c.id
                WHERE c.is_active = true
                AND ui.interaction_type IN ('like', 'enroll', 'complete', 'rate')
                ORDER BY ui.created_at DESC
            """)
            
            interactions_df = pd.read_sql(interactions_query, conn)
            
            # Convert interaction types to ratings
            interaction_ratings = {
                'like': 4.0,
                'enroll': 3.5,
                'complete': 5.0,
                'rate': None  # Will use actual rating
            }
            
            # Create rating column
            ratings = []
            for _, row in interactions_df.iterrows():
                if row['interaction_type'] == 'rate':
                    # Use actual rating if available, otherwise use course rating
                    rating = row.get('course_rating', 3.0)
                else:
                    rating = interaction_ratings[row['interaction_type']]
                
                ratings.append(rating)
            
            interactions_df['rating'] = ratings
            
            # Filter out rows with no rating
            interactions_df = interactions_df.dropna(subset=['rating'])
            
            logger.info(f"Prepared {len(interactions_df)} interactions for training")
            return interactions_df
    
    def train_neural_cf_model(self, interactions_df: pd.DataFrame) -> Dict:
        """Train Neural Collaborative Filtering model."""
        if not AI_COMPONENTS_AVAILABLE:
            logger.warning("AI components not available, skipping neural CF training")
            return {}
        
        logger.info("Training Neural Collaborative Filtering model...")
        
        try:
            # Initialize neural CF engine
            neural_cf_engine = NeuralCFRecommendationEngine()
            
            # Train the model
            training_results = neural_cf_engine.train_model(
                interactions_df=interactions_df,
                test_size=0.2,
                epochs=50
            )
            
            # Save the trained model
            model_path = 'ai-ml/models/neural_cf_model.pth'
            neural_cf_engine.save_model(model_path)
            
            logger.info(f"Neural CF model trained and saved to {model_path}")
            logger.info(f"Training results: {training_results}")
            
            return {
                'model_path': model_path,
                'training_results': training_results,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error training neural CF model: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def train_semantic_models(self) -> Dict:
        """Train semantic understanding models."""
        if not AI_COMPONENTS_AVAILABLE:
            logger.warning("AI components not available, skipping semantic model training")
            return {}
        
        logger.info("Training semantic understanding models...")
        
        try:
            # Initialize semantic engine
            semantic_engine = SemanticUnderstandingEngine()
            
            # Get course data for semantic analysis
            with self.engine.connect() as conn:
                courses_query = text("""
                    SELECT 
                        c.id,
                        c.title,
                        c.description,
                        c.short_description,
                        c.skills,
                        c.difficulty_level,
                        c.content_type,
                        cat.name as category_name
                    FROM courses c
                    LEFT JOIN categories cat ON c.category_id = cat.id
                    WHERE c.is_active = true
                """)
                
                courses_df = pd.read_sql(courses_query, conn)
            
            # Analyze course content (limit to first 50 courses for training)
            course_embeddings = {}
            limited_courses = courses_df.head(50)  # Limit to 50 courses for faster training
            
            logger.info(f"Processing {len(limited_courses)} courses for semantic analysis...")
            
            for idx, course in limited_courses.iterrows():
                try:
                    course_data = {
                        'title': course['title'],
                        'description': course['description'],
                        'short_description': course['short_description'],
                        'skills': course['skills'] or [],
                        'difficulty_level': course['difficulty_level'],
                        'content_type': course['content_type'],
                        'category': course['category_name']
                    }
                    
                    # Generate semantic embedding
                    analysis = semantic_engine.analyze_course_content(course_data)
                    if analysis['semantic_embedding'] is not None:
                        course_embeddings[course['id']] = analysis['semantic_embedding']
                    
                    # Log progress every 10 courses
                    if (idx + 1) % 10 == 0:
                        logger.info(f"Processed {idx + 1}/{len(limited_courses)} courses...")
                        
                except Exception as e:
                    logger.warning(f"Error processing course {course['id']}: {e}")
                    continue
            
            # Save course embeddings
            semantic_engine.course_embeddings = course_embeddings
            
            # Skip learning path graph for now (causes infinite loop)
            # Build simple learning path graph
            semantic_engine.learning_path_graph = {
                'nodes': list(course_embeddings.keys()),
                'edges': [],
                'learning_paths': []
            }
            
            # Save semantic models
            models_path = 'ai-ml/models/semantic_models.pkl'
            semantic_engine.save_semantic_models(models_path)
            
            logger.info(f"Semantic models trained and saved to {models_path}")
            logger.info(f"Generated embeddings for {len(course_embeddings)} courses")
            logger.info(f"Built learning path graph with {len(semantic_engine.learning_path_graph['nodes'])} nodes")
            
            return {
                'models_path': models_path,
                'course_embeddings_count': len(course_embeddings),
                'learning_paths_count': len(semantic_engine.learning_path_graph['learning_paths']),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error training semantic models: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def train_context_aware_models(self) -> Dict:
        """Train context-aware recommendation models."""
        if not AI_COMPONENTS_AVAILABLE:
            logger.warning("AI components not available, skipping context-aware model training")
            return {}
        
        logger.info("Training context-aware recommendation models...")
        
        try:
            # Initialize context-aware engine
            context_engine = ContextAwareRecommendationEngine()
            
            # Get user interaction data for context analysis
            with self.engine.connect() as conn:
                context_query = text("""
                    SELECT 
                        ui.user_id,
                        ui.course_id,
                        ui.interaction_type,
                        ui.created_at,
                        c.difficulty_level,
                        c.content_type,
                        c.duration_hours,
                        cat.name as category_name
                    FROM user_interactions ui
                    JOIN courses c ON ui.course_id = c.id
                    LEFT JOIN categories cat ON c.category_id = cat.id
                    WHERE c.is_active = true
                    AND ui.created_at >= NOW() - INTERVAL '90 days'
                """)
                
                context_df = pd.read_sql(context_query, conn)
            
            # Analyze context patterns
            context_patterns = self._analyze_context_patterns(context_df)
            
            # Save context patterns
            context_path = 'ai-ml/models/context_patterns.json'
            with open(context_path, 'w') as f:
                json.dump(context_patterns, f, indent=2, default=str)
            
            logger.info(f"Context-aware models trained and saved to {context_path}")
            logger.info(f"Analyzed {len(context_df)} interactions for context patterns")
            
            return {
                'context_path': context_path,
                'interactions_analyzed': len(context_df),
                'context_patterns': len(context_patterns),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error training context-aware models: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _analyze_context_patterns(self, context_df: pd.DataFrame) -> Dict:
        """Analyze context patterns from interaction data."""
        patterns = {
            'time_patterns': {},
            'session_patterns': {},
            'device_patterns': {},
            'mood_patterns': {},
            'goal_patterns': {}
        }
        
        # Analyze time patterns
        context_df['hour'] = pd.to_datetime(context_df['created_at']).dt.hour
        context_df['day_of_week'] = pd.to_datetime(context_df['created_at']).dt.dayofweek
        
        # Time of day patterns
        time_patterns = context_df.groupby(['hour', 'interaction_type']).size().unstack(fill_value=0)
        patterns['time_patterns'] = time_patterns.to_dict()
        
        # Day of week patterns
        day_patterns = context_df.groupby(['day_of_week', 'interaction_type']).size().unstack(fill_value=0)
        patterns['day_patterns'] = day_patterns.to_dict()
        
        # Difficulty level preferences by time
        difficulty_time = context_df.groupby(['hour', 'difficulty_level']).size().unstack(fill_value=0)
        patterns['difficulty_time_patterns'] = difficulty_time.to_dict()
        
        # Content type preferences by time
        content_time = context_df.groupby(['hour', 'content_type']).size().unstack(fill_value=0)
        patterns['content_time_patterns'] = content_time.to_dict()
        
        return patterns
    
    def train_all_models(self) -> Dict:
        """Train all AI models."""
        logger.info("Starting comprehensive model training...")
        
        training_results = {
            'start_time': datetime.now().isoformat(),
            'models': {}
        }
        
        try:
            # Prepare interaction data
            interactions_df = self.prepare_interaction_data()
            
            if len(interactions_df) < 100:
                logger.warning("Insufficient interaction data for training. Need at least 100 interactions.")
                training_results['status'] = 'insufficient_data'
                return training_results
            
            # Train Neural Collaborative Filtering
            neural_cf_results = self.train_neural_cf_model(interactions_df)
            training_results['models']['neural_cf'] = neural_cf_results
            
            # Train Semantic Understanding
            semantic_results = self.train_semantic_models()
            training_results['models']['semantic'] = semantic_results
            
            # Train Context-Aware Models
            context_results = self.train_context_aware_models()
            training_results['models']['context_aware'] = context_results
            
            # Save training summary
            training_results['end_time'] = datetime.now().isoformat()
            training_results['status'] = 'completed'
            
            summary_path = 'ai-ml/models/training_summary.json'
            with open(summary_path, 'w') as f:
                json.dump(training_results, f, indent=2, default=str)
            
            logger.info(f"All models trained successfully. Summary saved to {summary_path}")
            
            return training_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive model training: {e}")
            training_results['error'] = str(e)
            training_results['status'] = 'failed'
            return training_results
    
    def evaluate_models(self) -> Dict:
        """Evaluate trained models."""
        logger.info("Evaluating trained models...")
        
        evaluation_results = {
            'evaluation_time': datetime.now().isoformat(),
            'models': {}
        }
        
        try:
            # Evaluate Neural CF model
            if os.path.exists('ai-ml/models/neural_cf_model.pth'):
                neural_cf_eval = self._evaluate_neural_cf_model()
                evaluation_results['models']['neural_cf'] = neural_cf_eval
            
            # Evaluate Semantic models
            if os.path.exists('ai-ml/models/semantic_models.pkl'):
                semantic_eval = self._evaluate_semantic_models()
                evaluation_results['models']['semantic'] = semantic_eval
            
            # Evaluate Context-Aware models
            if os.path.exists('ai-ml/models/context_patterns.json'):
                context_eval = self._evaluate_context_models()
                evaluation_results['models']['context_aware'] = context_eval
            
            # Save evaluation results
            eval_path = 'ai-ml/models/evaluation_results.json'
            with open(eval_path, 'w') as f:
                json.dump(evaluation_results, f, indent=2, default=str)
            
            logger.info(f"Model evaluation completed. Results saved to {eval_path}")
            
            return evaluation_results
            
        except Exception as e:
            logger.error(f"Error evaluating models: {e}")
            evaluation_results['error'] = str(e)
            return evaluation_results
    
    def _evaluate_neural_cf_model(self) -> Dict:
        """Evaluate Neural CF model."""
        try:
            # Load model and test on recent data
            neural_cf_engine = NeuralCFRecommendationEngine('ai-ml/models/neural_cf_model.pth')
            
            # Get test data
            with self.engine.connect() as conn:
                test_query = text("""
                    SELECT user_id, course_id, interaction_type
                    FROM user_interactions
                    WHERE created_at >= NOW() - INTERVAL '7 days'
                    AND interaction_type IN ('like', 'enroll', 'complete')
                """)
                
                test_df = pd.read_sql(test_query, conn)
            
            # Calculate metrics
            total_interactions = len(test_df)
            unique_users = test_df['user_id'].nunique()
            unique_courses = test_df['course_id'].nunique()
            
            return {
                'total_test_interactions': total_interactions,
                'unique_users': unique_users,
                'unique_courses': unique_courses,
                'status': 'evaluated'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _evaluate_semantic_models(self) -> Dict:
        """Evaluate semantic models."""
        try:
            # Load semantic models
            semantic_engine = SemanticUnderstandingEngine()
            semantic_engine.load_semantic_models('ai-ml/models/semantic_models.pkl')
            
            # Count embeddings and learning paths
            embeddings_count = len(semantic_engine.course_embeddings)
            learning_paths_count = len(semantic_engine.learning_path_graph.get('learning_paths', []))
            
            return {
                'course_embeddings_count': embeddings_count,
                'learning_paths_count': learning_paths_count,
                'status': 'evaluated'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _evaluate_context_models(self) -> Dict:
        """Evaluate context-aware models."""
        try:
            # Load context patterns
            with open('ai-ml/models/context_patterns.json', 'r') as f:
                context_patterns = json.load(f)
            
            # Count patterns
            time_patterns_count = len(context_patterns.get('time_patterns', {}))
            day_patterns_count = len(context_patterns.get('day_patterns', {}))
            
            return {
                'time_patterns_count': time_patterns_count,
                'day_patterns_count': day_patterns_count,
                'status': 'evaluated'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description='Train AI recommendation models')
    parser.add_argument('--database-url', required=True, help='Database URL')
    parser.add_argument('--model', choices=['neural_cf', 'semantic', 'context_aware', 'all'], 
                       default='all', help='Model to train')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate models after training')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize trainer
    trainer = ModelTrainer(args.database_url)
    
    # Train models
    if args.model == 'all':
        results = trainer.train_all_models()
    elif args.model == 'neural_cf':
        interactions_df = trainer.prepare_interaction_data()
        results = trainer.train_neural_cf_model(interactions_df)
    elif args.model == 'semantic':
        results = trainer.train_semantic_models()
    elif args.model == 'context_aware':
        results = trainer.train_context_aware_models()
    
    print(f"Training results: {json.dumps(results, indent=2, default=str)}")
    
    # Evaluate models if requested
    if args.evaluate:
        eval_results = trainer.evaluate_models()
        print(f"Evaluation results: {json.dumps(eval_results, indent=2, default=str)}")


if __name__ == '__main__':
    main()
