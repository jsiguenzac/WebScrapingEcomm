'''import os
import selenium.webdriver as _webdriver

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
edge_driver_path = os.path.join(os.getcwd(), "utils", "driver", "msedgedriver.exe")
print("edge_driver_path: ", edge_driver_path)
edge_service = _webdriver.EdgeService(edge_driver_path)
edge_options = _webdriver.EdgeOptions()
edge_options.add_argument(f"user-agent={user_agent}")

# por si cambia la ubicacion del navegador edge
#edge_options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # Ruta a tu navegador Edge

browser = _webdriver.Edge(service=edge_service, options=edge_options)
browser.maximize_window()'''



