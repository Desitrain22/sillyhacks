import { useEffect } from 'react';
import * as TaskManager from 'expo-task-manager';
import * as Location from 'expo-location';
import { StatusBar } from 'expo-status-bar';
import { Stack } from 'expo-router/stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { BASE_URL } from '../../constants';

const LOCATION_TASK_NAME = 'background-location-task';

TaskManager.defineTask<{ locations: Location.LocationObject[] }>(LOCATION_TASK_NAME, async ({ data, error }) => {
  if (error) {
    // Error occurred - check `error.message` for more details.
    return;
  }
  if (data) {
    const { locations } = data;
    const userId = await AsyncStorage.getItem('user_id');
    const roomCode = await AsyncStorage.getItem('room_id');
    await Promise.allSettled(locations.map((location) => {
      const { latitude, longitude } = location.coords;
      return fetch(`${BASE_URL}/check_if_at_bell?user_id=${userId}&lat=${latitude}&lon=${longitude}&room_id=${roomCode}`)
    }));
    // do something with the locations captured in the background
  }
});


export default function App() {
  useEffect(() => {
    (async () => {
      const { status: foregroundStatus } = await Location.requestForegroundPermissionsAsync();
      if (foregroundStatus === 'granted') {
        const { status: backgroundStatus } = await Location.requestBackgroundPermissionsAsync();
        if (backgroundStatus === 'granted') {
          await Location.startLocationUpdatesAsync(LOCATION_TASK_NAME, {
            accuracy: Location.Accuracy.High,
          });
        }
      }
    })();
  }, []);

  return <>
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
    <StatusBar />
  </>;
}
