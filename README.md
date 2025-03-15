# 🤖 BoardBot

BoardBot é uma aplicação multiplataforma super legal que transforma suas imagens em desenhos físicos através de um robô plotter. Uma verdadeira mágica digital! 🎨 A interface é super amigável e permite selecionar imagens, visualizar o resultado processado e acompanhar seu desenho ganhando vida em tempo real.

## ✨ Funcionalidades

- 📱 Seleção de imagens da galeria do seu dispositivo usando expo-image-picker
- 📤 Upload e processamento de imagens para transformá-las em traços artísticos
- 👁️ Visualização prévia da imagem processada antes do desenho (pra você não ter surpresas!)
- 🤖 Geração automática de G-code para controle do robô plotter
- 🔌 Interface de status mostrando a conexão com o servidor
- 🎮 Controles fáceis para iniciar e cancelar o processo de desenho
- 📊 Monitoramento em tempo real do progresso (0-100%) - fique de olho enquanto a mágica acontece!
- 📡 Comunicação via WebSocket para instruções em tempo real
- 📱 Funciona em qualquer lugar: Web, iOS e Android (com URLs específicas para cada um)

## 🖼️ Interface do Usuário

- **Cabeçalho**: Título da aplicação e indicador de status de conexão (verde = tudo certo! 👍)
- **Visualização de Imagem**: Veja a transformação da sua foto em obra de arte
- **Controles**:
  - 📸 Botão para selecionar imagem da galeria (escolha sua obra-prima!)
  - 📤 Botão para enviar e processar a imagem (deixa com a gente!)
  - ▶️ Botão para iniciar o desenho após processamento (hora da verdade!)
  - ⏹️ Botão para cancelar o desenho em andamento (ops, mudei de ideia!)
- **Monitor de Progresso**: Acompanhe cada percentual enquanto seu desenho ganha vida

## 🧠 Processo de Vetorização

Nosso sistema usa um pipeline de processamento super esperto para transformar suas imagens em instruções de desenho (é quase mágica! ✨):

1. **Processamento de Imagem** (`image_processing.py`) 🖼️
   - Conversão para escala de cinza
   - Binarização usando o algoritmo de Otsu
   - Redução de ruídos com filtro gaussiano (adeus, imperfeições!)

2. **Extração de Contornos** (`vectorization.py`) ✏️
   - Identificação dos contornos na imagem binária
   - Vetorização das bordas identificadas

3. **Otimização de Caminho** (`optimization.py`) 🧩
   - Utilização de algoritmos de grafo para resolver o problema do caixeiro viajante (TSP)
   - Minimização da distância total percorrida pelo robô (economizando tempo e energia!)
   - Reordenação inteligente dos traços para maior eficiência (nosso robô é esperto!)

4. **Geração de G-code** (`gcode_generator.py`) 💾
   - Conversão dos contornos vetorizados em instruções G-code compatíveis
   - Comandos para controle preciso de movimentação (X, Y)
   - Controle de posicionamento da ferramenta (Z) para levantar/abaixar a caneta

5. **Simulação Visual** (`simulation.py`) 🔍
   - Geração de uma prévia do resultado final (para você não ter surpresas)
   - Visualização do caminho otimizado que o robô irá percorrer

6. **API REST** (`Http_server.py`) 🌐
   - Interface para upload de imagens (até 10MB - cuidado com aquelas fotos de férias gigantes!)
   - Processamento backend das imagens enviadas
   - Retorno da visualização e G-code prontos para execução

Esta abordagem garante que até as imagens mais complexas sejam convertidas em traços precisos e otimizados para um desenho eficiente pelo nosso pequeno artista robótico! 🎨

## ⚙️ Configuração de Hardware

### Pinos do Raspberry Pi utilizados
- **Motor da Correia 1 (Belt0)**: 🔄
  - Pino STEP: GPIO 14
  - Pino DIR: GPIO 15
- **Motor da Correia 2 (Belt1)**: 🔄
  - Pino STEP: GPIO 3
  - Pino DIR: GPIO 2
- **Servo da Caneta (Pen)**: ✏️
  - Pino de Sinal: GPIO 27

### Especificações mecânicas
- Área de desenho: 540mm x 350mm (espaço suficiente para sua obra-prima!)
- Precisão do passo: 0.2mm por passo (detalhe é tudo!)
- Posição de elevação da caneta: 200 (servo)
- Posição de contato da caneta: 110 (servo)

## 🤖 Interpretação do G-code

O BoardBot usa um interpretador de G-code simplificado (mas poderoso!) via WebSocket que entende os seguintes comandos:

### Comandos suportados:
- **G0**: Movimento rápido (modo "estou só passeando") 🚶
  - `G0 X[valor] Y[valor]`: Move para a posição especificada
  - `G0 Z[valor]`: Controla a posição da caneta
    - Z < 1: Pressiona a caneta contra a superfície (hora de desenhar!)
    - Z >= 1: Levanta a caneta da superfície (pausa dramática!)

