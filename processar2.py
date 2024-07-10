# Importando as bibliotecas necessárias
import cv2 as cv  # OpenCV para processamento de imagem
import numpy as np  # NumPy para manipulação de arrays
import os  # os para manipulação do sistema operacional
import concurrent.futures  # concurrent.futures para multithreading
import pyvips  # pyvips para manipulação de imagens grandes
import time  # time para medir o tempo de execução
from datetime import timedelta  # timedelta para formatar o tempo de execução
import threading  # threading para sincronização

# Carregando o arquivo xml treinado para detecção de barcos
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

# Lock para proteger as variáveis compartilhadas
lock = threading.Lock()

# Variável global para contar o número de barcos detectados
num_boats = 0

# Variável global para atribuir números às threads
thread_counter = 0

# Função para processar uma parte da imagem
def processar_parte(parte_filename):
    global num_boats
    global thread_counter
    
    with lock:
        thread_number = thread_counter
        thread_counter += 1

    print(f'Thread {thread_number + 1} começou a processar a parte {parte_filename}')
    
    try:
        # Carregando a parte da imagem
        parte_imagem = pyvips.Image.new_from_file(parte_filename)
        
        # Convertendo a parte da imagem para numpy array para usar com OpenCV
        parte_np = np.ndarray(buffer=parte_imagem.write_to_memory(),
                              dtype=np.uint8,
                              shape=[parte_imagem.height, parte_imagem.width])

        # Convertendo para BGR (OpenCV usa BGR por padrão)
        parte_np = cv.cvtColor(parte_np, cv.COLOR_GRAY2BGR)

        # Detectando os barcos na parte da imagem
        boats = carregaAlgoritmo.detectMultiScale(parte_np,
                                                  scaleFactor=1.1,
                                                  minNeighbors=3,
                                                  minSize=(250, 250),
                                                  maxSize=(800, 800))
        with lock:
            num_boats += len(boats)  # Incrementando o número de barcos detectados

        for (x, y, l, a) in boats:
            # Desenhando o retângulo diretamente na imagem PyVIPS
            parte_imagem = parte_imagem.draw_rect(255, x, y, l, a, fill=False)

        # Salvando a parte da imagem com os barcos detectados
        parte_imagem.write_to_file(parte_filename.replace('partes', 'partes_processadas'))
        print(f'Thread {thread_number + 1} processou a parte {parte_filename} com sucesso!')

    except Exception as e:
        print(f'Thread {thread_number + 1} encontrou um erro ao processar a parte {parte_filename}: {e}')

# Iniciando o contador de tempo
start_time = time.time()

# Criando a pasta 'partes_processadas' se não existir
if not os.path.exists('partes_processadas'):
    os.makedirs('partes_processadas')

# Obtendo a lista de arquivos de partes da imagem
partes_filenames = [os.path.join('partes', f) for f in os.listdir('partes') if f.endswith('.tiff')]

# Usando ThreadPoolExecutor para paralelizar o processamento das partes da imagem
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    future_to_filename = {executor.submit(processar_parte, filename): filename for filename in partes_filenames}
    for future in concurrent.futures.as_completed(future_to_filename):
        filename = future_to_filename[future]
        try:
            future.result()
        except Exception as exc:
            print(f'{filename} gerou uma exceção: {exc}')

# Imprimindo o número de threads usadas
print('\n\nNúmero de threads:', executor._max_workers)
print('Processamento finalizado!!\n')

# Parando o contador de tempo e calculando o tempo total
end_time = time.time()
total_time = end_time - start_time
time_formatted = str(timedelta(seconds=total_time))

# Imprimindo o número total de barcos detectados e o tempo total de processamento
print(f'Número total de barcos detectados: {num_boats}')
print(f'Tempo total de processamento: {time_formatted} segundos')
