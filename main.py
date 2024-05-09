import os
import glob
from pathlib import Path
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import shutil
import boto3

# Função que faz o upload para AWS S3
def upload_file_using_client(arquivo):
    s3 = boto3.client("s3",
                aws_access_key_id = "XXXXXXXXXXXXXXXXXXXX",
                aws_secret_access_key = "XXXXXXXXXXXX")
    bucket_name = "automacao-conecta"
    object_name = arquivo
    file_name =  arquivo

    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(True)
    except Exception as e:
        print(False)
        print("Erro ao fazer o upload do arquivo:", e)

sleep(3)


# Configuração do Selenium
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-dev-shm-usage")
prefs = {
         #"browser.downloads.dir": "/app",
         "download.prompt_for_download": False,
         "download.default_directory":  os.path.dirname(os.path.abspath(__file__)),
         "directory_upgrade": True}
chrome_options.add_experimental_option("prefs", prefs)

# Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)


# Acessa Site
driver.get("https://conectacampinas.exati.com.br/")
sleep(3)


################################### Login
wait = WebDriverWait(driver,60)
user_box = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="userInfo.password"]')))

# User
user_box = driver.find_element(By.XPATH,"//input[@id = 'userInfo.username']")
user_box.send_keys("XXXXXXXXX")
sleep(1)

# Password
password_box = driver.find_element(By.XPATH,'//*[@id="userInfo.password"]')
password_box.send_keys("XXXXXXXXXX")
sleep(1)

# Logar
login_box = driver.find_element(By.XPATH,'//span[. = " Acessar "]')
login_box.click()

print("Login Successfully")
################################### Guia
# Menu Principal
menu_principal = wait.until(EC.presence_of_element_located((By.XPATH,"//button[@class = 'v-app-bar__nav-icon ml-0 v-btn v-btn--icon v-btn--round theme--light v-size--default black--text']")))
menu_principal.click()
sleep(1)

# Guia Painel de Monitoramento
guia_solicitacoes = driver.find_element(By.XPATH,'//h4[. =" Materiais aplicados "]')
guia_solicitacoes.click()
sleep(1)

# Pesquisar (load all data)
pesquisar = driver.find_element(By.XPATH,"//button[@class = 'v-btn v-btn--bottom v-btn--fab v-btn--outlined v-btn--round v-btn--tile theme--light v-size--small dark--text dark--text']")
pesquisar.click()

# Espera Loadar os dados
espera_load_dados = wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@class = "v-btn v-btn--bottom v-btn--fab v-btn--outlined v-btn--round v-btn--tile theme--light v-size--small dark--text dark--text"]')))
sleep(1)

# Menu 3 pontos
menu_download = driver.find_element(By.XPATH,"//button[@class = 'v-btn v-btn--bottom v-btn--fab v-btn--has-bg v-btn--round v-btn--tile theme--light v-size--small mono-grey-2 mono-grey-40--text']")
menu_download.click()
sleep(1)

# Botao Exportar
exportar_box =  driver.find_element(By.XPATH,"//div[. = ' Exportar para ' and  @class ='v-list-item v-list-item--link theme--light' ]")
exportar_box.click()
sleep(1)

# Tipos Download
menu_tipos_download = driver.find_element(By.XPATH,"//div[. = 'Exportar para']")
menu_tipos_download.click()
sleep(1)

# csv Select
csv_select = driver.find_element(By.XPATH,"//div[. = 'CSV' and @class = 'v-list-item v-list-item--link theme--light']")
csv_select.click()
sleep(1)

# Baixa
download_at =  driver.find_element(By.XPATH,'//button[@class = "v-btn v-btn--bottom v-btn--has-bg theme--light v-size--default primary white--text"]')
download_at.click()

# Verifica Se Baixou
def baixou():
    try:
        arquivo =  f'{datetime.now().strftime("%d-%m-%Y")}.csv'
        while not os.path.exists(arquivo):
            sleep(1)  # Aguarda 1 segundo antes de verificar novamente
        return True
    except Exception as e:
        print("Ocorreu um erro:", e)
        return False
baixou()

print("Download Successfully")

# Rename File
old_name = os.path.join(f'{datetime.now().strftime("%d-%m-%Y")}.csv')
new_name = os.path.join(f'{"foi"}.csv')
shutil.move(old_name,new_name)
sleep(1)

# Exec função upload AWS
upload_file_using_client("foi.csv")


driver.close()
print("FIM")
