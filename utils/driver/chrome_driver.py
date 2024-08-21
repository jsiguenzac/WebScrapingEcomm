from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def init_driver():
    options = Options()
    options.add_argument('--log-level=3')  # Ajusta el nivel de registro a LOG_ERROR
    options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)