import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  SafeAreaView, 
  TouchableOpacity, 
  TextInput, 
  ScrollView,
  Platform,
  KeyboardAvoidingView
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { updateUser } from '../store/slices/authSlice';
import apiService from '../services/api';
import LoadingComponent from '../components/LoadingComponent';
import { profileBaseStyles } from '../styles/profileStyles';
import { 
  isWeb, 
  isTablet, 
  isDesktop, 
  isMobile,
  getResponsiveStyles,
  getTitleSize,
  getIconSize
} from '../styles/responsiveStyles';
import { validateField, validateFields } from '../utils/validation';

interface ProfileScreenProps {
  navigation: any;
}

const ProfileScreen: React.FC<ProfileScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const [showPageLoading, setShowPageLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState({
    email: '',
    username: '',
    full_name: '',
    password: ''
  });
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [touched, setTouched] = useState<{[key: string]: boolean}>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Get responsive styles
  const styles = getResponsiveStyles();

  useEffect(() => {
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, []);

  // No need for navigation listener in ProfileScreen
  // User data is already available in Redux state

  // Initialize user data when user changes
  useEffect(() => {
    if (user) {
      setEditedUser({
        email: user.email || '',
        username: user.username || '',
        full_name: user.full_name || '',
        password: ''
      });
    }
  }, [user]);

  const handleInputBlur = (field: string) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    handleValidateField(field, editedUser[field as keyof typeof editedUser]);
  };

  const handleValidateField = (field: string, value: string) => {
    const result = validateField(field, value);
    setErrors(prev => ({ ...prev, [field]: result.error }));
  };

  const validateForm = () => {
    const fieldsToValidate: { [key: string]: string } = {
      email: editedUser.email,
      username: editedUser.username,
      full_name: editedUser.full_name,
      password: editedUser.password
    };
    
    const validationErrors = validateFields(fieldsToValidate);
    setErrors(validationErrors);
    
    return Object.keys(validationErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Prepare update data
      const updateData: any = {
        email: editedUser.email,
        username: editedUser.username,
        full_name: editedUser.full_name,
      };
      
      // Only include password if it's provided
      if (editedUser.password.trim()) {
        updateData.password = editedUser.password;
      }
      
      // Call API to update user
      const updatedUser = await apiService.updateUser(updateData);
      
      // Update Redux state with new user data
      dispatch(updateUser(updatedUser));
      
      setIsEditing(false);
      setEditedUser({
        email: updatedUser.email || '',
        username: updatedUser.username || '',
        full_name: updatedUser.full_name || '',
        password: ''
      });
    } catch (error: any) {
      console.error('Profile update error:', error);
      
      let errorMessage = 'Failed to update profile. Please try again.';
      
      if (error.response?.data?.detail) {
        if (error.response.data.detail.includes('email already exists')) {
          setErrors({ email: 'The user with this email already exists in the system.' });
          errorMessage = 'The user with this email already exists in the system.';
        } else if (error.response.data.detail.includes('username already exists')) {
          setErrors({ username: 'The user with this username already exists in the system.' });
          errorMessage = 'The user with this username already exists in the system.';
        } else {
          errorMessage = error.response.data.detail;
        }
      }
      
      // Error messages are already displayed in the UI via setErrors
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    if (user) {
      setEditedUser({
        email: user.email || '',
        username: user.username || '',
        full_name: user.full_name || '',
        password: ''
      });
    }
    setErrors({});
    setTouched({});
    setIsEditing(false);
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
                name="person-circle" 
                size={getIconSize()} 
                color="#667eea" 
                style={styles.headerIcon}
              />
              <Text style={styles.title}>Profile</Text>
              <Text style={styles.subtitle}>Manage your account</Text>
            </View>

            {/* Navigation Buttons */}
            <View style={styles.navigationButtons}>
              <TouchableOpacity 
                style={styles.navButton}
                onPress={() => navigation.goBack()}
              >
                <Ionicons name="arrow-back" size={20} color="#667eea" />
                <Text style={styles.navButtonText}>Back</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.navButton}
                onPress={() => navigation.navigate('Home')}
              >
                <Ionicons name="home" size={20} color="#667eea" />
                <Text style={styles.navButtonText}>Home</Text>
              </TouchableOpacity>
            </View>

            {/* Profile Form */}
            <View style={styles.form}>
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
                  value={editedUser.email}
                  onChangeText={(text) => {
                    setEditedUser({...editedUser, email: text});
                    if (touched.email) {
                      validateField('email', text);
                    }
                  }}
                  onBlur={() => handleInputBlur('email')}
                  editable={isEditing}
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
              </View>
              {touched.email && errors.email && (
                <Text style={styles.fieldErrorText}>{errors.email}</Text>
              )}
            </View>

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
                  value={editedUser.username}
                  onChangeText={(text) => {
                    setEditedUser({...editedUser, username: text});
                    if (touched.username) {
                      validateField('username', text);
                    }
                  }}
                  onBlur={() => handleInputBlur('username')}
                  editable={isEditing}
                  autoCapitalize="none"
                />
              </View>
              {touched.username && errors.username && (
                <Text style={styles.fieldErrorText}>{errors.username}</Text>
              )}
            </View>

            <View style={styles.inputWrapper}>
              <View style={[
                styles.inputContainer,
                touched.full_name && errors.full_name && styles.inputError
              ]}>
                <Ionicons 
                  name="person-circle" 
                  size={20} 
                  color={touched.full_name && errors.full_name ? "#ff6b6b" : "#666"} 
                  style={styles.inputIcon} 
                />
                <TextInput
                  style={styles.input}
                  placeholder="Full Name *"
                  placeholderTextColor="#999"
                  value={editedUser.full_name}
                  onChangeText={(text) => {
                    setEditedUser({...editedUser, full_name: text});
                    if (touched.full_name) {
                      validateField('full_name', text);
                    }
                  }}
                  onBlur={() => handleInputBlur('full_name')}
                  editable={isEditing}
                  autoCapitalize="words"
                />
              </View>
              {touched.full_name && errors.full_name && (
                <Text style={styles.fieldErrorText}>{errors.full_name}</Text>
              )}
            </View>

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
                  placeholder={isEditing ? "Enter new password" : "••••••••"}
                  placeholderTextColor="#999"
                  value={editedUser.password}
                  onChangeText={(text) => {
                    setEditedUser({...editedUser, password: text});
                    if (touched.password) {
                      validateField('password', text);
                    }
                  }}
                  onBlur={() => handleInputBlur('password')}
                  editable={isEditing}
                  secureTextEntry={!showPassword}
                />
                {isEditing && (
                  <TouchableOpacity
                    style={styles.eyeIcon}
                    onPress={() => setShowPassword(!showPassword)}
                  >
                    <Ionicons 
                      name={showPassword ? "eye-off" : "eye"} 
                      size={20} 
                      color="#666" 
                    />
                  </TouchableOpacity>
                )}
              </View>
              {touched.password && errors.password && (
                <Text style={styles.fieldErrorText}>{errors.password}</Text>
              )}
            </View>

            {/* Action Buttons */}
            {isEditing ? (
              <>
                <TouchableOpacity 
                  style={[styles.button, isLoading && styles.disabledButton]}
                  onPress={handleSave}
                  disabled={isLoading}
                >
                  <Text style={styles.buttonText}>
                    {isLoading ? 'Saving...' : 'Save Changes'}
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity 
                  style={styles.secondaryButton}
                  onPress={handleCancel}
                >
                  <Text style={styles.secondaryButtonText}>Cancel</Text>
                </TouchableOpacity>
              </>
            ) : (
              <TouchableOpacity 
                style={styles.button}
                onPress={() => setIsEditing(true)}
              >
                <Text style={styles.buttonText}>Edit Profile</Text>
              </TouchableOpacity>
            )}
          </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
};

export default ProfileScreen;
