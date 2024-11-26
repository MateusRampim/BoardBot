import { StyleSheet, Image, Pressable, Platform } from 'react-native';
import React, { useState, useEffect, useRef } from 'react';
import { Text, View } from '@/components/Themed';
import * as ImagePicker from 'expo-image-picker';

export default function TabOneScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  const getWebSocketUrl = () => {
    if (Platform.OS === 'android') {
      return 'ws://10.0.2.2:8777'; // Para emulador Android
    }
    return 'ws://localhost:8777'; // Para web/iOS
  };

  useEffect(() => {
    const connectWebSocket = () => {
      if (ws.current && ws.current.readyState !== WebSocket.CLOSED) return;

      ws.current = new WebSocket(getWebSocketUrl());
      ws.current.onopen = () => setConnected(true);
      ws.current.onclose = () => {
        setConnected(false);
        ws.current = null;
      };
    };

    connectWebSocket();
  }, [connected]);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
      setProcessedImage(null);
    }
  };

  const uploadImage = async () => {
    if (!image) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: image,
        type: 'image/jpeg',
        name: 'upload.jpg',
      } as any);

      const response = await fetch('http://localhost:5000/process_image', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.processedImage) {
        setProcessedImage(data.processedImage);
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>BoardBot</Text>
        <View style={styles.statusContainer}>
          <View style={[styles.statusIndicator, { backgroundColor: connected ? 'green' : 'gray' }]} />
          <Text style={styles.statusText}>{connected ? 'Conectado' : 'Desconectado'}</Text>
        </View>
      </View>

      <View style={styles.imageContainer}>
        {processedImage ? (
          <Image source={{ uri: processedImage }} style={styles.preview} />
        ) : image ? (
          <Image source={{ uri: image }} style={styles.preview} />
        ) : null}
      </View>

      <View style={styles.buttonContainer}>
        <Pressable style={styles.button} onPress={pickImage}>
          <Text style={styles.buttonText}>Selecionar Imagem</Text>
        </Pressable>
        <Pressable style={styles.button} onPress={uploadImage} disabled={!image || loading}>
          <Text style={styles.buttonText}>{loading ? 'Enviando...' : 'Enviar Imagem'}</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    backgroundColor: '#f8f9fa',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  statusText: {
    marginLeft: 5,
    fontSize: 16,
  },
  imageContainer: {
    width: '70%',
    height: '65%',
    backgroundColor: '#E0E0E0',
    borderRadius: 20,
    borderWidth: 20,
    borderColor: '#fff',
    alignSelf: 'center',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 20,
  },
  preview: {
    width: '100%',
    height: '100%',
    borderRadius: 20,
    resizeMode: 'contain',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    marginHorizontal: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});
