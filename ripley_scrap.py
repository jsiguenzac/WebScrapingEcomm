from utils.ripley_url import _get_names_url_subcategories, _generate_url, _get_detail_prod, url_ripley
from utils.constants import _get_page
from utils.convert_excel import excel_by_category_ripley, excel_detail_prod

def scraper_category_ripley():
    try:
        lstProducts = []
        find_categories = _get_names_url_subcategories()
        print("-> Iniciando el proceso de scraping de productos")
        if len(find_categories) <= 0:
            print("No se encontraron categorias")
            return
        page_current = 1
        get_detail_first_prod = False
        #while True:
        # recorre las urls de categorias
        for cat in find_categories:
            name_cat = cat['category']
            lst_subcategories = cat['subcategories']
            
            for sub_cat in lst_subcategories:
                name_subcat = sub_cat['name']
                url_subcat = sub_cat['url']
                url_gen =  _generate_url(url_subcat, page_current)
                page = _get_page(url_gen)
                lst_products = page.find_all("div", class_="catalog-product-border")                    
                print(f"---> |{name_cat.upper()}| Obteniendo productos de la subcategoria : {name_subcat}")
                for item in lst_products:
                    url_product = url_ripley + item.find("a").get("href")
                    #print("url_product: ",url_product)
                    url_image = item.find("img").get("data-src")
                    #detalle del primer producto
                    if not get_detail_first_prod:
                        print("Obteniendo detalle del primer producto encontrado...")
                        get_detail_first_prod = True
                        detail = _get_detail_prod(url_product)
                        sku = detail.find("span", class_="sku sku-value").text.strip() #item.find("a").get("data-partnumber").strip()
                        tbl = detail.find("table", class_="table table-striped")
                        if tbl is not None:
                            rows = tbl.find("tbody").find_all("tr")                            
                            detail_complete = [
                                {
                                    "code": sku,
                                    "td1": row.find_all("td")[0].text.strip(), 
                                    "td2": row.find_all("td")[1].text.strip()
                                } 
                                for row in rows if len(row.find_all("td")) >= 2
                            ]
                            print("-> Detalle del primer producto guardado")
                        else:
                            print("No se encontró la tabla de especificaciones")
                    else:
                        sku = item.find("a").get("data-partnumber").strip()
                    product_current = item.find("div", class_="catalog-product-details")
                    b_prod = product_current.find("div", class_="catalog-product-name-container").find("div", class_="catalog-product-details__logo-container").find("div", class_="brand-logo").find("span").text.strip()
                    name = product_current.find("div", class_="catalog-product-details__name").text.strip()
                    price_prod = product_current.find("div", class_="catalog-product-details__prices").find("div", class_="catalog-prices").find("ul", class_="catalog-prices__list")
                    # diccionario para almacenar los precios
                    prices = {
                        "Precio Normal": "-",
                        "Precio Internet": "-",
                        "Precio Ripley": "-"
                    }
                    if price_prod:
                        #price_items = price_prod.find_all("li")
                        for price_item in price_prod:
                            price_title = price_item.get("title")
                            if price_title in prices:
                                prices[price_title] = price_item.text
                    # Accede a los precios utilizando el diccionario
                    '''normal_price = prices["Precio Normal"]
                    internet_price = prices["Precio Internet"]
                    ripley_price = prices["Precio Ripley"]
                    '''
                    products = {
                        'code': sku,
                        'url_image': url_image,
                        'url_product': url_product,
                        'category': name_cat,
                        'subcategory': name_subcat,
                        'brand': b_prod,
                        'name_product': name,
                        'normal_price': prices["Precio Normal"],
                        'internet_price': prices["Precio Internet"],
                        'ripley_price' : prices["Precio Ripley"]
                    }
                    lstProducts.append(products)
        print("-> Total Productos encontrados : ",len(lstProducts))
        if len(lstProducts) <= 0:
            print("-> No se encontraron productos")
        else:
            print("-> Organizando productos por categoría, espere un momento...")
            if excel_by_category_ripley(lstProducts):
                print("---> EXCEL DE PRODUCTOS CREADO, REVISA TU ESCRITORIO")
                print("-> Organizando detalle de productos, espere un momento...")
                if len(detail_complete) >= 1:
                    if excel_detail_prod(detail_complete):
                        print("---> EXCEL DE DETALLE DE PRODUCTOS CREADO, REVISA TU ESCRITORIO")
                    else:
                        print("---> FALLÓ AL CREAR EL EXCEL DE DETALLE DE PRODUCTOS")
            else:
                print("---> FALLÓ AL CREAR EL EXCEL DE PRODUCTOS")
    except Exception as e:
        print(f"-> error scraper : {e}")

scraper_category_ripley()

#input("Presione ENTER para salir...")