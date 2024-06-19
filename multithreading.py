import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw
import os
import concurrent.futures
import pyvips
import time

add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"C:\temp\vips-dev-w64-all-8.15.2\vips-dev-8.15\bin"
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ["PATH"] = os.pathsep.join((vipsbin, os.environ["PATH"]))

imagem = pyvips.Image.new_from_file('main-project/assets/imgGrande.tiff')

# Ajusta quantas partes a imagem terá e qual será a altura e largura de cada uma
largura, altura = imagem.width, imagem.height
num_partes = 5
parte_largura = largura
parte_altura = altura // num_partes

# Para carregar o arquivo xml já treinado
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

# Função para processar uma parte da imagem
def processar_parte(i):
    global num_boats
    # Define as coordenadas de recorte para esta parte
    x1 = 0
    y1 = i * parte_altura
    x2 = largura
    y2 = y1 + parte_altura
    
    print(f'Largura imagem {i}: {x1}-{x2} | Altura imagem {i}: {y1}-{y2}')

    # Recorta a parte da imagem
    parte_imagem = imagem.crop(x1, y1, parte_largura, parte_altura)
    
    # Converte a parte da imagem para numpy array para usar com OpenCV
    parte_np = np.ndarray(buffer=parte_imagem.write_to_memory(),
                          dtype=np.uint8,
                          shape=[parte_altura, parte_largura, 3])

    # Converte para BGR (OpenCV usa BGR por padrão)
    parte_np = cv.cvtColor(parte_np, cv.COLOR_RGB2BGR)

    # Deixando a imagem cinza para maior eficiência do opencv
    imagemCinza = cv.cvtColor(parte_np, cv.COLOR_BGR2GRAY)

    # Detecta os barcos na parte da imagem
    boats = carregaAlgoritmo.detectMultiScale(imagemCinza,
                                              scaleFactor=1.2,
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
    
start_time = time.time()
num_boats = 0

# Usa o ThreadPoolExecutor para paralelizar o processamento das partes da imagem
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(processar_parte, range(num_partes))
    
# max_workers=16

print('\n\nnúmero de threads:', executor._max_workers)
print('Processamento finalizado!!\n')
    
end_time = time.time()
total_time = end_time - start_time

print(f'Número total de barcos detectados: {num_boats}')
print(f'Tempo total de processamento: {total_time} segundos')
