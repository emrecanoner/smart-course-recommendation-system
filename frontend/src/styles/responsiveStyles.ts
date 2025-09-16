import { StyleSheet, Platform, Dimensions } from 'react-native';

// Get screen dimensions
const { width, height } = Dimensions.get('window');

// Breakpoints
export const isWeb = Platform.OS === 'web';
export const isTablet = width >= 768;
export const isDesktop = width >= 1024;
export const isMobile = width < 768;

// Responsive dimensions
export const responsiveDimensions = {
  // Container dimensions
  containerMaxWidth: {
    mobile: '100%',
    tablet: 375, // 500 * 0.75
    desktop: 450, // 600 * 0.75
  },
  
  // Padding
  padding: {
    mobile: 30,
    tablet: 37, // 50 * 0.75
    desktop: 45, // 60 * 0.75
  },
  
  // Form padding
  formPadding: {
    mobile: 30,
    tablet: 37, // 50 * 0.75
    desktop: 45, // 60 * 0.75
  },
  
  // Input dimensions
  inputHeight: {
    mobile: 56,
    web: 45, // 60 * 0.75
  },
  
  // Font sizes
  titleSize: {
    mobile: 32,
    tablet: 27, // 36 * 0.75
    desktop: 30, // 40 * 0.75
  },
  
  subtitleSize: {
    mobile: 16,
    tablet: 13, // 18 * 0.75
    desktop: 15, // 20 * 0.75
  },
  
  inputSize: {
    mobile: 16,
    web: 12, // 17 * 0.75
  },
  
  buttonTextSize: {
    mobile: 18,
    web: 14, // 19 * 0.75
  },
  
  // Icon sizes
  iconSize: {
    mobile: 60,
    tablet: 52, // 70 * 0.75
    desktop: 60, // 80 * 0.75
  },
  
  // Margins
  headerMargin: {
    mobile: 50,
    tablet: 30, // 40 * 0.75
    desktop: 26, // 35 * 0.75
  },
  
  inputMargin: {
    mobile: 20,
    web: 18, // 24 * 0.75
  },
};

// Base styles that work across all platforms
export const baseStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  
  keyboardAvoidingView: {
    flex: 1,
  },
  
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  
  content: {
    width: '100%',
    justifyContent: 'center',
    paddingHorizontal: responsiveDimensions.padding.mobile,
  },
  
  header: {
    alignItems: 'center',
    marginBottom: responsiveDimensions.headerMargin.mobile,
  },
  
  title: {
    fontSize: responsiveDimensions.titleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
  },
  
  subtitle: {
    fontSize: responsiveDimensions.subtitleSize.mobile,
    color: '#666',
    marginTop: 5,
  },
  
  form: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: responsiveDimensions.formPadding.mobile,
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
  
  inputWrapper: {
    marginBottom: responsiveDimensions.inputMargin.mobile,
  },
  
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    marginBottom: 0,
    paddingHorizontal: 16,
    height: responsiveDimensions.inputHeight.mobile,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  
  inputIcon: {
    marginRight: 12,
  },
  
  input: {
    flex: 1,
    fontSize: responsiveDimensions.inputSize.mobile,
    color: '#333',
    fontWeight: '400',
  },
  
  eyeIcon: {
    padding: 2,
    marginLeft: 4,
    minWidth: 24,
    alignItems: 'center',
    justifyContent: 'center',
  },
  
  button: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    height: responsiveDimensions.inputHeight.mobile,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
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
  
  buttonText: {
    color: 'white',
    fontSize: responsiveDimensions.buttonTextSize.mobile,
    fontWeight: '600',
  },
  
  secondaryButton: {
    marginTop: 20,
    alignItems: 'center',
  },
  
  secondaryButtonText: {
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
    fontSize: responsiveDimensions.inputSize.mobile,
    marginLeft: 8,
    flex: 1,
    fontWeight: '500',
  },
  
  fieldErrorText: {
    color: '#ff6b6b',
    fontSize: responsiveDimensions.inputSize.mobile,
    marginTop: 4,
    marginLeft: 4,
    fontWeight: '500',
  },
  
  inputError: {
    borderColor: '#ff6b6b',
    backgroundColor: '#fff5f5',
  },
});

