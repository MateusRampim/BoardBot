from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import traceback
import simulation
import image_processing
import vectorization
import optimization
import gcode_generator
import base64

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"]
    }
})

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['image']
        file_bytes = file.read()
        max_size = 10 * 1024 * 1024  # 10MB
        if len(file_bytes) > max_size:
            return jsonify({'error': 'Arquivo muito grande'}), 413

        npimg = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'error': 'Falha ao decodificar a imagem'}), 400

        # Executa o fluxo de processamento utilizando a imagem enviada
        imagem_bin = image_processing.processar_imagem(img)  # Função adaptada para aceitar o array da imagem
        contornos = vectorization.obter_contornos(imagem_bin)
        contornos_otimizados = optimization.otimizar_caminho(contornos)
        gcode = gcode_generator.gerar_gcode(contornos_otimizados)
        simulation_image = simulation.gerar_figura_simulacao(contornos_otimizados)

        return jsonify({
            'simulatedImage': f'data:image/png;base64,{simulation_image}',
            'gcode': gcode
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)