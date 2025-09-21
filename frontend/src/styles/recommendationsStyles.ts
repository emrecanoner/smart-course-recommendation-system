import { StyleSheet, Platform, Dimensions } from 'react-native';

// Get screen dimensions
const { width, height } = Dimensions.get('window');

// Breakpoints
export const isWeb = Platform.OS === 'web';
export const isTablet = width >= 768;
export const isDesktop = width >= 1024;
export const isMobile = width < 768;

// Recommendations Screen Responsive Dimensions
const recommendationsResponsiveDimensions = {
  // Header dimensions
  headerHeight: {
    mobile: 60,
    tablet: 70,
    desktop: 80,
  },
  
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
  
  // Font sizes
  titleSize: {
    mobile: 30,
    tablet: 25,
    desktop: 30,
  },
  
  subtitleSize: {
    mobile: 20,
    tablet: 18,
    desktop: 20,
  },
  
  bodyTextSize: {
    mobile: 16,
    tablet: 15,
    desktop: 18,
  },
  
  metaTextSize: {
    mobile: 14,
    tablet: 13,
    desktop: 16,
  },
  
  // Card dimensions
  cardSpacing: {
    mobile: 12,
    tablet: 16,
    desktop: 20,
  },
  
  sectionSpacing: {
    mobile: 16,
    tablet: 20,
    desktop: 24,
  },
  
  // Icon sizes
  iconSize: {
    mobile: 24,
    tablet: 22,
    desktop: 28,
  },
  
  // Badge sizes
  badgeSize: {
    mobile: 12,
    tablet: 11,
    desktop: 14,
  },
};

