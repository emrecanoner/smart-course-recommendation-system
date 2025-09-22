"""
Advanced Semantic Understanding and NLP for course recommendations.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
import logging
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import pickle
import os

# NLP libraries
try:
    import spacy
    from spacy.lang.en import English
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logging.warning("spaCy not available. Install with: pip install spacy")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available. Install with: pip install sentence-transformers")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.decomposition import TruncatedSVD
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. Install with: pip install scikit-learn")

logger = logging.getLogger(__name__)


class SemanticUnderstandingEngine:
    """
    Advanced semantic understanding engine for course content analysis
    and intelligent recommendation matching.
    """
    
    def __init__(self):
        self.nlp = None
        self.sentence_model = None
        self.tfidf_vectorizer = None
        self.svd_model = None
        self.course_embeddings = {}
        self.skill_ontology = {}
        self.learning_path_graph = {}
        
        # Initialize NLP components
        self._initialize_nlp()
        self._initialize_semantic_models()
        self._build_skill_ontology()
    
    def _initialize_nlp(self):
        """Initialize NLP components."""
        if SPACY_AVAILABLE:
            try:
                # Try to load the English model
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy English model loaded successfully")
            except OSError:
                logger.warning("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
                self.nlp = English()
        else:
            self.nlp = English()
        
        # Custom pipeline components will be added later if needed
        # For now, use default spaCy pipeline
    
    def _initialize_semantic_models(self):
        """Initialize semantic models."""
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Sentence transformer model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load sentence transformer: {e}")
        
        if SKLEARN_AVAILABLE:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=2000,
                stop_words='english',
                ngram_range=(1, 3),
                min_df=2,
                max_df=0.8
            )
            self.svd_model = TruncatedSVD(n_components=200, random_state=42)
    
    def _build_skill_ontology(self):
        """Build skill ontology for better understanding."""
        # Define skill categories and relationships
        self.skill_ontology = {
            'programming': {
                'languages': ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin'],
                'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel'],
                'concepts': ['algorithms', 'data structures', 'oop', 'functional programming', 'design patterns'],
                'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp']
            },
            'data_science': {
                'languages': ['python', 'r', 'sql', 'scala'],
                'libraries': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn'],
                'concepts': ['machine learning', 'deep learning', 'statistics', 'data visualization', 'big data'],
                'tools': ['jupyter', 'tableau', 'power bi', 'apache spark', 'hadoop']
            },
            'web_development': {
                'frontend': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'sass', 'typescript'],
                'backend': ['node.js', 'python', 'php', 'java', 'c#', 'ruby', 'go'],
                'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
                'concepts': ['rest api', 'graphql', 'microservices', 'responsive design', 'seo']
            },
            'mobile_development': {
                'platforms': ['ios', 'android', 'cross-platform'],
                'languages': ['swift', 'kotlin', 'java', 'dart', 'javascript'],
                'frameworks': ['react native', 'flutter', 'xamarin', 'ionic'],
                'concepts': ['ui/ux', 'app store optimization', 'push notifications', 'offline storage']
            },
            'cloud_computing': {
                'platforms': ['aws', 'azure', 'google cloud', 'ibm cloud'],
                'services': ['compute', 'storage', 'networking', 'databases', 'ai/ml services'],
                'concepts': ['serverless', 'microservices', 'containerization', 'devops', 'infrastructure as code'],
                'tools': ['docker', 'kubernetes', 'terraform', 'ansible', 'jenkins']
            }
        }
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text using NLP."""
        if not text:
            return []
        
        skills = set()
        
        # Process text with spaCy
        doc = self.nlp(text.lower())
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'TECHNOLOGY']:
                skills.add(ent.text.strip())
        
        # Extract technical terms using patterns
        technical_patterns = [
            r'\b[a-z]+\.js\b',  # JavaScript frameworks
            r'\b[a-z]+\.py\b',  # Python libraries
            r'\b[a-z]+\.net\b',  # .NET technologies
            r'\b[a-z]+\.io\b',   # Various tools
            r'\b(api|sdk|sdk)\b',  # Common tech terms
            r'\b(aws|azure|gcp)\b',  # Cloud platforms
            r'\b(docker|kubernetes|jenkins)\b',  # DevOps tools
        ]
        
        for pattern in technical_patterns:
            matches = re.findall(pattern, text.lower())
            skills.update(matches)
        
        # Extract skills from ontology
        for category, subcategories in self.skill_ontology.items():
            for subcategory, items in subcategories.items():
                for item in items:
                    if item.lower() in text.lower():
                        skills.add(item)
        
        return list(skills)
    
    def analyze_course_content(self, course_data: Dict) -> Dict[str, Any]:
        """Analyze course content for semantic understanding."""
        analysis = {
            'skills': [],
            'difficulty_indicators': [],
            'learning_objectives': [],
            'content_type_indicators': [],
            'target_audience': [],
            'semantic_embedding': None,
            'complexity_score': 0.0,
            'prerequisite_skills': [],
            'outcome_skills': []
        }
        
        # Combine all text content
        text_content = []
        if course_data.get('title'):
            text_content.append(course_data['title'])
        if course_data.get('description'):
            text_content.append(course_data['description'])
        if course_data.get('short_description'):
            text_content.append(course_data['short_description'])
        if course_data.get('skills'):
            text_content.extend(course_data['skills'])
        
        full_text = ' '.join(text_content)
        
        # Extract skills
        analysis['skills'] = self.extract_skills_from_text(full_text)
        
        # Analyze difficulty indicators
        analysis['difficulty_indicators'] = self._analyze_difficulty_indicators(full_text)
        
        # Extract learning objectives
        analysis['learning_objectives'] = self._extract_learning_objectives(full_text)
        
        # Analyze content type indicators
        analysis['content_type_indicators'] = self._analyze_content_type_indicators(full_text)
        
        # Determine target audience
        analysis['target_audience'] = self._determine_target_audience(full_text)
        
        # Calculate complexity score
        analysis['complexity_score'] = self._calculate_complexity_score(full_text, analysis['skills'])
        
        # Extract prerequisite and outcome skills
        analysis['prerequisite_skills'] = self._extract_prerequisite_skills(full_text)
        analysis['outcome_skills'] = self._extract_outcome_skills(full_text)
        
        # Generate semantic embedding
        if self.sentence_model:
            analysis['semantic_embedding'] = self._generate_semantic_embedding(full_text)
        
        return analysis
    
    def _analyze_difficulty_indicators(self, text: str) -> List[str]:
        """Analyze text for difficulty indicators."""
        difficulty_indicators = {
            'beginner': [
                'introduction', 'basics', 'fundamentals', 'getting started', 'beginner',
                'elementary', 'simple', 'easy', 'basic concepts', 'primer'
            ],
            'intermediate': [
                'intermediate', 'advanced concepts', 'deeper dive', 'building on',
                'next level', 'moderate', 'some experience', 'familiar with'
            ],
            'advanced': [
                'advanced', 'expert', 'mastery', 'complex', 'sophisticated',
                'cutting-edge', 'state-of-the-art', 'professional', 'enterprise'
            ]
        }
        
        found_indicators = []
        text_lower = text.lower()
        
        for level, indicators in difficulty_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    found_indicators.append(level)
        
        return found_indicators
    
    def _extract_learning_objectives(self, text: str) -> List[str]:
        """Extract learning objectives from text."""
        objectives = []
        
        # Look for objective patterns
        objective_patterns = [
            r'you will learn to (.+?)(?:\.|$)',
            r'learn how to (.+?)(?:\.|$)',
            r'understand (.+?)(?:\.|$)',
            r'master (.+?)(?:\.|$)',
            r'be able to (.+?)(?:\.|$)',
            r'gain knowledge of (.+?)(?:\.|$)',
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, text.lower())
            objectives.extend(matches)
        
        return objectives
    
    def _analyze_content_type_indicators(self, text: str) -> List[str]:
        """Analyze text for content type indicators."""
        content_indicators = {
            'video': ['video', 'lecture', 'tutorial', 'demo', 'screencast', 'recording'],
            'text': ['reading', 'article', 'documentation', 'guide', 'manual', 'textbook'],
            'interactive': ['hands-on', 'practice', 'exercise', 'project', 'lab', 'workshop', 'coding'],
            'assessment': ['quiz', 'test', 'exam', 'assignment', 'project', 'certification']
        }
        
        found_indicators = []
        text_lower = text.lower()
        
        for content_type, indicators in content_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    found_indicators.append(content_type)
        
        return found_indicators
    
    def _determine_target_audience(self, text: str) -> List[str]:
        """Determine target audience from text."""
        audience_indicators = {
            'students': ['student', 'academic', 'university', 'college', 'school'],
            'professionals': ['professional', 'developer', 'engineer', 'analyst', 'manager'],
            'beginners': ['beginner', 'newcomer', 'entry-level', 'starting'],
            'experts': ['expert', 'senior', 'advanced', 'experienced', 'veteran'],
            'career_changers': ['career change', 'transition', 'switch', 'new field']
        }
        
        found_audiences = []
        text_lower = text.lower()
        
        for audience, indicators in audience_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    found_audiences.append(audience)
        
        return found_audiences
    
    def _calculate_complexity_score(self, text: str, skills: List[str]) -> float:
        """Calculate complexity score based on text and skills."""
        score = 0.0
        
        # Base score from text length and vocabulary
        words = text.split()
        score += min(len(words) / 1000, 0.3)  # Max 0.3 for text length
        
        # Score from number of skills
        score += min(len(skills) / 20, 0.3)  # Max 0.3 for skill count
        
        # Score from technical terms
        technical_terms = [
            'algorithm', 'architecture', 'optimization', 'scalability', 'performance',
            'security', 'authentication', 'authorization', 'encryption', 'deployment'
        ]
        
        technical_count = sum(1 for term in technical_terms if term in text.lower())
        score += min(technical_count / 10, 0.2)  # Max 0.2 for technical terms
        
        # Score from advanced concepts
        advanced_concepts = [
            'machine learning', 'artificial intelligence', 'deep learning', 'neural networks',
            'microservices', 'distributed systems', 'cloud computing', 'devops'
        ]
        
        advanced_count = sum(1 for concept in advanced_concepts if concept in text.lower())
        score += min(advanced_count / 5, 0.2)  # Max 0.2 for advanced concepts
        
        return min(score, 1.0)  # Normalize to 0-1
    
    def _extract_prerequisite_skills(self, text: str) -> List[str]:
        """Extract prerequisite skills from text."""
        prerequisites = []
        
        # Look for prerequisite patterns
        prereq_patterns = [
            r'prerequisite[s]?:?\s*(.+?)(?:\.|$)',
            r'required knowledge:?\s*(.+?)(?:\.|$)',
            r'you should know (.+?)(?:\.|$)',
            r'familiarity with (.+?)(?:\.|$)',
            r'basic understanding of (.+?)(?:\.|$)',
        ]
        
        for pattern in prereq_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                # Split by common separators
                skills = re.split(r'[,;]', match)
                prerequisites.extend([skill.strip() for skill in skills])
        
        return list(set(prerequisites))  # Remove duplicates
    
    def _extract_outcome_skills(self, text: str) -> List[str]:
        """Extract outcome skills from text."""
        outcomes = []
        
        # Look for outcome patterns
        outcome_patterns = [
            r'you will be able to (.+?)(?:\.|$)',
            r'after this course, you can (.+?)(?:\.|$)',
            r'you will master (.+?)(?:\.|$)',
            r'learn to (.+?)(?:\.|$)',
            r'gain skills in (.+?)(?:\.|$)',
        ]
        
        for pattern in outcome_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                # Split by common separators
                skills = re.split(r'[,;]', match)
                outcomes.extend([skill.strip() for skill in skills])
        
        return list(set(outcomes))  # Remove duplicates
    
    def _generate_semantic_embedding(self, text: str) -> np.ndarray:
        """Generate semantic embedding for text."""
        if not self.sentence_model:
            return None
        
        try:
            embedding = self.sentence_model.encode(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating semantic embedding: {e}")
            return None
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        if not self.sentence_model:
            return 0.0
        
        try:
            embedding1 = self.sentence_model.encode(text1)
            embedding2 = self.sentence_model.encode(text2)
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def find_semantic_matches(self, query_text: str, course_embeddings: Dict[int, np.ndarray], 
                            top_k: int = 10) -> List[Tuple[int, float]]:
        """Find semantic matches for a query."""
        if not self.sentence_model or not course_embeddings:
            return []
        
        try:
            query_embedding = self.sentence_model.encode(query_text)
            
            similarities = []
            for course_id, course_embedding in course_embeddings.items():
                similarity = cosine_similarity([query_embedding], [course_embedding])[0][0]
                similarities.append((course_id, float(similarity)))
            
            # Sort by similarity and return top k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        except Exception as e:
            logger.error(f"Error finding semantic matches: {e}")
            return []
    
    def build_learning_path_graph(self, courses: List[Dict]) -> Dict[str, Any]:
        """Build learning path graph based on course relationships."""
        graph = {
            'nodes': {},
            'edges': [],
            'prerequisites': {},
            'learning_paths': []
        }
        
        # Create nodes for each course
        for course in courses:
            course_id = course['id']
            analysis = self.analyze_course_content(course)
            
            graph['nodes'][course_id] = {
                'course_id': course_id,
                'title': course['title'],
                'skills': analysis['skills'],
                'prerequisite_skills': analysis['prerequisite_skills'],
                'outcome_skills': analysis['outcome_skills'],
                'complexity_score': analysis['complexity_score'],
                'difficulty_level': course.get('difficulty_level', 'intermediate')
            }
        
        # Create edges based on skill relationships
        for course_id, node in graph['nodes'].items():
            for other_course_id, other_node in graph['nodes'].items():
                if course_id != other_course_id:
                    # Check if this course's outcomes match other course's prerequisites
                    outcome_skills = set(node['outcome_skills'])
                    prereq_skills = set(other_node['prerequisite_skills'])
                    
                    if outcome_skills.intersection(prereq_skills):
                        graph['edges'].append({
                            'from': course_id,
                            'to': other_course_id,
                            'weight': len(outcome_skills.intersection(prereq_skills)),
                            'type': 'prerequisite'
                        })
        
        # Generate learning paths
        graph['learning_paths'] = self._generate_learning_paths(graph)
        
        return graph
    
    def _generate_learning_paths(self, graph: Dict[str, Any]) -> List[List[int]]:
        """Generate learning paths from the graph."""
        paths = []
        
        # Find starting courses (courses with no prerequisites)
        starting_courses = []
        for course_id, node in graph['nodes'].items():
            has_prerequisites = any(
                edge['to'] == course_id for edge in graph['edges']
            )
            if not has_prerequisites:
                starting_courses.append(course_id)
        
        # Generate paths from starting courses
        for start_course in starting_courses:
            path = self._dfs_path(start_course, graph, max_depth=5)
            if len(path) > 1:  # Only include paths with multiple courses
                paths.append(path)
        
        return paths
    
    def _dfs_path(self, course_id: int, graph: Dict[str, Any], 
                  current_path: List[int] = None, max_depth: int = 5) -> List[int]:
        """Depth-first search to find learning paths."""
        if current_path is None:
            current_path = []
        
        if len(current_path) >= max_depth or course_id in current_path:
            return current_path
        
        current_path = current_path + [course_id]
        
        # Find next courses
        next_courses = [
            edge['to'] for edge in graph['edges']
            if edge['from'] == course_id and edge['to'] not in current_path
        ]
        
        if not next_courses:
            return current_path
        
        # Continue with the best next course (highest weight)
        best_next = max(next_courses, key=lambda cid: next(
            edge['weight'] for edge in graph['edges']
            if edge['from'] == course_id and edge['to'] == cid
        ))
        
        return self._dfs_path(best_next, graph, current_path, max_depth)
    
    def recommend_learning_path(self, user_skills: List[str], target_skills: List[str], 
                              available_courses: List[Dict]) -> List[int]:
        """Recommend a learning path based on user skills and target skills."""
        # Build learning path graph
        graph = self.build_learning_path_graph(available_courses)
        
        # Find courses that teach target skills
        target_courses = []
        for course_id, node in graph['nodes'].items():
            course_skills = set(node['skills'] + node['outcome_skills'])
            if any(skill in course_skills for skill in target_skills):
                target_courses.append(course_id)
        
        if not target_courses:
            return []
        
        # Find the best path to target courses
        best_path = []
        min_distance = float('inf')
        
        for target_course in target_courses:
            path = self._find_shortest_path_to_course(
                user_skills, target_course, graph
            )
            if path and len(path) < min_distance:
                best_path = path
                min_distance = len(path)
        
        return best_path
    
    def _find_shortest_path_to_course(self, user_skills: List[str], target_course: int, 
                                    graph: Dict[str, Any]) -> List[int]:
        """Find shortest path to a target course based on user skills."""
        # Find courses user can start with (prerequisites satisfied)
        startable_courses = []
        for course_id, node in graph['nodes'].items():
            prereq_skills = set(node['prerequisite_skills'])
            user_skill_set = set(user_skills)
            
            if prereq_skills.issubset(user_skill_set):
                startable_courses.append(course_id)
        
        if not startable_courses:
            return []
        
        # Use BFS to find shortest path
        from collections import deque
        
        queue = deque([(course, [course]) for course in startable_courses])
        visited = set()
        
        while queue:
            current_course, path = queue.popleft()
            
            if current_course == target_course:
                return path
            
            if current_course in visited:
                continue
            
            visited.add(current_course)
            
            # Add next courses
            for edge in graph['edges']:
                if edge['from'] == current_course and edge['to'] not in visited:
                    queue.append((edge['to'], path + [edge['to']]))
        
        return []
    
    def save_semantic_models(self, filepath: str):
        """Save semantic models and embeddings."""
        models_data = {
            'course_embeddings': self.course_embeddings,
            'skill_ontology': self.skill_ontology,
            'learning_path_graph': self.learning_path_graph
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(models_data, f)
        
        logger.info(f"Semantic models saved to {filepath}")
    
    def load_semantic_models(self, filepath: str):
        """Load semantic models and embeddings."""
        if not os.path.exists(filepath):
            logger.warning(f"Semantic models file not found: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            models_data = pickle.load(f)
        
        self.course_embeddings = models_data.get('course_embeddings', {})
        self.skill_ontology = models_data.get('skill_ontology', {})
        self.learning_path_graph = models_data.get('learning_path_graph', {})
        
        logger.info(f"Semantic models loaded from {filepath}")


# Custom spaCy component for skill extraction
def create_skill_extractor(nlp, name):
    """Create a custom spaCy component for skill extraction."""
    def skill_extractor(doc):
        # This is a placeholder for custom skill extraction logic
        # In a real implementation, you would add custom logic here
        return doc
    
    return skill_extractor

# Register the custom component
if SPACY_AVAILABLE:
    from spacy.language import Language
    
    @Language.component("skill_extractor")
    def skill_extractor_component(nlp, name):
        return create_skill_extractor(nlp, name)
