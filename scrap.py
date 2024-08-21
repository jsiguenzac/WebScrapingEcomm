# Scraping de la página web de Hiraoka: Productos por marca.
# pip install -r requeriments.txt
# python.exe -m pip install --upgrade pip

from utils.hiraoka_url import _url_brand, _get_page,url_hiraoka
from utils.convert_excel import excel_by_brand,excel_by_category
import re
# colocar nombres de marca en minúscula
search_brands = [
    "sony",
    "panasonic",
    "samsung",
]

def price_products_by_brand(brands: []):
    try:
        lstProducts = []
        if len(brands) <= 0:
            print("No se encontraron marcas")
            return
        print(">INICIANDO SCRAPING...")
        for brand in brands:
            page_current = 1
            while True:
                try:
                    url = _url_brand(brand, page_current)
                    page = _get_page(url)
                    lst_items =  page.find("ol", class_="products list items product-items").find_all("li", class_="item product product-item")
                except Exception as e:
                    print(f"-> No hay productos en la página {page_current} de la marca {brand}")
                    break
                count_items = len(lst_items)
                print(f"-> Cantidad en la página {page_current} =================================== ", count_items)
                if count_items <= 0 or lst_items is None:
                    break                
                page_current += 1
                for item in lst_items:
                    image_prod = item.find("div", class_="product-item-info").find("span", class_="product-image-wrapper").find("img", class_="product-image-photo")
                    url_image = image_prod.get("src")
                    #detalle de producto
                    product_current = item.find("div", class_="product details product-item-details")            
                    
                    brand_prod = product_current.find("strong", class_="product brand product-item-brand").find("a", class_="product-item-link").text
                    b_prod = brand_prod.strip()
                    name_product = product_current.find("strong", class_="product name product-item-name").find("a", class_="product-item-link").text
                    name = name_product.strip()
                    url_product = product_current.find("strong", class_="product name product-item-name").find("a", class_="product-item-link").get("href")
                    # sacar categoria - no hay elemento en la página
                    cat = name.split(" ")
                    code_prod = product_current.find("strong", class_="product sku product-item-sku").text
                    code = code_prod.strip()
                    new_old = product_current.find("div", class_="price-box price-final_price")
                    special = ""
                    old = ""
                    unique_price = ""
                    try:
                        special = new_old.find("span", class_="special-price").find("span", class_="price-wrapper").find("span", class_="price").text
                        old = new_old.find("span", class_="old-price").find("span", class_="price-wrapper").find("span", class_="price").text
                    except Exception as e:                    
                        unique_price = new_old.find("span", class_="price").text                    
                    products = {
                        'code': code,                        
                        'url_image': url_image,
                        'url_product': url_product,
                        'category': cat[0] if len(cat) > 0 else '',
                        'brand': b_prod,'name_product': name,
                        'special_price': special if special != "" else unique_price,
                        'old_price': old
                    }
                    lstProducts.append(products)
        print("-> Total Productos encontrados : ",len(lstProducts))
        if len(lstProducts) <= 0:
            print("-> No se encontraron productos")
        else:
            if excel_by_brand(lstProducts):
                print("---> EXCEL DE PRODUCTOS CREADO, REVISA TU ESCRITORIO")
            else:
                print("---> FALLÓ AL CREAR EL EXCEL DE PRODUCTOS")
    except Exception as e:
        print("> ERROR INESPERADO : ", str(e))

