import { useState, useEffect } from 'react';
import {
  Text as _Text,
  View as _View,
  ImageBackground as _ImageBackground,
  ScrollView as _ScrollView,
} from "react-native";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { styled } from "nativewind";
import { useFonts } from "expo-font";
import { router, usePathname } from 'expo-router';
import { LinearGradient as _LinearGradient } from 'expo-linear-gradient';
import { Image as _Image } from 'expo-image';
import { BASE_URL, colors } from '../../../constants';
import Loading from '../../../components/Loading'


const View = styled(_View)
const Text = styled(_Text)
const ScrollView = styled(_ScrollView)
const Image = styled(_Image)
const ImageBackground = styled(_ImageBackground)
const LinearGradient = styled(_LinearGradient)

export default function Leaderboard() {
  const [roomCode, setRoomCode] = useState('');
  const [leaderboard, setLeaderboard] = useState([]);
  const path = usePathname();

  useEffect(
    () => {
      (async () => {
        const roomCode = await AsyncStorage.getItem('room_id');
        if (!roomCode) return router.push('/onboarding');
        setRoomCode(roomCode);

        const res = await fetch(`${BASE_URL}/get_leaderboard?room_id=${roomCode}`);
        const data = await res.json();
        setLeaderboard(data.leaderboard);
      })();
    }
    , [path]);

  const [fontsLoaded] = useFonts({
    'Stretch Pro': require('../../../assets/fonts/Stretch Pro.otf'),
    'Comic Sans': require('../../../assets/fonts/Comic Sans.ttf')
  });

  if (!fontsLoaded) return <Loading />;

  return <>
    <LinearGradient colors={[colors.pink, colors.cyan]} className="w-full h-16 bg-transparent" />
    <ImageBackground
      source={require("../../../assets/bg/hardshell.png")}
      className="bg-cyan w-full h-full items-center justify-start mt-0 space-y-0"
      imageStyle={{ // TODO: refactor to use NativeWind
        resizeMode: "contain",
        height: 200,
        top: 300,
        position: 'absolute',
        bottom: 200,
        left: 0
      }}
    >
      <View className="p-8 items-start w-full -mb-4">
        <Text className="font-stretch text-lg text-purple left">DDonggg LLeadeerboard</Text>
      </View>

      <View className="h-1/4">
        <ScrollView className="flex-col w-full px-8 space-y-2">
          {leaderboard.map((data, i) => (Object.entries(data).map(
            ([key, value]) => (
              <View key={key} className="flex-row items-center justify-center border-solid border-purple border-2 w-full h-16 rounded-full px-8">
                <Text className="font-stretch text-purple mr-8">{i}</Text>
                <Text className="font-stretch text-purple">{key}</Text>
                <Text className="font-stretch text-pink ml-auto">{value as any}</Text>
              </View>
            ))).at(0))}
        </ScrollView>

      </View>
      <View className="h-2/3 justify-center items-center w-full bottom-0 p-16">
        <Text className="font-stretch text-lg text-purple">Group Code</Text>
        <Text className="font-stretch text-4xl text-purple">{Array.from(roomCode).join(`\u200B`)}</Text>
      </View>
    </ImageBackground>
    <LinearGradient colors={['rgba(255,255,255,0)', colors.green]} className="absolute bottom-0 w-full h-16 bg-transparent" />
  </>
}