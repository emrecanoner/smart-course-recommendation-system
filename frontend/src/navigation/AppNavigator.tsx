import React, { useEffect, useRef } from 'react';
import { View, Text, Animated, Easing, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { getCurrentUser } from '../store/slices/authSlice';

// Screens
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import HomeScreen from '../screens/HomeScreen';
import CoursesScreen from '../screens/CoursesScreen';
import CourseDetailScreen from '../screens/CourseDetailScreen';
import RecommendationsScreen from '../screens/RecommendationsScreen';
import ProfileScreen from '../screens/ProfileScreen';

// Types
import { RootStackParamList } from '../types';

const Stack = createStackNavigator<RootStackParamList>();

const AppNavigator: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { isAuthenticated, isLoading, isRegistering } = useSelector((state: RootState) => state.auth);
  const navigationRef = useRef<any>(null);
  
  // Show loading screen only when checking authentication (not during register/login)
  const [isCheckingAuth, setIsCheckingAuth] = React.useState(true);
  const spinValue = useRef(new Animated.Value(0)).current;

  // Navigate to Home when authenticated
  useEffect(() => {
    if (isAuthenticated && !isLoading && !isCheckingAuth && navigationRef.current) {
      navigationRef.current.navigate('Home');
    }
  }, [isAuthenticated, isLoading, isCheckingAuth]);
  
  useEffect(() => {
    // Check if user is already authenticated
    const token = localStorage.getItem('auth_token');
    
    if (token) {
      dispatch(getCurrentUser()).finally(() => {
        setIsCheckingAuth(false);
      });
    } else {
      setIsCheckingAuth(false);
    }
  }, [dispatch]);

  // Navigate to Login when not authenticated (only on initial load, not during register)
  useEffect(() => {
    if (!isAuthenticated && !isLoading && !isCheckingAuth && !isRegistering && navigationRef.current) {
      // Check current route to prevent navigation from Register screen
      const currentRoute = navigationRef.current.getCurrentRoute();
      
      if (currentRoute?.name !== 'Register') {
        navigationRef.current.navigate('Login');
      }
    }
  }, [isAuthenticated, isLoading, isCheckingAuth, isRegistering]);

  // Prevent navigation state changes during error handling
  const onStateChange = (state: any) => {
    // Navigation state change handler
  };

  // Start spinning animation
  useEffect(() => {
    if (isCheckingAuth) {
      const spin = Animated.loop(
        Animated.timing(spinValue, {
          toValue: 1,
          duration: 2000,
          easing: Easing.linear,
          useNativeDriver: true,
        })
      );
      spin.start();
      return () => spin.stop();
    }
  }, [isCheckingAuth, spinValue]);

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  if (isCheckingAuth) {
    return (
      <View style={styles.loadingContainer}>
        <View style={styles.loadingContent}>
          <Animated.View style={[styles.iconContainer, { transform: [{ rotate: spin }] }]}>
            <Ionicons name="school" size={60} color="#667eea" />
          </Animated.View>
          <Text style={styles.loadingTitle}>Smart Course</Text>
          <Text style={styles.loadingSubtitle}>Loading your learning experience...</Text>
          <View style={styles.loadingDots}>
            <View style={[styles.dot, styles.dot1]} />
            <View style={[styles.dot, styles.dot2]} />
            <View style={[styles.dot, styles.dot3]} />
          </View>
        </View>
      </View>
    );
  }

  return (
    <NavigationContainer 
      ref={navigationRef} 
      onStateChange={onStateChange}
      onReady={() => {
        // Navigation ready
      }}
      linking={{
        enabled: false,
        prefixes: [],
      }}
    >
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        {/* Always render all screens to prevent navigation state changes */}
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Courses" component={CoursesScreen} />
        <Stack.Screen name="CourseDetail" component={CourseDetailScreen} />
        <Stack.Screen name="Recommendations" component={RecommendationsScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
  loadingContent: {
    alignItems: 'center',
  },
  iconContainer: {
    marginBottom: 20,
  },
  loadingTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#667eea',
    marginBottom: 10,
  },
  loadingSubtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 30,
    textAlign: 'center',
  },
  loadingDots: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#667eea',
    marginHorizontal: 4,
  },
  dot1: {
    opacity: 0.4,
  },
  dot2: {
    opacity: 0.7,
  },
  dot3: {
    opacity: 1,
  },
});

export default AppNavigator;
