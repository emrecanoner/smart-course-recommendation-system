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

// HomeScreen specific responsive dimensions
export const homeResponsiveDimensions = {
  // Header dimensions
  headerHeight: {
    mobile: 80,
    tablet: 90,
    desktop: 100,
  },
  
  // Card dimensions
  actionCardWidth: {
    mobile: '48%',
    tablet: '48%',
    desktop: '48%',
  },
  
  recommendationCardWidth: {
    mobile: 240, // Reduced from 280
    tablet: 280, // Reduced from 320
    desktop: 300, // Reduced from 350
  },
  
  // Spacing
  sectionSpacing: {
    mobile: 24,
    tablet: 24, // Reduced from 30
    desktop: 28, // Reduced from 36
  },
  
  cardSpacing: {
    mobile: 12,
    tablet: 16,
    desktop: 20,
  },
  
  // Font sizes for home screen (slightly larger than login/register)
  welcomeTextSize: {
    mobile: 14, // Original size
    tablet: 12, // 16 * 0.75
    desktop: 14, // 18 * 0.75
  },
  
  userNameSize: {
    mobile: 20, // Original size
    tablet: 18, // 24 * 0.75
    desktop: 22, // 28 * 0.75
  },
  
  sectionTitleSize: {
    mobile: 16, // Further reduced for mobile
    tablet: 19, // 26 * 0.75
    desktop: 24, // 30 * 0.75
  },
  
  actionTitleSize: {
    mobile: 16, // Original size
    tablet: 14, // 18 * 0.75
    desktop: 16, // 20 * 0.75
  },
  
  actionSubtitleSize: {
    mobile: 12, // Original size
    tablet: 11, // 14 * 0.75
    desktop: 12, // 16 * 0.75
  },
  
  recommendationTitleSize: {
    mobile: 16, // Original size
    tablet: 14, // 18 * 0.75
    desktop: 16, // 20 * 0.75
  },
  
  recommendationTextSize: {
    mobile: 12, // Original size
    tablet: 11, // 14 * 0.75
    desktop: 12, // 16 * 0.75
  },
};

// HomeScreen specific styles
export const homeBaseStyles = StyleSheet.create({
  homeContainer: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  
  homeHeader: {
    backgroundColor: '#ffffff',
    paddingTop: Platform.OS === 'ios' ? 0 : 20,
    paddingBottom: 20,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  
  homeHeaderContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: homeResponsiveDimensions.headerHeight.mobile,
  },
  
  homeUserInfo: {
    flex: 1,
  },
  
  homeWelcomeText: {
    fontSize: homeResponsiveDimensions.welcomeTextSize.mobile,
    color: '#6c757d',
    fontWeight: '500',
  },
  
  homeUserName: {
    fontSize: homeResponsiveDimensions.userNameSize.mobile,
    color: '#333',
    fontWeight: 'bold',
    marginTop: 2,
  },
  
  homeLogoutButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
  },
  
  homeHeaderActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  
  homeHeaderButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
  },
  
  homeContent: {
    flex: 1,
    paddingHorizontal: 20,
  },
  
  homeMainContent: {
    flex: 1,
    flexDirection: 'column',
  },
  
  homeScrollContent: {
    flex: 1,
    paddingHorizontal: 20,
  },
  
  homeProfileSection: {
    paddingHorizontal: 20,
    paddingBottom: 20,
    paddingTop: 10,
    backgroundColor: '#f8f9fa',
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  
  homeSection: {
    marginTop: homeResponsiveDimensions.sectionSpacing.mobile,
  },
  
  homeSectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  
  homeSectionTitle: {
    fontSize: homeResponsiveDimensions.sectionTitleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
  },
  
  homeSeeAllText: {
    fontSize: 16,
    color: '#007bff',
    fontWeight: '600',
  },
  
  homeQuickActions: {
    flexDirection: 'row',
    justifyContent: 'space-between', // Equal spacing from edges
    flexWrap: 'wrap',
    gap: 12, // Gap between cards
  },
  
  homeActionCard: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 20,
    width: homeResponsiveDimensions.actionCardWidth.mobile as any,
    marginBottom: homeResponsiveDimensions.cardSpacing.mobile,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  
  homeActionIconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#f8f9fa',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  
  homeActionTitle: {
    fontSize: homeResponsiveDimensions.actionTitleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  
  homeActionSubtitle: {
    fontSize: homeResponsiveDimensions.actionSubtitleSize.mobile,
    color: '#6c757d',
    lineHeight: 18,
  },
  
  homeLoadingContainer: {
    padding: 40,
    alignItems: 'center',
  },
  
  homeLoadingText: {
    fontSize: 16,
    color: '#6c757d',
  },
  
  homeRecommendationCard: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 16, // Reduced padding
    width: homeResponsiveDimensions.recommendationCardWidth.mobile,
    marginRight: homeResponsiveDimensions.cardSpacing.mobile,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#e9ecef',
    justifyContent: 'space-between', // Distribute content evenly
    flexShrink: 0, // Prevent shrinking for horizontal scroll
  },
  
  homeRecommendationGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 12,
  },
  
  homeRecommendationCardMobile: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 16,
    width: '48%', // 2 cards per row
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#e9ecef',
    justifyContent: 'space-between',
    minHeight: 200,
  },
  
  homeRecommendationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  
  homeRecommendationTitle: {
    fontSize: homeResponsiveDimensions.recommendationTitleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 8,
  },
  
  homeRatingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  
  homeRatingText: {
    fontSize: 14,
    color: '#333',
    marginLeft: 4,
    fontWeight: '600',
  },
  
  homeRecommendationInstructor: {
    fontSize: homeResponsiveDimensions.recommendationTextSize.mobile,
    color: '#6c757d',
    marginBottom: 8,
  },
  
  homeRecommendationReason: {
    fontSize: homeResponsiveDimensions.recommendationTextSize.mobile,
    color: '#495057',
    lineHeight: 18,
    marginBottom: 12,
  },
  
  homeRecommendationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  
  homeConfidenceScore: {
    fontSize: 12,
    color: '#28a745',
    fontWeight: '600',
    backgroundColor: '#d4edda',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  
  homePriceText: {
    fontSize: 16,
    color: '#007bff',
    fontWeight: 'bold',
  },
  
  homeEmptyContainer: {
    padding: 40,
    alignItems: 'center',
  },
  
  homeEmptyText: {
    fontSize: 18,
    color: '#6c757d',
    fontWeight: '600',
    marginTop: 12,
    marginBottom: 4,
  },
  
  homeEmptySubtext: {
    fontSize: 14,
    color: '#6c757d',
    textAlign: 'center',
  },
  
  homeProfileCard: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#e9ecef',
    marginBottom: 20, // Add bottom margin for mobile
  },
  
  homeProfileInfo: {
    flex: 1,
    marginLeft: 16,
  },
  
  homeProfileTitle: {
    fontSize: 13, // Further reduced for mobile
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  
  homeProfileSubtitle: {
    fontSize: 10, // Further reduced for mobile
    color: '#6c757d',
  },
  
  homeFooter: {
    marginTop: 40,
    paddingVertical: 30,
    paddingHorizontal: 20,
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  
  homeFooterContent: {
    alignItems: 'center',
  },
  
  homeFooterText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  
  homeFooterSubtext: {
    fontSize: 14,
    color: '#6c757d',
    textAlign: 'center',
  },
});

