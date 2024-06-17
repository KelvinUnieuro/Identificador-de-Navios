import cv2 as cv
import numpy as np
# import time
import os

add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"C:\temp\vips-dev-w64-all-8.15.2\vips-dev-8.15\bin"  # LibVIPS binary dir
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:   
    os.environ["PATH"] = os.pathsep.join((vipsbin, os.environ["PATH"]))

import pyvips

num_boats = 0

# Pegando a imagem
# imagem = cv.imread('main-project/assets/varios-barco18.tiff')
imagem = pyvips.Image.new_from_file('main-project/assets/varios-barco18.tiff')

# Ajustando quantas partes a imagem terá e qual será a altura e largura de cada uma
largura, altura = imagem.width, imagem.height
num_partes = 2
parte_largura = largura // num_partes
parte_altura = altura // num_partes 

# Para carregar o arquivo xml já treinado
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

for i in range(num_partes):
    linha_imagem = None
    for j in range(num_partes):
        # Define as coordenadas de recorte para esta parte
        x1 = i * parte_largura
        y1 = j * parte_altura
        x2 = x1 + parte_largura
        y2 = y1 + parte_altura

        # Recorta a parte da imagem
        parte_imagem = imagem.crop(x1, y1, parte_largura, parte_altura)

        # Converte a parte da imagem para numpy array para usar com OpenCV
        parte_np = np.ndarray(buffer=parte_imagem.write_to_memory(),
                               dtype=np.uint8,
                               shape=[parte_altura, parte_largura, 3])

        # Converte para BGR (OpenCV usa BGR por padrão)
        parte_np = cv.cvtColor(parte_np, cv.COLOR_RGB2BGR)

        # Para carregar o arquivo xml já treinado
        carregaAlgoritmo = cv.CascadeClassifier(
            'main-project/haarcascades/first_cascade.xml')

        # Deixando a imagem cinza para maior eficiência do opencv
        imagemCinza = cv.cvtColor(parte_np, cv.COLOR_BGR2GRAY)

        # Detecta os barcos na parte da imagem
        boats = carregaAlgoritmo.detectMultiScale(imagemCinza,
                                                  scaleFactor=1.4,
                                                  minNeighbors=14,
                                                  minSize=(150, 150),
                                                  maxSize=(250, 250))

        # Desenha retângulos nos barcos detectados
        for (x, y, l, a) in boats:
            cv.rectangle(parte_np, (x, y), (x + l, y + a), (0, 255, 0), 2)
            cv.rectangle(parte_np, (x, y), (x + l, y + a), (0, 255, 0), 5)
            num_boats += 1  # Incrementa o contador de barcos

        # Salva a parte da imagem com os barcos detectados
        cv.imwrite(f'parte_{i}_{j}.jpg', parte_np)
        
print(f'Número total de barcos detectados: {num_boats}')



# Deixando a imagem cinza para maior eficiência do opencv
# if imagem is None:
#     print("Erro ao carregar a imagem")
# else:
#     imagemCinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

# boats = carregaAlgoritmo.detectMultiScale(imagemCinza,
#                                           scaleFactor=1.4,
#                                           minNeighbors=14,
#                                           minSize=(150, 150),
#                                           maxSize=(250, 250))

# print(boats)

# for (x, y, l, a) in boats:
#     cv.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 2)
#     cv.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 5)
#     num_boats += 1  # Incrementa o número de navios detectados

# end_time = time.time()  # Finaliza o contador de tempo

# # Parte que calcula o tempo
# start_time = time.time()  # Inicia o contador de tempo
# tempo_decorrido = end_time - start_time

# # Convertendo o tempo decorrido para hh:mm:ss:ms
# tempo_restante = time.strftime("%H:%M:%S:", time.gmtime(tempo_decorrido))
# milissegundos = int((tempo_decorrido - int(tempo_decorrido)) * 1000)
# tempo_restante += f"{milissegundos:03d}"

# print(f"Tempo decorrido: {tempo_restante} segundos")
# print(f"Número de navios detectados: {num_boats}")

# # Salvando a imagem
# largura = 1400
# altura = 720
# imagem = cv.resize(imagem, (largura, altura))
# cv.imshow('Boats', imagem)
# cv.waitKey(0)
