import pandas as pd
import datetime
import os

def excel_by_brand(products: []):
    try:
        # Crear un archivo Excel en el escritorio del user.
        desktop_location = os.path.join(os.path.expanduser('~'), 'Desktop')
        date_time_current = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name_file = f'Products_By_Brand_{date_time_current}.xlsx'
        file_path = os.path.join(desktop_location, name_file)
        print("file_path : ",file_path)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframes_by_brand = {} # hojas de excel por marca
        for item in products:
            brand = item['brand']
            if brand not in dataframes_by_brand:
                dataframes_by_brand[brand] = pd.DataFrame(columns=['Código del Producto', 'URL de Imagen', 'URL del Producto', 'Categoría', 'Marca', 'Nombre del Producto', 'Precio Especial', 'Precio Anterior'])
        # llenar hoja
        for item in products:
            brand = item['brand']
            data_dict = {
                'Código del Producto': item['code'],
                'URL de Imagen': item['url_image'],
                'URL del Producto': item['url_product'],
                'Categoría': item['category'],
                'Marca': item['brand'],
                'Nombre del Producto': item['name_product'],
                'Precio Especial': item['special_price'],
                'Precio Anterior': item['old_price']
            }
            df = pd.DataFrame([data_dict])
            dataframes_by_brand[brand] = pd.concat([dataframes_by_brand[brand], df], ignore_index=True)
        
        for brand, df in dataframes_by_brand.items():
            df.to_excel(excel_writer, sheet_name=brand, index=False)
        # Cerrar el libro de trabajo y guardar.
        excel_writer.close()
        return True
    except Exception as e:
        print("Error al crear el archivo Excel: ", e)
        return False

def excel_by_category(products: []):
    try:
        # Crear un archivo Excel en el escritorio del user.
        desktop_location = os.path.join(os.path.expanduser('~'), 'Desktop')
        date_time_current = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name_file = f'Products_By_Category_{date_time_current}.xlsx'
        file_path = os.path.join(desktop_location, name_file)
        print("file_path : ",file_path)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframes_by_main_category = {} # hojas de excel por marca
        for item in products:
            main_category = item['main_category']
            if main_category not in dataframes_by_main_category:
                dataframes_by_main_category[main_category] = pd.DataFrame(columns=['Código del Producto', 'URL de Imagen', 'URL del Producto', 'Marca', 'Nombre del Producto', 'Precio Especial', 'Precio Anterior'])
        # llenar hoja
        for item in products:
            main_category = item['main_category']
            data_dict = {
                'Código del Producto': item['code'],
                'URL de Imagen': item['url_image'],
                'URL del Producto': item['url_product'],
                'Producto': item['product'],
                'Marca': item['brand'],
                'Nombre del Producto': item['name_product'],
                'Precio Especial': item['special_price'],
                'Precio Anterior': item['old_price'],
                'SubCategoria' : item['sub_category'],
                'Categoria Principal' : item['main_category'],
                'stock': item['stock'],
                'Ficha Tecnica' : item['ficha_tecnica']
            }
            df = pd.DataFrame([data_dict])
            dataframes_by_main_category[main_category] = pd.concat([dataframes_by_main_category[main_category], df], ignore_index=True)
        
        for main_category, df in dataframes_by_main_category.items():
            df.to_excel(excel_writer, sheet_name=main_category, index=False)
        # Cerrar el libro de trabajo y guardar.
        excel_writer.close()
        return True
    except Exception as e:
        print("Error al crear el archivo Excel: ", e)
        return False



def excel_by_category_ripley(products: []):
    try:
        desktop_location = os.path.join(os.path.expanduser('~'), 'Desktop')
        date_time_current = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name_file = f'Products_By_Category_{date_time_current}.xlsx'
        file_path = os.path.join(desktop_location, name_file)
        print("Ubicación de descarga : ",file_path)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframes_by_cat = {} # hojas de excel por categoria
        for item in products:
            category = item['category']
            if category not in dataframes_by_cat:
                dataframes_by_cat[category] = pd.DataFrame(columns=['Código del Producto','URL de Imagen', 'URL del Producto', 'Categoría', 'Subcategoría', 'Marca', 'Nombre del Producto', 'Precio Normal', 'Precio Internet', 'Precio Ripley'])
        # llenar hoja
        for item in products:
            cateogry = item['category']
            data_dict = {
                'Código del Producto': item['code'],
                'URL de Imagen': item['url_image'],
                'URL del Producto': item['url_product'],
                'Categoría': item['category'],
                'Subcategoría': item['subcategory'],
                'Marca': item['brand'],
                'Nombre del Producto': item['name_product'],
                'Precio Normal': item['normal_price'],
                'Precio Internet': item['internet_price'],
                'Precio Ripley': item['ripley_price']
            }
            df = pd.DataFrame([data_dict])
            dataframes_by_cat[cateogry] = pd.concat([dataframes_by_cat[cateogry], df], ignore_index=True)
        
        for category, df in dataframes_by_cat.items():
            df.to_excel(excel_writer, sheet_name=category, index=False)
        # Cerrar el libro de trabajo y guardar.
        excel_writer.close()
        return True        
    except Exception as e:
        print("Error al crear el archivo Excel: ", e)
        return False
    
