import { View as _View, Text as _Text } from "react-native";
import { Image as _Image } from "expo-image";
import { styled } from "nativewind"

const View = styled(_View)
const Image = styled(_Image)

export default function Loader() {
  return <View className="bg-pink w-full h-full flex-col items-center justify-start p-8">
    <Image className="w-full h-full" contentFit='contain' source={require("../assets/loading_logo.svg")} />
  </View>
}
