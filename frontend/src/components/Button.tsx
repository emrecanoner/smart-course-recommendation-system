import React from 'react';
import {
  StyleSheet,
  Text,
  Pressable,
  Animated,
  ViewStyle,
  TextStyle,
  Platform,
} from 'react-native';
import { getResponsiveStyles } from '../styles/responsiveStyles';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'success' | 'secondary';
  disabled?: boolean;
  icon?: React.ReactNode;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  disabled = false,
  icon,
  style,
  textStyle,
}) => {
  const backgroundColorRef = new Animated.Value(0);
  const responsiveStyles = getResponsiveStyles();

  const handlePressIn = () => {
    if (!disabled) {
      Animated.timing(backgroundColorRef, {
        toValue: 1,
        duration: 60,
        useNativeDriver: false,
      }).start();
    }
  };

  const handlePressOut = () => {
    if (!disabled) {
      Animated.timing(backgroundColorRef, {
        toValue: 0,
        duration: 60,
        useNativeDriver: false,
      }).start();
    }
  };

  const getVariantStyles = () => {
    switch (variant) {
      case 'success':
        return {
          backgroundColor: disabled ? '#6c757d' : '#10b981', // Bright green
          shadowColor: disabled ? '#6c757d' : '#10b981',
          pressedColor: '#059669',
        };
      case 'secondary':
        return {
          backgroundColor: disabled ? '#6c757d' : '#ef4444', // Bright red
          shadowColor: disabled ? '#6c757d' : '#ef4444',
          pressedColor: '#dc2626',
        };
      default: // primary
        return {
          backgroundColor: disabled ? '#6c757d' : '#3b82f6', // Bright blue
          shadowColor: disabled ? '#6c757d' : '#3b82f6',
          pressedColor: '#2563eb',
        };
    }
  };

  const variantStyles = getVariantStyles();

  const backgroundColor = backgroundColorRef.interpolate({
    inputRange: [0, 1],
    outputRange: [variantStyles.backgroundColor, variantStyles.pressedColor],
  });

  const buttonStyles = [
    responsiveStyles.button,
    {
      backgroundColor: disabled ? variantStyles.backgroundColor : backgroundColor,
      borderWidth: 0,
      shadowColor: variantStyles.shadowColor,
      opacity: disabled ? 0.6 : 1,
    },
    style,
  ];

  const textStyles = [
    responsiveStyles.buttonText,
    { color: disabled ? '#ffffff' : '#ffffff' },
    textStyle,
  ];

  return (
    <Pressable
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={onPress}
      disabled={disabled}
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={title}
    >
      <Animated.View style={buttonStyles}>
        {icon ? (
          <Animated.View style={styles.buttonContent}>
            {icon}
            <Text style={[textStyles, { marginLeft: 8 }]}>{title}</Text>
          </Animated.View>
        ) : (
          <Text style={textStyles}>{title}</Text>
        )}
      </Animated.View>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  buttonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default Button;