def price_products_by_category():
    try:
        print(">INICIANDO SCRAPING...")  
        page_current = 1
        try:
            lstProducts = []
            page = _get_page(url_hiraoka)
            # Encontrar la categoría "Cómputo y Tecnología"
            main_category = page.find_all("a", class_="level-top")
            unique_categories = []
            for text in main_category:
                span_element = text.find('span')
                if span_element:
                    span_text = span_element.get_text()
                    if span_text not in unique_categories:
                        unique_categories.append(span_text)
            for category in unique_categories:
                if category in ["Televisores", "Cómputo y Tecnología"]:
                    print(f"-> INGRESANDO A LA CATEGORÍA : {category}")
                    # Buscar el enlace que contiene la categoría
                    category_link = page.find("a", class_="level-top", string=category) 
                    if category_link:
                        # Buscar el elemento ul siguiente
                        ul = category_link.find_next("ul")
                        if ul:
                            # Buscar todas las etiquetas li con clases específicas
                            subcategories = ul.find_all("li", class_=re.compile(r'level1 nav-\d+-\d+ category-item( first| last)? parent'))
                            for subcategory in subcategories:
                                # Buscar la etiqueta a dentro de la subcategoría
                                a = subcategory.find("a")
                                href = a['href']
                                subcategory_name = a.get_text()
                                print(f"  -> CAPTURANDO SUBCATEGORÍA DE LA CATEGORÍA  {category.upper()} : {subcategory_name}")
                                print(f"  -> OBTENIENDO URL : {href}")
                                #hacer peticion
                                pageHref = _get_page(href)
                                # Entra en la subcategoría y busca los títulos
                                lst_items = pageHref.find("ol", class_="products list items product-items").find_all("li", class_="item product product-item")     
                                for item in lst_items:
                                    image_prod = item.find("div", class_="product-item-info").find("span", class_="product-image-wrapper").find("img", class_="product-image-photo")
                                    url_image = image_prod.get("src")
                                    #detalle de producto
                                    product_current = item.find("div", class_="product details product-item-details")
                                    brand_prod = product_current.find("strong", class_="product brand product-item-brand").find("a", class_="product-item-link").text
                                    b_prod = brand_prod.strip()
                                    name_product = product_current.find("strong", class_="product name product-item-name").find("a", class_="product-item-link").text
                                    name = name_product.strip()
                                    url_product = product_current.find("strong", class_="product name product-item-name").find("a", class_="product-item-link").get("href")
                                    # sacar categoria - no hay elemento en la página
                                    cat = name.split(" ")
                                    code_prod = product_current.find("strong", class_="product sku product-item-sku").text
                                    code = code_prod.strip()
                                    new_old = product_current.find("div", class_="price-box price-final_price")
                                    special = ""
                                    old = ""
                                    unique_price = ""
                                    try:
                                        special = new_old.find("span", class_="special-price").find("span", class_="price-wrapper").find("span", class_="price").text
                                        old = new_old.find("span", class_="old-price").find("span", class_="price-wrapper").find("span", class_="price").text
                                    except Exception as e:
                                        unique_price = new_old.find("span", class_="price").text
                                    #hacer peticion
                                    pageHref = _get_page(url_product)
                                    form = pageHref.find("form", id="product_addtocart_form")
                                    if form:
                                        stock = form.find("div", class_="box-tocart hiraoka-controls").find("h3",class_="conteo-cart").text    
                                    div_with_table = pageHref.find("div", class_="xpec-tab hiraoka-product-details-datasheet cambio-prueba")
                                    if div_with_table:
                                        table = div_with_table.find("table")
                                        data_dict = {}
                                        thead = table.find("thead")
                                        if thead:
                                            header_row = thead.find("tr")
                                            header_cells = header_row.find_all("th")
                                            headers = [cell.get_text() for cell in header_cells]
                                        tbody = table.find("tbody")
                                        if tbody:
                                            data_rows = tbody.find_all("tr")
                                            for row in data_rows:
                                                data_cells = row.find_all("td")
                                                details = [cell.get_text() for cell in data_cells]
                                                data_entry = dict(zip(headers, details))
                                                data_dict[row.get_text()] = data_entry
                                    ficha_tecnica = "FICHA TECNICA:\n"
                                    for key, value in data_dict.items():
                                        ficha_tecnica += f"Atributo: {value['Atributo']}\n"
                                        ficha_tecnica += f"Detalle: {value['Detalle']}\n"
                                    print(f"    -> CAPTURANDO DATOS DEL PRODUCTO : {name}")
                                    print(f"    -> CAPTURANDO URL : {url_product}")
                                    print(f"    -> CAPTURANDO PRECIO ESPECIAL : {special}")
                                    print(f"    -> CAPTURANDO PRECIO ANTIGUO : {old}")
                                    print(f"    -> CAPTURANDO STOCK : {stock}")
                                    print(f"    ->{ficha_tecnica}")   
                                    products = {
                                    'code': code,
                                    'url_image': url_image,
                                    'url_product': url_product,
                                    'product': cat[0] if len(cat) > 0 else '',
                                    'brand': b_prod,
                                    'name_product': name,
                                    'special_price': special if special != "" else unique_price,
                                    'old_price': old,
                                    "sub_category":subcategory_name,
                                    "main_category":category,
                                    "stock":stock,
                                    "ficha_tecnica":ficha_tecnica
                                    }
                                    lstProducts.append(products)
                                   
            print("-> Total Productos encontrados : ",len(lstProducts))
            if len(lstProducts) <= 0:
                print("-> No se encontraron productos")
            else:
                if excel_by_category(lstProducts):
                    print("---> EXCEL DE PRODUCTOS CREADO, REVISA TU ESCRITORIO")
                else:
                    print("---> FALLÓ AL CREAR EL EXCEL DE PRODUCTOS")
        except Exception as e:
            print(f"-> No hay productos en la página jehe")
    except Exception as e:
            print(f"-> No hay productos en la página)")


price_products_by_brand(search_brands)
price_products_by_category()

#input("Presione ENTER para salir...")