// HomeScreen web-specific styles
export const homeWebStyles = StyleSheet.create({
  homeContainer: {
    ...(isWeb ? {
      minHeight: '100vh' as any,
    } : {}),
  },
  
  homeHeader: {
    ...(isWeb ? {
      position: 'sticky' as any,
      top: 0,
      zIndex: 1000,
    } : {}),
  },
  
  homeHeaderContent: {
    height: homeResponsiveDimensions.headerHeight.tablet,
  },
  
  homeWelcomeText: {
    fontSize: homeResponsiveDimensions.welcomeTextSize.tablet,
  },
  
  homeUserName: {
    fontSize: homeResponsiveDimensions.userNameSize.tablet,
  },
  
  homeLogoutButton: {
    ...(isWeb ? {
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } : {}),
  },
  
  homeHeaderActions: {
    gap: 12, // Larger gap for web
  },
  
  homeHeaderButton: {
    ...(isWeb ? {
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } : {}),
  },
  
  homeContent: {
    paddingHorizontal: 24,
  },
  
  homeScrollContent: {
    paddingHorizontal: 24,
  },
  
  homeProfileSection: {
    paddingHorizontal: 24,
    paddingBottom: 24,
    paddingTop: 16,
  },
  
  homeSection: {
    marginTop: homeResponsiveDimensions.sectionSpacing.tablet,
  },
  
  homeSectionTitle: {
    fontSize: homeResponsiveDimensions.sectionTitleSize.tablet,
  },
  
  homeActionCard: {
    width: homeResponsiveDimensions.actionCardWidth.tablet as any,
    marginBottom: homeResponsiveDimensions.cardSpacing.tablet,
    ...(isWeb ? {
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } : {}),
  },
  
  homeActionTitle: {
    fontSize: homeResponsiveDimensions.actionTitleSize.tablet,
  },
  
  homeActionSubtitle: {
    fontSize: homeResponsiveDimensions.actionSubtitleSize.tablet,
  },
  
  homeRecommendationCard: {
    width: homeResponsiveDimensions.recommendationCardWidth.tablet,
    marginRight: homeResponsiveDimensions.cardSpacing.tablet,
    padding: 18, // Reduced padding for web
    justifyContent: 'space-between', // Distribute content evenly
    flexShrink: 0, // Prevent shrinking for horizontal scroll
    ...(isWeb ? {
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } : {}),
  },
  
  homeRecommendationTitle: {
    fontSize: homeResponsiveDimensions.recommendationTitleSize.tablet,
  },
  
  homeRecommendationInstructor: {
    fontSize: homeResponsiveDimensions.recommendationTextSize.tablet,
  },
  
  homeRecommendationReason: {
    fontSize: homeResponsiveDimensions.recommendationTextSize.tablet,
  },
  
  homeProfileCard: {
    ...(isWeb ? {
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    } : {}),
  },
  
  homeProfileTitle: {
    fontSize: 18, // Larger for web
  },
  
  homeProfileSubtitle: {
    fontSize: 14, // Larger for web
  },
  
  homeFooter: {
    marginTop: 50,
    paddingVertical: 40,
    paddingHorizontal: 24,
  },
  
  homeFooterText: {
    fontSize: 18,
    marginBottom: 10,
  },
  
  homeFooterSubtext: {
    fontSize: 16,
  },
});

