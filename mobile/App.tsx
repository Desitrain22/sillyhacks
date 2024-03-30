import { useEffect } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useFonts } from 'expo-font';
import * as TaskManager from 'expo-task-manager';
import * as Location from 'expo-location';
import { StatusBar } from 'expo-status-bar';

const LOCATION_TASK_NAME = 'background-location-task';

TaskManager.defineTask<{ locations: Location.LocationObject[] }>(LOCATION_TASK_NAME, ({ data, error }) => {
  if (error) {
    // Error occurred - check `error.message` for more details.
    return;
  }
  if (data) {
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
  const [fontsLoaded] = useFonts({
    'StretchPro': require('./assets/fonts/StretchPro.otf'),
  });

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


  return (
    <View style={styles.container}>
      <Text>wtf are we even going to silly hacks for? to give labor for some bitch to call us cringe? to find out that we are unfunny and bitchless and in my moms basement? miss me with that. i am funny. i am funny.</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
