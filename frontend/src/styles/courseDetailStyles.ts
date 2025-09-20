import { StyleSheet, Platform } from 'react-native';

// Platform detection
const isWeb = Platform.OS === 'web';
const { width: screenWidth } = require('react-native').Dimensions.get('window');
const isTablet = screenWidth >= 768 && screenWidth < 1024;
const isDesktop = screenWidth >= 1024;
const isMobile = screenWidth < 768;

// Course Detail Responsive Dimensions
const courseDetailResponsiveDimensions = {
  headerHeight: {
    mobile: 60,
    tablet: 70,
    desktop: 80,
  },
  titleSize: {
    mobile: 32,
    tablet: 27,
    desktop: 36,
  },
  subtitleSize: {
    mobile: 16,
    tablet: 13,
    desktop: 18,
  },
  bodySize: {
    mobile: 14,
    tablet: 13,
    desktop: 16,
  },
  buttonHeight: {
    mobile: 56,
    tablet: 56,
    desktop: 56,
  },
  cardPadding: {
    mobile: 16,
    tablet: 20,
    desktop: 24,
  },
  sectionSpacing: {
    mobile: 20,
    tablet: 24,
    desktop: 32,
  },
  imageHeight: {
    mobile: 200,
    tablet: 250,
    desktop: 300,
  },
};

// Course Detail Base Styles
const courseDetailBaseStyles = StyleSheet.create({
  courseDetailContainer: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  courseDetailHeader: {
    paddingTop: courseDetailResponsiveDimensions.headerHeight.mobile,
    paddingBottom: 20,
    paddingHorizontal: 20,
    backgroundColor: '#ffffff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  courseDetailHeaderContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  courseDetailBackButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
  },
  courseDetailHeaderTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
  },
  courseDetailHeaderPlaceholder: {
    width: 40,
  },
  courseDetailScrollContent: {
    flexGrow: 1,
    paddingBottom: 20,
  },
  courseDetailImage: {
    width: '100%',
    height: courseDetailResponsiveDimensions.imageHeight.mobile,
    borderRadius: 12,
    marginBottom: courseDetailResponsiveDimensions.sectionSpacing.mobile,
    backgroundColor: '#f8f9fa',
    marginHorizontal: 20,
  },
  courseDetailInfo: {
    paddingHorizontal: 20,
    marginBottom: courseDetailResponsiveDimensions.sectionSpacing.mobile,
  },
  courseDetailTitleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  courseDetailTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 12,
  },
  courseDetailLikeButton: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  courseDetailInstructorRating: {
    marginBottom: 20,
  },
  courseDetailInstructor: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    marginBottom: 8,
  },
  courseDetailRating: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  courseDetailRatingText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    marginLeft: 6,
  },
  courseDetailMeta: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: courseDetailResponsiveDimensions.sectionSpacing.mobile,
  },
  courseDetailMetaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
    marginBottom: 8,
  },
  courseDetailMetaText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    marginLeft: 6,
  },
  courseDetailDescription: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#333',
    lineHeight: 22,
    marginBottom: courseDetailResponsiveDimensions.sectionSpacing.mobile,
  },
  courseDetailContentTitle: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.mobile,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  courseDetailContentItems: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  courseDetailContentItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
  },
  courseDetailContentText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#333',
    marginLeft: 6,
  },
  courseDetailSkills: {
    paddingHorizontal: 20,
    marginBottom: courseDetailResponsiveDimensions.sectionSpacing.mobile,
    paddingTop: 0,
  },
  courseDetailSkillsTitle: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.mobile,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  courseDetailSkillsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginTop: 8,
  },
  courseDetailSkillTag: {
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#bbdefb',
  },
  courseDetailSkillText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile - 1,
    color: '#1976d2',
    fontWeight: '500',
  },
  courseDetailSkillsText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    lineHeight: 20,
  },
  courseDetailActions: {
    paddingHorizontal: 20,
    paddingBottom: 40,
    paddingTop: 20,
    alignItems: 'center',
  },
  courseDetailEnrollButton: {
    height: courseDetailResponsiveDimensions.buttonHeight.mobile,
    marginBottom: 12,
  },
  courseDetailSimilarTitle: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.mobile,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  courseDetailSimilarList: {
    // paddingHorizontal: 20, // Removed since it's now inside courseDetailInfo
  },
  courseDetailSimilarCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: courseDetailResponsiveDimensions.cardPadding.mobile,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  courseDetailSimilarCardTitle: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  courseDetailSimilarCardDescription: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile - 1,
    color: '#666',
    lineHeight: 18,
  },
  courseDetailLoading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  courseDetailError: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  courseDetailErrorText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#ff3b30',
    textAlign: 'center',
    marginBottom: 16,
  },
  courseDetailRetryButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
  },
  courseDetailRetryButtonText: {
    color: '#ffffff',
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    fontWeight: '600',
  },
  courseDetailActionButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  courseDetailActionButton: {
    flex: 1,
  },
  courseDetailUnenrollButton: {
    marginTop: 12,
    paddingVertical: 8,
    alignItems: 'center',
  },
  courseDetailUnenrollText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    textDecorationLine: 'underline',
  },
  ratingModalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  ratingModalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 24,
    margin: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  ratingModalTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  ratingModalSubtitle: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    textAlign: 'center',
    marginBottom: 24,
  },
  ratingStarsContainer: {
    flexDirection: 'row',
    marginBottom: 24,
  },
  ratingStarButton: {
    padding: 8,
  },
  ratingModalCloseButton: {
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  ratingModalCloseText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.mobile,
    color: '#666',
    textDecorationLine: 'underline',
  },
});

