import React from 'react';
import {
  StyleSheet,
  Text,
  Pressable,
  Animated,
  ViewStyle,
  TextStyle,
} from 'react-native';

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
          backgroundColor: disabled ? '#6c757d' : '#28a745',
          borderColor: disabled ? '#6c757d' : '#1e7e34',
          shadowColor: disabled ? '#6c757d' : '#28a745',
          pressedColor: '#218838',
        };
      case 'secondary':
        return {
          backgroundColor: disabled ? '#6c757d' : '#6c757d',
          borderColor: disabled ? '#6c757d' : '#5a6268',
          shadowColor: disabled ? '#6c757d' : '#6c757d',
          pressedColor: '#5a6268',
        };
      default: // primary
        return {
          backgroundColor: disabled ? '#6c757d' : '#4A90E2',
          borderColor: disabled ? '#6c757d' : '#357ABD',
          shadowColor: disabled ? '#6c757d' : '#4A90E2',
          pressedColor: '#357ABD',
        };
    }
  };

  const variantStyles = getVariantStyles();

  const backgroundColor = backgroundColorRef.interpolate({
    inputRange: [0, 1],
    outputRange: [variantStyles.backgroundColor, variantStyles.pressedColor],
  });

  const buttonStyles = [
    styles.button,
    {
      backgroundColor: disabled ? variantStyles.backgroundColor : backgroundColor,
      borderColor: variantStyles.borderColor,
      shadowColor: variantStyles.shadowColor,
    },
    style,
  ];

  const textStyles = [
    styles.buttonText,
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
  button: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
    paddingVertical: 12,
    borderRadius: 12,
    borderWidth: 2,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
    minWidth: 200,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '700',
    textAlign: 'center',
  },
  buttonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default Button;
