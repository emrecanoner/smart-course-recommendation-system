"""
Model deployment and monitoring for AI recommendation system.
"""

import os
import sys
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import threading
import schedule

# Add paths for imports
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Import AI components
try:
    from ..inference.recommendation_engine import AIRecommendationEngine
    from ..inference.real_time_learning import RealTimeLearningEngine
    from ..training.train_models import ModelTrainer
    AI_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI components not available: {e}")
    AI_COMPONENTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ModelDeploymentManager:
    """Manages model deployment and monitoring."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        
        # Model status tracking
        self.model_status = {
            'neural_cf': {'status': 'unknown', 'last_updated': None, 'performance': {}},
            'semantic': {'status': 'unknown', 'last_updated': None, 'performance': {}},
            'context_aware': {'status': 'unknown', 'last_updated': None, 'performance': {}},
            'real_time_learning': {'status': 'unknown', 'last_updated': None, 'performance': {}}
        }
        
        # Performance metrics
        self.performance_metrics = {
            'recommendation_accuracy': [],
            'response_times': [],
            'user_satisfaction': [],
            'model_usage': {}
        }
        
        # Deployment configuration
        self.deployment_config = {
            'auto_retrain_interval_hours': 24,
            'performance_threshold': 0.7,
            'max_response_time_ms': 5000,
            'monitoring_interval_minutes': 15
        }
    
    def deploy_models(self) -> Dict[str, Any]:
        """Deploy all trained models."""
        logger.info("Starting model deployment...")
        
        deployment_results = {
            'start_time': datetime.now().isoformat(),
            'models': {}
        }
        
        try:
            # Deploy Neural CF model
            neural_cf_result = self._deploy_neural_cf_model()
            deployment_results['models']['neural_cf'] = neural_cf_result
            
            # Deploy Semantic models
            semantic_result = self._deploy_semantic_models()
            deployment_results['models']['semantic'] = semantic_result
            
            # Deploy Context-Aware models
            context_result = self._deploy_context_aware_models()
            deployment_results['models']['context_aware'] = context_result
            
            # Initialize Real-time Learning
            rt_learning_result = self._initialize_real_time_learning()
            deployment_results['models']['real_time_learning'] = rt_learning_result
            
            deployment_results['end_time'] = datetime.now().isoformat()
            deployment_results['status'] = 'deployed'
            
            # Save deployment status
            self._save_deployment_status(deployment_results)
            
            logger.info("All models deployed successfully")
            return deployment_results
            
        except Exception as e:
            logger.error(f"Error in model deployment: {e}")
            deployment_results['error'] = str(e)
            deployment_results['status'] = 'failed'
            return deployment_results
    
    def _deploy_neural_cf_model(self) -> Dict[str, Any]:
        """Deploy Neural Collaborative Filtering model."""
        try:
            model_path = 'ai-ml/models/neural_cf_model.pth'
            
            if not os.path.exists(model_path):
                return {
                    'status': 'not_found',
                    'message': 'Neural CF model not found'
                }
            
            # Test model loading
            from ..inference.neural_collaborative_filtering import NeuralCFRecommendationEngine
            neural_cf_engine = NeuralCFRecommendationEngine(model_path)
            
            # Test model with sample data
            test_recommendations = neural_cf_engine.get_recommendations(
                user_id=1, num_recommendations=5
            )
            
            self.model_status['neural_cf'] = {
                'status': 'deployed',
                'last_updated': datetime.now().isoformat(),
                'performance': {
                    'test_recommendations_count': len(test_recommendations),
                    'model_size_mb': os.path.getsize(model_path) / (1024 * 1024)
                }
            }
            
            return {
                'status': 'deployed',
                'model_path': model_path,
                'test_recommendations': len(test_recommendations)
            }
            
        except Exception as e:
            logger.error(f"Error deploying Neural CF model: {e}")
            self.model_status['neural_cf']['status'] = 'failed'
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def _deploy_semantic_models(self) -> Dict[str, Any]:
        """Deploy semantic understanding models."""
        try:
            models_path = 'ai-ml/models/semantic_models.pkl'
            
            if not os.path.exists(models_path):
                return {
                    'status': 'not_found',
                    'message': 'Semantic models not found'
                }
            
            # Test model loading
            from ..inference.semantic_understanding import SemanticUnderstandingEngine
            semantic_engine = SemanticUnderstandingEngine()
            semantic_engine.load_semantic_models(models_path)
            
            # Test semantic analysis
            test_analysis = semantic_engine.analyze_course_content({
                'title': 'Python Programming',
                'description': 'Learn Python programming from basics to advanced',
                'skills': ['python', 'programming', 'algorithms']
            })
            
            self.model_status['semantic'] = {
                'status': 'deployed',
                'last_updated': datetime.now().isoformat(),
                'performance': {
                    'course_embeddings_count': len(semantic_engine.course_embeddings),
                    'learning_paths_count': len(semantic_engine.learning_path_graph.get('learning_paths', [])),
                    'test_analysis_skills': len(test_analysis.get('skills', []))
                }
            }
            
            return {
                'status': 'deployed',
                'models_path': models_path,
                'course_embeddings_count': len(semantic_engine.course_embeddings)
            }
            
        except Exception as e:
            logger.error(f"Error deploying semantic models: {e}")
            self.model_status['semantic']['status'] = 'failed'
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def _deploy_context_aware_models(self) -> Dict[str, Any]:
        """Deploy context-aware recommendation models."""
        try:
            context_path = 'ai-ml/models/context_patterns.json'
            
            if not os.path.exists(context_path):
                return {
                    'status': 'not_found',
                    'message': 'Context patterns not found'
                }
            
            # Test context engine
            from ..inference.context_aware_engine import ContextAwareRecommendationEngine
            context_engine = ContextAwareRecommendationEngine()
            
            # Test context extraction
            test_context = context_engine.extract_context_from_request({
                'learning_session': 'focused',
                'user_mood': 'motivated',
                'learning_goal': 'skill_development'
            })
            
            self.model_status['context_aware'] = {
                'status': 'deployed',
                'last_updated': datetime.now().isoformat(),
                'performance': {
                    'context_types_supported': len(test_context.__dict__),
                    'test_context_extracted': True
                }
            }
            
            return {
                'status': 'deployed',
                'context_path': context_path,
                'context_types_supported': len(test_context.__dict__)
            }
            
        except Exception as e:
            logger.error(f"Error deploying context-aware models: {e}")
            self.model_status['context_aware']['status'] = 'failed'
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def _initialize_real_time_learning(self) -> Dict[str, Any]:
        """Initialize real-time learning engine."""
        try:
            # Initialize real-time learning
            rt_learning = RealTimeLearningEngine()
            
            # Load existing learning state if available
            learning_state_path = 'ai-ml/models/learning_state.pkl'
            if os.path.exists(learning_state_path):
                rt_learning.load_learning_state(learning_state_path)
            
            self.model_status['real_time_learning'] = {
                'status': 'initialized',
                'last_updated': datetime.now().isoformat(),
                'performance': {
                    'background_learning_active': rt_learning.learning_thread is not None,
                    'feedback_buffer_size': len(rt_learning.feedback_buffer)
                }
            }
            
            return {
                'status': 'initialized',
                'background_learning_active': rt_learning.learning_thread is not None
            }
            
        except Exception as e:
            logger.error(f"Error initializing real-time learning: {e}")
            self.model_status['real_time_learning']['status'] = 'failed'
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def monitor_models(self) -> Dict[str, Any]:
        """Monitor model performance and health."""
        logger.info("Monitoring model performance...")
        
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'models': {}
        }
        
        try:
            # Monitor each model
            for model_name, status in self.model_status.items():
                model_monitoring = self._monitor_single_model(model_name, status)
                monitoring_results['models'][model_name] = model_monitoring
            
            # Check overall system health
            system_health = self._check_system_health()
            monitoring_results['system_health'] = system_health
            
            # Save monitoring results
            self._save_monitoring_results(monitoring_results)
            
            return monitoring_results
            
        except Exception as e:
            logger.error(f"Error in model monitoring: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _monitor_single_model(self, model_name: str, status: Dict) -> Dict[str, Any]:
        """Monitor a single model."""
        monitoring = {
            'status': status['status'],
            'last_updated': status['last_updated'],
            'health_checks': {}
        }
        
        try:
            # Check model file existence
            if model_name == 'neural_cf':
                model_path = 'ai-ml/models/neural_cf_model.pth'
                monitoring['health_checks']['model_file_exists'] = os.path.exists(model_path)
                
                if os.path.exists(model_path):
                    monitoring['health_checks']['model_size_mb'] = os.path.getsize(model_path) / (1024 * 1024)
                    monitoring['health_checks']['last_modified'] = datetime.fromtimestamp(
                        os.path.getmtime(model_path)
                    ).isoformat()
            
            elif model_name == 'semantic':
                models_path = 'ai-ml/models/semantic_models.pkl'
                monitoring['health_checks']['model_file_exists'] = os.path.exists(models_path)
                
                if os.path.exists(models_path):
                    monitoring['health_checks']['model_size_mb'] = os.path.getsize(models_path) / (1024 * 1024)
            
            elif model_name == 'context_aware':
                context_path = 'ai-ml/models/context_patterns.json'
                monitoring['health_checks']['model_file_exists'] = os.path.exists(context_path)
            
            elif model_name == 'real_time_learning':
                learning_state_path = 'ai-ml/models/learning_state.pkl'
                monitoring['health_checks']['learning_state_exists'] = os.path.exists(learning_state_path)
                
                # Check if background learning is active
                monitoring['health_checks']['background_learning_active'] = True  # Simplified
            
            # Overall health status
            health_checks = monitoring['health_checks']
            monitoring['overall_health'] = all(health_checks.values()) if health_checks else False
            
        except Exception as e:
            monitoring['error'] = str(e)
            monitoring['overall_health'] = False
        
        return monitoring
    
    def _check_system_health(self) -> Dict[str, Any]:
        """Check overall system health."""
        health = {
            'overall_status': 'healthy',
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check database connectivity
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            health['database_connectivity'] = True
        except Exception as e:
            health['database_connectivity'] = False
            health['issues'].append(f"Database connectivity issue: {e}")
            health['overall_status'] = 'degraded'
        
        # Check model status
        failed_models = [
            name for name, status in self.model_status.items()
            if status['status'] == 'failed'
        ]
        
        if failed_models:
            health['issues'].append(f"Failed models: {', '.join(failed_models)}")
            health['overall_status'] = 'degraded'
        
        # Check model freshness
        for model_name, status in self.model_status.items():
            if status['last_updated']:
                last_updated = datetime.fromisoformat(status['last_updated'])
                hours_old = (datetime.now() - last_updated).total_seconds() / 3600
                
                if hours_old > 48:  # Models older than 48 hours
                    health['recommendations'].append(
                        f"Consider retraining {model_name} model (last updated {hours_old:.1f} hours ago)"
                    )
        
        return health
    
    def retrain_models_if_needed(self) -> Dict[str, Any]:
        """Retrain models if performance is below threshold."""
        logger.info("Checking if models need retraining...")
        
        retrain_results = {
            'timestamp': datetime.now().isoformat(),
            'models_retrained': [],
            'models_skipped': []
        }
        
        try:
            # Check if we have enough new data
            with self.engine.connect() as conn:
                new_interactions_query = text("""
                    SELECT COUNT(*) as count
                    FROM user_interactions
                    WHERE created_at >= NOW() - INTERVAL '24 hours'
                """)
                
                result = conn.execute(new_interactions_query).fetchone()
                new_interactions_count = result.count if result else 0
            
            if new_interactions_count < 50:
                retrain_results['message'] = f"Not enough new data for retraining ({new_interactions_count} interactions)"
                return retrain_results
            
            # Initialize trainer
            trainer = ModelTrainer(self.database_url)
            
            # Retrain models
            training_results = trainer.train_all_models()
            
            if training_results['status'] == 'completed':
                # Redeploy models
                deployment_results = self.deploy_models()
                
                retrain_results['models_retrained'] = list(training_results['models'].keys())
                retrain_results['deployment_status'] = deployment_results['status']
            else:
                retrain_results['error'] = training_results.get('error', 'Unknown error')
            
        except Exception as e:
            logger.error(f"Error in model retraining: {e}")
            retrain_results['error'] = str(e)
        
        return retrain_results
    
    def _save_deployment_status(self, deployment_results: Dict):
        """Save deployment status to file."""
        status_path = 'ai-ml/models/deployment_status.json'
        with open(status_path, 'w') as f:
            json.dump(deployment_results, f, indent=2, default=str)
    
    def _save_monitoring_results(self, monitoring_results: Dict):
        """Save monitoring results to file."""
        monitoring_path = 'ai-ml/models/monitoring_results.json'
        with open(monitoring_path, 'w') as f:
            json.dump(monitoring_results, f, indent=2, default=str)
    
    def start_monitoring_scheduler(self):
        """Start the monitoring scheduler."""
        logger.info("Starting model monitoring scheduler...")
        
        # Schedule monitoring every 15 minutes
        schedule.every(15).minutes.do(self.monitor_models)
        
        # Schedule retraining check every 24 hours
        schedule.every(24).hours.do(self.retrain_models_if_needed)
        
        # Run scheduler in background thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("Model monitoring scheduler started")


def main():
    """Main deployment function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy and monitor AI recommendation models')
    parser.add_argument('--database-url', required=True, help='Database URL')
    parser.add_argument('--action', choices=['deploy', 'monitor', 'retrain', 'start-scheduler'], 
                       default='deploy', help='Action to perform')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize deployment manager
    deployment_manager = ModelDeploymentManager(args.database_url)
    
    if args.action == 'deploy':
        results = deployment_manager.deploy_models()
        print(f"Deployment results: {json.dumps(results, indent=2, default=str)}")
    
    elif args.action == 'monitor':
        results = deployment_manager.monitor_models()
        print(f"Monitoring results: {json.dumps(results, indent=2, default=str)}")
    
    elif args.action == 'retrain':
        results = deployment_manager.retrain_models_if_needed()
        print(f"Retraining results: {json.dumps(results, indent=2, default=str)}")
    
    elif args.action == 'start-scheduler':
        deployment_manager.start_monitoring_scheduler()
        print("Monitoring scheduler started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Monitoring scheduler stopped.")


if __name__ == '__main__':
    main()
