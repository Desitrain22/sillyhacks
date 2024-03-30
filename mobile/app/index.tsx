import { View as _View, Text as _Text, Pressable as _Pressable } from "react-native";
import { Image as _Image } from "expo-image";
import { Link as _Link } from "expo-router";
import { styled } from "nativewind"

const Image = styled(_Image)
const Pressable = styled(_Pressable)
const Link = styled(_Link)

export default function Loader() {
  return <Link href='/onboarding' asChild>
    <Pressable className="bg-purple w-screen h-screen flex-col items-center justify-center p-8 m-0">
      <Image className="w-full h-24" contentFit='contain' source={require("../assets/donger/yellow.svg")} />
      <Image className="w-full h-24" contentFit='contain' source={require("../assets/donger/pink.svg")} />
      <Image className="w-full h-24" contentFit='contain' source={require("../assets/donger/cyan.svg")} />
    </Pressable>
  </Link>
}