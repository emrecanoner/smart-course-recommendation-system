import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { registerUser, clearError } from '../store/slices/authSlice';
import { Ionicons } from '@expo/vector-icons';

interface RegisterScreenProps {
  navigation: any;
}

const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    fullName: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [touched, setTouched] = useState<{[key: string]: boolean}>({});

  const dispatch = useDispatch<AppDispatch>();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear validation errors when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
    // Clear Redux error when user starts typing
    if (error) {
      dispatch(clearError());
    }
  };

  const handleInputBlur = (field: string) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    validateField(field, formData[field as keyof typeof formData]);
  };

  const validateEmail = (email: string): string => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim()) return 'Email is required';
    if (!emailRegex.test(email)) return 'Please enter a valid email address';
    return '';
  };

  const validatePassword = (password: string): string => {
    if (!password.trim()) return 'Password is required';
    if (password.length < 8) return 'Password must be at least 8 characters long';
    if (!/(?=.*[a-z])/.test(password)) return 'Password must contain at least one lowercase letter';
    if (!/(?=.*[A-Z])/.test(password)) return 'Password must contain at least one uppercase letter';
    if (!/(?=.*\d)/.test(password)) return 'Password must contain at least one number';
    return '';
  };

  const validateUsername = (username: string): string => {
    if (!username.trim()) return 'Username is required';
    if (username.length < 3) return 'Username must be at least 3 characters long';
    if (!/^[a-zA-Z0-9_]+$/.test(username)) return 'Username can only contain letters, numbers, and underscores';
    return '';
  };

  const validateField = (field: string, value: string) => {
    let error = '';
    
    switch (field) {
      case 'email':
        error = validateEmail(value);
        break;
      case 'password':
        error = validatePassword(value);
        break;
      case 'username':
        error = validateUsername(value);
        break;
      case 'confirmPassword':
        if (!value.trim()) {
          error = 'Please confirm your password';
        } else if (value !== formData.password) {
          error = 'Passwords do not match';
        }
        break;
    }
    
    setErrors(prev => ({ ...prev, [field]: error }));
  };

  const validateForm = () => {
    const fields = ['email', 'username', 'password', 'confirmPassword'];
    let isValid = true;
    const newErrors: {[key: string]: string} = {};

    fields.forEach(field => {
      const value = formData[field as keyof typeof formData];
      validateField(field, value);
      if (errors[field] || !value.trim()) {
        isValid = false;
      }
    });

    return isValid;
  };

  const handleRegister = async () => {
    // Validate form first
    if (!validateForm()) {
      return;
    }

    // Clear any previous errors
    dispatch(clearError());

    try {
      const result = await dispatch(registerUser({
        email: formData.email,
        username: formData.username,
        password: formData.password,
        full_name: formData.fullName || undefined,
      })).unwrap();
      
      console.log('Register result:', result);
      
      // Show success message and navigate to login
      console.log('Showing success alert...');
      Alert.alert(
        'Success',
        'Account created successfully! Please sign in.',
        [{ 
          text: 'OK',
          onPress: () => {
            console.log('Navigating to Login...');
            // Navigate to login screen after successful registration
            navigation.navigate('Login');
          }
        }]
      );
      
      // Direct navigation as backup (in case alert onPress doesn't work)
      console.log('Direct navigation to Login...');
      setTimeout(() => {
        navigation.navigate('Login');
      }, 1000); // 1 second delay to allow user to see the alert
    } catch (error) {
      console.log('Register error:', error);
      // Error will be shown in UI via Redux state
      // Don't navigate anywhere on error - stay on current screen
      // Error will be displayed in UI via Redux state
    }
  };

  const handleLogin = () => {
    dispatch(clearError()); // Clear error before navigating
    navigation.navigate('Login');
  };

  return (
    <View style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardAvoidingView}
      >
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <View style={styles.content}>
            {/* Header */}
            <View style={styles.header}>
              <Ionicons name="person-add" size={60} color="#667eea" />
              <Text style={styles.title}>Create Account</Text>
              <Text style={styles.subtitle}>Join Smart Course today</Text>
            </View>

            {/* Error Message */}
            {error && (
              <View style={styles.errorContainer}>
                <Ionicons name="alert-circle" size={20} color="#ff6b6b" />
                <Text style={styles.errorText}>
                  {typeof error === 'string' ? error : 'Registration failed. Please try again.'}
                </Text>
              </View>
            )}

            {/* Register Form */}
            <View style={styles.form}>
              {/* Email Input */}
              <View style={styles.inputGroup}>
                <View style={[
                  styles.inputContainer,
                  touched.email && errors.email && styles.inputError
                ]}>
                  <Ionicons 
                    name="mail" 
                    size={20} 
                    color={touched.email && errors.email ? "#ff6b6b" : "#666"} 
                    style={styles.inputIcon} 
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Email *"
                    placeholderTextColor="#999"
                    value={formData.email}
                    onChangeText={(value) => handleInputChange('email', value)}
                    onBlur={() => handleInputBlur('email')}
                    keyboardType="email-address"
                    autoCapitalize="none"
                    autoCorrect={false}
                    selectionColor="#667eea"
                  />
                </View>
                {touched.email && errors.email && (
                  <View>
                    <Text style={styles.fieldErrorText}>{errors.email}</Text>
                  </View>
                )}
              </View>

              {/* Username Input */}
              <View style={styles.inputGroup}>
                <View style={[
                  styles.inputContainer,
                  touched.username && errors.username && styles.inputError
                ]}>
                  <Ionicons 
                    name="person" 
                    size={20} 
                    color={touched.username && errors.username ? "#ff6b6b" : "#666"} 
                    style={styles.inputIcon} 
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Username *"
                    placeholderTextColor="#999"
                    value={formData.username}
                    onChangeText={(value) => handleInputChange('username', value)}
                    onBlur={() => handleInputBlur('username')}
                    autoCapitalize="none"
                    autoCorrect={false}
                    selectionColor="#667eea"
                  />
                </View>
                {touched.username && errors.username && (
                  <View>
                    <Text style={styles.fieldErrorText}>{errors.username}</Text>
                  </View>
                )}
              </View>

              {/* Full Name Input */}
              <View style={styles.inputGroup}>
                <View style={styles.inputContainer}>
                  <Ionicons 
                    name="person-circle" 
                    size={20} 
                    color="#666" 
                    style={styles.inputIcon} 
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Full Name"
                    placeholderTextColor="#999"
                    value={formData.fullName}
                    onChangeText={(value) => handleInputChange('fullName', value)}
                    autoCapitalize="words"
                    selectionColor="#667eea"
                  />
                </View>
              </View>

              {/* Password Input */}
              <View style={styles.inputGroup}>
                <View style={[
                  styles.inputContainer,
                  touched.password && errors.password && styles.inputError
                ]}>
                  <Ionicons 
                    name="lock-closed" 
                    size={20} 
                    color={touched.password && errors.password ? "#ff6b6b" : "#666"} 
                    style={styles.inputIcon} 
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Password *"
                    placeholderTextColor="#999"
                    value={formData.password}
                    onChangeText={(value) => handleInputChange('password', value)}
                    onBlur={() => handleInputBlur('password')}
                    secureTextEntry={!showPassword}
                    autoCapitalize="none"
                    autoCorrect={false}
                    selectionColor="#667eea"
                  />
                  <TouchableOpacity
                    style={styles.eyeIcon}
                    onPress={() => setShowPassword(!showPassword)}
                  >
                    <Ionicons
                      name={showPassword ? 'eye-off' : 'eye'}
                      size={20}
                      color="#666"
                    />
                  </TouchableOpacity>
                </View>
                {touched.password && errors.password && (
                  <View>
                    <Text style={styles.fieldErrorText}>{errors.password}</Text>
                  </View>
                )}
              </View>

              {/* Confirm Password Input */}
              <View style={styles.inputGroup}>
                <View style={[
                  styles.inputContainer,
                  touched.confirmPassword && errors.confirmPassword && styles.inputError
                ]}>
                  <Ionicons 
                    name="lock-closed" 
                    size={20} 
                    color={touched.confirmPassword && errors.confirmPassword ? "#ff6b6b" : "#666"} 
                    style={styles.inputIcon} 
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Confirm Password *"
                    placeholderTextColor="#999"
                    value={formData.confirmPassword}
                    onChangeText={(value) => handleInputChange('confirmPassword', value)}
                    onBlur={() => handleInputBlur('confirmPassword')}
                    secureTextEntry={!showConfirmPassword}
                    autoCapitalize="none"
                    autoCorrect={false}
                    selectionColor="#667eea"
                  />
                  <TouchableOpacity
                    style={styles.eyeIcon}
                    onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    <Ionicons
                      name={showConfirmPassword ? 'eye-off' : 'eye'}
                      size={20}
                      color="#666"
                    />
                  </TouchableOpacity>
                </View>
                {touched.confirmPassword && errors.confirmPassword && (
                  <View>
                    <Text style={styles.fieldErrorText}>{errors.confirmPassword}</Text>
                  </View>
                )}
              </View>

              {/* Register Button */}
              <TouchableOpacity
                style={[styles.registerButton, isLoading && styles.disabledButton]}
                onPress={handleRegister}
                disabled={isLoading}
              >
                <Text style={styles.registerButtonText}>
                  {isLoading ? 'Creating Account...' : 'Create Account'}
                </Text>
              </TouchableOpacity>

              {/* Login Button */}
              <TouchableOpacity
                style={styles.loginButton}
                onPress={handleLogin}
              >
                <Text style={styles.loginButtonText}>
                  Already have an account? Sign In
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  keyboardAvoidingView: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 30,
    paddingVertical: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 40,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  form: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 30,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
    borderWidth: 1,
    borderColor: '#f0f0f0',
  },
  inputGroup: {
    marginBottom: 20,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    paddingHorizontal: 16,
    height: 56,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  inputError: {
    borderColor: '#ff6b6b',
    backgroundColor: '#fff5f5',
  },
  inputIcon: {
    marginRight: 12,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: '#333',
    fontWeight: '400',
  },
  eyeIcon: {
    padding: 8,
  },
  fieldErrorText: {
    fontSize: 12,
    color: '#ff6b6b',
    marginTop: 6,
    marginLeft: 4,
  },
  registerButton: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    height: 56,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
    shadowColor: '#667eea',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  disabledButton: {
    opacity: 0.6,
  },
  registerButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  loginButton: {
    marginTop: 24,
    alignItems: 'center',
  },
  loginButtonText: {
    color: '#667eea',
    fontSize: 16,
    fontWeight: '500',
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff5f5',
    borderColor: '#ff6b6b',
    borderWidth: 2,
    borderRadius: 8,
    padding: 16,
    marginBottom: 20,
    minHeight: 50,
  },
  errorText: {
    color: '#ff6b6b',
    fontSize: 14,
    marginLeft: 8,
    flex: 1,
    fontWeight: '500',
  },
});

export default RegisterScreen;