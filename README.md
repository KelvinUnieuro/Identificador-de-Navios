Bem-vindo ao Identificador de Navios! Utilizamos diversas técnologias nesse projeto, desde aprendizado de máquina até paralelização com multithreading, para conseguir maior eficiência de processamento ao buscar os navios dentro da imagem grande criada.

![ezgif com-animated-gif-maker](https://github.com/user-attachments/assets/df5548e0-66e6-4b13-a20f-ed7a85187517)
![print02](https://github.com/user-attachments/assets/32698fba-84a5-48f6-8975-5fcde79a6afa)
![print03](https://github.com/user-attachments/assets/a289db7a-234e-44ed-aef4-81d83af934e9)


## Índice

- [📄Sobre o Projeto](#sobre-o-projeto)
- [🔎Como Funciona](#como-funciona)
- [📋Pré-requisitos](#pré-requisitos)
- [🔧Instalação](#instalação)
- [🚀Uso](#uso)
- [💡Contribuindo](#contribuindo)
- [❓Problemas Comuns](#problemas-comuns)
- [✍️Observações importantes](#observações-importantes)
- [🤝Colaboradores do projeto](#colaboradores-do-projeto)

<br>

## 📄Sobre o Projeto
O Projeto Identificador de Navios é uma aplicação que utiliza técnicas de visão computacional para detectar navios em grandes imagens. O projeto é dividido em duas partes principais: a divisão da imagem original em partes menores e o processamento dessas partes para detectar os navios.

<br>

## 🔎Como Funciona

### Dividir-imagem.py
1. A imagem grande é dividida em partes menores, de acordo com a quantidade de partes que o usuário determinar.
2. As partes menores são convertidas para pb (preto e branco) e depois armazenadas dentro da pasta "partes".

### Processar.py
1. O usuário decide quantas threads o script irá utilizar, sendo recomendado no máximo a quantidade de processadores lógicos que o sistema utilizado possui.
2. O script distribui as threads para realizar o processamento das imagens armazenadas na pasta "partes" paralelamente.
3. Após terminar o processamento de cada parte, marcando e contabilizando a quantidade de navios encontrados dentro dela, a parte é armazenada dentro da pasta "partes_processadas".
4. No terminal aparecem as informações de quantas navios foram encontrados no total e a quantidade de tempo que levou o processamento das partes.

<br>

## 📋Pré-requisitos

Certifique-se de seguir os pré-requisitos do sistema para que o programa funcione corretamente.

* Imagem de no máximo 4.0gb no formato "tiff"
* Python v3.12.4
* Pip v24.0
* pyvips v2.2.3
* OpenCv v4.10.0
* NumPy v1.26.4

### Instalando pyvips

1. Baixe e instale o `pyvips-all`:

   - Para Windows, você pode baixar o pacote `vips-dev-w64-all v8.15.2` do repositório [libvips/libvips](https://github.com/libvips/libvips/releases).

2. Extraia o conteúdo do arquivo baixado em um diretório de sua escolha, por exemplo, `C:\vips`.

3. Adicione o diretório `bin` do `pyvips` ao `PATH` nas variáveis de ambiente do sistema, em varíaveis de usuário:

   - No Windows:
     1. Abra a barra de pesquisa do windows e encontre "Editar as variáveis de ambiente do sistema.
     2. Clique em "Variáveis de Ambiente"
     3. Na seção "Variáveis do Sistema", encontre a variável `Path`, em  variáveis de usuário e edite-a.
     4. Adicione o caminho para o diretório `bin` do `pyvips`, por exemplo: `C:\vips\bin`.

4. Instale o pacote `pyvips` no seu ambiente Python:

   ```sh
   pip install pyvips

5. Certifique-se de substituir o caminho da variável "vipsbin" no script "dividir-imagem.py" pelo mesmo caminho `bin` de seu `pyvips-all`

<br>

## 🔧Instalação

1. Clone o repositório:
```
git clone https://github.com/guiibrag4/Identificador-de-Navios.git
```
2. Navegue até o diretório do projeto:
```
cd Identificador-de-Navios
```
3.  Instale as dependências:
```
pip install -r requirements.txt
```

<br>

## 🚀Uso

1. No script de divisão de imagem, entre com a quantidade de partes que você deseja dividir a imagem original, armazenada no caminho `"main-project/assets/nome-imagem".` Certifique-se de colocar o caminho original e o nome da imagem selecionada.
2. Após isso, escolha o número de threads que será utilizada no script `processar.py`, substituindo o número da variável `max-workers`.
3. Inicia o script e aguarde o processamento da imagem.

<br>

## 💡Contribuindo

Contribuições são bem-vindas! Por favor, siga os passos abaixo para contribuir:

1. Fork o repositório.
2. Crie uma nova branch:

```
git checkout -b feature/sua-feature
```

3. Faça suas modificações.
4. Faça o commit das suas alterações:

```
git commit -m 'Adiciona nova funcionalidade'
```


5. Envie para o branch:
```
git push origin feature/sua-feature
```

6. Abra um Pull Request.

<br>

## ❓Problemas Comuns

### Erro com o funcionamente do libvips42.dll
* Certifique-se de adicionar o `pyvips-all` nas variáveis de ambiente do sistema, além disso, certifique-se que o mesmo caminho está na variável `vipsbin` do script de divisão de imagens.
  
### Carregamento e Processamento de Imagens
* Tente usar números diferentes de partes em que a imagem será dividida e também da quantidade de threads utilizadas. Processar várias partes de uma imagem simultaneamente em threads pode levar a um aumento no consumo de memória, especialmente se não houver controle adequado sobre o número de threads ou sobre o gerenciamento de recursos compartilhados.
* Ao dividir a imagem principal, não ultrapasse o limite de tamanho (4gb) e verifique o uso de memória do seu sistema. Carregar uma imagem grande inteira na memória pode utilizar muitos recursos, principalmente se houver operações de processamento ocorrento simultaneamente.
* Diminua o consumo de memória de sua máquina, para que ela consiga focar seus recursos no funcionamento do script.

<br>

## ✍Observações importantes e créditos 
Para encontrar os navios dentro da imagem foi utilizado um modelo de "cascata de haar", que possui parâmetros que podem ser alterados dentro de `processar.py`. A modificação desses parâmetros pode fazer com que o sistema encontre mais ou menos navios. Por isso, é importante saber que ao mudar de imagem é necessário também modificar os parâmetros `parte_np`, `scaleFactor`,`minNeighbors`,`minSize` e `maxSize`. 
  
O script haarcascade utilizado neste projeto foi adaptado a partir do repositório de [nicolagulmini](https://github.com/nicolagulmini/Boat_Detector).

## 🤝Colaboradores do projeto

- [@Guilherme Braga](https://github.com/guiibrag4)
- [@Kelvin Lima](https://github.com/KelvinUnieuro)

---
