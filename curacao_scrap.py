from utils.curacao_url import get_categories_curacao, _generate_url, _get_detail_prod
from utils.constants import _get_page
from utils.convert_excel import excel_by_category_curacao, excel_detail_prod

def main():
    try:
        lstProducts = []
        response = get_categories_curacao()
        if len(response) <= 0:
                print("No se encontraron categorias")
                return
        print("-> Iniciando el proceso de scraping de productos")
        
        page_current = 1
        get_detail_first_prod = False
        #while True:
        
        for cat in response:
            name_cat = cat['category']
            lst_subcategories = cat['subcategories']
            for sub_cat in lst_subcategories:
                name_subcat = sub_cat['name']
                url_subcat = sub_cat['url']
                url_gen =  _generate_url(url_subcat, page_current)
                page = _get_page(url_gen)
                lst_products = page.find_all('li', class_=lambda x: x and 'item product product-item' in x)
                print(f"--> |{name_cat.upper()}| {len(lst_products)} productos obtenidos de la subcategoria : {name_subcat}")
                for item in lst_products:
                    url_product = item.find("a").get("href")
                    url_image = item.find("img").get("src")
                    #detalle del primer producto
                    if not get_detail_first_prod:
                        print("Obteniendo detalle del primer producto encontrado...")
                        get_detail_first_prod = True
                        detail = _get_detail_prod(url_product)
                        sku = detail.find("div", class_="value").text.strip()
                        tbl = detail.find("table", class_="data table additional-attributes")
                        if tbl is not None:
                            rows = tbl.find("tbody").find_all("tr")
                            detail_complete = [
                                {
                                    "code": sku,
                                    "td1": row.find_all("th")[0].text.strip(), 
                                    "td2": row.find_all("td")[0].text.strip()
                                }
                                for row in rows if len(row.find_all("th")) >= 1
                            ]
                            print("-> Detalle del primer producto guardado")
                        else:
                            print("No se encontró la tabla de especificaciones")
                    else:
                        try:
                            sku = item.find("div", class_="actions-primary").find("form").get("data-product-sku").strip()
                        except Exception as e:
                            #detail = _get_detail_prod(url_product)
                            #print("Obteniendo SKU de producto sin stock")
                            #sku = detail.find("div", class_="value").text.strip()
                            sku = "PRODUCTO SIN STOCK"
                    product_current = item.find("div", class_="product details product-item-details")
                    try:
                        b_prod = product_current.find("div", class_="product-item-brand").find("span", class_="brand-name").text.strip()
                    except Exception as e:
                        b_prod = "-"
                    
                    name = product_current.find("a", class_="product-item-link").text.strip()
                    
                    prices_prod = product_current.find("div", class_="price-box price-final_price")
                    # Para almacenar los precios
                    special_price = "-"
                    old_price = "-"
                    unique_price = "-"
                    try:
                        special_price = prices_prod.find("span", class_="special-price").find("span", class_="price-wrapper ").find("span", class_="price").text.strip()
                        #print("special_price: OK")
                        old_price = prices_prod.find("span", class_="old-price").find("span", class_="price-wrapper ").find("span", class_="price").text.strip()
                        #print("old_price: OK")
                    except Exception as e:
                        unique_price = prices_prod.find("span", class_="price").text.strip()
                        #print("unique_price: OK")
                    
                    products = {
                        'code': sku,
                        'url_image': url_image,
                        'url_product': url_product,
                        'category': name_cat,
                        'subcategory': name_subcat,
                        'brand': b_prod,
                        'name_product': name,
                        'special_price': special_price,
                        'old_price': old_price,
                        'final_price' : unique_price
                    }
                    lstProducts.append(products)
        print("-> Total Productos encontrados : ",len(lstProducts))
        if len(lstProducts) <= 0:
            print("-> No se encontraron productos")
        else:
            print("-> Organizando productos por categoría, espere un momento...")
            if excel_by_category_curacao(lstProducts):
                print("---> EXCEL DE PRODUCTOS CREADO, REVISA TU ESCRITORIO")
                if len(detail_complete) >= 1:
                    print("-> Organizando detalle de productos, espere un momento...")
                    if excel_detail_prod(detail_complete):
                        print("---> EXCEL DE DETALLE DE PRODUCTOS CREADO, REVISA TU ESCRITORIO")
                    else:
                        print("---> FALLÓ AL CREAR EL EXCEL DE DETALLE DE PRODUCTOS")
            else:
                print("---> FALLÓ AL CREAR EL EXCEL DE PRODUCTOS")
    except Exception as e:
        print("Error en el proceso: ", str(e))
        return

main()

#input("Presione ENTER para salir...")