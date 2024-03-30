import { 
  ImageBackground as _ImageBackground,
  Text as _Text,
  View as _View,
  Pressable as _Pressable,
  ScrollView as _ScrollView,
  StyleProp,
  ViewStyle
 } from 'react-native';
import { styled } from 'nativewind';
import { Image as _Image } from 'expo-image';
import { useFonts } from 'expo-font';
import { LinearGradient as _LinearGradient } from 'expo-linear-gradient';
import { colors } from '../../../constants';
import Loading from '../../../components/Loading';

const View = styled(_View)
const Text = styled(_Text)
const Pressable = styled(_Pressable)
const ScrollView = styled(_ScrollView)
const ImageBackground = styled(_ImageBackground)
const LinearGradient = styled(_LinearGradient)

type ClaimableProps = {
  active?: boolean;
  name: string;
  address: string;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
}
const Claimable = ({
  style,
  active,
  name,
  address,
  onPress
}: ClaimableProps) => <View style={style} className={`${active ? 'bg-green' : 'bg-light-green'} w-36 h-36 p-1 px-2 rounded-lg`}>
    <Text className="font-comic text-purple">{active ? 'now' : '2hr ago'}</Text>
    <Text className='font-stretch text-lg leading-5 text-purple'>{name}</Text>
    <Text className="font-comic text-purple leading-4">📍{address}</Text>
    {active ? <Pressable 
      className="bg-purple text-green w-full items-center justify-center p-1 py-2 rounded-full mt-auto mb-2"
      onPress={onPress}
    >
      <Text className="font-comic text-green">CLAIM DONG</Text>
    </Pressable>
      : <View className="w-full items-center justify-center p-1 py-2 mt-auto mb-2">
        <Text className="font-comic text-purple">DONG EXPIRED</Text>
      </View>
    }
  </View>

type DongableProps = {
  name: string;
  dongs?: number;
  style: StyleProp<ViewStyle>;
  onPress: () => void;
}
const Dongable = ({
  name,
  dongs = 0,
  style,
  onPress
}: DongableProps) => <View style={style} className='flex-1 h-36 bg-purple rounded-lg p-2 px-3'>
<Text className='font-stretch text-white text-lg ml-3 leading-5'>
  {name}
</Text>
<View className='flex-row mt-auto mb-2 justify-center items-center space-x-8'>
  <Text className='font-stretch text-light-green text-2xl'>{dongs}</Text>
  <Pressable onPress={onPress} className='p-1 px-2 bg-magenta rounded-full'>
    <Text className='font-comic text-light-green'>{dongs > 0 ? 'DONG' : 'NAAH'}</Text>
  </Pressable>
</View>
</View>

export default function Page() {

  const [fontsLoaded] = useFonts({
    'Stretch Pro': require('../../../assets/fonts/Stretch Pro.otf'),
    'Comic Sans': require('../../../assets/fonts/Comic Sans.ttf')
  });

  if (!fontsLoaded) return <Loading />;

  return <>
    <LinearGradient colors={[colors.pink, colors.cyan]} className="w-full h-16 bg-transparent" />    
    <ImageBackground 
      source={require("../../../assets/bg/pizza.png")}
      imageStyle={{ // TODO: refactor to use NativeWind
        resizeMode: "contain",
        height: 300,
        top: undefined,
        position: 'absolute',
        bottom: 0,
        left: 0
      }}
      className="flex-1 items-start justify-start pt-4 w-full h-full bg-cyan"
    >
      <Text className="ml-8 items-start font-stretch text-lg text-purple">Claimable DDongggs</Text>
      <ScrollView horizontal className="w-full px-8">
        <View className="mt-2 mb-4 flex-row space-x-4">
          <Claimable active name="Neal Patel" address="58A Fulton St." />
          <Claimable name="Neal Patel" address="58A Fulton St." />
        </View>
      </ScrollView>

      <Text className="font-stretch text-lg text-purple ml-8 mb-2">DDongggable</Text>
      <ScrollView className="w-full h-72">
        <View className='w-full px-8'>
          <View className='flex-row space-x-2'>
            <Dongable name="Neal Patel" dongs={5} />
            <Dongable name="Mama" dongs={2} />
          </View>
        </View>
        <View className='mt-2 w-full px-8'>
          <View className='flex-row space-x-2'>
            <Dongable name="Daniel Tao" dongs={2} />
            <Dongable name="Iris Xie" dongs={0} />
          </View>
        </View>
      </ScrollView>
    </ImageBackground>
    <LinearGradient colors={[colors.cyan, colors.green]} className="absolute bottom-0 w-full h-16 bg-transparent" />    
  </>;
}
