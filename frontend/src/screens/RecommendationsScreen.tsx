import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  FlatList,
  RefreshControl,
  Alert,
  Platform,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { 
  fetchRecommendations, 
  generateRecommendations, 
  submitFeedback,
  clearRecommendations 
} from '../store/slices/recommendationSlice';
import { fetchCategories } from '../store/slices/courseSlice';
import { Recommendation, RecommendationRequest } from '../types';
import { Ionicons } from '@expo/vector-icons';
import LoadingComponent from '../components/LoadingComponent';
import apiService from '../services/api';
import { 
  getResponsiveRecommendationsStyles, 
  isWeb, 
  isTablet, 
  isDesktop, 
  isMobile 
} from '../styles/recommendationsStyles';

interface RecommendationsScreenProps {
  navigation: any;
}

const RecommendationsScreen: React.FC<RecommendationsScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { recommendations, isLoading, error } = useSelector((state: RootState) => state.recommendations);
  const { categories } = useSelector((state: RootState) => state.courses);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string>('hybrid');
  const [selectedFilters, setSelectedFilters] = useState({
    difficulty: '',
    category: '',
    maxDuration: '',
    contentType: '',
  });
  const [dataRequirements, setDataRequirements] = useState<{
    has_sufficient_data: boolean;
    interaction_count: number;
    enrollment_count: number;
    min_interactions_required: number;
    min_enrollments_required: number;
    interaction_progress: number;
    enrollment_progress: number;
    recommendations: {
      interactions_needed: number;
      enrollments_needed: number;
      suggestions: string[];
    };
  } | null>(null);
  const [loadingRequirements, setLoadingRequirements] = useState(true);
  const [showMinLoading, setShowMinLoading] = useState(false);
  const [showPageLoading, setShowPageLoading] = useState(true);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  
  const styles = getResponsiveRecommendationsStyles();

  const algorithms = [
    { id: 'hybrid', name: 'Hybrid AI', description: 'Best overall recommendations' },
    { id: 'collaborative', name: 'Collaborative', description: 'Based on similar users' },
    { id: 'content', name: 'Content-Based', description: 'Based on course content' },
    { id: 'popularity', name: 'Popularity', description: 'Trending courses' },
  ];

  const [difficultyLevels, setDifficultyLevels] = useState<string[]>([]);
  const categoryNames = ['All', ...categories.map(cat => cat.name)];

  useEffect(() => {
    loadDataRequirements();
    dispatch(fetchCategories());
    loadDifficultyLevels();
    
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [dispatch]);

  // Listen for navigation focus to refresh data requirements
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      loadDataRequirements();
    });

    return unsubscribe;
  }, [navigation]);

  const loadDataRequirements = async () => {
    try {
      setLoadingRequirements(true);
      const requirements = await apiService.getDataRequirements();
      setDataRequirements(requirements);
      
      // Don't auto-fetch recommendations, let user choose algorithm and filters first
    } catch (error) {
      console.error('Error loading data requirements:', error);
    } finally {
      setLoadingRequirements(false);
    }
  };

  const loadDifficultyLevels = async () => {
    try {
      const levels = await apiService.getDifficultyLevels();
      // Capitalize first letter of each difficulty level
      const capitalizedLevels = levels.map(level => 
        level.charAt(0).toUpperCase() + level.slice(1).toLowerCase()
      );
      setDifficultyLevels(capitalizedLevels);
    } catch (error) {
      console.error('Error loading difficulty levels:', error);
      // Fallback to default levels if API fails
      setDifficultyLevels(['Beginner', 'Intermediate', 'Advanced']);
    }
  };

  const getRecommendationTitle = () => {
    if (selectedAlgorithm === 'hybrid') {
      return 'AI-Powered Recommendations';
    } else if (selectedAlgorithm === 'collaborative') {
      return 'Based on Similar Learners';
    } else if (selectedAlgorithm === 'content') {
      return 'Content-Based Recommendations';
    } else if (selectedAlgorithm === 'popularity') {
      return 'Popular & Trending Courses';
    }
    return 'Recommended for You';
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await dispatch(fetchRecommendations({ limit: 20 }));
    setRefreshing(false);
  };

  const handleGenerateRecommendations = () => {
    if (!dataRequirements?.has_sufficient_data) {
      Alert.alert(
        'Insufficient Data',
        'You need more course interactions to get personalized AI recommendations. Please browse and enroll in more courses first.',
        [{ text: 'OK' }]
      );
      return;
    }

    const request: RecommendationRequest = {
      limit: 20,
      algorithm: selectedAlgorithm,
    };

    if (selectedFilters.difficulty) {
      request.difficulty_level = selectedFilters.difficulty;
    }
    if (selectedFilters.category && selectedFilters.category !== 'All') {
      request.category = selectedFilters.category;
    }
    if (selectedFilters.maxDuration) {
      request.max_duration_hours = parseInt(selectedFilters.maxDuration);
    }
    if (selectedFilters.contentType) {
      request.content_type = selectedFilters.contentType;
    }

    // console.log('DEBUG: Final request object:', request);
    
    // Show minimum loading for 2 seconds
    setShowMinLoading(true);
    dispatch(generateRecommendations(request));
    
    // Hide minimum loading after 2 seconds
    setTimeout(() => {
      setShowMinLoading(false);
    }, 2000);
  };

  const handleFeedback = async (courseId: number, feedbackType: 'like' | 'dislike') => {
    try {
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const deviceType = Platform.OS === 'web' ? 'web' : Platform.OS;
      const referrer = 'ai_recommendations';
      
      if (feedbackType === 'like') {
        await apiService.trackCourseLike(courseId, sessionId, deviceType, referrer);
        Alert.alert('Thank you!', 'Course added to favorites! This will help improve future recommendations.');
      } else {
        await apiService.trackCourseUnlike(courseId, sessionId, deviceType, referrer);
        Alert.alert('Thank you!', 'Course removed from favorites. This will help improve future recommendations.');
      }
    } catch (error) {
      console.error('Error tracking feedback:', error);
      Alert.alert('Error', 'Failed to record feedback. Please try again.');
    }
  };

  const handleCoursePress = (courseId: number) => {
    navigation.navigate('CourseDetail', { courseId, referrer: 'ai_recommendations' });
  };

  const renderRecommendationItem = ({ item, index }: { item: Recommendation; index: number }) => (
    <TouchableOpacity
      style={[
        styles.recommendationCard,
        hoveredCard === item.course_id.toString() && styles.recommendationCardHovered
      ]}
      onPress={() => handleCoursePress(item.course_id)}
      onPressIn={() => setHoveredCard(item.course_id.toString())}
      onPressOut={() => setHoveredCard(null)}
    >
      <View style={styles.recommendationHeader}>
        <View style={styles.rankBadge}>
          <Text style={styles.rankText}>#{index + 1}</Text>
        </View>
        <View style={styles.aiBadge}>
          <Ionicons name="bulb" size={12} color="white" />
          <Text style={styles.aiBadgeText}>AI</Text>
        </View>
        <View style={styles.confidenceBadge}>
          <Ionicons name="trending-up" size={12} color="white" />
          <Text style={styles.confidenceText}>
            {Math.round(item.confidence_score * 100)}%
          </Text>
        </View>
      </View>

      <View style={styles.recommendationContent}>
        <Text style={styles.recommendationTitle} numberOfLines={2}>
          {item.title}
        </Text>
        <Text style={styles.recommendationInstructor}>{item.instructor}</Text>
        
        <View style={styles.recommendationMeta}>
          <View style={styles.metaItem}>
            <Ionicons name="star" size={14} color="#FFD700" />
            <Text style={styles.metaText}>{item.rating.toFixed(2)}</Text>
          </View>
          <View style={styles.metaItem}>
            <Ionicons name="time" size={14} color="#666" />
            <Text style={styles.metaText}>{item.duration_hours}h</Text>
          </View>
          <View style={styles.metaItem}>
            <Ionicons name="people" size={14} color="#666" />
            <Text style={styles.metaText}>{item.enrollment_count}</Text>
          </View>
        </View>

        {item.recommendation_reason && (
          <Text style={styles.recommendationReason} numberOfLines={2}>
            {item.recommendation_reason}
          </Text>
        )}

        <View style={styles.recommendationFooter}>
          <Text style={styles.priceText}>
            {item.is_free ? 'Free' : `$${item.price}`}
          </Text>
          <View style={styles.feedbackButtons}>
            <TouchableOpacity
              style={styles.feedbackButton}
              onPress={() => handleFeedback(item.course_id, 'like')}
            >
              <Ionicons name="thumbs-up" size={16} color="#4CAF50" />
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.feedbackButton}
              onPress={() => handleFeedback(item.course_id, 'dislike')}
            >
              <Ionicons name="thumbs-down" size={16} color="#ff6b6b" />
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );

  const renderAlgorithmItem = ({ item }: { item: typeof algorithms[0] }) => (
    <TouchableOpacity
      style={[
        styles.algorithmCard,
        selectedAlgorithm === item.id && styles.selectedAlgorithmCard,
      ]}
      onPress={() => {
        setSelectedAlgorithm(item.id);
        // Clear recommendations when algorithm changes
        dispatch(clearRecommendations());
      }}
    >
      <Text style={[
        styles.algorithmName,
        selectedAlgorithm === item.id && styles.selectedAlgorithmName,
      ]}>
        {item.name}
      </Text>
      <Text style={[
        styles.algorithmDescription,
        selectedAlgorithm === item.id && styles.selectedAlgorithmDescription,
      ]}>
        {item.description}
      </Text>
    </TouchableOpacity>
  );

  // Show loading screen
  if (showPageLoading) {
    return <LoadingComponent />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        style={styles.scrollContainer}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        {...(isWeb && {
          scrollEventThrottle: 16,
          nestedScrollEnabled: true,
        })}
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <TouchableOpacity
              style={styles.backButton}
              onPress={() => navigation.goBack()}
            >
              <Ionicons 
                name="arrow-back" 
                size={isDesktop ? 28 : isTablet ? 26 : 24} 
                color="#666" 
              />
            </TouchableOpacity>
            <Text style={styles.headerTitle}>
              AI Courses
            </Text>
            <View style={styles.headerPlaceholder} />
          </View>
        </View>
        {/* Data Requirements Warning */}
        {loadingRequirements ? (
          <View style={styles.loadingContainer}>
            <LoadingComponent visible={true} overlayColor="transparent" />
          </View>
        ) : dataRequirements && !dataRequirements.has_sufficient_data ? (
          <View style={styles.warningContainer}>
            <View style={styles.warningHeader}>
              <Ionicons name="information-circle" size={24} color="#ff9800" />
              <Text style={styles.warningTitle}>More Data Needed for AI Recommendations</Text>
            </View>
            
            <View style={styles.progressContainer}>
              <View style={styles.progressItem}>
                <Text style={styles.progressLabel}>Course Interactions</Text>
                <View style={styles.progressBar}>
                  <View style={[styles.progressFill, { width: `${dataRequirements.interaction_progress}%` }]} />
                </View>
                <Text style={styles.progressText}>
                  {dataRequirements.interaction_count} / {dataRequirements.min_interactions_required}
                </Text>
              </View>
              
              <View style={styles.progressItem}>
                <Text style={styles.progressLabel}>Course Enrollments</Text>
                <View style={styles.progressBar}>
                  <View style={[styles.progressFill, { width: `${dataRequirements.enrollment_progress}%` }]} />
                </View>
                <Text style={styles.progressText}>
                  {dataRequirements.enrollment_count} / {dataRequirements.min_enrollments_required}
                </Text>
              </View>
            </View>
            
            <View style={styles.suggestionsContainer}>
              <Text style={styles.suggestionsTitle}>To get personalized AI recommendations:</Text>
              {dataRequirements.recommendations.suggestions.map((suggestion, index) => (
                <View key={index} style={styles.suggestionItem}>
                  <Ionicons name="checkmark-circle" size={16} color="#4CAF50" />
                  <Text style={styles.suggestionText}>{suggestion}</Text>
                </View>
              ))}
            </View>
            
            <TouchableOpacity
              style={styles.browseButton}
              onPress={() => navigation.navigate('Courses')}
            >
              <Ionicons name="book" size={20} color="white" />
              <Text style={styles.browseButtonText}>Browse Courses</Text>
            </TouchableOpacity>
          </View>
        ) : null}

        {/* Show algorithm and filters only if user has sufficient data */}
        {dataRequirements && dataRequirements.has_sufficient_data && (
          <>
            {/* AI Algorithm Selection */}
            <View style={styles.algorithmSection}>
          <Text style={styles.sectionTitle}>Choose AI Algorithm</Text>
          <FlatList
            data={algorithms}
            renderItem={renderAlgorithmItem}
            keyExtractor={(item) => item.id}
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.algorithmsList}
          />
        </View>

        {/* Filters */}
        <View style={styles.filtersSection}>
          <Text style={styles.sectionTitle}>Filters</Text>
          <View style={styles.filtersContainer}>
            <View style={styles.filterRow}>
              <Text style={styles.filterLabel}>Difficulty:</Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                {difficultyLevels.map((level) => (
                  <TouchableOpacity
                    key={level}
                    style={[
                      styles.filterChip,
                      selectedFilters.difficulty === level && styles.selectedFilterChip,
                    ]}
                    onPress={() => setSelectedFilters(prev => ({
                      ...prev,
                      difficulty: prev.difficulty === level ? '' : level
                    }))}
                  >
                    <Text style={[
                      styles.filterChipText,
                      selectedFilters.difficulty === level && styles.selectedFilterChipText,
                    ]}>
                      {level}
                    </Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>
            </View>

            <View style={styles.filterRow}>
              <Text style={styles.filterLabel}>Category:</Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                {categoryNames.map((category) => (
                  <TouchableOpacity
                    key={category}
                    style={[
                      styles.filterChip,
                      selectedFilters.category === category && styles.selectedFilterChip,
                    ]}
                    onPress={() => setSelectedFilters(prev => ({
                      ...prev,
                      category: prev.category === category ? '' : category
                    }))}
                  >
                    <Text style={[
                      styles.filterChipText,
                      selectedFilters.category === category && styles.selectedFilterChipText,
                    ]}>
                      {category}
                    </Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>
            </View>
          </View>
        </View>

        {/* Generate Button */}
        <View style={styles.generateButtonContainer}>
          <TouchableOpacity
            style={styles.generateButton}
            onPress={handleGenerateRecommendations}
            disabled={isLoading}
          >
            <Ionicons name="bulb" size={20} color="white" />
            <Text style={styles.generateButtonText}>
              {isLoading ? 'Generating...' : 'Generate New Recommendations'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Recommendations List */}
        <View style={styles.recommendationsSection}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>{getRecommendationTitle()}</Text>
            <Text style={styles.recommendationsCount}>
              {recommendations.length} courses
            </Text>
          </View>

          {(isLoading || showMinLoading) && recommendations.length === 0 ? (
            <View style={styles.loadingContainer}>
              <LoadingComponent visible={true} overlayColor="transparent" />
            </View>
          ) : error ? (
            <View style={styles.errorContainer}>
              <Ionicons name="alert-circle" size={50} color="#ff6b6b" />
              <Text style={styles.errorText}>Failed to load recommendations</Text>
              <Text style={styles.errorSubtext}>{error}</Text>
              <TouchableOpacity
                style={styles.retryButton}
                onPress={() => dispatch(fetchRecommendations({ limit: 20 }))}
              >
                <Text style={styles.retryButtonText}>Retry</Text>
              </TouchableOpacity>
            </View>
          ) : recommendations.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="bulb-outline" size={50} color="#ccc" />
              <Text style={styles.emptyText}>No recommendations yet</Text>
              <Text style={styles.emptySubtext}>
                Generate recommendations to see personalized course suggestions
              </Text>
            </View>
          ) : (
            <FlatList
              data={recommendations}
              renderItem={renderRecommendationItem}
              keyExtractor={(item) => item.course_id.toString()}
              refreshControl={
                <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
              }
              scrollEnabled={false}
              contentContainerStyle={styles.recommendationsList}
            />
          )}
        </View>
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

// Styles are now handled by responsive styles

export default RecommendationsScreen;
