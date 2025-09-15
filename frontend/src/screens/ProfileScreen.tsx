import React from 'react';
import { View, Text, StyleSheet, SafeAreaView } from 'react-native';
import LoadingComponent from '../components/LoadingComponent';

const ProfileScreen: React.FC = () => {
  const [showPageLoading, setShowPageLoading] = React.useState(true);

  React.useEffect(() => {
    // Show page loading for 1.5 seconds
    const timer = setTimeout(() => {
      setShowPageLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, []);

  // Show loading screen when page opens
  if (showPageLoading) {
    return (
      <LoadingComponent 
        visible={true}
      />
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Profile</Text>
        <Text style={styles.subtitle}>Coming soon...</Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
});

export default ProfileScreen;
