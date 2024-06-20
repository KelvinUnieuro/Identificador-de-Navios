# Importando as bibliotecas necessárias
import cv2 as cv  # OpenCV para processamento de imagem
import numpy as np  # NumPy para manipulação de arrays
import os  # os para manipulação do sistema operacional
import multiprocessing  # multiprocessing para multithreading
import pyvips  # pyvips para manipulação de imagens grandes
import time  # time para medir o tempo de execução

# Adicionando o diretório DLL para o pyvips
add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"C:\temp\vips-dev-w64-all-8.15.2\vips-dev-8.15\bin"
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ["PATH"] = os.pathsep.join((vipsbin, os.environ["PATH"]))

# Carregando a imagem grande usando pyvips
imagem = pyvips.Image.new_from_file('main-project/assets/imgGrande.tiff')

# Definindo o número de partes que a imagem será dividida e o tamanho de cada parte
largura, altura = imagem.width, imagem.height
num_partes = 16
parte_largura = largura
parte_altura = altura // num_partes

# Carregando o arquivo xml treinado para detecção de barcos
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

# Função para processar uma parte da imagem
def processar_parte(i):
    # Definindo as coordenadas de recorte para esta parte
    x1 = 0
    y1 = i * parte_altura
    x2 = largura
    y2 = y1 + parte_altura

    # Recortando a parte da imagem
    parte_imagem = imagem.crop(x1, y1, parte_largura, parte_altura)
    
    parte_imagem = parte_imagem.resize(0.5)
    
    # Convertendo a parte da imagem para numpy array para usar com OpenCV
    parte_np = np.ndarray(buffer=parte_imagem.write_to_memory(),
                          dtype=np.uint8,
                          shape=[parte_altura, parte_largura, 3])

    # Convertendo para BGR (OpenCV usa BGR por padrão)
    parte_np = cv.cvtColor(parte_np, cv.COLOR_RGB2BGR)

    # Convertendo a imagem para cinza para maior eficiência do OpenCV
    imagemCinza = cv.cvtColor(parte_np, cv.COLOR_BGR2GRAY)

    # Detectando os barcos na parte da imagem
    boats = carregaAlgoritmo.detectMultiScale(imagemCinza,
                                              scaleFactor=1.3,
                                              minNeighbors=4,
                                              minSize=(300, 300),
                                              maxSize=(2000, 2000))
    num_boats = len(boats)
    for (x, y, l, a) in boats:
        # Desenhando o retângulo diretamente na imagem PyVIPS
        parte_imagem = parte_imagem.draw_rect(255, x, y, l, a, fill=False)

    # Salvando a parte da imagem com os barcos detectados
    parte_imagem.write_to_file(f'parte_{i}.tiff')

    return num_boats

if __name__ == "__main__":
    # Iniciando o contador de tempo
    start_time = time.time()

    # Usando Pool para paralelizar o processamento das partes da imagem
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.map(processar_parte, range(num_partes))

    num_boats = sum(results)

    # Imprimindo o número de threads usadas
    print('\n\nnúmero de processadores lógicos:', multiprocessing.cpu_count())
    print('Processamento finalizado!!\n')

    # Parando o contador de tempo e calculando o tempo total
    end_time = time.time()
    total_time = end_time - start_time

    # Imprimindo o número total de barcos detectados e o tempo total de processamento
    print(f'Número total de barcos detectados: {num_boats}')
    print(f'Tempo total de processamento: {total_time} segundos')