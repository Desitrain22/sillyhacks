import { useEffect, useState } from 'react';
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
import { router, usePathname } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { LinearGradient as _LinearGradient } from 'expo-linear-gradient';
import { BASE_URL, colors } from '../../../constants';
import Loading from '../../../components/Loading';

const View = styled(_View)
const Text = styled(_Text)
const Pressable = styled(_Pressable)
const ScrollView = styled(_ScrollView)
const ImageBackground = styled(_ImageBackground)
const LinearGradient = styled(_LinearGradient)

const chunks = (a: any[], size: number) =>
  Array.from(
    new Array(Math.ceil(a.length / size)),
    (_, i) => a.slice(i * size, i * size + size)
  );

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
    <Text className="font-comic text-purple">{active ? 'now' : 'expired'}</Text>
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
  const [userId, setUserId] = useState('');
  const [roomCode, setRoomCode] = useState('');
  const [dongable, setDongable] = useState<any[]>([]);
  const [dongCounter, setDongCounter] = useState<{ [key: string]: number }>({});

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

        const dongableRes = await fetch(`${BASE_URL}/get_users_status_for_room?room_id=${roomCode}`);
        const dongableData = await dongableRes.json();
        setDongable(dongableData.dongable);

        const dongCounterRes = await fetch(`${BASE_URL}/get_loaded_dongs?room_id=${roomCode}&user_id=${userId}`);
        const dongCounterData = await dongCounterRes.json();
        setDongCounter(dongCounterData);
      })();
    }
    , [path])

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
      {dongable.length > 0 && <>
        <Text className="ml-8 items-start font-stretch text-lg text-purple">Claimable DDongggs</Text>
        <ScrollView horizontal className="w-full px-8 -mb-16">
          <View className="mt-2 mb-4 flex-row space-x-4">
            {dongable.map(({ user_id, location, can_dong }, i) => <Claimable
              name={user_id}
              address={location}
              active={can_dong}
              key={user_id}
              onPress={async () => {
                try {
                  const res = await fetch(`${BASE_URL}/dong_by_api?room_id=${roomCode}&donger=${userId}&dongee=${user_id}&dong_type=1&location_id=1`);
                  await res.json();
                  dongable[i].can_dong = false;
                  setDongable([...dongable]);
                } catch (e) {
                  console.error(e);
                }
              }}
            />)}
          </View>
        </ScrollView>
      </>
      }

      <Text className="font-stretch text-lg text-purple ml-8 mb-2 -mt-4">DDongggable</Text>
      <ScrollView className="w-full h-72">
        {chunks(Object.entries(dongCounter), 2).map(([entry1, entry2], i) => {
          const [name1, dongs1] = entry1
          const [name2, dongs2] = entry2 ?? []
          return <View className={`${i === 0 ? '' : 'mt-2'} w-full px-8`}>
            <View key={`${name1} ${name2}`} className='flex-row space-x-2'>
              <Dongable
                onPress={(dongs1 > 0) ? async () => {
                  try {
                    const res = await fetch(`${BASE_URL}/dong_by_api?room_id=${roomCode}&donger=${userId}&dongee=${name1}&dong_type=-1&location_id=1`);
                    await res.json();
                    setDongCounter({ ...dongCounter, [name1]: dongs1 - 1 })
                  } catch (e) {
                    console.log(e)
                  }
                } : () => {}}
                name={name1}
                dongs={dongs1}
              />
              {name2 && <Dongable
                onPress={(dongs2 > 0) ? async () => {
                  try {
                    const res = await fetch(`${BASE_URL}/dong_by_api?room_id=${roomCode}&donger=${userId}&dongee=${name2}&dong_type=-1`);
                    await res.json();
                    setDongCounter({ ...dongCounter, [name2]: dongs2 - 1 })
                  } catch (e) {
                    console.log(e)
                  }
                } : () => {}}
                name={name2}
                dongs={dongs2}
              />}
            </View>
          </View>
        })}
      </ScrollView>
    </ImageBackground>
    <LinearGradient colors={['rgba(255,255,255,0)', colors.green]} className="absolute bottom-0 w-full h-16 bg-transparent" />
  </>;
}
