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

interface CourseDetailScreenProps {
  navigation: any;
  route: {
    params: {
      courseId: number;
    };
  };
}

const CourseDetailScreen: React.FC<CourseDetailScreenProps> = ({ navigation, route }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { selectedCourse, isLoading, error } = useSelector((state: RootState) => state.courses);
  // const { recommendations: similarCourses } = useSelector((state: RootState) => state.recommendations);
  const { isLoading: enrollmentLoading, enrollments, enrollmentStatus } = useSelector((state: RootState) => state.enrollments);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [showPageLoading, setShowPageLoading] = React.useState(true);

  const { courseId } = route.params;
  const styles = getResponsiveCourseDetailStyles();

  useEffect(() => {
    dispatch(fetchCourse(courseId));
    // dispatch(fetchSimilarCourses({ courseId, limit: 3 }));
    dispatch(checkEnrollment(courseId));
    
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
      dispatch(fetchCourse(courseId));
      dispatch(checkEnrollment(courseId));
      
      // Hide loading after data is fetched
      const timer = setTimeout(() => {
        setShowPageLoading(false);
      }, 1500);
      
      return () => clearTimeout(timer);
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
  }, [enrollments, enrollmentStatus, courseId]);

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
          <Text style={styles.courseDetailTitle}>{selectedCourse.title}</Text>
          
          <View style={styles.courseDetailInstructorRating}>
            <Text style={styles.courseDetailInstructor}>by {selectedCourse.instructor}</Text>
            <View style={styles.courseDetailRating}>
              {renderStars(selectedCourse.rating)}
              <Text style={styles.courseDetailRatingText}>
                {(selectedCourse.rating).toFixed(1)} ({selectedCourse.rating_count} reviews)
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
          <Button
            title={isEnrolled ? 'Unenroll' : 'Enroll Now'}
            onPress={handleEnroll}
            variant={isEnrolled ? 'secondary' : 'primary'}
            disabled={enrollmentLoading}
            icon={isEnrolled ? <Ionicons name="close-circle" size={20} color="#ffffff" /> : undefined}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};


export default CourseDetailScreen;
