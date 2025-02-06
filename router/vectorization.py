import cv2
import numpy as np

def obter_contornos(imagem_bin):
    contornos, _ = cv2.findContours(imagem_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos pequenos (ajuste o valor 100 conforme necessário)
    contornos_filtrados = [c for c in contornos if cv2.contourArea(c) > 100]
    
    # Simplificar contornos
    contornos_simplificados = [cv2.approxPolyDP(c, epsilon=2, closed=True) for c in contornos_filtrados]
    
    return contornos_simplificados