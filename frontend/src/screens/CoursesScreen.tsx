import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  TextInput,
  FlatList,
  RefreshControl,
  Dimensions,
  Platform,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { fetchCourses, clearCourses, fetchCategories } from '../store/slices/courseSlice';
import { Course } from '../types';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import LoadingComponent from '../components/LoadingComponent';
import { getResponsiveCoursesStyles, isWeb, isTablet, isDesktop, isMobile } from '../styles/responsiveStyles';

interface CoursesScreenProps {
  navigation: any;
}

const CoursesScreen: React.FC<CoursesScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { courses, isLoading, error, pagination, categories } = useSelector((state: RootState) => state.courses);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [refreshing, setRefreshing] = useState(false);
  const [showPageLoading, setShowPageLoading] = React.useState(true);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  
  const styles = getResponsiveCoursesStyles();

  // Categories will be loaded from backend
  const categoryNames = ['All', ...categories.map(cat => cat.name)];

  useEffect(() => {
    dispatch(fetchCourses({}));
    dispatch(fetchCategories());
    
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [dispatch]);

  // Listen for navigation focus to refresh data
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      // Show loading and refresh courses and categories when screen comes into focus
      setShowPageLoading(true);
      dispatch(fetchCourses({}));
      dispatch(fetchCategories());
      
      // Hide loading after data is fetched
      const timer = setTimeout(() => {
        setShowPageLoading(false);
      }, 1500);
      
      return () => clearTimeout(timer);
    });

    return unsubscribe;
  }, [navigation, dispatch]);

  const handleRefresh = async () => {
    setRefreshing(true);
    if (searchQuery.trim()) {
      await dispatch(fetchCourses({ search: searchQuery.trim(), page: 1 }));
    } else if (selectedCategory) {
      await dispatch(fetchCourses({ category: selectedCategory, page: 1 }));
    } else {
      await dispatch(fetchCourses({ page: 1 }));
    }
    setRefreshing(false);
  };

  const handleSearch = () => {
    dispatch(fetchCourses({ search: searchQuery, page: 1 }));
  };

  const handleCategoryFilter = (category: string) => {
    setSelectedCategory(category);
    if (category === 'All') {
      dispatch(fetchCourses({ page: 1 }));
    } else {
      dispatch(fetchCourses({ category, page: 1 }));
    }
  };

  const handleNextPage = () => {
    if (pagination.hasNextPage) {
      const nextPage = pagination.currentPage + 1;
      if (searchQuery.trim()) {
        dispatch(fetchCourses({ search: searchQuery.trim(), page: nextPage }));
      } else if (selectedCategory) {
        dispatch(fetchCourses({ category: selectedCategory, page: nextPage }));
      } else {
        dispatch(fetchCourses({ page: nextPage }));
      }
    }
  };

  const handlePreviousPage = () => {
    if (pagination.hasPreviousPage) {
      const prevPage = pagination.currentPage - 1;
      if (searchQuery.trim()) {
        dispatch(fetchCourses({ search: searchQuery.trim(), page: prevPage }));
      } else if (selectedCategory) {
        dispatch(fetchCourses({ category: selectedCategory, page: prevPage }));
      } else {
        dispatch(fetchCourses({ page: prevPage }));
      }
    }
  };

  const handleCoursePress = (course: Course) => {
    navigation.navigate('CourseDetail', { courseId: course.id });
  };

  const formatSkills = (skills: string | undefined): string => {
    if (!skills || skills.trim() === '' || skills.trim() === '[]') return 'No skillset defined';
    
    try {
      // If it comes as string array format (e.g., "['skill1', 'skill2']")
      if (skills.startsWith("['") && skills.endsWith("']") || 
          skills.startsWith('["') && skills.endsWith('"]')) {
        // Extract array from string
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
      // Return original string in case of parse error
      return skills;
    }
  };

  const renderCourseItem = ({ item }: { item: Course }) => (
    <TouchableOpacity
      style={[
        styles.courseCard,
        hoveredCard === `course-${item.id}` && isWeb && {
          transform: [{ translateY: -4 }],
          shadowOpacity: 0.15,
          borderColor: '#007bff',
          shadowColor: '#007bff',
        }
      ]}
      onPress={() => handleCoursePress(item)}
      onPressIn={() => isWeb && setHoveredCard(`course-${item.id}`)}
      onPressOut={() => isWeb && setHoveredCard(null)}
    >
      <View style={styles.courseHeader}>
        <View style={styles.courseInfo}>
          <Text style={styles.courseTitle} numberOfLines={2}>
            {item.title}
          </Text>
          <Text style={styles.courseInstructor}>{item.instructor}</Text>
        </View>
        <View style={styles.courseRating}>
          <Ionicons name="star" size={isDesktop ? 18 : isTablet ? 16 : 14} color="#FFD700" />
          <Text style={styles.ratingText}>{item.rating.toFixed(1)}</Text>
        </View>
      </View>

      <Text style={styles.courseDescription} numberOfLines={3}>
        {formatSkills(item.skills) || item.short_description || item.description}
      </Text>

      <View style={styles.courseFooter}>
        <View style={styles.courseMeta}>
          <View style={styles.metaItem}>
            <Ionicons name="time" size={isDesktop ? 16 : isTablet ? 14 : 12} color="#666" />
            <Text style={styles.metaText}>{item.duration_hours}h</Text>
          </View>
          <View style={styles.metaItem}>
            <Ionicons name="people" size={isDesktop ? 16 : isTablet ? 14 : 12} color="#666" />
            <Text style={styles.metaText}>{item.enrollment_count}</Text>
          </View>
          <View style={styles.metaItem}>
            <Ionicons name="trending-up" size={isDesktop ? 16 : isTablet ? 14 : 12} color="#666" />
            <Text style={styles.metaText}>{item.completion_rate.toFixed(1)}%</Text>
          </View>
        </View>
        <View style={styles.priceContainer}>
          <Text style={styles.priceText}>
            {item.is_free ? 'Free' : `$${item.price}`}
          </Text>
        </View>
      </View>

      {item.category && (
        <View style={styles.courseSkills}>
          <Text style={styles.skillsText}>
            {item.category.name}
          </Text>
        </View>
      )}

      {item.is_featured && (
        <View style={styles.featuredBadge}>
          <Text style={styles.featuredText}>Featured</Text>
        </View>
      )}
    </TouchableOpacity>
  );

  const renderCategoryItem = ({ item }: { item: string }) => (
    <TouchableOpacity
      style={[
        styles.categoryChip,
        selectedCategory === item && styles.selectedCategoryChip,
      ]}
      onPress={() => handleCategoryFilter(item)}
    >
      <Text
        style={[
          styles.categoryText,
          selectedCategory === item && styles.selectedCategoryText,
        ]}
      >
        {item}
      </Text>
    </TouchableOpacity>
  );

  // Show loading screen when page opens
  if (showPageLoading) {
    return (
      <LoadingComponent 
        visible={true}
      />
    );
  }

  return (
    <SafeAreaView style={styles.coursesContainer}>
      <ScrollView 
        style={styles.coursesScrollContainer}
        contentContainerStyle={styles.coursesScrollContent}
        showsVerticalScrollIndicator={false}
        {...(isWeb && {
          scrollEventThrottle: 16,
          nestedScrollEnabled: true,
        })}
      >
        {/* Header */}
        <View style={styles.coursesHeader}>
          <View style={styles.coursesHeaderContent}>
            <TouchableOpacity
              style={styles.coursesBackButton}
              onPress={() => navigation.goBack()}
            >
              <Ionicons 
                name="arrow-back" 
                size={isDesktop ? 28 : isTablet ? 26 : 24} 
                color="#666" 
              />
            </TouchableOpacity>
            <Text style={styles.coursesHeaderTitle}>
              {isDesktop ? 'Browse All Courses' : 'Courses'}
            </Text>
            <View style={styles.coursesHeaderPlaceholder} />
          </View>
        </View>

      {/* Search Bar */}
      <View style={styles.coursesSearchContainer}>
        <View style={styles.coursesSearchBar}>
          <Ionicons 
            name="search" 
            size={isDesktop ? 22 : isTablet ? 20 : 18} 
            color="#666" 
          />
          <TextInput
            style={styles.coursesSearchInput}
            placeholder="Search courses..."
            placeholderTextColor="#999"
            value={searchQuery}
            onChangeText={setSearchQuery}
            onSubmitEditing={handleSearch}
          />
          <TouchableOpacity onPress={handleSearch}>
            <Ionicons 
              name="arrow-forward" 
              size={isDesktop ? 22 : isTablet ? 20 : 18} 
              color="#007bff" 
            />
          </TouchableOpacity>
        </View>
      </View>

      {/* Categories */}
      <View style={styles.coursesCategoriesContainer}>
        <FlatList
          data={categoryNames}
          renderItem={renderCategoryItem}
          keyExtractor={(item) => item}
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.coursesCategoriesList}
        />
      </View>

      {/* Courses List */}
      <View style={styles.coursesListContainer}>
        {isLoading && courses.length === 0 ? (
          <View style={styles.coursesLoadingContainer}>
            <LoadingComponent visible={true} />
          </View>
        ) : error ? (
          <View style={styles.coursesErrorContainer}>
            <Ionicons 
              name="alert-circle" 
              size={isDesktop ? 60 : isTablet ? 50 : 40} 
              color="#ff6b6b" 
            />
            <Text style={styles.coursesErrorText}>Failed to load courses</Text>
            <Text style={styles.coursesErrorSubtext}>{error}</Text>
            <TouchableOpacity
              style={styles.coursesRetryButton}
              onPress={() => dispatch(fetchCourses({}))}
            >
              <Text style={styles.coursesRetryButtonText}>Retry</Text>
            </TouchableOpacity>
          </View>
        ) : courses.length === 0 ? (
          <View style={styles.coursesEmptyContainer}>
            <Ionicons 
              name="book-outline" 
              size={isDesktop ? 60 : isTablet ? 50 : 40} 
              color="#ccc" 
            />
            <Text style={styles.coursesEmptyText}>No courses found</Text>
            <Text style={styles.coursesEmptySubtext}>
              Try adjusting your search or filters
            </Text>
          </View>
        ) : (
          <FlatList
            data={courses}
            renderItem={renderCourseItem}
            keyExtractor={(item) => item.id.toString()}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
            }
            contentContainerStyle={styles.coursesList}
            showsVerticalScrollIndicator={false}
            numColumns={isDesktop ? 2 : 1}
            key={isDesktop ? 'two-column' : 'single-column'}
            columnWrapperStyle={isDesktop ? styles.courseRow : undefined}
          />
        )}
        
        {/* Pagination */}
        {courses.length > 0 && (
          <View style={styles.paginationContainer}>
            <TouchableOpacity
              style={[
                styles.paginationButton,
                !pagination.hasPreviousPage && styles.paginationButtonDisabled
              ]}
              onPress={handlePreviousPage}
              disabled={!pagination.hasPreviousPage}
            >
              <Text style={[
                styles.paginationButtonText,
                !pagination.hasPreviousPage && styles.paginationButtonTextDisabled
              ]}>
                Previous
              </Text>
            </TouchableOpacity>
            
            <Text style={styles.paginationInfo}>
              {pagination.currentPage} of {pagination.totalPages}
            </Text>
            
            <TouchableOpacity
              style={[
                styles.paginationButton,
                !pagination.hasNextPage && styles.paginationButtonDisabled
              ]}
              onPress={handleNextPage}
              disabled={!pagination.hasNextPage}
            >
              <Text style={[
                styles.paginationButtonText,
                !pagination.hasNextPage && styles.paginationButtonTextDisabled
              ]}>
                Next
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
      </ScrollView>
    </SafeAreaView>
  );
};


export default CoursesScreen;
