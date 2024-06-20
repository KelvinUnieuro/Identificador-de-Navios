from tkinter import Tk, filedialog
from PIL import Image
import time

def get_image_path():
    root = Tk()
    root.withdraw()  # Oculta a janela principal

    file_path = filedialog.askopenfilename()  # Abre a caixa de diálogo para selecionar o arquivo
    root.destroy()  # Fecha a janela após a seleção do arquivo

    return file_path

def replicate_image(image_path, n):
    # Abre a imagem
    img = Image.open(image_path)
   
    # Obtém as dimensões da imagem
    width, height = img.size
    cor_de_fundo = (255, 255, 255)
    # Cria uma nova imagem com dimensões multiplicadas por n
    new_width = width * n
    new_height = height * n
    #new_img = Image.new("RGB", (new_width, new_height))
    new_img = Image.new("RGB", (new_width, new_height), color=cor_de_fundo)
    print(new_width, new_height)
   
    # Preenche a nova imagem com cópias da imagem original
    for i in range(n):
        for j in range(n):
            new_img.paste(img, (i * width, j * height))
   
    # Salva a nova imagem
    start_time = time.time()  # Inicia o cronômetro
    new_img.save("replicated_image.tiff", format="TIFF", compression="tiff_lzw")
    end_time = time.time()  # Encerra o cronômetro
    elapsed_time = end_time - start_time
    print("Tempo de execução:", elapsed_time, "segundos")

# Solicita ao usuário que escolha a imagem usando o explorador de arquivos
image_path = get_image_path()

# Solicita ao usuário o valor de n
while True:
    try:
        n = int(input("Digite o valor de n para replicação da imagem: "))
        break
    except ValueError:
        print("Por favor, insira um número inteiro válido.")

# Chama a função para replicar a imagem
replicate_image(image_path,n)