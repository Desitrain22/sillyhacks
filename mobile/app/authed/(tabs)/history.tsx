import { useEffect, useState } from 'react';
import {
  Text as _Text,
  View as _View,
  ImageBackground as _ImageBackground,
  ScrollView as _ScrollView,
} from "react-native";
import { styled } from "nativewind";
import { useFonts } from "expo-font";
import { router, usePathname } from 'expo-router';
import { LinearGradient as _LinearGradient } from 'expo-linear-gradient';
import PieChart from 'react-native-pie-chart'
import AsyncStorage from '@react-native-async-storage/async-storage';
import { BASE_URL, colors, chartColors } from '../../../constants';
import Loading from '../../../components/Loading';

const PIE_CHART_COLORS = Object.values(chartColors);

const View = styled(_View)
const Text = styled(_Text)
const ScrollView = styled(_ScrollView)

const ImageBackground = styled(_ImageBackground)
const LinearGradient = styled(_LinearGradient)

// Generate random hex color
const generateRandomHexColor = () => {
  return `#${Math.floor(Math.random() * 16777215).toString(16)}`
}

export default function History() {
  const [userId, setUserId] = useState('');
  const [roomCode, setRoomCode] = useState('');
  const [count, setCount] = useState<number>(0);
  const [history, setHistory] = useState<any[]>([]);

  const [fontsLoaded] = useFonts({
    'Stretch Pro': require('../../../assets/fonts/Stretch Pro.otf'),
    'Comic Sans': require('../../../assets/fonts/Comic Sans.ttf')
  });

  const path = usePathname();
  useEffect(
    () => {
      (async () => {
        const roomCode = await AsyncStorage.getItem('room_id');
        if (!roomCode) return router.push('/onboarding');
        setRoomCode(roomCode);

        const userId = await AsyncStorage.getItem('user_id')
        if (!userId) return router.push('/onboarding');
        setUserId(userId);

        const unloadableRes = await fetch(`${BASE_URL}/get_total_unloadable?room_id=${roomCode}&user_id=${userId}`);
        const unloadableData = await unloadableRes.json();
        setCount(unloadableData.dongs_unloadable);

        const dongHistory = await fetch(`${BASE_URL}/get_dong_history?room_id=${roomCode}&user_id=${userId}`);
        const dongHistoryData = await dongHistory.json();
        setHistory(dongHistoryData.dongs);
      })();
    }
    , [path])

  if (!fontsLoaded) return <Loading />;

  const series = [123, 321, 123, 789, 537]
  const seriesColors = series.map((_, i) => PIE_CHART_COLORS[i % PIE_CHART_COLORS.length])

  return <>
    <LinearGradient colors={[colors.pink, colors.cyan]} className="w-screen h-16 bg-transparent" />
    <View className="bg-cyan w-full h-full flex items-center justify-start mt-0">
      <ImageBackground
        className="w-screen"
        source={require("../../../assets/bg/crunchwrap.png")}
        imageStyle={{ // TODO: refactor to use NativeWind
          resizeMode: "contain",
          position: 'absolute',
          height: 150,
          top: 0,
          left: "40%",
          bottom: undefined
        }}
      >
        <View className="w-screen flex items-center justify-center pt-4">
          <Text className="font-stretch text-lg text-purple leading-5">You Have</Text>
          <Text className="font-stretch text-7xl text-purple">{count}</Text>
          <Text className="font-stretch text-lg text-purple leading-5">DDongggs to Unload</Text>
        </View>
      </ImageBackground>

      <View className="p-8 items-start w-full">
        <Text className="font-stretch text-lg text-purple left">DDonggg Distribution</Text>
      </View>
      <View className="flex-row justify-center items-center space-x-8">
        <PieChart widthAndHeight={120} series={series} sliceColor={seriesColors} coverRadius={0.45} />
        <View className="flex-col space-y-2">
          {seriesColors.map((color, i) =>
            <View key={`${color}-${i}`} className="flex-row items-center">
              <View key={i} className="w-4 h-4 mr-2" style={{ backgroundColor: color }} />
              <Text className="font-stretch text-xs text-purple">Neal Patel</Text>
            </View>)}
        </View>
      </View>

      <View className="p-8 items-start w-full -mb-4">
        <Text className="font-stretch text-lg text-purple left">DDonggg History</Text>
      </View>

      <View className="h-1/4">
        <ScrollView className="flex-col w-full px-2 space-y-2">
          {history.map(({
            dongee,
            dong_time,
            location
          }) => <View className="flex-row items-center justify-center border-solid border-purple border-2 w-full h-16 rounded-full px-8">
            <Text className="font-comic text-xs text-purple mr-4">{dong_time}</Text>
            <Text className="font-stretch text-xs text-purple">{dongee}</Text>
            <Text className="font-stretch text-xs text-pink ml-auto">📍{location}</Text>
          </View>)}
        </ScrollView>
      </View>
    </View>
    <LinearGradient colors={['rgba(255,255,255,0)', colors.green]} className="absolute bottom-0 w-full h-16 bg-transparent" />
  </>
}