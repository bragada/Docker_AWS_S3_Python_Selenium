# Docker_AWS_S3_Python_Selenium
Docker que contém um script Python e utiliza Selenium para baixar arquivos e subir para uma base AWS S3

Para criar a imagem, rode no terminal:

* docker build -t python-selenium:1.0 .

Para criar e rodar o conteiner, rode no terminal:

* docker run --name python-selenium-conteiner1.0 -d python-selenium:1.0 
