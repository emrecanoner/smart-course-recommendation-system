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
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { 
  fetchRecommendations, 
  generateRecommendations, 
  submitFeedback,
  clearRecommendations 
} from '../store/slices/recommendationSlice';
import { Recommendation, RecommendationRequest } from '../types';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

interface RecommendationsScreenProps {
  navigation: any;
}

const RecommendationsScreen: React.FC<RecommendationsScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { recommendations, isLoading, error } = useSelector((state: RootState) => state.recommendations);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string>('hybrid');
  const [selectedFilters, setSelectedFilters] = useState({
    difficulty: '',
    category: '',
    maxDuration: '',
    contentType: '',
  });

  const algorithms = [
    { id: 'hybrid', name: 'Hybrid AI', description: 'Best overall recommendations' },
    { id: 'collaborative', name: 'Collaborative', description: 'Based on similar users' },
    { id: 'content', name: 'Content-Based', description: 'Based on course content' },
    { id: 'popularity', name: 'Popularity', description: 'Trending courses' },
  ];

  const difficultyLevels = ['Beginner', 'Intermediate', 'Advanced'];
  const categories = ['Programming', 'Design', 'Business', 'Marketing', 'Data Science'];
  const contentTypes = ['Video', 'Interactive', 'Text', 'Mixed'];

  useEffect(() => {
    dispatch(fetchRecommendations({ limit: 20 }));
  }, [dispatch]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await dispatch(fetchRecommendations({ limit: 20 }));
    setRefreshing(false);
  };

  const handleGenerateRecommendations = () => {
    const request: RecommendationRequest = {
      limit: 20,
      algorithm: selectedAlgorithm,
    };

    if (selectedFilters.difficulty) {
      request.difficulty_level = selectedFilters.difficulty;
    }
    if (selectedFilters.category) {
      request.categories = [selectedFilters.category];
    }
    if (selectedFilters.maxDuration) {
      request.max_duration_hours = parseInt(selectedFilters.maxDuration);
    }
    if (selectedFilters.contentType) {
      request.content_type = selectedFilters.contentType;
    }

    dispatch(generateRecommendations(request));
  };

  const handleFeedback = (courseId: number, feedbackType: 'like' | 'dislike') => {
    dispatch(submitFeedback({ courseId, feedbackType }));
    Alert.alert(
      'Thank you!',
      `Your ${feedbackType} feedback has been recorded and will help improve future recommendations.`
    );
  };

  const handleCoursePress = (courseId: number) => {
    navigation.navigate('CourseDetail', { courseId });
  };

  const renderRecommendationItem = ({ item, index }: { item: Recommendation; index: number }) => (
    <TouchableOpacity
      style={styles.recommendationCard}
      onPress={() => handleCoursePress(item.course_id)}
    >
      <View style={styles.recommendationHeader}>
        <View style={styles.rankBadge}>
          <Text style={styles.rankText}>#{index + 1}</Text>
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
            <Text style={styles.metaText}>{item.rating.toFixed(1)}</Text>
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
      onPress={() => setSelectedAlgorithm(item.id)}
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

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Ionicons name="arrow-back" size={24} color="white" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>AI Recommendations</Text>
          <TouchableOpacity
            style={styles.refreshButton}
            onPress={handleGenerateRecommendations}
          >
            <Ionicons name="refresh" size={24} color="white" />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* AI Algorithm Selection */}
        <View style={styles.section}>
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
        <View style={styles.section}>
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
                {categories.map((category) => (
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
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recommended for You</Text>
            <Text style={styles.recommendationsCount}>
              {recommendations.length} courses
            </Text>
          </View>

          {isLoading && recommendations.length === 0 ? (
            <View style={styles.loadingContainer}>
              <Ionicons name="bulb" size={50} color="#667eea" />
              <Text style={styles.loadingText}>AI is analyzing your preferences...</Text>
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
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    paddingTop: 20,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  backButton: {
    padding: 5,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  refreshButton: {
    padding: 5,
  },
  section: {
    backgroundColor: 'white',
    marginTop: 10,
    padding: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  recommendationsCount: {
    fontSize: 14,
    color: '#666',
  },
  algorithmsList: {
    paddingRight: 20,
  },
  algorithmCard: {
    backgroundColor: '#f5f5f5',
    borderRadius: 12,
    padding: 15,
    marginRight: 15,
    width: 150,
  },
  selectedAlgorithmCard: {
    backgroundColor: '#667eea',
  },
  algorithmName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  selectedAlgorithmName: {
    color: 'white',
  },
  algorithmDescription: {
    fontSize: 12,
    color: '#666',
  },
  selectedAlgorithmDescription: {
    color: 'rgba(255, 255, 255, 0.8)',
  },
  filtersContainer: {
    gap: 15,
  },
  filterRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  filterLabel: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
    marginRight: 15,
    minWidth: 80,
  },
  filterChip: {
    backgroundColor: '#f5f5f5',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    marginRight: 8,
  },
  selectedFilterChip: {
    backgroundColor: '#667eea',
  },
  filterChipText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '500',
  },
  selectedFilterChipText: {
    color: 'white',
  },
  generateButtonContainer: {
    padding: 20,
  },
  generateButton: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingVertical: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  generateButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  recommendationsList: {
    paddingBottom: 20,
  },
  recommendationCard: {
    backgroundColor: 'white',
    borderRadius: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  recommendationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    paddingBottom: 10,
  },
  rankBadge: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  rankText: {
    fontSize: 12,
    color: 'white',
    fontWeight: 'bold',
  },
  confidenceBadge: {
    backgroundColor: '#4CAF50',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    flexDirection: 'row',
    alignItems: 'center',
  },
  confidenceText: {
    fontSize: 12,
    color: 'white',
    fontWeight: 'bold',
    marginLeft: 4,
  },
  recommendationContent: {
    padding: 15,
    paddingTop: 0,
  },
  recommendationTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  recommendationInstructor: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  recommendationMeta: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 15,
  },
  metaText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  recommendationReason: {
    fontSize: 13,
    color: '#888',
    fontStyle: 'italic',
    marginBottom: 15,
  },
  recommendationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  priceText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#667eea',
  },
  feedbackButtons: {
    flexDirection: 'row',
  },
  feedbackButton: {
    padding: 8,
    marginLeft: 5,
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
    marginTop: 15,
    textAlign: 'center',
  },
  errorContainer: {
    alignItems: 'center',
    padding: 40,
  },
  errorText: {
    fontSize: 18,
    color: '#ff6b6b',
    marginTop: 15,
    textAlign: 'center',
  },
  errorSubtext: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
    textAlign: 'center',
  },
  retryButton: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingHorizontal: 20,
    paddingVertical: 10,
    marginTop: 20,
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    marginTop: 15,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    marginTop: 5,
    textAlign: 'center',
  },
});

export default RecommendationsScreen;
