import cv2 as cv

# Para carregar o arquivo xml já treinado
carregaAlgoritmo = cv.CascadeClassifier('testes-1/haarcascades/first_cascade.xml')

# Pegando a imagem
# imagem = cv.imread('testes-1/assets/img-boat.jpg')
# imagem = cv.imread('testes-1/assets/barco4.jpg')
# imagem = cv.imread('testes-1/assets/barco3.jpg')
# imagem = cv.imread('testes-1/assets/barco2.jpg')
# imagem = cv.imread('testes-1/assets/barco.jpg')
# imagem = cv.imread('testes-1/assets/barco5.jpg')
# imagem = cv.imread('testes-1/assets/barco6.jpg')
# imagem = cv.imread('testes-1/assets/barco7.jpg')
# imagem = cv.imread('testes-1/assets/barco8.jpg')
# imagem = cv.imread('testes-1/assets/barco9.jpg')
# imagem = cv.imread('testes-1/assets/barco10.jpg')
# imagem = cv.imread('testes-1/assets/barco11.jpg')
# imagem = cv.imread('testes-1/assets/barco12.jpg')
# imagem = cv.imread('testes-1/assets/barco13.jpg')
# imagem = cv.imread('testes-1/assets/barco14.jpg')
# imagem = cv.imread('testes-1/assets/barco15.jpg')
# imagem = cv.imread('testes-1/assets/barco16.jpg')
# imagem = cv.imread('testes-1/assets/barco17.jpg')
# imagem = cv.imread('testes-1/assets/barco18.jpg')
imagem = cv.imread('testes-1/assets/varios-barco18.tiff')



# Deixando a imagem cinza para maior eficiência do opencv
if imagem is None:
    print("Erro ao carregar a imagem")
else:
    imagemCinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

boats = carregaAlgoritmo.detectMultiScale(imagemCinza, scaleFactor=1.4, minNeighbors=14, minSize=(150, 150), maxSize=(250, 250))

print (boats)

for (x, y, l, a) in boats:
    cv.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 5)

largura = 1400
# altura = int(largura * imagem.shape[0] / imagem.shape[1])  # Mantendo a proporção da imagem
altura = 720
imagem = cv.resize(imagem, (largura, altura))

cv.imshow('Boats', imagem)
cv.waitKey(0)

# Imagens que mais tão dando certo: barco13, 

