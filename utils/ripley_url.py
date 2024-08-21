from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import requests as rq
import bs4 as _bs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--log-level=3')  # Ajusta el nivel de registro a LOG_ERROR
options.add_argument('--ignore-certificate-errors')
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#DRIVER = webdriver.Chrome()
url_ripley = "https://simple.ripley.com.pe"

def _get_names_url_subcategories():
    info_complete = []
    names_cat = []
    list_subcategories = []
    try:
        print("Iniciando Chrome")
        DRIVER.get(url_ripley)
        
        while True:
            if close_alert():
                #back()
                break
        
        # Esperar a que el elemento sea interactivo
        menu_cat = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ripley-header__menu-button-container']")))
        menu_cat.click()
        print("Accediendo al menu")
        
        time.sleep(5)
        categories = DRIVER.find_elements(By.XPATH, "//div[@class='tree-node-items']/a")
        #categories = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='tree-node-items']/a")))
        print("Filtrando categorias")
        if len(categories) > 2:
            # Tecnologia, Celulares
            names_cat.append(categories[0].text)
            names_cat.append(categories[2].text)
        else:
            print("No se encontraron suficientes categorías : ", len(categories))
        for i in range(len(names_cat)):
            print(f"Categoria Obtenida: {names_cat[i]}")
            try:
                category = WebDriverWait(DRIVER, 20).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{names_cat[i]}')]")))
                category.click()
                
                subcategories = DRIVER.find_elements(By.XPATH, "//div[@class='category-tree__expanded-categories']/ul/li/ul/li/a")
                
                for subcategory in subcategories:
                    subcat = subcategory.text
                    print(f"Subcategoria: {subcat}")
                    sub_category_element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{subcat}')]")))
                    sub_category_url = sub_category_element.get_attribute("href")
                    sub_cat_current = {"name": subcat, "url": sub_category_url}
                    list_subcategories.append(sub_cat_current)
                complete = {"category": names_cat[i], "subcategories": list_subcategories}
                info_complete.append(complete)
                list_subcategories = []
                back()
            except Exception as e:
                print(f"-> error en la categoria: {names_cat[i]} ---> {e}")
        return info_complete
    except Exception as e:
        print(f"-> error en el metodo get_names_url_subcategories: {e}")
    finally:
        print("Información obtenida. Continuando...")
        #DRIVER.quit()

def back():
    try:
        back = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='category-tree-container-expanded__header']/div/a/span[contains(text(),'Volver')]")))
        back.click()
    except Exception as e:
        print("")

def close_alert():
    try:
        #ventana_original = DRIVER.current_window_handle
        print("Buscando alerta")
        # Intenta encontrar el botón para cerrar el div con un tiempo de espera corto
        cancel_button = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.ID, "onesignal-slidedown-cancel-button")))
        cancel_button.click()
        try:
            cbar_POP2_46981 = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.XPATH, "//div/img[@class='cbar-close-button']")))
            #alert_cyber = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='alignment']")))
            #close_cyber = WebDriverWait(DRIVER, 20).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='cbar-close-button']")))
            #c = cbar_POP2_46981.get_attribute("img", class_="cbar-close-button")
            cbar_POP2_46981.click()
            #DRIVER.switch_to.window(DRIVER.window_handles[-1])
            #DRIVER.close()
            #DRIVER.switch_to.window(ventana_original)
            print("Alerta Cyber wow cerrada")
            #close_cyber.find_element(By.XPATH, "//img[@class='cbar-close-button']")
        except Exception as e:
            print("No se encontro alerta de Cyber wow, Continuando..." + str(e))
        print("Alerta Cerrada. Continuando...")
        return True
    except Exception as e:
        print("Alerta no encontrada. Por favor espere...")
        return  False

def _generate_url(url: str, page: int):
    short_url = url.split("?")[0]
    return short_url + "?page=" + str(page)

def _get_detail_prod(url: str):
    try:
        print("Redireccionando al Detalle")
        DRIVER.get(url)
        # Esperar a que el elemento sea interactivo        
        specific = WebDriverWait(DRIVER, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Especificaciones')]")))
        specific.click()
        print("Accediendo a la sección de especificaciones")
        time.sleep(8)
        # Obtiene el contenido actualizado de la página con Selenium
        page_source = DRIVER.page_source
        return _bs.BeautifulSoup(page_source, "html.parser")
    except Exception as e:
        print("Error en: "+ str(e))
    finally:
        print("Información obtenida. Cerrando Chrome...")
        DRIVER.quit()