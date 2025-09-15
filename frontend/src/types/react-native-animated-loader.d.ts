declare module 'react-native-animated-loader' {
  import { Component } from 'react';
  import { ViewStyle } from 'react-native';

  interface AnimatedLoaderProps {
    visible?: boolean;
    overlayColor?: string;
    source?: any;
    animationStyle?: ViewStyle;
    animationType?: string;
    speed?: number;
    loop?: boolean;
    children?: React.ReactNode;
  }

  export default class AnimatedLoader extends Component<AnimatedLoaderProps> {}
}
