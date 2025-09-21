import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
  Modal,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { fetchCourse, setSelectedCourse } from '../store/slices/courseSlice';
// import { fetchSimilarCourses } from '../store/slices/recommendationSlice';
import { createEnrollment, checkEnrollment, unenrollFromCourse } from '../store/slices/enrollmentSlice';
import { Course, Recommendation } from '../types';
import { Ionicons } from '@expo/vector-icons';
import { getResponsiveCourseDetailStyles } from '../styles/courseDetailStyles';
import { isWeb, isTablet, isDesktop, isMobile } from '../styles/responsiveStyles';
import LoadingComponent from '../components/LoadingComponent';
import Button from '../components/Button';
import apiService from '../services/api';

interface CourseDetailScreenProps {
  navigation: any;
  route: {
    params: {
      courseId: number;
      referrer?: string;
    };
  };
}

const CourseDetailScreen: React.FC<CourseDetailScreenProps> = ({ navigation, route }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { selectedCourse, isLoading, error } = useSelector((state: RootState) => state.courses);
  // const { recommendations: similarCourses } = useSelector((state: RootState) => state.recommendations);
  const { isLoading: enrollmentLoading, enrollments, enrollmentStatus } = useSelector((state: RootState) => state.enrollments);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const [showPageLoading, setShowPageLoading] = React.useState(true);
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const [userRating, setUserRating] = useState(0);
  const [showRatingModal, setShowRatingModal] = useState(false);

  const { courseId, referrer = 'course_detail' } = route.params;
  const styles = getResponsiveCourseDetailStyles();

  useEffect(() => {
    dispatch(fetchCourse(courseId));
    // dispatch(fetchSimilarCourses({ courseId, limit: 3 }));
    dispatch(checkEnrollment(courseId));
    
    // Track course view
    trackCourseView();
    
    // Check if course is liked
    checkLikeStatus();
    
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [dispatch, courseId]);

  // Listen for navigation focus to refresh data
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      // Show loading and refresh course details and enrollment status when screen comes into focus
      setShowPageLoading(true);
      dispatch(fetchCourse(courseId)).finally(() => {
        // Hide loading after course data is fetched
        setTimeout(() => {
          setShowPageLoading(false);
        }, 500);
      });
      dispatch(checkEnrollment(courseId));
      // Don't check like status on focus to avoid overriding user actions
    });

    return unsubscribe;
  }, [navigation, dispatch, courseId]);

  // Check if user is enrolled in this course
  useEffect(() => {
    // First check enrollmentStatus from checkEnrollment API
    if (enrollmentStatus[courseId] !== undefined) {
      setIsEnrolled(enrollmentStatus[courseId]);
    } else {
      // Fallback to enrollments array
      const enrolled = enrollments.some(enrollment => 
        enrollment.course_id === courseId && enrollment.is_active
      );
      setIsEnrolled(enrolled);
    }
    
    // Check if course is completed
    const enrollment = enrollments.find(e => e.course_id === courseId && e.is_active);
    if (enrollment) {
      setIsCompleted(enrollment.is_completed || enrollment.completion_percentage >= 100);
    }
  }, [enrollments, enrollmentStatus, courseId]);

  // Tracking functions
  const trackCourseView = async () => {
    try {
      const deviceType = isWeb ? 'web' : isTablet ? 'tablet' : 'mobile';
      await apiService.trackCourseView(courseId, sessionId, deviceType, referrer);
    } catch (error) {
      // Error tracking course view
    }
  };

  const checkLikeStatus = async () => {
    try {
      const response = await apiService.getUserInteractionSummary();
      const summary = response.summary;
      if (summary && summary.interactions && Array.isArray(summary.interactions)) {
        // Find all like/unlike interactions for this course
        const courseInteractions = summary.interactions.filter(
          (interaction: any) => interaction.course_id === courseId && 
          (interaction.interaction_type === 'like' || interaction.interaction_type === 'unlike')
        );
        
        if (courseInteractions.length > 0) {
          // Sort by created_at to get the most recent interaction
          courseInteractions.sort((a: any, b: any) => 
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          );
          
          // Check the most recent interaction
          const latestInteraction = courseInteractions[0];
          setIsLiked(latestInteraction.interaction_type === 'like');
        } else {
          setIsLiked(false);
        }
      }
    } catch (error) {
      // Don't change state on error - keep current like status
    }
  };

  const handleLike = async () => {
    try {
      const deviceType = isWeb ? 'web' : isTablet ? 'tablet' : 'mobile';
      
      if (isLiked) {
        // Unlike
        await apiService.trackCourseUnlike(courseId, sessionId, deviceType, 'course_detail');
        setIsLiked(false);
        
        if (isWeb) {
          alert('Course removed from favorites!');
        } else {
          Alert.alert('Success', 'Course removed from favorites!');
        }
      } else {
        // Like
        await apiService.trackCourseLike(courseId, sessionId, deviceType, 'course_detail');
        setIsLiked(true);
        
        if (isWeb) {
          alert('Course added to favorites!');
        } else {
          Alert.alert('Success', 'Course added to favorites!');
        }
      }
    } catch (error) {
      console.log('Error tracking course like/unlike:', error);
    }
  };

  const handleCompleteCourse = async () => {
    try {
      const deviceType = isWeb ? 'web' : isTablet ? 'tablet' : 'mobile';
      
      await apiService.trackCourseComplete(courseId, 100, sessionId, deviceType, 'course_detail');
      setIsCompleted(true);
      
      // Show rating modal after completion
      setShowRatingModal(true);
      
      if (isWeb) {
        alert('Congratulations! Course completed! Please rate the course.');
      } else {
        Alert.alert('Congratulations!', 'Course completed! Please rate the course.');
      }
    } catch (error) {
      console.log('Error tracking course completion:', error);
    }
  };

  const handleRating = async (rating: number) => {
    try {
      const deviceType = isWeb ? 'web' : isTablet ? 'tablet' : 'mobile';
      await apiService.trackCourseRate(courseId, rating, sessionId, deviceType, 'course_detail');
      setUserRating(rating);
      setShowRatingModal(false);
      
      if (isWeb) {
        alert(`Thank you for rating ${rating} stars!`);
      } else {
        Alert.alert('Thank you!', `You rated this course ${rating} stars!`);
      }
    } catch (error) {
      console.log('Error tracking course rating:', error);
    }
  };

  const handleEnroll = () => {
    if (selectedCourse) {
      if (isEnrolled) {
        // Unenroll confirmation
        if (isWeb) {
          const confirmed = window.confirm(`Are you sure you want to unenroll from "${selectedCourse.title}"?`);
          if (confirmed) {
            performUnenrollment();
          }
        } else {
          Alert.alert(
            'Unenroll from Course',
            `Are you sure you want to unenroll from "${selectedCourse.title}"?`,
            [
              { text: 'Cancel', style: 'cancel' },
              { 
                text: 'Unenroll', 
                onPress: performUnenrollment
              },
            ]
          );
        }
      } else {
        // Enroll confirmation
        if (isWeb) {
          const confirmed = window.confirm(`Are you sure you want to enroll in "${selectedCourse.title}"?`);
          if (confirmed) {
            performEnrollment();
          }
        } else {
          Alert.alert(
            'Enroll in Course',
            `Are you sure you want to enroll in "${selectedCourse.title}"?`,
            [
              { text: 'Cancel', style: 'cancel' },
              { 
                text: 'Enroll', 
                onPress: performEnrollment
              },
            ]
          );
        }
      }
    }
  };

  const performEnrollment = async () => {
    try {
      const result = await dispatch(createEnrollment({ course_id: courseId })).unwrap();
      setIsEnrolled(true);
      
      // Track enrollment
      const deviceType = isWeb ? 'web' : isTablet ? 'tablet' : 'mobile';
      await apiService.trackCourseEnroll(courseId, sessionId, deviceType, 'course_detail');
      
      if (isWeb) {
        alert('Successfully enrolled in the course!');
      } else {
        Alert.alert('Success', 'Successfully enrolled in the course!');
      }
    } catch (error) {
      const errorMessage = `Failed to enroll in the course: ${error}`;
      
      if (isWeb) {
        alert(errorMessage);
      } else {
        Alert.alert('Error', errorMessage);
      }
    }
  };

  const performUnenrollment = async () => {
    try {
      const result = await dispatch(unenrollFromCourse(courseId)).unwrap();
      setIsEnrolled(false);
      
      // Track unenrollment
      const deviceType = isWeb ? 'web' : isTablet ? 'tablet' : 'mobile';
      await apiService.trackCourseUnenroll(courseId, sessionId, deviceType, 'course_detail');
      
      if (isWeb) {
        alert('Successfully unenrolled from the course!');
      } else {
        Alert.alert('Success', 'Successfully unenrolled from the course!');
      }
    } catch (error) {
      const errorMessage = `Failed to unenroll from the course: ${error}`;
      
      if (isWeb) {
        alert(errorMessage);
      } else {
        Alert.alert('Error', errorMessage);
      }
    }
  };

  const formatSkills = (skills: string | undefined): string => {
    if (!skills || skills.trim() === '' || skills.trim() === '[]') return 'No skillset defined';
    
    try {
      // If it comes as string array format (e.g., "['skill1', 'skill2']")
      if (skills.startsWith("['") && skills.endsWith("']") || 
          skills.startsWith('["') && skills.endsWith('"]')) {
        const arrayString = skills.slice(1, -1); // Remove first and last characters
        const skillsArray = arrayString.split("', '").map(skill => 
          skill.replace(/['"]/g, '').trim()
        );
        return skillsArray
          .map((skill: string) => {
            return skill.charAt(0).toUpperCase() + skill.slice(1).toLowerCase();
          })
          .join(', ');
      }
      
      // If it comes as real JSON array format, parse it
      if (skills.startsWith('[') && skills.endsWith(']')) {
        const skillsArray = JSON.parse(skills);
        return skillsArray
          .map((skill: string) => {
            const trimmed = skill.trim().replace(/['"]/g, '');
            return trimmed.charAt(0).toUpperCase() + trimmed.slice(1).toLowerCase();
          })
          .join(', ');
      }
      
      // If it's comma-separated string, format directly
      return skills
        .split(',')
        .map(skill => {
          const trimmed = skill.trim().replace(/['"]/g, '');
          return trimmed.charAt(0).toUpperCase() + trimmed.slice(1).toLowerCase();
        })
        .join(', ');
    } catch (error) {
      return skills; // Return original string in case of parse error
    }
  };

  // const handleSimilarCoursePress = (courseId: number) => {
  //   navigation.navigate('CourseDetail', { courseId });
  // };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<Ionicons key={i} name="star" size={16} color="#FFD700" />);
    }

    if (hasHalfStar) {
      stars.push(<Ionicons key="half" name="star-half" size={16} color="#FFD700" />);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<Ionicons key={`empty-${i}`} name="star-outline" size={16} color="#FFD700" />);
    }

    return stars;
  };

  // const renderSimilarCourse = ({ item }: { item: Recommendation }) => (
  //   <TouchableOpacity
  //     style={styles.courseDetailSimilarCard}
  //     onPress={() => handleSimilarCoursePress(item.course_id)}
  //   >
  //     <Text style={styles.courseDetailSimilarCardTitle} numberOfLines={2}>
  //       {item.title}
  //     </Text>
  //     <Text style={styles.courseDetailSimilarCardDescription} numberOfLines={3}>
  //       {item.instructor} • {item.is_free ? 'Free' : `$${item.price}`}
  //     </Text>
  //   </TouchableOpacity>
  // );

  if (isLoading || showPageLoading) {
    return <LoadingComponent />;
  }

  if (error || !selectedCourse) {
    return (
      <SafeAreaView style={styles.courseDetailContainer}>
        <View style={styles.courseDetailError}>
          <Ionicons name="alert-circle" size={50} color="#ff6b6b" />
          <Text style={styles.courseDetailErrorText}>Failed to load course</Text>
          <Text style={styles.courseDetailErrorText}>{error}</Text>
          <TouchableOpacity
            style={styles.courseDetailRetryButton}
            onPress={() => dispatch(fetchCourse(courseId))}
          >
            <Text style={styles.courseDetailRetryButtonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.courseDetailContainer}>
      <ScrollView 
        style={styles.courseDetailScrollContent}
        showsVerticalScrollIndicator={false}
        {...(isWeb && {
          scrollEventThrottle: 16,
          nestedScrollEnabled: true,
        })}
      >
        {/* Header */}
        <View style={styles.courseDetailHeader}>
          <View style={styles.courseDetailHeaderContent}>
            <TouchableOpacity
              style={styles.courseDetailBackButton}
              onPress={() => navigation.goBack()}
            >
              <Ionicons 
                name="arrow-back" 
                size={isDesktop ? 28 : isTablet ? 26 : 24} 
                color="#666" 
              />
            </TouchableOpacity>
            <Text style={styles.courseDetailHeaderTitle}>
              {isDesktop ? 'Course Details' : 'Course Details'}
            </Text>
            <View style={styles.courseDetailHeaderPlaceholder} />
          </View>
        </View>


        {/* Course Info */}
        <View style={styles.courseDetailInfo}>
          <View style={styles.courseDetailTitleContainer}>
            <Text style={styles.courseDetailTitle}>{selectedCourse.title}</Text>
            <TouchableOpacity
              style={styles.courseDetailLikeButton}
              onPress={handleLike}
            >
              <Ionicons 
                name={isLiked ? "heart" : "heart-outline"} 
                size={isDesktop ? 28 : isTablet ? 26 : 24} 
                color={isLiked ? "#ff6b6b" : "#666"} 
              />
            </TouchableOpacity>
          </View>
          
          <View style={styles.courseDetailInstructorRating}>
            <Text style={styles.courseDetailInstructor}>by {selectedCourse.instructor}</Text>
            <View style={styles.courseDetailRating}>
              {renderStars(selectedCourse.rating)}
              <Text style={styles.courseDetailRatingText}>
                {(selectedCourse.rating).toFixed(2)} ({selectedCourse.rating_count} reviews)
              </Text>
            </View>
          </View>

          <View style={styles.courseDetailMeta}>
            <View style={styles.courseDetailMetaItem}>
              <Ionicons name="time" size={16} color="#666" />
              <Text style={styles.courseDetailMetaText}>{selectedCourse.duration_hours} hours</Text>
            </View>
            <View style={styles.courseDetailMetaItem}>
              <Ionicons name="people" size={16} color="#666" />
              <Text style={styles.courseDetailMetaText}>{selectedCourse.enrollment_count} students</Text>
            </View>
            <View style={styles.courseDetailMetaItem}>
              <Ionicons name="trending-up" size={16} color="#666" />
              <Text style={styles.courseDetailMetaText}>{selectedCourse.completion_rate.toFixed(1)}% completion</Text>
            </View>
          </View>
        </View>

        {/* Description */}
        <View style={styles.courseDetailInfo}>
          <Text style={styles.courseDetailDescription}>{selectedCourse.description}</Text>
        </View>

        {/* Course Content Info */}
        <View style={styles.courseDetailInfo}>
          <Text style={styles.courseDetailContentTitle}>Course Content</Text>
          <View style={styles.courseDetailContentItems}>
            <View style={styles.courseDetailContentItem}>
              <Ionicons name="play-circle" size={16} color="#007AFF" />
              <Text style={styles.courseDetailContentText}>3 videos</Text>
            </View>
            <View style={styles.courseDetailContentItem}>
              <Ionicons name="document-text" size={16} color="#007AFF" />
              <Text style={styles.courseDetailContentText}>1 assignment</Text>
            </View>
            <View style={styles.courseDetailContentItem}>
              <Ionicons name="book" size={16} color="#007AFF" />
              <Text style={styles.courseDetailContentText}>1 reading</Text>
            </View>
            <View style={styles.courseDetailContentItem}>
              <Ionicons name="extension-puzzle" size={16} color="#007AFF" />
              <Text style={styles.courseDetailContentText}>1 plugin</Text>
            </View>
          </View>
        </View>

        {/* Skills */}
        <View style={styles.courseDetailSkills}>
          <Text style={styles.courseDetailSkillsTitle}>Skills You'll Learn</Text>
          <View style={styles.courseDetailSkillsContainer}>
            {formatSkills(selectedCourse.skills).split(', ').map((skill, index) => (
              <View key={index} style={styles.courseDetailSkillTag}>
                <Text style={styles.courseDetailSkillText}>{skill}</Text>
              </View>
            ))}
          </View>
        </View>


        {/* Actions */}
        <View style={styles.courseDetailActions}>
          {!isEnrolled ? (
            // Not enrolled - show enroll button
            <Button
              title="Enroll Now"
              onPress={handleEnroll}
              variant="primary"
              disabled={enrollmentLoading}
              icon={<Ionicons name="add-circle" size={20} color="#ffffff" />}
            />
          ) : isCompleted ? (
            // Completed - show disabled completed button
            <Button
              title="Course Completed"
              onPress={() => {}}
              variant="success"
              disabled={true}
              icon={<Ionicons name="checkmark-circle" size={20} color="#ffffff" />}
            />
          ) : (
            // Enrolled but not completed - show complete course button (like Enroll Now)
            <View>
              <Button
                title="Complete Course"
                onPress={handleCompleteCourse}
                variant="primary"
                disabled={enrollmentLoading}
                icon={<Ionicons name="checkmark-circle" size={20} color="#ffffff" />}
              />
              <TouchableOpacity
                style={styles.courseDetailUnenrollButton}
                onPress={handleEnroll}
                disabled={enrollmentLoading}
              >
                <Text style={styles.courseDetailUnenrollText}>Unenroll from this course</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      </ScrollView>

      {/* Rating Modal */}
      <Modal
        visible={showRatingModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowRatingModal(false)}
      >
        <View style={styles.ratingModalOverlay}>
          <View style={styles.ratingModalContent}>
            <Text style={styles.ratingModalTitle}>Rate This Course</Text>
            <Text style={styles.ratingModalSubtitle}>How would you rate your learning experience?</Text>
            
            <View style={styles.ratingStarsContainer}>
              {[1, 2, 3, 4, 5].map((star) => (
                <TouchableOpacity
                  key={star}
                  onPress={() => handleRating(star)}
                  style={styles.ratingStarButton}
                >
                  <Ionicons
                    name={star <= userRating ? "star" : "star-outline"}
                    size={isDesktop ? 40 : isTablet ? 36 : 32}
                    color={star <= userRating ? "#FFD700" : "#DDD"}
                  />
                </TouchableOpacity>
              ))}
            </View>
            
            <TouchableOpacity
              style={styles.ratingModalCloseButton}
              onPress={() => setShowRatingModal(false)}
            >
              <Text style={styles.ratingModalCloseText}>Skip Rating</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
};


export default CourseDetailScreen;
