import cv2
import numpy as np

def processar_imagem(caminho_imagem):
    # Carregar imagem em escala de cinza
    imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

    # Binarizar usando Otsu
    _, imagem_bin = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Reduzir ruído
    imagem_suave = cv2.GaussianBlur(imagem_bin, (5, 5), 0)

    return imagem_suave
