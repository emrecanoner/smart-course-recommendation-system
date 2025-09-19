import { StyleSheet, Platform } from 'react-native';
import { isWeb, isDesktop } from './responsiveStyles';

// ProfileScreen specific styles
export const profileBaseStyles = StyleSheet.create({
  profileContainer: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  
  profileHeader: {
    backgroundColor: '#ffffff',
    paddingTop: Platform.OS === 'ios' ? 0 : 20,
    paddingBottom: 20,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  
  profileHeaderContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 50,
  },
  
  profileBackButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
  },
  
  profileHeaderTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    textAlign: 'center',
  },
  
  profileHeaderPlaceholder: {
    width: 40,
  },
  
  profileScrollContent: {
    flex: 1,
    paddingHorizontal: 20,
  },
  
  profileScrollContentStyle: {
    flexGrow: 1,
    paddingBottom: 20,
  },
  
  profileContent: {
    paddingTop: 20,
  },
  
  profileSection: {
    marginBottom: 30,
  },
  
  profileSectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
  },
  
  profileField: {
    marginBottom: 20,
  },
  
  profileFieldLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  
  profileFieldInput: {
    borderWidth: 1,
    borderColor: '#e9ecef',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    backgroundColor: '#ffffff',
    color: '#333',
  },
  
  profileActions: {
    marginTop: 30,
    marginBottom: 20,
  },
  
  profileActionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
  },
  
  profileActionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    gap: 8,
  },
  
  profileEditButton: {
    backgroundColor: '#007bff',
    width: '100%',
  },
  
  profileEditButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  
  profileCancelButton: {
    backgroundColor: '#6c757d',
    flex: 1,
  },
  
  profileCancelButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  
  profileSaveButton: {
    backgroundColor: '#28a745',
    flex: 1,
  },
  
  profileSaveButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
});

// ProfileScreen web-specific styles
export const profileWebStyles = StyleSheet.create({
  profileHeader: {
    ...(isWeb ? {
      position: 'sticky' as any,
      top: 0,
      zIndex: 1000,
    } : {}),
  },
  
  profileHeaderContent: {
    height: 60,
  },
  
  profileHeaderTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
  },
  
  profileScrollContent: {
    ...(isWeb && {
      height: 'calc(100vh - 120px)',
      maxHeight: 'calc(100vh - 120px)',
      overflowY: 'scroll',
      overflowX: 'hidden',
      WebkitOverflowScrolling: 'touch',
      scrollbarWidth: 'thin',
    } as any),
  },
  
  profileScrollContentStyle: {
    ...(isWeb && {
      minHeight: '100%',
    } as any),
  },
  
  profileFieldInput: {
    ...(isWeb ? {
      cursor: 'text' as any,
      transition: 'border-color 0.3s ease',
    } : {}),
  },
  
  profileActionButton: {
    ...(isWeb ? {
      cursor: 'pointer' as any,
      transition: 'all 0.3s ease',
    } : {}),
  },
});

// ProfileScreen desktop-specific styles
export const profileDesktopStyles = StyleSheet.create({
  profileHeaderContent: {
    height: 70,
  },
  
  profileHeaderTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  
  profileContent: {
    paddingTop: 30,
  },
  
  profileSectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 24,
  },
  
  profileFieldLabel: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 10,
  },
  
  profileFieldInput: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    fontSize: 18,
  },
  
  profileActionButton: {
    paddingVertical: 16,
    paddingHorizontal: 32,
  },
  
  profileEditButtonText: {
    fontSize: 18,
    fontWeight: '600',
  },
  
  profileCancelButtonText: {
    fontSize: 18,
    fontWeight: '600',
  },
  
  profileSaveButtonText: {
    fontSize: 18,
    fontWeight: '600',
  },
});

// ProfileScreen responsive styles function
export const getResponsiveProfileStyles = () => {
  const baseStyles = profileBaseStyles;
  const webStyles = isWeb ? profileWebStyles : {};
  const desktopStyles = isDesktop ? profileDesktopStyles : {};
  
  return {
    ...baseStyles,
    ...webStyles,
    ...desktopStyles,
  };
};
