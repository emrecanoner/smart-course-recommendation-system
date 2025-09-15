import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { fetchRecommendations } from '../store/slices/recommendationSlice';
import { logout } from '../store/slices/authSlice';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

interface HomeScreenProps {
  navigation: any;
}

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const { recommendations, isLoading } = useSelector((state: RootState) => state.recommendations) as { recommendations: any[], isLoading: boolean };

  useEffect(() => {
    // Fetch recommendations when component mounts
    dispatch(fetchRecommendations({ limit: 5 }));
  }, [dispatch]);

  const handleLogout = () => {
    dispatch(logout());
    // Navigate to login screen after logout
    navigation.navigate('Login');
  };

  const handleNavigateToCourses = () => {
    navigation.navigate('Courses');
  };

  const handleNavigateToRecommendations = () => {
    navigation.navigate('Recommendations');
  };

  const handleNavigateToProfile = () => {
    navigation.navigate('Profile');
  };

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.welcomeText}>Welcome back!</Text>
            <Text style={styles.userName}>{user?.full_name || user?.username}</Text>
          </View>
          <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
            <Ionicons name="log-out-outline" size={24} color="white" />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content}>
        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.quickActions}>
            <TouchableOpacity
              style={styles.actionCard}
              onPress={handleNavigateToCourses}
            >
              <Ionicons name="book" size={30} color="#667eea" />
              <Text style={styles.actionTitle}>Browse Courses</Text>
              <Text style={styles.actionSubtitle}>Explore all courses</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.actionCard}
              onPress={handleNavigateToRecommendations}
            >
              <Ionicons name="bulb" size={30} color="#667eea" />
              <Text style={styles.actionTitle}>AI Recommendations</Text>
              <Text style={styles.actionSubtitle}>Personalized for you</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Recommended Courses */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recommended for You</Text>
            <TouchableOpacity onPress={handleNavigateToRecommendations}>
              <Text style={styles.seeAllText}>See All</Text>
            </TouchableOpacity>
          </View>

          {isLoading ? (
            <View style={styles.loadingContainer}>
              <Text style={styles.loadingText}>Loading recommendations...</Text>
            </View>
          ) : recommendations.length > 0 ? (
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {recommendations.map((recommendation: any) => (
                <TouchableOpacity
                  key={recommendation.course_id}
                  style={styles.recommendationCard}
                  onPress={() => navigation.navigate('CourseDetail', { 
                    courseId: recommendation.course_id 
                  })}
                >
                  <View style={styles.recommendationHeader}>
                    <Text style={styles.recommendationTitle} numberOfLines={2}>
                      {recommendation.title}
                    </Text>
                    <View style={styles.ratingContainer}>
                      <Ionicons name="star" size={16} color="#FFD700" />
                      <Text style={styles.ratingText}>{recommendation.rating.toFixed(1)}</Text>
                    </View>
                  </View>
                  <Text style={styles.recommendationInstructor}>
                    {recommendation.instructor}
                  </Text>
                  <Text style={styles.recommendationReason} numberOfLines={2}>
                    {recommendation.recommendation_reason}
                  </Text>
                  <View style={styles.recommendationFooter}>
                    <Text style={styles.confidenceScore}>
                      {Math.round(recommendation.confidence_score * 100)}% match
                    </Text>
                    <Text style={styles.priceText}>
                      {recommendation.is_free ? 'Free' : `$${recommendation.price}`}
                    </Text>
                  </View>
                </TouchableOpacity>
              ))}
            </ScrollView>
          ) : (
            <View style={styles.emptyContainer}>
              <Ionicons name="bulb-outline" size={50} color="#ccc" />
              <Text style={styles.emptyText}>No recommendations yet</Text>
              <Text style={styles.emptySubtext}>
                Browse courses to get personalized recommendations
              </Text>
            </View>
          )}
        </View>

        {/* Profile Section */}
        <View style={styles.section}>
          <TouchableOpacity
            style={styles.profileCard}
            onPress={handleNavigateToProfile}
          >
            <Ionicons name="person-circle" size={40} color="#667eea" />
            <View style={styles.profileInfo}>
              <Text style={styles.profileTitle}>Manage Profile</Text>
              <Text style={styles.profileSubtitle}>
                Update your preferences and learning goals
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#ccc" />
          </TouchableOpacity>
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
    paddingBottom: 30,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  welcomeText: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginTop: 5,
  },
  logoutButton: {
    padding: 10,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  section: {
    marginTop: 30,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  seeAllText: {
    fontSize: 16,
    color: '#667eea',
    fontWeight: '500',
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionCard: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 20,
    marginHorizontal: 5,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 10,
  },
  actionSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
    textAlign: 'center',
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
  },
  recommendationCard: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 15,
    marginRight: 15,
    width: 280,
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
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  recommendationTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 10,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingText: {
    fontSize: 14,
    color: '#333',
    marginLeft: 5,
  },
  recommendationInstructor: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  recommendationReason: {
    fontSize: 14,
    color: '#888',
    marginBottom: 15,
  },
  recommendationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  confidenceScore: {
    fontSize: 12,
    color: '#667eea',
    fontWeight: '500',
  },
  priceText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
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
  profileCard: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  profileInfo: {
    flex: 1,
    marginLeft: 15,
  },
  profileTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  profileSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
});

export default HomeScreen;
