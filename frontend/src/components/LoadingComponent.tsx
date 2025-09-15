import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated } from 'react-native';

interface LoadingComponentProps {
  visible?: boolean;
  overlayColor?: string;
  size?: 'small' | 'medium' | 'large';
  color?: string;
}

const LoadingComponent: React.FC<LoadingComponentProps> = ({
  visible = true,
  overlayColor = "transparent",
  size = 'medium',
  color = '#000000'
}) => {
  const spinValue = useRef(new Animated.Value(0)).current;
  const pulseValue = useRef(new Animated.Value(1)).current;
  const dot1Value = useRef(new Animated.Value(0)).current;
  const dot2Value = useRef(new Animated.Value(0)).current;
  const dot3Value = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (!visible) return;

    // Spinning circle animation
    const spinAnimation = Animated.loop(
      Animated.timing(spinValue, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      })
    );

    // Pulse animation for the container
    const pulseAnimation = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseValue, {
          toValue: 1.1,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(pulseValue, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
      ])
    );

    // Dots animation
    const createDotAnimation = (dotValue: Animated.Value, delay: number) => {
      return Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(dotValue, {
            toValue: 1,
            duration: 400,
            useNativeDriver: true,
          }),
          Animated.timing(dotValue, {
            toValue: 0,
            duration: 400,
            useNativeDriver: true,
          }),
        ])
      );
    };

    const dot1Animation = createDotAnimation(dot1Value, 0);
    const dot2Animation = createDotAnimation(dot2Value, 200);
    const dot3Animation = createDotAnimation(dot3Value, 400);

    spinAnimation.start();
    pulseAnimation.start();
    dot1Animation.start();
    dot2Animation.start();
    dot3Animation.start();

    return () => {
      spinAnimation.stop();
      pulseAnimation.stop();
      dot1Animation.stop();
      dot2Animation.stop();
      dot3Animation.stop();
    };
  }, [visible, spinValue, pulseValue, dot1Value, dot2Value, dot3Value]);

  if (!visible) return null;

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return { width: 32, height: 32, borderWidth: 2 };
      case 'large':
        return { width: 64, height: 64, borderWidth: 3 };
      default:
        return { width: 48, height: 48, borderWidth: 2 };
    }
  };


  return (
    <View style={[styles.overlay, { backgroundColor: overlayColor }]}>
      <Animated.View style={[styles.container, { transform: [{ scale: pulseValue }] }]}>
        {/* Modern spinning circle with gradient effect */}
        <Animated.View
          style={[
            styles.spinner,
            getSizeStyles(),
            { 
              borderColor: color,
              borderTopColor: 'transparent',
              borderRightColor: 'transparent',
              transform: [{ rotate: spin }] 
            }
          ]}
        />
        
        {/* Modern animated dots with staggered animation */}
        <View style={styles.dotsContainer}>
          <Animated.View
            style={[
              styles.dot,
              {
                backgroundColor: color,
                opacity: dot1Value,
                transform: [{ scale: dot1Value }]
              }
            ]}
          />
          <Animated.View
            style={[
              styles.dot,
              {
                backgroundColor: color,
                opacity: dot2Value,
                transform: [{ scale: dot2Value }]
              }
            ]}
          />
          <Animated.View
            style={[
              styles.dot,
              {
                backgroundColor: color,
                opacity: dot3Value,
                transform: [{ scale: dot3Value }]
              }
            ]}
          />
        </View>
      </Animated.View>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 0,
    backgroundColor: 'transparent',
  },
  spinner: {
    borderRadius: 50,
    marginBottom: 16,
  },
  dotsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  dot: {
    width: 4,
    height: 4,
    borderRadius: 2,
    marginHorizontal: 2,
  },
});

export default LoadingComponent;
