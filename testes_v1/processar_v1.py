import cv2 as cv  
import numpy as np  
import os  
import concurrent.futures  
import pyvips  
import time  
from datetime import timedelta  
from threading import Lock
import gc

# Adicionando o diretório DLL para o pyvips
add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"C:\temp\vips-dev-w64-all-8.15.2\vips-dev-8.15\bin"
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ["PATH"] = os.pathsep.join((vipsbin, os.environ["PATH"]))

# Diretório onde as partes da imagem são armazenadas
partes_dir = 'partes'

# Listando as partes disponíveis na pasta
partes = [f for f in os.listdir(partes_dir) if f.endswith('.tiff')]
num_partes = len(partes)

print(f'Número de partes encontradas: {num_partes}')
print(f'Partes encontradas: {partes}')

# Carregando o arquivo xml treinado para detecção de barcos
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

# Inicializando um Lock para proteger o acesso ao contador de barcos
lock = Lock()
num_boats = 0

# Função para processar uma parte da imagem
def processar_parte(filename):
    global num_boats  

    try:
        print(f'Processando {filename}...')

        # Carregando a parte da imagem
        parte_imagem = pyvips.Image.new_from_file(os.path.join(partes_dir, filename))
        parte_largura, parte_altura = parte_imagem.width, parte_imagem.height

        # Convertendo a parte da imagem para numpy array para usar com OpenCV
        memory_buffer = parte_imagem.write_to_memory()
        parte_np = np.ndarray(buffer=memory_buffer,
                              dtype=np.uint8,
                              shape=[parte_altura, parte_largura])

        # Convertendo para BGR (OpenCV usa BGR por padrão)
        parte_np = cv.cvtColor(parte_np, cv.COLOR_RGB2BGR)
        
        # Detectando os barcos na parte da imagem
        boats = carregaAlgoritmo.detectMultiScale(parte_np,
                                                  scaleFactor=1.1,
                                                  minNeighbors=3,
                                                  minSize=(250, 250),
                                                  maxSize=(800, 800))
        for (x, y, l, a) in boats:
            # Desenhando o retângulo diretamente na imagem PyVIPS
            parte_imagem = parte_imagem.draw_rect(255, x, y, l, a, fill=False)
            with lock:
                num_boats += 1  # Protegendo a atualização do contador de barcos

        # Salvando a parte da imagem com os barcos detectados
        parte_imagem.write_to_file(os.path.join(partes_dir, f'{filename[:-5]}_detectada.tiff'))
        print(f'{filename} processada e salva.')

        # Liberando recursos
        del memory_buffer
        del parte_imagem
        del parte_np
        cv.destroyAllWindows()
        gc.collect()
    
    except Exception as e:
        print(f'Erro ao processar {filename}: {e}')

# Iniciando o contador de tempo
start_time = time.time()

# Usando ThreadPoolExecutor para paralelizar o processamento das partes da imagem
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    executor.map(processar_parte, partes)

# Imprimindo o número de threads usadas
print('\n\nNúmero de threads:', 4)
print('Processamento finalizado!!\n')

# Parando o contador de tempo e calculando o tempo total
end_time = time.time()
total_time = end_time - start_time
time_formatted = str(timedelta(seconds=total_time))

# Imprimindo o número total de barcos detectados e o tempo total de processamento
print(f'Número total de barcos detectados: {num_boats}')
print(f'Tempo total de processamento: {time_formatted} segundos')
