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
import { fetchSimilarCourses } from '../store/slices/recommendationSlice';
import { Course, Recommendation } from '../types';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

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
  const { recommendations: similarCourses } = useSelector((state: RootState) => state.recommendations);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  const { courseId } = route.params;

  useEffect(() => {
    dispatch(fetchCourse(courseId));
    dispatch(fetchSimilarCourses({ courseId, limit: 3 }));
  }, [dispatch, courseId]);

  const handleEnroll = () => {
    if (selectedCourse?.is_free) {
      Alert.alert(
        'Enroll in Course',
        `Are you sure you want to enroll in "${selectedCourse.title}"?`,
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Enroll', onPress: () => setIsEnrolled(true) },
        ]
      );
    } else {
      Alert.alert(
        'Purchase Course',
        `This course costs $${selectedCourse?.price}. Would you like to proceed with the purchase?`,
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Purchase', onPress: () => setIsEnrolled(true) },
        ]
      );
    }
  };

  const handleToggleFavorite = () => {
    setIsFavorite(!isFavorite);
  };

  const handleSimilarCoursePress = (courseId: number) => {
    navigation.navigate('CourseDetail', { courseId });
  };

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

  const renderSimilarCourse = ({ item }: { item: Recommendation }) => (
    <TouchableOpacity
      style={styles.similarCourseCard}
      onPress={() => handleSimilarCoursePress(item.course_id)}
    >
      <View style={styles.similarCourseHeader}>
        <Text style={styles.similarCourseTitle} numberOfLines={2}>
          {item.title}
        </Text>
        <View style={styles.similarCourseRating}>
          <Ionicons name="star" size={14} color="#FFD700" />
          <Text style={styles.similarRatingText}>{item.rating.toFixed(1)}</Text>
        </View>
      </View>
      <Text style={styles.similarCourseInstructor}>{item.instructor}</Text>
      <Text style={styles.similarCoursePrice}>
        {item.is_free ? 'Free' : `$${item.price}`}
      </Text>
    </TouchableOpacity>
  );

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading course details...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (error || !selectedCourse) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={50} color="#ff6b6b" />
          <Text style={styles.errorText}>Failed to load course</Text>
          <Text style={styles.errorSubtext}>{error}</Text>
          <TouchableOpacity
            style={styles.retryButton}
            onPress={() => dispatch(fetchCourse(courseId))}
          >
            <Text style={styles.retryButtonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
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
            <TouchableOpacity
              style={styles.favoriteButton}
              onPress={handleToggleFavorite}
            >
              <Ionicons
                name={isFavorite ? "heart" : "heart-outline"}
                size={24}
                color={isFavorite ? "#ff6b6b" : "white"}
              />
            </TouchableOpacity>
          </View>
        </LinearGradient>

        {/* Course Image Placeholder */}
        <View style={styles.imageContainer}>
          <View style={styles.imagePlaceholder}>
            <Ionicons name="play-circle" size={60} color="#667eea" />
            <Text style={styles.imagePlaceholderText}>Course Preview</Text>
          </View>
        </View>

        {/* Course Info */}
        <View style={styles.courseInfo}>
          <View style={styles.courseHeader}>
            <Text style={styles.courseTitle}>{selectedCourse.title}</Text>
            {selectedCourse.is_featured && (
              <View style={styles.featuredBadge}>
                <Text style={styles.featuredText}>Featured</Text>
              </View>
            )}
          </View>

          <Text style={styles.courseInstructor}>by {selectedCourse.instructor}</Text>

          <View style={styles.ratingContainer}>
            <View style={styles.starsContainer}>
              {renderStars(selectedCourse.rating)}
            </View>
            <Text style={styles.ratingText}>
              {selectedCourse.rating.toFixed(1)} ({selectedCourse.rating_count} reviews)
            </Text>
          </View>

          <View style={styles.courseMeta}>
            <View style={styles.metaItem}>
              <Ionicons name="time" size={16} color="#666" />
              <Text style={styles.metaText}>{selectedCourse.duration_hours} hours</Text>
            </View>
            <View style={styles.metaItem}>
              <Ionicons name="people" size={16} color="#666" />
              <Text style={styles.metaText}>{selectedCourse.enrollment_count} students</Text>
            </View>
            <View style={styles.metaItem}>
              <Ionicons name="trending-up" size={16} color="#666" />
              <Text style={styles.metaText}>{selectedCourse.completion_rate}% completion</Text>
            </View>
          </View>

          <View style={styles.courseDetails}>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Language:</Text>
              <Text style={styles.detailValue}>{selectedCourse.language}</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Difficulty:</Text>
              <Text style={styles.detailValue}>{selectedCourse.difficulty_level}</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Type:</Text>
              <Text style={styles.detailValue}>{selectedCourse.content_type}</Text>
            </View>
            {selectedCourse.has_certificate && (
              <View style={styles.detailRow}>
                <Text style={styles.detailLabel}>Certificate:</Text>
                <Text style={styles.detailValue}>Available</Text>
              </View>
            )}
          </View>
        </View>

        {/* Description */}
        <View style={styles.descriptionContainer}>
          <Text style={styles.sectionTitle}>About This Course</Text>
          <Text style={styles.description}>{selectedCourse.description}</Text>
        </View>

        {/* Similar Courses */}
        {similarCourses.length > 0 && (
          <View style={styles.similarCoursesContainer}>
            <Text style={styles.sectionTitle}>Similar Courses</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {similarCourses.map((course: Recommendation) => (
                <View key={course.course_id} style={styles.similarCourseWrapper}>
                  {renderSimilarCourse({ item: course })}
                </View>
              ))}
            </ScrollView>
          </View>
        )}
      </ScrollView>

      {/* Bottom Action Bar */}
      <View style={styles.bottomBar}>
        <View style={styles.priceContainer}>
          <Text style={styles.priceLabel}>Price</Text>
          <Text style={styles.priceText}>
            {selectedCourse.is_free ? 'Free' : `$${selectedCourse.price}`}
          </Text>
        </View>
        <TouchableOpacity
          style={[
            styles.enrollButton,
            isEnrolled && styles.enrolledButton,
          ]}
          onPress={handleEnroll}
        >
          <Text style={styles.enrollButtonText}>
            {isEnrolled ? 'Enrolled' : selectedCourse.is_free ? 'Enroll Free' : 'Purchase'}
          </Text>
        </TouchableOpacity>
      </View>
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
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  backButton: {
    padding: 5,
  },
  favoriteButton: {
    padding: 5,
  },
  imageContainer: {
    height: 200,
    backgroundColor: '#e0e0e0',
  },
  imagePlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  imagePlaceholderText: {
    fontSize: 16,
    color: '#666',
    marginTop: 10,
  },
  courseInfo: {
    backgroundColor: 'white',
    padding: 20,
    marginTop: -20,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  courseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  courseTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 10,
  },
  featuredBadge: {
    backgroundColor: '#ff6b6b',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  featuredText: {
    fontSize: 10,
    color: 'white',
    fontWeight: 'bold',
  },
  courseInstructor: {
    fontSize: 16,
    color: '#666',
    marginBottom: 15,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  starsContainer: {
    flexDirection: 'row',
    marginRight: 10,
  },
  ratingText: {
    fontSize: 14,
    color: '#666',
  },
  courseMeta: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
    paddingVertical: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  metaText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 5,
  },
  courseDetails: {
    marginBottom: 20,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  detailLabel: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  detailValue: {
    fontSize: 14,
    color: '#333',
  },
  descriptionContainer: {
    backgroundColor: 'white',
    padding: 20,
    marginTop: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  description: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  similarCoursesContainer: {
    backgroundColor: 'white',
    padding: 20,
    marginTop: 10,
  },
  similarCourseWrapper: {
    marginRight: 15,
  },
  similarCourseCard: {
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    padding: 15,
    width: 200,
  },
  similarCourseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  similarCourseTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 8,
  },
  similarCourseRating: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  similarRatingText: {
    fontSize: 12,
    color: '#333',
    marginLeft: 3,
  },
  similarCourseInstructor: {
    fontSize: 12,
    color: '#666',
    marginBottom: 8,
  },
  similarCoursePrice: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#667eea',
  },
  bottomBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  priceContainer: {
    flex: 1,
  },
  priceLabel: {
    fontSize: 12,
    color: '#666',
  },
  priceText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  enrollButton: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingHorizontal: 30,
    paddingVertical: 15,
  },
  enrolledButton: {
    backgroundColor: '#4CAF50',
  },
  enrollButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
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
});

export default CourseDetailScreen;
