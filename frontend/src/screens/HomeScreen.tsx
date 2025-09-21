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
import { fetchEnrollments } from '../store/slices/enrollmentSlice';
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
  const { enrollments, isLoading } = useSelector((state: RootState) => state.enrollments);
  const [showPageLoading, setShowPageLoading] = React.useState(true);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  
  const styles = getResponsiveHomeStyles();

  useEffect(() => {
    // Fetch enrolled courses when component mounts
    dispatch(fetchEnrollments());
    
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [dispatch]);

  // Listen for navigation focus to refresh data
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      // Show loading and refresh enrolled courses when screen comes into focus
      setShowPageLoading(true);
      dispatch(fetchEnrollments());
      
      // Hide loading after data is fetched
      const timer = setTimeout(() => {
        setShowPageLoading(false);
      }, 1500);
      
      return () => clearTimeout(timer);
    });

    return unsubscribe;
  }, [navigation, dispatch]);

  const handleLogout = () => {
    dispatch(logout());
    // Navigate to login screen after logout
    navigation.navigate('Login');
  };

  const handleNavigateToCourses = () => {
    navigation.navigate('Courses');
  };

  const handleNavigateToEnrollments = () => {
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
          contentContainerStyle={styles.homeScrollContentStyle}
          {...(isWeb && {
            scrollEventThrottle: 16,
            nestedScrollEnabled: true,
          })}
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
              onPress={handleNavigateToEnrollments}
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
            <View style={styles.homeSectionHeader}>
              <Text style={styles.homeSectionTitle}>
                Enrolled Courses
              </Text>
            </View>
          ) : (
            // Desktop/Tablet layout - side by side
            <View style={styles.homeSectionHeader}>
              <Text style={styles.homeSectionTitle}>
                {isDesktop ? 'My Enrolled Courses' : 'Enrolled Courses'}
              </Text>
            </View>
          )}

          {enrollments.length > 0 ? (
            isMobile ? (
              // Mobile: 2 rows layout
              <View style={styles.homeRecommendationGrid}>
                {enrollments.filter((enrollment: any) => enrollment.course).map((enrollment: any) => (
                  <TouchableOpacity
                    key={enrollment.course_id}
                    style={[
                      styles.homeRecommendationCardMobile,
                      hoveredCard === `rec-${enrollment.course_id}` && isWeb && {
                        transform: [{ translateY: -4 }],
                        shadowOpacity: 0.15,
                        borderColor: '#007bff',
                        shadowColor: '#007bff',
                      }
                    ]}
                    onPress={() => navigation.navigate('CourseDetail', { 
                      courseId: enrollment.course_id,
                      referrer: 'home'
                    })}
                    onPressIn={() => isWeb && setHoveredCard(`rec-${enrollment.course_id}`)}
                    onPressOut={() => isWeb && setHoveredCard(null)}
                  >
                    <View style={{ flex: 1 }}>
                      <View style={styles.homeRecommendationHeader}>
                        <Text style={styles.homeRecommendationTitle} numberOfLines={2}>
                          {enrollment.course.title}
                        </Text>
                        <View style={styles.homeRatingContainer}>
                          <Ionicons 
                            name="star" 
                            size={16} 
                            color="#FFD700" 
                          />
                          <Text style={styles.homeRatingText}>
                            {enrollment.course.rating.toFixed(1)}
                          </Text>
                        </View>
                      </View>
                      <Text style={styles.homeRecommendationInstructor}>
                        {enrollment.course.instructor}
                      </Text>
                      <Text style={styles.homeRecommendationReason} numberOfLines={2}>
                        Enrolled on {new Date(enrollment.enrollment_date).toLocaleDateString()}
                      </Text>
                    </View>
                    <View style={styles.homeRecommendationFooter}>
                      <Text style={styles.homeConfidenceScore}>
                        {enrollment.completion_percentage.toFixed(0)}% completed
                      </Text>
                      <Text style={styles.homePriceText}>
                        {!enrollment.course.is_free && `$${enrollment.course.price}`}
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
                    overflowX: 'auto' as any,
                    overflowY: 'hidden' as any,
                    WebkitOverflowScrolling: 'touch' as any,
                    scrollbarWidth: 'thin' as any,
                    msOverflowStyle: 'auto' as any,
                    cursor: 'grab' as any,
                  })
                }}
                nestedScrollEnabled={true}
                scrollEventThrottle={16}
                {...(isWeb && {
                  scrollEnabled: true,
                  directionalLockEnabled: true,
                })}
              >
                {enrollments.filter((enrollment: any) => enrollment.course).map((enrollment: any) => (
                <TouchableOpacity
                  key={enrollment.course_id}
                  style={[
                    styles.homeRecommendationCard,
                    hoveredCard === `rec-${enrollment.course_id}` && isWeb && {
                      transform: [{ translateY: -4 }],
                      shadowOpacity: 0.15,
                      borderColor: '#007bff',
                      shadowColor: '#007bff',
                    }
                  ]}
                  onPress={() => navigation.navigate('CourseDetail', { 
                    courseId: enrollment.course_id,
                    referrer: 'home'
                  })}
                  onPressIn={() => isWeb && setHoveredCard(`rec-${enrollment.course_id}`)}
                  onPressOut={() => isWeb && setHoveredCard(null)}
                >
                  <View style={{ flex: 1 }}>
                    <View style={styles.homeRecommendationHeader}>
                      <Text style={styles.homeRecommendationTitle} numberOfLines={2}>
                        {enrollment.course.title}
                      </Text>
                      <View style={styles.homeRatingContainer}>
                        <Ionicons 
                          name="star" 
                          size={isDesktop ? 18 : 16} 
                          color="#FFD700" 
                        />
                        <Text style={styles.homeRatingText}>
                        {enrollment.course.rating.toFixed(1)}
                        </Text>
                      </View>
                    </View>
                    <Text style={styles.homeRecommendationInstructor}>
                      {enrollment.course.instructor}
                    </Text>
                    <Text style={styles.homeRecommendationReason} numberOfLines={isDesktop ? 3 : 2}>
                      Enrolled on {new Date(enrollment.enrollment_date).toLocaleDateString()}
                    </Text>
                  </View>
                  <View style={styles.homeRecommendationFooter}>
                    <Text style={styles.homeConfidenceScore}>
                      {enrollment.completion_percentage.toFixed(0)}% completed
                    </Text>
                    <Text style={styles.homePriceText}>
                      {enrollment.course.is_free ? 'Free' : `$${enrollment.course.price}`}
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
                size={isDesktop ? 40 : 32} 
                color="#6c757d" 
              />
              <Text style={styles.homeEmptyText}>
                {isDesktop ? 'No enrolled courses yet' : 'No enrolled courses yet'}
              </Text>
              <Text style={styles.homeEmptySubtext}>
                {isDesktop 
                  ? 'Start exploring courses and enroll in ones that interest you to see them here.'
                  : 'Browse courses to enroll in them'
                }
              </Text>
            </View>
          )}
        </View>

        </ScrollView>
      </View>

      {/* Fixed Footer Section */}
      <View style={styles.homeFooter}>
        <View style={styles.homeFooterContent}>
          <View style={styles.homeFooterStats}>
            <View style={styles.homeFooterStatItem}>
              <Ionicons name="book-outline" size={isDesktop ? 24 : 20} color="#007bff" />
              <Text style={styles.homeFooterStatNumber}>
                {enrollments.length}
              </Text>
              <Text style={styles.homeFooterStatLabel}>
                {isDesktop ? 'Enrolled Courses' : 'Courses'}
              </Text>
            </View>
            
            <View style={styles.homeFooterStatItem}>
              <Ionicons name="trophy-outline" size={isDesktop ? 24 : 20} color="#28a745" />
              <Text style={styles.homeFooterStatNumber}>
                {enrollments.filter((e: any) => e.completion_percentage === 100).length}
              </Text>
              <Text style={styles.homeFooterStatLabel}>
                {isDesktop ? 'Completed' : 'Done'}
              </Text>
            </View>
            
            <View style={styles.homeFooterStatItem}>
              <Ionicons name="trending-up-outline" size={isDesktop ? 24 : 20} color="#ffc107" />
              <Text style={styles.homeFooterStatNumber}>
                {enrollments.length > 0 
                  ? Math.round(enrollments.reduce((sum: number, e: any) => sum + e.completion_percentage, 0) / enrollments.length)
                  : 0
                }%
              </Text>
              <Text style={styles.homeFooterStatLabel}>
                {isDesktop ? 'Avg Progress' : 'Progress'}
              </Text>
            </View>
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
};


export default HomeScreen;
