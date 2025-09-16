import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  Platform,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { fetchRecommendations } from '../store/slices/recommendationSlice';
import { logout } from '../store/slices/authSlice';
import { Ionicons } from '@expo/vector-icons';
import LoadingComponent from '../components/LoadingComponent';
import { 
  getResponsiveHomeStyles, 
  isWeb, 
  isTablet, 
  isDesktop,
  isMobile 
} from '../styles/responsiveStyles';

interface HomeScreenProps {
  navigation: any;
}

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const { recommendations, isLoading } = useSelector((state: RootState) => state.recommendations) as { recommendations: any[], isLoading: boolean };
  const [showPageLoading, setShowPageLoading] = React.useState(true);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  
  const styles = getResponsiveHomeStyles();

  useEffect(() => {
    // Fetch recommendations when component mounts
    dispatch(fetchRecommendations({ limit: 5 }));
    
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
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

  // Show loading screen when page opens
  if (showPageLoading) {
    return (
      <LoadingComponent 
        visible={true}
      />
    );
  }

  return (
    <SafeAreaView style={styles.homeContainer}>
      {/* Modern Responsive Header */}
      <View style={styles.homeHeader}>
        <View style={styles.homeHeaderContent}>
          <View style={styles.homeUserInfo}>
            <Text style={styles.homeWelcomeText}>
              {isDesktop ? 'Welcome back to Smart Course!' : 'Welcome back!'}
            </Text>
            <Text style={styles.homeUserName}>{user?.full_name || user?.username}</Text>
          </View>
          <View style={styles.homeHeaderActions}>
            <TouchableOpacity 
              onPress={handleNavigateToProfile} 
              style={styles.homeHeaderButton}
              onPressIn={() => isWeb && setHoveredCard('profile')}
              onPressOut={() => isWeb && setHoveredCard(null)}
            >
              <Ionicons 
                name="person-circle-outline" 
                size={isDesktop ? 28 : isTablet ? 26 : 24} 
                color="#666" 
              />
            </TouchableOpacity>
            <TouchableOpacity 
              onPress={handleLogout} 
              style={styles.homeHeaderButton}
              onPressIn={() => isWeb && setHoveredCard('logout')}
              onPressOut={() => isWeb && setHoveredCard(null)}
            >
              <Ionicons 
                name="log-out-outline" 
                size={isDesktop ? 28 : isTablet ? 26 : 24} 
                color="#666" 
              />
            </TouchableOpacity>
          </View>
        </View>
      </View>

      <View style={styles.homeMainContent}>
        <ScrollView 
          style={styles.homeScrollContent} 
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{ paddingBottom: 40 }}
        >
        {/* Quick Actions */}
        <View style={styles.homeSection}>
          <View style={styles.homeSectionHeader}>
            <Text style={styles.homeSectionTitle}>
              {isDesktop ? 'Quick Actions & Navigation' : 'Quick Actions'}
            </Text>
          </View>
          <View style={styles.homeQuickActions}>
            <TouchableOpacity
              style={[
                styles.homeActionCard,
                hoveredCard === 'courses' && isWeb && {
                  transform: [{ translateY: -4 }],
                  shadowOpacity: 0.15,
                  borderColor: '#007bff',
                  shadowColor: '#007bff',
                }
              ]}
              onPress={handleNavigateToCourses}
              onPressIn={() => isWeb && setHoveredCard('courses')}
              onPressOut={() => isWeb && setHoveredCard(null)}
            >
              <View style={styles.homeActionIconContainer}>
                <Ionicons 
                  name="library" 
                  size={isDesktop ? 40 : isTablet ? 36 : 32} 
                  color="#007bff" 
                />
              </View>
              <Text style={styles.homeActionTitle}>
                {isDesktop ? 'Browse All Courses' : 'Browse Courses'}
              </Text>
              <Text style={styles.homeActionSubtitle}>
                {isDesktop ? 'Explore our comprehensive course library' : 'Explore all available courses'}
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.homeActionCard,
                hoveredCard === 'recommendations' && isWeb && {
                  transform: [{ translateY: -4 }],
                  shadowOpacity: 0.15,
                  borderColor: '#007bff',
                  shadowColor: '#007bff',
                }
              ]}
              onPress={handleNavigateToRecommendations}
              onPressIn={() => isWeb && setHoveredCard('recommendations')}
              onPressOut={() => isWeb && setHoveredCard(null)}
            >
              <View style={styles.homeActionIconContainer}>
                <Ionicons 
                  name="sparkles" 
                  size={isDesktop ? 40 : isTablet ? 36 : 32} 
                  color="#007bff" 
                />
              </View>
              <Text style={styles.homeActionTitle}>
                {isDesktop ? 'AI-Powered Recommendations' : 'AI Recommendations'}
              </Text>
              <Text style={styles.homeActionSubtitle}>
                {isDesktop ? 'Get personalized course suggestions based on your learning patterns' : 'Personalized course suggestions'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Recommended Courses */}
        <View style={styles.homeSection}>
          {isMobile ? (
            // Mobile layout - stacked vertically
            <View>
              <Text style={styles.homeSectionTitle}>
                Recommended for You
              </Text>
              <TouchableOpacity 
                onPress={handleNavigateToRecommendations}
                style={{ marginTop: 8, marginBottom: 16 }}
              >
                <Text style={styles.homeSeeAllText}>
                  See All
                </Text>
              </TouchableOpacity>
            </View>
          ) : (
            // Desktop/Tablet layout - side by side
            <View style={styles.homeSectionHeader}>
              <Text style={styles.homeSectionTitle}>
                {isDesktop ? 'AI-Powered Recommendations for You' : 'Recommended for You'}
              </Text>
              <TouchableOpacity onPress={handleNavigateToRecommendations}>
                <Text style={styles.homeSeeAllText}>
                  {isDesktop ? 'View All Recommendations' : 'See All'}
                </Text>
              </TouchableOpacity>
            </View>
          )}

          {isLoading ? (
            <View style={styles.homeLoadingContainer}>
              <Ionicons name="hourglass-outline" size={isDesktop ? 40 : 30} color="#6c757d" />
              <Text style={styles.homeLoadingText}>
                {isDesktop ? 'Loading personalized recommendations...' : 'Loading recommendations...'}
              </Text>
            </View>
          ) : recommendations.length > 0 ? (
            isMobile ? (
              // Mobile: 2 rows layout
              <View style={styles.homeRecommendationGrid}>
                {recommendations.map((recommendation: any) => (
                  <TouchableOpacity
                    key={recommendation.course_id}
                    style={[
                      styles.homeRecommendationCardMobile,
                      hoveredCard === `rec-${recommendation.course_id}` && isWeb && {
                        transform: [{ translateY: -4 }],
                        shadowOpacity: 0.15,
                        borderColor: '#007bff',
                        shadowColor: '#007bff',
                      }
                    ]}
                    onPress={() => navigation.navigate('CourseDetail', { 
                      courseId: recommendation.course_id 
                    })}
                    onPressIn={() => isWeb && setHoveredCard(`rec-${recommendation.course_id}`)}
                    onPressOut={() => isWeb && setHoveredCard(null)}
                  >
                    <View style={{ flex: 1 }}>
                      <View style={styles.homeRecommendationHeader}>
                        <Text style={styles.homeRecommendationTitle} numberOfLines={2}>
                          {recommendation.title}
                        </Text>
                        <View style={styles.homeRatingContainer}>
                          <Ionicons 
                            name="star" 
                            size={16} 
                            color="#FFD700" 
                          />
                          <Text style={styles.homeRatingText}>
                            {recommendation.rating.toFixed(1)}
                          </Text>
                        </View>
                      </View>
                      <Text style={styles.homeRecommendationInstructor}>
                        {recommendation.instructor}
                      </Text>
                      <Text style={styles.homeRecommendationReason} numberOfLines={2}>
                        {recommendation.recommendation_reason}
                      </Text>
                    </View>
                    <View style={styles.homeRecommendationFooter}>
                      <Text style={styles.homeConfidenceScore}>
                        {Math.round(recommendation.confidence_score * 100)}% match
                      </Text>
                      <Text style={styles.homePriceText}>
                        {recommendation.is_free ? 'Free' : `$${recommendation.price}`}
                      </Text>
                    </View>
                  </TouchableOpacity>
                ))}
              </View>
            ) : (
              // Desktop/Tablet: Horizontal scroll
              <ScrollView 
                horizontal 
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={{ 
                  paddingRight: isDesktop ? 20 : 10,
                  paddingLeft: 0,
                  alignItems: 'stretch'
                }}
                style={{ 
                  flexGrow: 0,
                  ...(isWeb && { 
                    overflow: 'auto' as any,
                    WebkitOverflowScrolling: 'touch' as any,
                    scrollbarWidth: 'none' as any,
                    msOverflowStyle: 'none' as any
                  })
                }}
                nestedScrollEnabled={true}
                scrollEventThrottle={16}
              >
                {recommendations.map((recommendation: any) => (
                <TouchableOpacity
                  key={recommendation.course_id}
                  style={[
                    styles.homeRecommendationCard,
                    hoveredCard === `rec-${recommendation.course_id}` && isWeb && {
                      transform: [{ translateY: -4 }],
                      shadowOpacity: 0.15,
                      borderColor: '#007bff',
                      shadowColor: '#007bff',
                    }
                  ]}
                  onPress={() => navigation.navigate('CourseDetail', { 
                    courseId: recommendation.course_id 
                  })}
                  onPressIn={() => isWeb && setHoveredCard(`rec-${recommendation.course_id}`)}
                  onPressOut={() => isWeb && setHoveredCard(null)}
                >
                  <View style={{ flex: 1 }}>
                    <View style={styles.homeRecommendationHeader}>
                      <Text style={styles.homeRecommendationTitle} numberOfLines={2}>
                        {recommendation.title}
                      </Text>
                      <View style={styles.homeRatingContainer}>
                        <Ionicons 
                          name="star" 
                          size={isDesktop ? 18 : 16} 
                          color="#FFD700" 
                        />
                        <Text style={styles.homeRatingText}>
                          {recommendation.rating.toFixed(1)}
                        </Text>
                      </View>
                    </View>
                    <Text style={styles.homeRecommendationInstructor}>
                      {recommendation.instructor}
                    </Text>
                    <Text style={styles.homeRecommendationReason} numberOfLines={isDesktop ? 3 : 2}>
                      {recommendation.recommendation_reason}
                    </Text>
                  </View>
                  <View style={styles.homeRecommendationFooter}>
                    <Text style={styles.homeConfidenceScore}>
                      {Math.round(recommendation.confidence_score * 100)}% match
                    </Text>
                    <Text style={styles.homePriceText}>
                      {recommendation.is_free ? 'Free' : `$${recommendation.price}`}
                    </Text>
                  </View>
                </TouchableOpacity>
                ))}
              </ScrollView>
            )
          ) : (
            <View style={styles.homeEmptyContainer}>
              <Ionicons 
                name="bulb-outline" 
                size={isDesktop ? 60 : 50} 
                color="#6c757d" 
              />
              <Text style={styles.homeEmptyText}>
                {isDesktop ? 'No personalized recommendations available yet' : 'No recommendations yet'}
              </Text>
              <Text style={styles.homeEmptySubtext}>
                {isDesktop 
                  ? 'Start browsing courses and interacting with content to receive AI-powered recommendations tailored to your learning preferences.'
                  : 'Browse courses to get personalized recommendations'
                }
              </Text>
            </View>
          )}
        </View>

        {/* Footer Section */}
        <View style={styles.homeFooter}>
          <View style={styles.homeFooterContent}>
            <Text style={styles.homeFooterText}>
              {isDesktop 
                ? 'Smart Course - AI-Powered Learning Platform' 
                : 'Smart Course'
              }
            </Text>
            <Text style={styles.homeFooterSubtext}>
              {isDesktop 
                ? 'Discover your next learning journey with personalized recommendations'
                : 'AI-Powered Learning'
              }
            </Text>
          </View>
        </View>

        </ScrollView>
      </View>
    </SafeAreaView>
  );
};


export default HomeScreen;
