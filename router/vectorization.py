import cv2
import numpy as np

def obter_contornos(imagem_bin):
    contornos, _ = cv2.findContours(imagem_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos pequenos (ajuste o valor 100 conforme necessário)
    contornos_filtrados = [c for c in contornos if cv2.contourArea(c) > 100]

    # Simplificar contornos
    contornos_simplificados = [cv2.approxPolyDP(c, epsilon=2, closed=True) for c in contornos_filtrados]

    # Fecha contornos
    contornos_fechados = [np.vstack([c, np.array([c[0]])]) for c in contornos_simplificados]

    # Normaliza contornos para a área de desenho
    width = 300
    height = 250
    max_x = max([max(c.reshape(-1, 2)[:,0]) for c in contornos_fechados])
    max_y = max([max(c.reshape(-1, 2)[:,1]) for c in contornos_fechados])
    contornos_normalizados = [np.array([[[p[0][0]*width/max_x, p[0][1]*height/max_y]] for p in c]) for c in contornos_fechados]

    print(contornos_fechados[0])
    print(contornos_normalizados[0])

    return contornos_normalizados
