import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw
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
# imagem = pyvips.Image.new_from_file('main-project/assets/varios-barco18.tiff')
imagem = pyvips.Image.new_from_file('main-project/assets/barco18.jpg')
# imagem = pyvips.Image.new_from_file('main-project/assets/img-grande.tiff')

# Ajustando quantas partes a imagem terá e qual será a altura e largura de cada uma
largura, altura = imagem.width, imagem.height
num_partes = 5
parte_largura = largura
parte_altura = altura // num_partes

# Para carregar o arquivo xml já treinado
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

for i in range(num_partes):
    linha_imagem = None
    # Define as coordenadas de recorte para esta parte
    x1 = 0
    y1 = i * parte_altura
    x2 = largura
    y2 = y1 + parte_altura
    
    print(f'Largura imagem {i}: {x1}-{x2} | Altura imagem {i}: {y1}-{y2}')

    # Recorta a parte da imagem
    parte_imagem = imagem.crop(x1, y1, parte_largura, parte_altura)
    

    # Restante do código...

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
                                                  minNeighbors=4,
                                                  minSize=(200, 200),
                                                  maxSize=(250, 250))
    for (x, y, l, a) in boats:
        # Converte a imagem PyVIPS para PIL
        parte_imagem_pil = Image.fromarray(np.array(parte_imagem))

        # Cria um objeto de desenho
        draw = ImageDraw.Draw(parte_imagem_pil)

        # Desenha o retângulo
        draw.rectangle([(x, y), (x + l, y + a)], outline=(0, 255, 0), width=5)

        # Converte a imagem PIL de volta para PyVIPS
        parte_imagem = pyvips.Image.new_from_array(np.array(parte_imagem_pil), 1)
        num_boats += 1  # Incrementa o número de navios detectados

    # Salva a parte da imagem com os barcos detectados    
    parte_imagem.write_to_file(f'parte_{i}.tiff')
        
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
