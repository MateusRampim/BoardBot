import matplotlib.pyplot as plt

def visualizar_trajeto(contornos):
    plt.figure(figsize=(6,6))

    for c in contornos:
        pontos = c.reshape(-1, 2)
        plt.plot(pontos[:, 0], pontos[:, 1], marker="o")

    plt.gca().invert_yaxis()  # Ajustar para coordenadas do plotter
    plt.title("Simulação do Caminho do Plotter")
    plt.show()
