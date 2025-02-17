import { StyleSheet, Image, Pressable, Platform, ScrollView, Alert } from 'react-native';
import React, { useState, useEffect, useRef } from 'react';
import { Text, View } from '@/components/Themed';
import * as ImagePicker from 'expo-image-picker';
import lightTheme from '../theme/lightTheme';

export default function MainScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const [gcode, setGcode] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [uploadDone, setUploadDone] = useState(false);
  const [drawingActive, setDrawingActive] = useState(false); // novo estado
  const ws = useRef<WebSocket | null>(null);

  // Função auxiliar para obter o host base do WebSocket
  const getWSHost = () => {
    return Platform.OS === 'android' ? 'ws://10.0.2.2' : 'ws://10.0.0.1';
  };

  const getWebSocketUrl = () => `${getWSHost()}:8765`; // Mesma porta e mesmo servidor para todos

  const getServerUrl = () => {
    if (Platform.OS === 'android') {
      return 'http://192.168.100.2:5000'; // Para emulador Android
    } else if (Platform.OS === 'ios') {
      return 'http://localhost:5000'; // Para iOS
    } else {
      return 'http://127.0.0.1:5000'; // Para web
    }
  };

  useEffect(() => {
    // Solicita permissão da biblioteca de imagens
    (async () => {
      const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (status !== 'granted') {
        alert('Desculpe, precisamos acessar a biblioteca de imagens para funcionar.');
      }
    })();

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
      setGcode(null);
      setProgress(0);
      setUploadDone(false);
    }
  };

  const uploadImage = async () => {
    if (!image) return;

    setLoading(true);
    try {
      const formData = new FormData();
      
      if (Platform.OS === 'web') {
        const response = await fetch(image);
        const blob = await response.blob();
        formData.append('image', blob, 'image.jpg');
      } else {
        // Para dispositivos móveis
        formData.append('image', {
          uri: image,
          type: 'image/jpeg',
          name: 'image.jpg',
        } as any);
      }

      console.log('Enviando para:', `${getServerUrl()}/process_image`);

      const response = await fetch(`${getServerUrl()}/process_image`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${await response.text()}`);
      }
      
      const data = await response.json();
      if (data.simulatedImage) {
        setProcessedImage(data.simulatedImage);
      }
      if (data.gcode) {
        setGcode(data.gcode);
        // Removida a conexão imediata: será feita via botão "Desenhar"
      }
      setUploadDone(true); // marca upload finalizado
    } catch (error) {
      console.error('Erro no upload:', error);
      alert('Erro ao enviar imagem: ' + error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setProcessedImage(null);
    setGcode(null);
    setProgress(0);
    setUploadDone(false);
    setDrawingActive(false);
  };

  // Atualiza a função connectGcodeInterpreter para tratar mensagens via onmessage
  const connectGcodeInterpreter = (gcodePayload: string) => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      alert("WebSocket não está conectado.");
      return;
    }
    ws.current.send(JSON.stringify({ gcode: gcodePayload }));
    ws.current.onmessage = (event) => {
      console.log("Mensagem recebida:", event.data);
      try {
        const data = JSON.parse(event.data);
        if (data.progress !== undefined) setProgress(data.progress);
        if (data.status === "finalizado" || data.status === "cancelado") {
          console.log("status");
          if (ws.current) {
            ws.current.onmessage = null; 
          }
          if (Platform.OS === 'web') {
            window.alert(data.status === "finalizado" ? "Processamento finalizado" : "Processamento cancelado");
            handleReset();
          } else {
            Alert.alert(
              "G-Code",
              data.status === "finalizado" ? "Processamento finalizado" : "Processamento cancelado",
              [{ text: "OK", onPress: handleReset }]
            );
          }
        }
      } catch (error) {
        console.error("Erro ao processar mensagem do websocket:", error);
      }
    };
  };

  // Modifica enviarGcode para não limpar a imagem processada
  const enviarGcode = () => {
    if (gcode) {
      // Removemos a limpeza da imagem processada para manter a imagem da request
      connectGcodeInterpreter(gcode);
      setDrawingActive(true);
    }
  };

  // Nova função para cancelar o desenho
  const cancelarDesenho = () => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      alert("WebSocket não está conectado.");
      return;
    }
    ws.current.send(JSON.stringify({ cancel: true }));
    setDrawingActive(false);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
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
        {/* Exibe "Selecionar Imagem" somente se o upload ainda não foi realizado */}
        {!uploadDone && (
          <Pressable style={styles.button} onPress={pickImage}>
            <Text style={styles.buttonText}>Selecionar Imagem</Text>
          </Pressable>
        )}
        {/* Permanece o botão "Enviar Imagem" até o upload ser concluído */}
        {!uploadDone && (
          <Pressable style={styles.button} onPress={uploadImage} disabled={!image || loading}>
            <Text style={styles.buttonText}>{loading ? 'Enviando...' : 'Enviar Imagem'}</Text>
          </Pressable>
        )}
        {/* Botões de desenhar e cancelar */}
        {uploadDone && gcode && (
          <>
            <Pressable style={[styles.button, drawingActive && styles.buttonDisabled]} onPress={enviarGcode} disabled={drawingActive}>
              <Text style={styles.buttonText}>Desenhar</Text>
            </Pressable>
            {drawingActive && (
              <Pressable style={styles.button} onPress={cancelarDesenho}>
                <Text style={styles.buttonText}>Cancelar</Text>
              </Pressable>
            )}
          </>
        )}
      </View>

      {gcode && (
        <View style={styles.gcodeContainer}>
          <Text style={styles.gcodeTitle}>Interpretação do G-Code:</Text>
          <Text style={styles.gcodeText}>Progresso: {progress.toFixed(0)}%</Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightTheme.background, // forçado para tema claro
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    backgroundColor: lightTheme.headerBackground, // cor do tema claro
    borderBottomWidth: 1,
    borderBottomColor: lightTheme.headerBorder,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: lightTheme.textPrimary,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: lightTheme.headerBackground,
  },
  statusIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  statusText: {
    marginLeft: 5,
    fontSize: 16,
    color: lightTheme.textPrimary,
  },
  imageContainer: {
    width: '70%',
    height: '65%',
    backgroundColor: lightTheme.imageContainer,
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
    backgroundColor: lightTheme.background, // mesmo fundo claro
  },
  button: {
    backgroundColor: lightTheme.button,
    padding: 15,
    borderRadius: 10,
    marginHorizontal: 10,
  },
  buttonText: {
    color: lightTheme.background,
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  gcodeContainer: {
    marginTop: 20,
    paddingHorizontal: 10,
    backgroundColor: lightTheme.background, // forçando fundo claro
  },
  gcodeTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
    color: lightTheme.textPrimary,
  },
  gcodeText: {
    fontSize: 14,
    color: lightTheme.textPrimary,
  },
  buttonDisabled: {
    backgroundColor: lightTheme.buttonDisabled,
  },
});