// Course Detail Web Styles
const courseDetailWebStyles = StyleSheet.create({
  courseDetailContainer: {
    backgroundColor: '#ffffff',
  },
  courseDetailHeader: {
    paddingTop: courseDetailResponsiveDimensions.headerHeight.tablet,
    paddingBottom: 24,
    paddingHorizontal: 20,
  },
  courseDetailHeaderTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.tablet,
    fontWeight: 'bold',
    color: '#333',
  },
  courseDetailScrollContent: {
    ...(isWeb && {
      height: '100vh',
      maxHeight: '100vh',
      overflowY: 'auto',
      overflowX: 'hidden',
      WebkitOverflowScrolling: 'touch',
      scrollbarWidth: 'thin',
    } as any),
  },
  courseDetailImage: {
    height: courseDetailResponsiveDimensions.imageHeight.tablet,
  },
  courseDetailTitleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  courseDetailTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.tablet,
    flex: 1,
    marginRight: 12,
  },
  courseDetailLikeButton: {
    padding: 10,
    borderRadius: 22,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  courseDetailInstructor: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
  },
  courseDetailRatingText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    marginLeft: 6,
  },
  courseDetailMetaText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    marginLeft: 6,
  },
  courseDetailDescription: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    lineHeight: 24,
  },
  courseDetailSkillsText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    lineHeight: 22,
  },
  courseDetailEnrollButton: {
    height: courseDetailResponsiveDimensions.buttonHeight.tablet,
  },
  courseDetailEnrollButtonText: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.tablet,
  },
  courseDetailSimilarTitle: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.tablet,
  },
  courseDetailSimilarCard: {
    padding: courseDetailResponsiveDimensions.cardPadding.tablet,
  },
  courseDetailSimilarCardTitle: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
  },
  courseDetailSimilarCardDescription: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet - 1,
    lineHeight: 20,
  },
  courseDetailActionButtons: {
    flexDirection: 'row',
    gap: 14,
  },
  courseDetailActionButton: {
    flex: 1,
  },
  courseDetailUnenrollButton: {
    marginTop: 14,
    paddingVertical: 10,
    alignItems: 'center',
  },
  courseDetailUnenrollText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    color: '#666',
    textDecorationLine: 'underline',
  },
  ratingModalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 18,
    padding: 28,
    margin: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  ratingModalTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.tablet,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  ratingModalSubtitle: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    color: '#666',
    textAlign: 'center',
    marginBottom: 28,
  },
  ratingStarsContainer: {
    flexDirection: 'row',
    marginBottom: 28,
  },
  ratingStarButton: {
    padding: 10,
  },
  ratingModalCloseText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.tablet,
    color: '#666',
    textDecorationLine: 'underline',
  },
});