- **G1**: Movimento linear (modo "estou desenhando agora") ✏️
  - `G1 X[valor] Y[valor]`: Desenha uma linha até a posição especificada

### Processo de execução:
1. O cliente envia o código G-code completo via WebSocket
2. O servidor processa linha por linha sequencialmente (paciência é uma virtude!)
3. Para cada movimento, as coordenadas cartesianas são convertidas para coordenadas polares (matemágica!)
4. Os dois motores de passo são acionados simultaneamente para mover o mecanismo
5. O progresso é reportado em tempo real de volta ao cliente (para você não ficar ansioso!)
6. O processo pode ser cancelado a qualquer momento enviando um comando de cancelamento (mudou de ideia? Sem problemas!)

### Sistema de coordenadas:
- Origem (0,0): Canto inferior esquerdo da área de desenho
- Eixo X: Horizontal (direita positivo)
- Eixo Y: Vertical (cima positivo)
- Unidade: milímetros (mm)

## 📋 Requisitos

- Node.js e npm/yarn (os básicos!)
- Expo CLI para desenvolvimento mobile (super fácil de usar!)
- Servidor Python backend (porta 5000)
- Servidor WebSocket (porta 8765)
- Configuração do robô plotter compatível com G-code
- Raspberry Pi com GPIO configurado (nosso pequeno cérebro eletrônico!)

## 🚀 Como Usar

1. Inicie o servidor backend Python e o servidor WebSocket (ligue os motores!)
2. Inicie a aplicação web/mobile (escolha sua plataforma favorita!)
3. Selecione uma imagem da galeria (as melhores, por favor!)
4. Envie a imagem para processamento (e deixe a mágica começar!)
5. Visualize a prévia do resultado (parece bom? Então vamos lá!)
6. Clique em "Desenhar" para iniciar o processo (mãos à obra!)
7. Monitore o progresso do desenho (e prepare-se para se impressionar!)

## 👨‍💻 Desenvolvimento

### 🚀 Inicializando o Sistema

Para que a mágica aconteça, você precisa iniciar os serviços antes do frontend:

1. **No seu computador**: Inicie o servidor de roteamento (nosso maestro das comunicações!)
   ```bash
   python router/websocket_server.py
   ```

2. **No Raspberry Pi**: Inicie o controlador do motor (nosso domador de robôs! 🤖)
   ```bash
   python motor_controller/gcode_websocket.py
   ```

3. **Ou use nosso script conveniente** (só se ambos os serviços estiverem no mesmo dispositivo):
   ```bash
   python start_router_motor_servers.py
   ```

> ⚠️ **Atenção, humano!** O controlador do motor (gcode_websocket.py) deve ser executado no Raspberry Pi que está conectado aos motores de passo e ao servo. Se tentar executá-lo no seu computador, você vai ficar olhando para a tela esperando um robô que não existe! 🙃

### 🖥️ Iniciando o Frontend

Depois que os servidores estiverem funcionando e dançando felizes juntos:

```bash
# Instalar dependências 
npm install

# Iniciar em desenvolvimento
npm start
```

Para diferentes plataformas (escolha seu veneno! 😉):
- Web: `npm run web`
- iOS: `npm run ios` 
- Android: `npm run android`

Agora sim! Frontend e backend trabalhando juntos como numa orquestra perfeita! 🎵

## 🔧 Detalhes Técnicos

- Frontend desenvolvido com React Native (v0.76.2) e Expo (v52.0.8) - stack moderna e poderosa!
- Interface adaptativa para diferentes plataformas (web/mobile)
- Comunicação em tempo real via WebSocket (porta 8765)
- API REST para processamento de imagens (porta 5000)
- Configurações de URL específicas para cada plataforma (Android/iOS/Web)
- Temas visuais consistentes (usando lightTheme - bonito e clean!)
- Sistema de notificações adaptado por plataforma (Alert no mobile, window.alert no web)
- Tratamento assíncrono para upload e processamento de imagens
- Gerenciamento de estado do processamento com indicadores visuais
- Controle completo do fluxo de desenho com opção de cancelamento

## 📚 Dependências Principais

- React (v18.3.1) e React Native (v0.76.2) - o dinâmico duo!
- Expo Framework (v52.0.8) - facilitando nossas vidas!
- expo-image-picker: Para seleção de imagens da galeria
- expo-router: Para navegação entre telas
- react-native-reanimated: Para animações fluidas (suave como manteiga!)
- WebSocket API: Para comunicação em tempo real
- Servidor Python backend personalizado
- Bibliotecas Python: NumPy, OpenCV, NetworkX, SciPy (o esquadrão da ciência de dados!)
- RpiMotorLib para controle de motores de passo e servo
