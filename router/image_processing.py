import cv2
import numpy as np

def processar_imagem(input_imagem):
    # Se for caminho para imagem
    if isinstance(input_imagem, str):
        imagem = cv2.imread(input_imagem, cv2.IMREAD_GRAYSCALE)
        if imagem is None:
            raise ValueError("Falha ao ler a imagem do caminho fornecido")
    # Se já for array da imagem
    elif isinstance(input_imagem, np.ndarray):
        # Verifica se é colorida e converte
        if len(input_imagem.shape) == 3:
            imagem = cv2.cvtColor(input_imagem, cv2.COLOR_BGR2GRAY)
        else:
            imagem = input_imagem
    else:
        raise ValueError("Tipo de entrada inválido para processar_imagem")

    # Binarizar usando Otsu
    _, imagem_bin = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Reduzir ruído
    imagem_suave = cv2.GaussianBlur(imagem_bin, (5, 5), 0)

    return imagem_suave