// HomeScreen desktop-specific styles
export const homeDesktopStyles = StyleSheet.create({
  homeHeaderContent: {
    height: homeResponsiveDimensions.headerHeight.desktop,
  },
  
  homeWelcomeText: {
    fontSize: homeResponsiveDimensions.welcomeTextSize.desktop,
  },
  
  homeUserName: {
    fontSize: homeResponsiveDimensions.userNameSize.desktop,
  },
  
  homeHeaderActions: {
    gap: 16, // Even larger gap for desktop
  },
  
  homeContent: {
    paddingHorizontal: 32,
  },
  
  homeScrollContent: {
    paddingHorizontal: 32,
  },
  
  homeProfileSection: {
    paddingHorizontal: 32,
    paddingBottom: 32,
    paddingTop: 20,
  },
  
  homeSection: {
    marginTop: homeResponsiveDimensions.sectionSpacing.desktop,
  },
  
  homeSectionTitle: {
    fontSize: homeResponsiveDimensions.sectionTitleSize.desktop,
  },
  
  homeActionCard: {
    width: homeResponsiveDimensions.actionCardWidth.desktop as any,
    marginBottom: homeResponsiveDimensions.cardSpacing.desktop,
  },
  
  homeActionTitle: {
    fontSize: homeResponsiveDimensions.actionTitleSize.desktop,
  },
  
  homeActionSubtitle: {
    fontSize: homeResponsiveDimensions.actionSubtitleSize.desktop,
  },
  
  homeRecommendationCard: {
    width: homeResponsiveDimensions.recommendationCardWidth.desktop,
    marginRight: homeResponsiveDimensions.cardSpacing.desktop,
    padding: 20, // Reduced padding for desktop
    justifyContent: 'space-between', // Distribute content evenly
    flexShrink: 0, // Prevent shrinking for horizontal scroll
  },
  
  homeRecommendationTitle: {
    fontSize: homeResponsiveDimensions.recommendationTitleSize.desktop,
  },
  
  homeRecommendationInstructor: {
    fontSize: homeResponsiveDimensions.recommendationTextSize.desktop,
  },
  
  homeRecommendationReason: {
    fontSize: homeResponsiveDimensions.recommendationTextSize.desktop,
  },
  
  homeProfileTitle: {
    fontSize: 20, // Larger for desktop
  },
  
  homeProfileSubtitle: {
    fontSize: 16, // Larger for desktop
  },
  
  homeFooter: {
    marginTop: 60,
    paddingVertical: 50,
    paddingHorizontal: 32,
  },
  
  homeFooterText: {
    fontSize: 20,
    marginBottom: 12,
  },
  
  homeFooterSubtext: {
    fontSize: 18,
  },
});

// Helper function to get responsive home styles
export const getResponsiveHomeStyles = () => {
  const styles: any = { ...homeBaseStyles };
  
  if (isWeb) {
    // Apply web styles
    Object.keys(homeWebStyles).forEach(key => {
      if (styles[key]) {
        styles[key] = { ...styles[key], ...homeWebStyles[key as keyof typeof homeWebStyles] };
      } else {
        styles[key] = homeWebStyles[key as keyof typeof homeWebStyles];
      }
    });
    
    // Apply desktop styles
    if (isDesktop) {
      Object.keys(homeDesktopStyles).forEach(key => {
        if (styles[key]) {
          styles[key] = { ...styles[key], ...homeDesktopStyles[key as keyof typeof homeDesktopStyles] };
        } else {
          styles[key] = homeDesktopStyles[key as keyof typeof homeDesktopStyles];
        }
      });
    }
  }
  
  return styles;
};