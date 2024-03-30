import { useState } from "react";
import { View as _View, Text as _Text, TextInput as _TextInput, Pressable as _Pressable } from "react-native";
import { styled } from "nativewind";
import Loading from '../components/Loading'
import { useFonts } from "expo-font";
import { router, Link } from "expo-router";

type OnboardingStepEnum = 'onboarding' | 'join_group' | 'create_group' | 'joined'

const View = styled(_View)
const Text = styled(_Text)
const TextInput = styled(_TextInput)
const Pressable = styled(_Pressable)

export default function Page() {
  const [name, setName] = useState('');
  const [groupCode, setGroupCode] = useState('');
  const [groupName, setGroupName] = useState('');
  const [step, setStep] = useState<OnboardingStepEnum>('onboarding');
  const [fontsLoaded] = useFonts({
    'Stretch Pro': require('../assets/fonts/Stretch Pro.otf'),
    'Comic Sans': require('../assets/fonts/Comic Sans.ttf')
  });

  if (!fontsLoaded) return <Loading />

  const Onboarding = <>
    <Text className="font-stretch text-purple">Hello DDongger.</Text>
    <Text className="font-stretch text-purple">What is your name?</Text>
    <TextInput
      value={name}
      onChangeText={setName}
      className="font-comic w-full bg-white p-2 border-solid border-purple border-2 rounded-full my-2"
    />
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={() => setStep('join_group')}
    >
      <Text className="font-comic text-light-green text-lg">ENTER NAME</Text>
    </Pressable>
  </>

  const JoinGroup = <>
    <Text className="font-stretch text-purple">Join or Create a Group</Text>
    <TextInput
      value={groupCode}
      onChangeText={setGroupCode}
      className="font-comic w-full bg-white p-2 border-solid border-purple border-2 rounded-full my-2"
    />
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={() => setStep('join_group')}
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
      onPress={() => setStep('joined')}
    >
      <Text className="font-comic text-light-green text-lg">CREATE</Text>
    </Pressable>
  </>

  const Joined = <View className="items-center w-full">
    <Text className="font-stretch text-purple">Here is your group code:</Text>
    <Text className="item-self-center font-stretch text-purple text-6xl my-2">XXXX</Text>
    <Link href='authed' asChild>
    <Pressable
      className="bg-purple w-full items-center justify-center p-1 py-2 rounded-full"
      onPress={() => setStep('joined')}
    >
      <Text className="font-comic text-light-green text-lg">START DONGING</Text>
    </Pressable>
    </Link>
  </View>

  return <View className="w-full h-full flex-1 items-start justify-center bg-cyan p-8">
    {step === 'onboarding' && Onboarding}
    {step === 'join_group' && JoinGroup}
    {step === 'create_group' && CreateGroup}
    {step === 'joined' && Joined}
  </View>
}