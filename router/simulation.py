import matplotlib
matplotlib.use('Agg')  # Configura backend não-interativo
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def visualizar_trajeto(contornos):
    plt.figure(figsize=(6,6))
    for c in contornos:
        pontos = c.reshape(-1, 2)
        plt.plot(pontos[:, 0], pontos[:, 1], marker="o")
    plt.gca().invert_yaxis()  
    plt.title("Simulação do Caminho do Plotter")
    plt.show()

def gerar_figura_simulacao(contornos):
    # Cria a figura sem exibir
    plt.figure(figsize=(6,6))
    for c in contornos:
        pontos = c.reshape(-1, 2)
        plt.plot(pontos[:, 0], pontos[:, 1], marker="o")
    plt.gca().invert_yaxis()
    plt.title("Simulação do Caminho do Plotter")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()  # Fecha a figura para liberar memória
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
