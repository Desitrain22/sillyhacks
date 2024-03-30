import { useEffect } from 'react';
import * as TaskManager from 'expo-task-manager';
import * as Location from 'expo-location';
import { StatusBar } from 'expo-status-bar';
import { Stack } from 'expo-router/stack';

const LOCATION_TASK_NAME = 'background-location-task';

var wsSingleton: WebSocket | null = null;

TaskManager.defineTask<{ locations: Location.LocationObject[] }>(LOCATION_TASK_NAME, ({ data, error }) => {
  if (error) {
    // Error occurred - check `error.message` for more details.
    return;
  }
  if (wsSingleton && data) {
    const { locations } = data;
    for (const location in locations) {
      if (location) {
        console.log(location);
      }
    }
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
