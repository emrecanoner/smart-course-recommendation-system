import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { registerUser, clearError } from '../store/slices/authSlice';
import { Ionicons } from '@expo/vector-icons';
import LoadingComponent from '../components/LoadingComponent';
import { 
  getResponsiveStyles, 
  getIconSize, 
  getTitleSize, 
  getSubtitleSize,
  isWeb,
  isTablet,
  isDesktop 
} from '../styles/responsiveStyles';
import { validateField, validateFields } from '../utils/validation';

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
  const [showSuccessLoading, setShowSuccessLoading] = useState(false);

  const dispatch = useDispatch<AppDispatch>();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);

  // Get responsive styles
  const styles = getResponsiveStyles();

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
    handleValidateField(field, formData[field as keyof typeof formData]);
  };

  const handleValidateField = (field: string, value: string) => {
    const result = validateField(field, value, field === 'confirmPassword' ? formData.password : undefined);
    setErrors(prev => ({ ...prev, [field]: result.error }));
  };

  const validateForm = () => {
    const fieldsToValidate = {
      email: formData.email,
      username: formData.username,
      password: formData.password,
      confirmPassword: formData.confirmPassword
    };
    
    const validationErrors = validateFields(fieldsToValidate);
    setErrors(validationErrors);
    
    return Object.keys(validationErrors).length === 0;
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
      
      // Show success loading for 1.5 seconds then navigate
      setShowSuccessLoading(true);
      
      // Navigate to login after 1.5 seconds
      setTimeout(() => {
        setShowSuccessLoading(false);
        navigation.navigate('Login');
      }, 1500);
    } catch (error) {
      // Error will be shown in UI via Redux state
      // Don't navigate anywhere on error - stay on current screen
      // Error will be displayed in UI via Redux state
    }
  };

  const handleLogin = () => {
    dispatch(clearError()); // Clear error before navigating
    navigation.navigate('Login');
  };

  // Show loading screen after successful registration
  if (showSuccessLoading) {
    return (
      <LoadingComponent 
        visible={true}
      />
    );
  }

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
              <Ionicons 
                name="person-add" 
                size={getIconSize()} 
                color="#667eea" 
              />
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
              <View style={styles.inputWrapper}>
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
                  <Text style={styles.fieldErrorText}>{errors.email}</Text>
                )}
              </View>

              {/* Username Input */}
              <View style={styles.inputWrapper}>
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
                  <Text style={styles.fieldErrorText}>{errors.username}</Text>
                )}
              </View>

              {/* Full Name Input */}
              <View style={styles.inputWrapper}>
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
              <View style={styles.inputWrapper}>
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
                  <Text style={styles.fieldErrorText}>{errors.password}</Text>
                )}
              </View>

              {/* Confirm Password Input */}
              <View style={styles.inputWrapper}>
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
                  <Text style={styles.fieldErrorText}>{errors.confirmPassword}</Text>
                )}
              </View>

              {/* Register Button */}
              <TouchableOpacity
                style={[styles.button, isLoading && styles.disabledButton]}
                onPress={handleRegister}
                disabled={isLoading}
              >
                <Text style={styles.buttonText}>
                  {isLoading ? 'Creating Account...' : 'Create Account'}
                </Text>
              </TouchableOpacity>

              {/* Login Button */}
              <TouchableOpacity
                style={styles.secondaryButton}
                onPress={handleLogin}
              >
                <Text style={styles.secondaryButtonText}>
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


export default RegisterScreen;