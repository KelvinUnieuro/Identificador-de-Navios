# Importando as bibliotecas necessárias
import pyvips
import os

# Adicionando o diretório DLL para o pyvips
add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"C:\temp\vips-dev-w64-all-8.15.2\vips-dev-8.15\bin"
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ["PATH"] = os.pathsep.join((vipsbin, os.environ["PATH"]))

# Carregando a imagem grande usando pyvips
imagem = pyvips.Image.new_from_file('main-project/assets/replicated_image.tiff')

# Definindo o número de partes que a imagem será dividida e o tamanho de cada parte
largura, altura = imagem.width, imagem.height
num_partes = 1
parte_largura = largura
parte_altura = altura // num_partes

# Criando a pasta 'partes' se não existir
if not os.path.exists('partes'):
    os.makedirs('partes')

# Dividindo a imagem e salvando cada parte em preto e branco
for i in range(num_partes):
    x1 = 0
    y1 = i * parte_altura
    parte_imagem = imagem.crop(x1, y1, parte_largura, parte_altura)
    # Convertendo a parte da imagem para preto e branco
    parte_imagem_bw = parte_imagem.colourspace('b-w')
    parte_imagem_bw.write_to_file(f'partes/parte_{i}.tiff')

print('Divisão da imagem concluída e partes salvas em preto e branco!')
