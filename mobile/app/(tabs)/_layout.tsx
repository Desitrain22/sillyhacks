import React from 'react';
import { Animated, StyleProp, ViewStyle, View as _View } from 'react-native';
import { styled } from 'nativewind';
import { Tabs as Tabs } from 'expo-router';
import { Image as _Image } from 'expo-image';

const View = styled(_View)
const Image = styled(_Image)

type TabsProps = React.ComponentProps<typeof Tabs>
type TabBarStyle = Animated.WithAnimatedValue<StyleProp<ViewStyle>>;
function _Tabs({ style, children, screenOptions, ...props }: TabsProps & { style?: TabBarStyle }) {
  return <Tabs screenOptions={{
    tabBarStyle: style,
    ...screenOptions,
  }} {...props}>
    {children}
  </Tabs>
}

const StyledTabs = styled(_Tabs);

export default function TabLayout() {
  return (
    <>
      <StyledTabs
        className="bg-green -mb-4 mt-0"
        screenOptions={{ headerShown: false }}
      >
        <Tabs.Screen
          name="history"
          options={{
            title: '',
            tabBarIcon: ({ focused }) => <View className="w-full h-full flex-row items-center justify-center">
              <Image style={{
                width: 242.45 / 3,
                height: 195.93 / 3,
                marginBottom: -17
              }} source={focused ? require("../../assets/nav/inventory_active.svg") : require("../../assets/nav/inventory.svg")} />
            </View>,
          }}
        />
        <Tabs.Screen
          name="index"
          options={{
            title: '',
            tabBarIcon: ({ focused }) => <View className="w-full h-full flex-row items-center justify-center">
              <Image style={{
                width: 151.57 / 3,
                height: 148.24 / 3,
              }} source={focused ? require("../../assets/nav/home_active.svg") : require("../../assets/nav/home.svg")} />
            </View>,
          }}
        />
        <Tabs.Screen
          name="leaderboard"
          options={{
            title: '',
            tabBarIcon: ({ focused }) => <View className="w-full h-full flex-row items-center justify-center">
              <Image style={{
                width: 337.46 / 3,
                height: 152.05 / 3,
              }} source={focused ? require("../../assets/nav/leaderboard_active.svg") : require("../../assets/nav/leaderboard.svg")} />
            </View>,
          }}
        />
      </StyledTabs>
      <View className="w-full bg-green">
      <View className="h-16 w-1/3 mx-auto">
        <Image className="w-full h-full" contentFit='contain' source={require("../../assets/logo.svg")} />
      </View>
      </View>
    </>
  );
}