// Base styles for recommendations
const recommendationsBaseStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  scrollContainer: {
    flex: 1,
    ...(isWeb && {
      height: '100vh',
      maxHeight: '100vh',
      overflowY: 'scroll',
      overflowX: 'hidden',
      WebkitOverflowScrolling: 'touch',
      scrollbarWidth: 'thin',
    } as any),
  },
  scrollContent: {
    flexGrow: 1,
    ...(isWeb && {
      minHeight: '100%',
      paddingBottom: 20,
    } as any),
  },
  header: {
    paddingTop: recommendationsResponsiveDimensions.headerHeight.mobile,
    paddingBottom: 20,
    paddingHorizontal: 20,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  backButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
  },
  headerTitle: {
    fontSize: recommendationsResponsiveDimensions.titleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
  },
  headerPlaceholder: {
    width: 40,
  },
  algorithmSection: {
    marginTop: 10,
    paddingHorizontal: 20,
    paddingVertical: 15,
  },
  filtersSection: {
    marginTop: 10,
    paddingHorizontal: 20,
    paddingVertical: 15,
  },
  recommendationsSection: {
    flex: 1,
    marginTop: 10,
    paddingHorizontal: 20,
    paddingVertical: 15,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  recommendationsCount: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    color: '#666',
  },
  algorithmsList: {
    paddingRight: 20,
  },
  algorithmCard: {
    backgroundColor: '#f5f5f5',
    borderRadius: 12,
    padding: 15,
    marginRight: 15,
    width: 150,
  },
  selectedAlgorithmCard: {
    backgroundColor: '#667eea',
  },
  algorithmName: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  selectedAlgorithmName: {
    color: 'white',
  },
  algorithmDescription: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile - 2,
    color: '#666',
  },
  selectedAlgorithmDescription: {
    color: 'rgba(255, 255, 255, 0.8)',
  },
  filtersContainer: {
    gap: 15,
  },
  filterRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  filterLabel: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    color: '#666',
    fontWeight: '500',
    minWidth: 80,
  },
  filterChip: {
    backgroundColor: '#f5f5f5',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    marginRight: 8,
  },
  selectedFilterChip: {
    backgroundColor: '#667eea',
  },
  filterChipText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile - 2,
    color: '#666',
    fontWeight: '500',
  },
  selectedFilterChipText: {
    color: 'white',
  },
  generateButtonContainer: {
    padding: recommendationsResponsiveDimensions.padding.mobile,
    marginTop: 10,
  },
  generateButton: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingVertical: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  generateButtonText: {
    color: 'white',
    fontSize: recommendationsResponsiveDimensions.subtitleSize.mobile,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  recommendationsList: {
    paddingBottom: 20,
  },
  recommendationCard: {
    backgroundColor: 'white',
    borderRadius: 15,
    marginBottom: recommendationsResponsiveDimensions.cardSpacing.mobile,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  recommendationCardHovered: {
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 6,
    transform: [{ scale: 1.02 }],
  },
  recommendationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    paddingBottom: 10,
  },
  rankBadge: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  rankText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.mobile,
    color: 'white',
    fontWeight: 'bold',
  },
  confidenceBadge: {
    backgroundColor: '#4CAF50',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    flexDirection: 'row',
    alignItems: 'center',
  },
  confidenceText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.mobile,
    color: 'white',
    fontWeight: 'bold',
    marginLeft: 4,
  },
  recommendationContent: {
    padding: 15,
    paddingTop: 0,
  },
  recommendationTitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  recommendationInstructor: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    color: '#666',
    marginBottom: 10,
  },
  recommendationMeta: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 15,
  },
  metaText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile - 2,
    color: '#666',
    marginLeft: 4,
  },
  recommendationReason: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile - 1,
    color: '#888',
    fontStyle: 'italic',
    marginBottom: 15,
  },
  recommendationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  priceText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    fontWeight: 'bold',
    color: '#667eea',
  },
  feedbackButtons: {
    flexDirection: 'row',
  },
  feedbackButton: {
    padding: 8,
    marginLeft: 5,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  loadingTitle: {
    fontSize: recommendationsResponsiveDimensions.titleSize.mobile,
    color: '#667eea',
    marginTop: 15,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  loadingSubtitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    color: '#666',
    marginTop: 10,
    textAlign: 'center',
  },
  loadingText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    color: '#666',
    marginTop: 15,
    textAlign: 'center',
  },
  errorContainer: {
    alignItems: 'center',
    padding: 40,
  },
  errorText: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.mobile,
    color: '#ff6b6b',
    marginTop: 15,
    textAlign: 'center',
  },
  errorSubtext: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
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
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    fontWeight: 'bold',
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.mobile,
    color: '#666',
    marginTop: 15,
  },
  emptySubtext: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    color: '#999',
    marginTop: 5,
    textAlign: 'center',
  },
  // Data Requirements Warning Styles
  warningContainer: {
    backgroundColor: '#fff3cd',
    margin: recommendationsResponsiveDimensions.padding.mobile,
    padding: recommendationsResponsiveDimensions.padding.mobile,
    borderRadius: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#ff9800',
  },
  warningHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  warningTitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    fontWeight: 'bold',
    color: '#856404',
    marginLeft: 8,
  },
  progressContainer: {
    marginBottom: 20,
  },
  progressItem: {
    marginBottom: 15,
  },
  progressLabel: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    color: '#856404',
    marginBottom: 5,
    fontWeight: '500',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#ffeaa7',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#ff9800',
    borderRadius: 4,
  },
  progressText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile - 2,
    color: '#856404',
    marginTop: 5,
    textAlign: 'right',
  },
  suggestionsContainer: {
    marginBottom: 20,
  },
  suggestionsTitle: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile,
    fontWeight: 'bold',
    color: '#856404',
    marginBottom: 10,
  },
  suggestionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  suggestionText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.mobile - 1,
    color: '#856404',
    marginLeft: 8,
    flex: 1,
  },
  browseButton: {
    backgroundColor: '#667eea',
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  browseButtonText: {
    color: 'white',
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.mobile,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  // AI Badge Styles
  aiBadge: {
    backgroundColor: '#9c27b0',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 8,
  },
  aiBadgeText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.mobile,
    color: 'white',
    fontWeight: 'bold',
    marginLeft: 4,
  },
});