def excel_detail_prod(details: []):
    try:
        desktop_location = os.path.join(os.path.expanduser('~'), 'Desktop')
        date_time_current = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name_file = f'Detail_Product_By_SKU_{date_time_current}.xlsx'
        file_path = os.path.join(desktop_location, name_file)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframes_by_sku = {} # hojas de excel por categoria
        for item in details:
            sku = item['code']
            if sku not in dataframes_by_sku:
                dataframes_by_sku[sku] = pd.DataFrame(columns=['Especificaciones', 'Detalle'])
        # llenar hoja
        for item in details:
            sku = item['code']
            data_dict = {
                'Especificaciones': item['td1'],
                'Detalle': item['td2']
            }
            df = pd.DataFrame([data_dict])
            dataframes_by_sku[sku] = pd.concat([dataframes_by_sku[sku], df], ignore_index=True)
        
        for sku, df in dataframes_by_sku.items():
            df.to_excel(excel_writer, sheet_name=sku, index=False)
        # Cerrar el libro de trabajo y guardar.
        excel_writer.close()
        return True        
    except Exception as e:
        print("Error al crear el archivo Excel: ", e)
        return False

def excel_by_category_curacao(products: []):
    try:
        desktop_location = os.path.join(os.path.expanduser('~'), 'Desktop')
        date_time_current = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name_file = f'Products_By_Category_Curacao_{date_time_current}.xlsx'
        file_path = os.path.join(desktop_location, name_file)
        print("Ubicación de descarga : ",file_path)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframes_by_cat = {} # hojas de excel por categoria
        for item in products:
            category = item['category']
            if category not in dataframes_by_cat:
                dataframes_by_cat[category] = pd.DataFrame(columns=['Código del Producto','URL de Imagen', 'URL del Producto', 'Categoría', 'Subcategoría', 'Marca', 'Nombre del Producto', 'Precio Especial', 'Precio Anterior', 'Precio Final'])
        # llenar hoja
        for item in products:
            cateogry = item['category']
            data_dict = {
                'Código del Producto': item['code'],
                'URL de Imagen': item['url_image'],
                'URL del Producto': item['url_product'],
                'Categoría': item['category'],
                'Subcategoría': item['subcategory'],
                'Marca': item['brand'],
                'Nombre del Producto': item['name_product'],
                'Precio Especial': item['special_price'], #if item['special_price'] != "-" else item['final_price'],
                'Precio Anterior': item['old_price'],
                'Precio Final': item['final_price']
            }
            df = pd.DataFrame([data_dict])
            dataframes_by_cat[cateogry] = pd.concat([dataframes_by_cat[cateogry], df], ignore_index=True)
        
        for category, df in dataframes_by_cat.items():
            df.to_excel(excel_writer, sheet_name=category, index=False)
        # Cerrar el libro de trabajo y guardar.
        excel_writer.close()
        return True        
    except Exception as e:
        print("Error al crear el archivo Excel: ", e)
        return False
    
def create_excel_by_category(products: [], columns: [], store: str):
    try:
        desktop_location = os.path.join(os.path.expanduser('~'), 'Desktop')
        date_time_current = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name_file = f'Products_By_Category_{store}_{date_time_current}.xlsx'
        file_path = os.path.join(desktop_location, name_file)
        print("Ubicación de descarga : ",file_path)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        dataframes_by_cat = {} # hojas de excel por categoria
        for item in products:
            category = item['category']
            if category not in dataframes_by_cat:
                dataframes_by_cat[category] = pd.DataFrame(columns=columns)
        # llenar hoja
        for item in products:
            cateogry = item['category']
            data_dict = {}
            for i, column in enumerate(columns):
                data_dict[column] = item[i] #item[column.lower().replace(' ', '_')]
            df = pd.DataFrame([data_dict])
            dataframes_by_cat[cateogry] = pd.concat([dataframes_by_cat[cateogry], df], ignore_index=True)
        
        for category, df in dataframes_by_cat.items():
            df.to_excel(excel_writer, sheet_name=category, index=False)
        # Cerrar el libro de trabajo y guardar.
        excel_writer.close()
        return True        
    except Exception as e:
        print("Error al crear el archivo Excel: ", e)
        return False    
