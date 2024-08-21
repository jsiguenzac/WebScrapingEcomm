from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#from selenium import webdriver
from utils.driver.chrome_driver import init_driver
import time
import bs4 as _bs
#from selenium.webdriver.common.action_chains import ActionChains

DRIVER = init_driver() #webdriver.Chrome()

url_curacao = "https://www.lacuracao.pe"

def get_categories_curacao():
    count_valid = 1
    print("Iniciando Chrome")
    while True:        
        try:
            count_valid += 1
            DRIVER.get(url_curacao)            
            while True:
                if count_valid == 3:
                    print("Alertas cerradas, Continuando...")
                    break
                if close_alert():
                    break
            # Esperar a que el elemento sea interactivo
            menu_cat = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-middle-left ']")))
            menu_cat.click()
            print("Accediendo al menu")
            names_cat = []
            info_complete = []
            list_subcategories = []
            time.sleep(2)
            categories = DRIVER.find_elements(By.XPATH, "//ul[@class='expand-desktop navigation-menu menu-initialized menu-only-first-level']/li/a")
            print("Filtrando categorias")
            if len(categories) > 2:
                # Tecnologia, Electrohogar
                names_cat.append(categories[1].text)
                names_cat.append(categories[2].text)
            else:
                print("No se encontraron suficientes categorías : ", len(categories))
            
            for i, category_name in enumerate(names_cat):
                #print(f"Categoria Obtenida: {category_name}")
                try:
                    #category = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.XPATH, f"//a/span[contains(text(),'{names_cat[i]}')]")))
                    #category = DRIVER.find_element(By.XPATH, f"//li[@class='level0 nav-2 category-item level-top parent parent-menu grand-parent']/a/span[contains(text(),'{names_cat[i]}')]")
                    category = DRIVER.find_element(By.XPATH, f"//li/a/span[contains(text(),'{category_name}')]")
                    '''actions = ActionChains(DRIVER)
                    actions.move_to_element(category).perform()'''
                    category.click()
                    print("Accediendo a la categoria: ", category_name)
                    time.sleep(5)
                    subcategories = DRIVER.find_elements(By.XPATH, "//div[@class='level1 submenu-wrapper']/div/ul/li/a")
                    #subcat_select = DRIVER.find_elements(By.CSS_SELECTOR, "li[class^='level1']")
                    for subcategory in subcategories:
                        name_subcat = subcategory.text
                        if name_subcat == "Ver todo" or name_subcat.__len__() == 0:
                            subcategories.remove(subcategory)
                        else:
                            name_subcat = subcategory.text
                            print(f"Subcategoria: {name_subcat}")
                            sub_category_url = subcategory.get_attribute("href")
                            sub_cat_current = {"name": name_subcat, "url": sub_category_url}
                            list_subcategories.append(sub_cat_current)
                            complete = {"category": names_cat[i], "subcategories": list_subcategories}
                            info_complete.append(complete)  
                            list_subcategories = []
                except Exception as e:
                    print(f"-> error en la categoria: {names_cat[i]} ---> {e}")
            print("Subcategorias obtenidas. Continuando...")
            break
        except Exception as e:
            print(f"-> Volviendo a intentar...")
    print("Categorias obtenidas. Continuando...")
    return info_complete

def close_alert():
    try:
        #ventana_original = DRIVER.current_window_handle
        DRIVER.refresh()
        print("Buscando alerta...")
        time.sleep(5)
        # Intenta encontrar el botón para cerrar el div con un tiempo de espera corto
        cancel_button = WebDriverWait(DRIVER, 20).until(EC.presence_of_element_located((By.ID, "onesignal-slidedown-cancel-button")))
        cancel_button.click()
        return True
    except Exception as e:
        print("Alerta no encontrada. Por favor espere...")
        return  False

def  _generate_url(url_subcat, page_current):
    url_gen = url_subcat + f"?p={page_current}"
    return url_gen

def _get_detail_prod(url_product):
    try:
        print("Redireccionando al Detalle")
        DRIVER.get(url_product)
        # Esperar a que el elemento sea interactivo        
        #specific = WebDriverWait(DRIVER, 30).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Especificaciones')]")))
        specific = WebDriverWait(DRIVER, 30).until(EC.presence_of_element_located((By.ID, "tab-label-additional-title")))
        specific.click()
        print("Accediendo a la sección de especificaciones")
        time.sleep(5)
        # Obtiene el contenido actualizado de la página con Selenium
        page_source = DRIVER.page_source
        return _bs.BeautifulSoup(page_source, "html.parser")
    except Exception as e:
        print("Error en: "+ str(e))
    finally:
        print("Información obtenida. Cerrando Chrome...")
        DRIVER.quit()
