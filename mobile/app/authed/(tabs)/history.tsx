import {
  Text as _Text,
  View as _View,
  ImageBackground as _ImageBackground,
  ScrollView as _ScrollView,
} from "react-native";
import { styled } from "nativewind";
import { useFonts } from "expo-font";
import { LinearGradient as _LinearGradient } from 'expo-linear-gradient';
import PieChart from 'react-native-pie-chart'
import { colors, chartColors } from '../../../constants';
import Loading from '../../../components/Loading';

const PIE_CHART_COLORS = Object.values(chartColors);

const View = styled(_View)
const Text = styled(_Text)
const ScrollView = styled(_ScrollView)

const ImageBackground = styled(_ImageBackground)
const LinearGradient = styled(_LinearGradient)

export default function History() {
  const [fontsLoaded] = useFonts({
    'Stretch Pro': require('../../../assets/fonts/Stretch Pro.otf'),
    'Comic Sans': require('../../../assets/fonts/Comic Sans.ttf')
  });

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
          <Text className="font-stretch text-7xl text-purple">12</Text>
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
          <View className="flex-row items-center justify-center border-solid border-purple border-2 w-full h-16 rounded-full px-8">
            <Text className="font-comic text-xs text-purple mr-4">Monday</Text>
            <Text className="font-stretch text-xs text-purple">Neal Patel</Text>
            <Text className="font-stretch text-xs text-pink ml-auto">📍58A Fulton St.</Text>
          </View>
          <View className="flex-row items-center justify-center border-solid border-purple border-2 w-full h-16 rounded-full px-8">
            <Text className="font-comic text-xs text-purple mr-4">Tuesday</Text>
            <Text className="font-stretch text-xs text-purple">Neal Patel</Text>
            <Text className="font-stretch text-xs text-pink ml-auto">📍58A Fulton St.</Text>
          </View>
          <View className="flex-row items-center justify-center border-solid border-purple border-2 w-full h-16 rounded-full px-8">
            <Text className="font-comic text-xs text-purple mr-4">Sunday</Text>
            <Text className="font-stretch text-xs text-purple">Neal Patel</Text>
            <Text className="font-stretch text-xs text-pink ml-auto">📍58A Fulton St.</Text>
          </View>
        </ScrollView>
      </View>
    </View>
    <LinearGradient colors={[colors.cyan, colors.green]} className="absolute bottom-0 w-full h-16 bg-transparent" />
  </>
}