// Web-specific styles
export const webStyles = StyleSheet.create({
  container: {
    ...(isWeb ? {
      minHeight: '100vh' as any,
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    } : {
      minHeight: 1000,
    }),
  },
  
  scrollContainer: {
    ...(isWeb ? {
      minHeight: '100vh' as any,
      justifyContent: 'center',
      alignItems: 'center',
    } : {
      minHeight: 1000,
      justifyContent: 'center',
      alignItems: 'center',
    }),
  },
  
  content: {
    width: '100%',
    maxWidth: 375, // 500 * 0.75
    paddingHorizontal: 30, // 40 * 0.75
    paddingVertical: 45, // 60 * 0.75
  },
  
  tabletContent: {
    maxWidth: responsiveDimensions.containerMaxWidth.tablet,
    paddingHorizontal: responsiveDimensions.padding.tablet,
  },
  
  desktopContent: {
    maxWidth: responsiveDimensions.containerMaxWidth.desktop,
    paddingHorizontal: responsiveDimensions.padding.desktop,
  },
  
  header: {
    marginBottom: responsiveDimensions.headerMargin.tablet,
  },
  
  title: {
    fontSize: responsiveDimensions.titleSize.tablet,
    marginTop: 24,
  },
  
  subtitle: {
    fontSize: responsiveDimensions.subtitleSize.tablet,
    marginTop: 8,
  },
  
  form: {
    padding: 30, // 40 * 0.75
    maxWidth: '100%',
    ...(isWeb && {
      boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
    }),
  },
  
  tabletForm: {
    padding: responsiveDimensions.formPadding.tablet,
  },
  
  desktopForm: {
    padding: responsiveDimensions.formPadding.desktop,
  },
  
  inputWrapper: {
    marginBottom: responsiveDimensions.inputMargin.web,
  },
  
  inputContainer: {
    height: responsiveDimensions.inputHeight.web,
    marginBottom: 0,
    ...(isWeb && {
      transition: 'all 0.3s ease',
    }),
  },
  
  input: {
    fontSize: responsiveDimensions.inputSize.web,
  },
  
  fieldErrorText: {
    fontSize: responsiveDimensions.inputSize.web,
  },
  
  errorText: {
    fontSize: responsiveDimensions.inputSize.web,
  },
  
  button: {
    height: responsiveDimensions.inputHeight.web,
    marginTop: 20,
    ...(isWeb && {
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    }),
  },
  
  buttonText: {
    fontSize: responsiveDimensions.buttonTextSize.web,
  },
  
  secondaryButton: {
    marginTop: 24,
    ...(isWeb && {
      cursor: 'pointer',
    }),
  },
  
  secondaryButtonText: {
    fontSize: 12, // 17 * 0.75
  },
});

// Helper function to get responsive styles
export const getResponsiveStyles = () => {
  const styles: any = { ...baseStyles };
  
  if (isWeb) {
    // Apply web styles
    Object.keys(webStyles).forEach(key => {
      if (styles[key]) {
        styles[key] = { ...styles[key], ...webStyles[key as keyof typeof webStyles] };
      } else {
        styles[key] = webStyles[key as keyof typeof webStyles];
      }
    });
    
    // Apply responsive content styles
    if (isTablet) {
      styles.content = { ...styles.content, ...webStyles.tabletContent };
      styles.form = { ...styles.form, ...webStyles.tabletForm };
    }
    
    if (isDesktop) {
      styles.content = { ...styles.content, ...webStyles.desktopContent };
      styles.form = { ...styles.form, ...webStyles.desktopForm };
    }
  }
  
  return styles;
};

// Helper function to get responsive icon size
export const getIconSize = () => {
  if (isDesktop) return responsiveDimensions.iconSize.desktop;
  if (isTablet) return responsiveDimensions.iconSize.tablet;
  return responsiveDimensions.iconSize.mobile;
};

// Helper function to get responsive title size
export const getTitleSize = () => {
  if (isDesktop) return responsiveDimensions.titleSize.desktop;
  if (isTablet) return responsiveDimensions.titleSize.tablet;
  return responsiveDimensions.titleSize.mobile;
};

// Helper function to get responsive subtitle size
export const getSubtitleSize = () => {
  if (isDesktop) return responsiveDimensions.subtitleSize.desktop;
  if (isTablet) return responsiveDimensions.subtitleSize.tablet;
  return responsiveDimensions.subtitleSize.mobile;
};
