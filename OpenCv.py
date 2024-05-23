import cv2 as cv
import numpy as np

# Para carregar o arquivo xml já treinado
carregaAlgoritmo = cv.CascadeClassifier('testes-1/haarcascades/first_cascade.xml')

# Pegando a imagem

# imagem = cv.imread('testes-1/assets/varios-barco18.tiff')
imagem = cv.imread('testes-1/assets/varios-barco18-img-grande.png')

# Deixando a imagem cinza para maior eficiência do opencv
if imagem is None:
    print("Erro ao carregar a imagem")
else:
    # Divide a imagem em 4 partes
    altura, largura = imagem.shape[:2]
    sub_imagens = [imagem[:altura//2, :largura//2], imagem[:altura//2, largura//2:],
                   imagem[altura//2:, :largura//2], imagem[altura//2:, largura//2:]] 
    imagemCinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    
# Processa cada parte da imagem
sub_imagens_processadas = []
for sub_imagem in sub_imagens:
        sub_imagem_cinza = cv.cvtColor(sub_imagem, cv.COLOR_BGR2GRAY)
        boats = carregaAlgoritmo.detectMultiScale(sub_imagem_cinza, scaleFactor=1.4, minNeighbors=14, minSize=(150, 150), maxSize=(250, 250))
        print (boats)
        for (x, y, l, a) in boats:
            cv.rectangle(sub_imagem, (x, y), (x + l, y + a), (0, 255, 0), 5)
        sub_imagens_processadas.append(sub_imagem)

# Junta as partes da imagem novamente
imagem_processada = np.concatenate((np.concatenate(sub_imagens_processadas[:2], axis=1),
                                        np.concatenate(sub_imagens_processadas[2:], axis=1)), axis=0)

largura = 1400
altura = 720
imagem = cv.resize(imagem, (largura, altura))

cv.imshow('Boats', imagem)
cv.waitKey(0)