// Course Detail Desktop Styles
const courseDetailDesktopStyles = StyleSheet.create({
  courseDetailHeader: {
    paddingTop: courseDetailResponsiveDimensions.headerHeight.desktop,
    paddingBottom: 28,
    paddingHorizontal: 20,
  },
  courseDetailHeaderTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.desktop,
    fontWeight: 'bold',
    color: '#333',
  },
  courseDetailImage: {
    height: courseDetailResponsiveDimensions.imageHeight.desktop,
  },
  courseDetailTitleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  courseDetailTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.desktop,
    flex: 1,
    marginRight: 12,
  },
  courseDetailLikeButton: {
    padding: 12,
    borderRadius: 24,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  courseDetailInstructor: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
  },
  courseDetailRatingText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    marginLeft: 6,
  },
  courseDetailMetaText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    marginLeft: 6,
  },
  courseDetailDescription: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    lineHeight: 26,
  },
  courseDetailSkillsText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    lineHeight: 24,
  },
  courseDetailEnrollButton: {
    height: courseDetailResponsiveDimensions.buttonHeight.desktop,
  },
  courseDetailEnrollButtonText: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.desktop,
  },
  courseDetailSimilarTitle: {
    fontSize: courseDetailResponsiveDimensions.subtitleSize.desktop,
  },
  courseDetailSimilarCard: {
    padding: courseDetailResponsiveDimensions.cardPadding.desktop,
  },
  courseDetailSimilarCardTitle: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
  },
  courseDetailSimilarCardDescription: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop - 1,
    lineHeight: 22,
  },
  courseDetailActionButtons: {
    flexDirection: 'row',
    gap: 16,
  },
  courseDetailActionButton: {
    flex: 1,
  },
  courseDetailUnenrollButton: {
    marginTop: 16,
    paddingVertical: 12,
    alignItems: 'center',
  },
  courseDetailUnenrollText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    color: '#666',
    textDecorationLine: 'underline',
  },
  ratingModalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 32,
    margin: 28,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  ratingModalTitle: {
    fontSize: courseDetailResponsiveDimensions.titleSize.desktop,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  ratingModalSubtitle: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    color: '#666',
    textAlign: 'center',
    marginBottom: 32,
  },
  ratingStarsContainer: {
    flexDirection: 'row',
    marginBottom: 32,
  },
  ratingStarButton: {
    padding: 12,
  },
  ratingModalCloseText: {
    fontSize: courseDetailResponsiveDimensions.bodySize.desktop,
    color: '#666',
    textDecorationLine: 'underline',
  },
});

// Course Detail Screen Responsive Styles
export const getResponsiveCourseDetailStyles = () => {
  const styles = { ...courseDetailBaseStyles } as any;
  
  if (isWeb) {
    Object.keys(courseDetailWebStyles).forEach(key => {
      if (courseDetailWebStyles[key as keyof typeof courseDetailWebStyles]) {
        styles[key] = courseDetailWebStyles[key as keyof typeof courseDetailWebStyles];
      }
    });
    
    if (isDesktop) {
      Object.keys(courseDetailDesktopStyles).forEach(key => {
        if (courseDetailDesktopStyles[key as keyof typeof courseDetailDesktopStyles]) {
          styles[key] = courseDetailDesktopStyles[key as keyof typeof courseDetailDesktopStyles];
        }
      });
    }
  }
  
  return styles;
};
