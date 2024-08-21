## Crear entorno virtual
* python -m venv scrap-env
## activar entorno virtual
* scrap-env\Scripts\activate
### pip install -r requeriments.txt
* desactivar:  deactivate
# crear ejecutable
* pyinstaller --onefile --add-data "utils;utils" ripley_scrap.py
* pyinstaller --onefile --add-data "utils;utils" curacao_scrap.py
* pyinstaller --onefile --add-data "utils;utils" scrap.py