// Web-specific styles
const recommendationsWebStyles = StyleSheet.create({
  header: {
    paddingTop: recommendationsResponsiveDimensions.headerHeight.tablet,
    paddingBottom: 24,
    paddingHorizontal: 20,
  },
  headerTitle: {
    fontSize: recommendationsResponsiveDimensions.titleSize.tablet,
  },
  algorithmSection: {
    paddingHorizontal: 24,
    paddingVertical: 15,
  },
  filtersSection: {
    paddingHorizontal: 24,
    paddingVertical: 15,
  },
  recommendationsSection: {
    flex: 1,
    paddingHorizontal: 24,
    paddingVertical: 15,
  },
  sectionTitle: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.tablet,
  },
  recommendationsCount: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  algorithmName: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  algorithmDescription: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet - 2,
  },
  filterLabel: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  filterChipText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet - 2,
  },
  generateButtonText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  recommendationCard: {
    marginBottom: recommendationsResponsiveDimensions.cardSpacing.tablet,
  },
  rankText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.tablet,
  },
  confidenceText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.tablet,
  },
  recommendationTitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  recommendationInstructor: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  metaText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet - 2,
  },
  recommendationReason: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet - 1,
  },
  priceText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  loadingTitle: {
    fontSize: recommendationsResponsiveDimensions.titleSize.tablet,
  },
  loadingSubtitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  loadingText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  errorText: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.tablet,
  },
  errorSubtext: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  retryButtonText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  emptyText: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.tablet,
  },
  emptySubtext: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  warningContainer: {
    margin: recommendationsResponsiveDimensions.padding.tablet,
    padding: recommendationsResponsiveDimensions.padding.tablet,
  },
  warningTitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  progressLabel: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  progressText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet - 2,
  },
  suggestionsTitle: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet,
  },
  suggestionText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.tablet - 1,
  },
  browseButtonText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.tablet,
  },
  aiBadgeText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.tablet,
  },
});

// Desktop-specific styles
const recommendationsDesktopStyles = StyleSheet.create({
  header: {
    paddingTop: recommendationsResponsiveDimensions.headerHeight.desktop,
    paddingBottom: 28,
    paddingHorizontal: 20,
  },
  headerTitle: {
    fontSize: recommendationsResponsiveDimensions.titleSize.desktop,
  },
  algorithmSection: {
    paddingHorizontal: 32,
    paddingVertical: 15,
  },
  filtersSection: {
    paddingHorizontal: 32,
    paddingVertical: 15,
  },
  recommendationsSection: {
    flex: 1,
    paddingHorizontal: 32,
    paddingVertical: 15,
  },
  sectionTitle: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.desktop,
  },
  recommendationsCount: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  algorithmName: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  algorithmDescription: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop - 2,
  },
  filterLabel: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  filterChipText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop - 2,
  },
  generateButtonText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  recommendationCard: {
    marginBottom: recommendationsResponsiveDimensions.cardSpacing.desktop,
  },
  rankText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.desktop,
  },
  confidenceText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.desktop,
  },
  recommendationTitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  recommendationInstructor: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  metaText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop - 2,
  },
  recommendationReason: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop - 1,
  },
  priceText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  loadingTitle: {
    fontSize: recommendationsResponsiveDimensions.titleSize.desktop,
  },
  loadingSubtitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  loadingText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  errorText: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.desktop,
  },
  errorSubtext: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  retryButtonText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  emptyText: {
    fontSize: recommendationsResponsiveDimensions.subtitleSize.desktop,
  },
  emptySubtext: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  warningContainer: {
    margin: recommendationsResponsiveDimensions.padding.desktop,
    padding: recommendationsResponsiveDimensions.padding.desktop,
  },
  warningTitle: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  progressLabel: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  progressText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop - 2,
  },
  suggestionsTitle: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop,
  },
  suggestionText: {
    fontSize: recommendationsResponsiveDimensions.metaTextSize.desktop - 1,
  },
  browseButtonText: {
    fontSize: recommendationsResponsiveDimensions.bodyTextSize.desktop,
  },
  aiBadgeText: {
    fontSize: recommendationsResponsiveDimensions.badgeSize.desktop,
  },
});

export const getResponsiveRecommendationsStyles = () => {
  const styles: any = { ...recommendationsBaseStyles };
  
  if (isWeb) {
    // Apply web styles
    Object.keys(recommendationsWebStyles).forEach(key => {
      if (styles[key]) {
        styles[key] = { ...styles[key], ...recommendationsWebStyles[key as keyof typeof recommendationsWebStyles] };
      } else {
        styles[key] = recommendationsWebStyles[key as keyof typeof recommendationsWebStyles];
      }
    });
    
    // Apply desktop styles if desktop
    if (isDesktop) {
      Object.keys(recommendationsDesktopStyles).forEach(key => {
        if (styles[key]) {
          styles[key] = { ...styles[key], ...recommendationsDesktopStyles[key as keyof typeof recommendationsDesktopStyles] };
        } else {
          styles[key] = recommendationsDesktopStyles[key as keyof typeof recommendationsDesktopStyles];
        }
      });
    }
  }
  
  return styles;
};
