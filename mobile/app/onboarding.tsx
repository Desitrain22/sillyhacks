import { useState } from "react";
import { View as _View, Text as _Text, TextInput as _TextInput, Pressable as _Pressable } from "react-native";
import { styled } from "nativewind";
import Loading from '../components/Loading'
import { useFonts } from "expo-font";
import { router } from "expo-router";
import { BASE_URL } from "../constants";
import AsyncStorage from '@react-native-async-storage/async-storage';

type OnboardingStepEnum = 'create_user' | 'join_group' | 'create_group' | 'created' | 'joined'

const View = styled(_View)
const Text = styled(_Text)
const TextInput = styled(_TextInput)
const Pressable = styled(_Pressable)

export default function Page() {
  const [name, setName] = useState('');
  const [nameExists, setNameExists] = useState(false);
  const [groupCode, setGroupCode] = useState('');
  const [groupCodeExists, setGroupCodeExists] = useState(true);
  const [groupName, setGroupName] = useState('');
  const [roomCode, setRoomCode] = useState('');
  const [step, setStep] = useState<OnboardingStepEnum>('join_group');
  const [fontsLoaded] = useFonts({
    'Stretch Pro': require('../assets/fonts/Stretch Pro.otf'),
    'Comic Sans': require('../assets/fonts/Comic Sans.ttf')
  });

  if (!fontsLoaded) return <Loading />

  const JoinGroup = <>
    <Text className="font-stretch text-purple">Join or Create a Group</Text>
    <TextInput
      value={groupCode}
      onChangeText={setGroupCode}
      className="font-comic w-full bg-white p-2 border-solid border-purple border-2 rounded-full my-2"
    />
    {!groupCodeExists && <Text className="font-stretch text-magenta">A group with this code does not exist</Text>}
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={async () => {
        const response = await fetch(`${BASE_URL}/check_room?room_id=${groupCode}`)
        const { room_exists, room_name } = await response.json();
        if (!room_exists) return setGroupCodeExists(false);
        setRoomCode(groupCode);
        setGroupName(room_name);
        await AsyncStorage.setItem('room_id', groupCode);
        await AsyncStorage.setItem('room_name', room_name);
        setStep('joined')
      }}
    >
      <Text className="font-comic text-light-green text-lg">ENTER CODE</Text>
    </Pressable>

    <Pressable
      className="bg-pink w-full items-center justify-center p-1 py-2 rounded-full mt-12"
      onPress={() => setStep('create_group')}
    >
      <Text className="font-comic text-light-green text-lg">CREATE A GROUP</Text>
    </Pressable>
  </>

  const CreateGroup = <>
    <Text className="font-stretch text-purple">Group Name</Text>
    <TextInput
      value={groupName}
      onChangeText={setGroupName}
      className="font-comic w-full bg-white p-2 border-solid border-purple border-2 rounded-full my-2"
    />
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={async () => {
        const response = await fetch(`${BASE_URL}/create_room?name=${groupName}`)
        const data = await response.json();
        setRoomCode(data.room_id);
        await AsyncStorage.setItem('room_id', data.room_id);
        setStep('created')
      }}
    >
      <Text className="font-comic text-light-green text-lg">CREATE</Text>
    </Pressable>
  </>

  const CreateUser = <>
    <Text className="font-stretch text-purple">Hello DDongger.</Text>
    <Text className="font-stretch text-purple">What is your name?</Text>
    <TextInput
      value={name}
      onChangeText={setName}
      className="font-comic w-full bg-white p-2 border-solid border-purple border-2 rounded-full my-2"
    />
    {nameExists && <Text className="font-stretch text-magenta">A user with this name already exists</Text>}
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={async () => {
        try {
          const res = await fetch(`${BASE_URL}/create_user?user_id=${name}&room_id=${roomCode}`)
          await res.json();
          await AsyncStorage.setItem('user_id', name);
          router.push('/authed');
        } catch (e) {
          return setNameExists(true);
        }
      }}
    >
      <Text className="font-comic text-light-green text-lg">ENTER NAME</Text>
    </Pressable>
  </>


  const Joined = <View className="items-center w-full">
    <Text className="font-stretch text-purple">You have joined: </Text>
    <Text className="item-self-center font-stretch text-purple text-6xl my-2">{groupName}</Text>
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={() => setStep('create_user')}
    >
      <Text className="font-comic text-light-green text-lg">START DONGING</Text>
    </Pressable>
  </View>

  const Created = <View className="items-center w-full">
    <Text className="font-stretch text-purple">Here is your group code:</Text>
    <Text className="item-self-center font-stretch text-purple text-6xl my-2">{Array.from(roomCode).join(`\u200B`)}</Text>
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={() => setStep('create_user')}
    >
      <Text className="font-comic text-light-green text-lg">START DONGING</Text>
    </Pressable>
  </View>

  return <View className="w-full h-full flex-1 items-start justify-center bg-cyan p-8">
    {step === 'join_group' && JoinGroup}
    {step === 'create_group' && CreateGroup}
    {step === 'create_user' && CreateUser}
    {step === 'joined' && Joined}
    {step === 'created' && Created}
  </View>
}