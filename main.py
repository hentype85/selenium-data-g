import time
import json
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver_options = Options()
driver_options.add_argument('--headless') # no abrir interfaz grafica
driver_options.add_argument('--no-sandbox')  # no usar sandbox para correr en docker
driver_options.add_argument('--disable-dev-shm-usage')  # no usa memoria compartida
driver_options.add_argument("--disable-notifications")  # deshabilita las notificaciones

# servicio de Chrome
chrome_path = '/usr/bin/google-chrome'  # especificar la ruta al ejecutable de Chrome
service = Service(ChromeDriverManager().install(), chrome_path=chrome_path)

# inicializar el driver de Chrome
driver = webdriver.Chrome(service=service, options=driver_options)

# website en alquiler de inmuebles
website = "https://www.gallito.com.uy"
time.sleep(2)

driver.get(website)
driver.maximize_window()

time.sleep(4)

# elemento del menu
elemento = driver.find_element(By.XPATH, '//*[@id="cat_inmuebles_li"]/a')
# mueve el mouse sobre el elemento para desplegar menu
action = ActionChains(driver)
action.move_to_element(elemento).perform()

time.sleep(2)

# click en el menu de alquileres
menu_alquileres = driver.find_element(By.XPATH, '//div[@id="cat_inmuebles"]/div[2]/ul/li[2]/h3/a')
urlalquileres = menu_alquileres.get_attribute("href")
driver.get(urlalquileres)

time.sleep(2)

# seleccionar zona
seleccionarDep = driver.find_element(By.XPATH, '//*[@id="Div_Departamentos"]/li[1]/a')
selecDepart = seleccionarDep.get_attribute("href")
driver.get(selecDepart)

time.sleep(2)

# boton avanzar de pagina con zona filtrada
avanzar_pag = driver.find_element(By.XPATH, '//*[@id="paginador"]/ul/li[6]/a')
custom_avanzar = avanzar_pag.get_attribute("href")

# lista en la que se van a guardar los datos de cada publicacion
lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
for i in range(0, 1):

    if i > 0:
        # se crea url cambiando el último char de la url
        custom_url_avanzando = f"{custom_avanzar[:-1]}{i + 1}"
        driver.get(custom_url_avanzando)
        time.sleep(2)

    # captura la lista de elementos de alquiler
    lst_alquiler = driver.find_elements(By.XPATH, '//div[3]/div[1]/div/div[1]/a')

    # creo una lista con las urls para que no pierda la informacion al hacer el back()
    urls_alquiler = []
    for alquiler in lst_alquiler:
        url_alquiler = alquiler.get_attribute('href')
        urls_alquiler.append(url_alquiler)

    # abre cada uno de los URL de alquileres
    for j, url_alquiler in enumerate(urls_alquiler):
        driver.get(url_alquiler)
        time.sleep(2)

        # imprimir pagina y alquiler en el que se encuentra el driver
        # print(f"página: {i} alquiler: {j} url: {url_alquiler}")

        # capturar informacion de URL abierta
        try:
            id = "gallito_{}".format(url_alquiler.split("-")[-1])
            precioString = driver.find_element(By.XPATH, '//div[@id="div_datosBasicos"]/div[2]/span').text
            precio = float(precioString.split(" ")[-1].replace(".", ""))
            moneda = precioString.split(" ")[0]
            if moneda == '$U':
                moneda = 'UYU'
            elif moneda == 'U$S':
                moneda = 'USD'

        except Exception:
            pass
        try:
            title = driver.find_element(By.XPATH, '//div[@id="div_datosBasicos"]/h1').text
        except Exception:
            title = ""
            pass
        try:
            departamento = driver.find_element(By.XPATH, '//*[@id="ol_breadcrumb"]/li[5]/a').text
            zona = driver.find_element(By.XPATH, '//*[@id="ol_breadcrumb"]/li[6]/a').text
        except Exception:
            pass
        try:
            tipo_propiedad = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[1]/p').text
        except:
            tipo_propiedad = ""
        try:
            lst_amenities_elements = driver.find_elements(By.XPATH, '//div[@id="div_datosOperacion"]/div//p')
            lst_comodidades = [amenity.text for amenity in lst_amenities_elements]
        except Exception:
            pass
        try:
            dormitorios = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[4]/p').text.split()[0]
        except Exception:
            dormitorios = 0
            pass
        try:
            time.sleep(1)
            # capturar informacion de galeria de imagenes
            lst_imgs = driver.find_elements(By.XPATH, '//*[@id="divInner_Galeria"]/div/a/picture/img')
            img_urls = [img.get_attribute("src") for img in lst_imgs]
        except Exception:
            img_urls = []
            pass
        try:
            # voy a seccion de ubicacion
            place_map = driver.find_element(By.XPATH, '//*[@id="ulNavGaleria"]/li[4]/a')
            place_map.click()
            time.sleep(3.5)

            url_map = driver.find_element(By.XPATH, '//*[@id="iframeMapa"]')
            src = url_map.get_attribute('src')
            lat = src.split("=")[2].split(",")[0][:11]
            lon = src.split("=")[2].split(",")[-1][:11]
        except Exception:
            lat = 0
            lon = 0
            pass

        # guardar informacion en diccionario
        try:
            dic_alquiler = {
                "id": id,
                "title": str(title),
                "url_link": url_alquiler,
                "origin": "gallito",
                "operation_type": "Alquiler",
                "price": precio,
                "currency": str(moneda),
                "state_name": departamento,
                "zone_name": zona,
                "property_type": tipo_propiedad,
                "amenities": lst_comodidades,
                "location": {
                    "latitude": float(lat),
                    "longitude": float(lon)
                },
                "images": img_urls
            }
            lst_data.append(dic_alquiler)
        except Exception:
            pass

        # abrir enlace
        if i == 0:
            # volver pagina 0 de alquileres
            driver.get(selecDepart)
        else:
            # volver pagina distinta a 0
            driver.get(custom_url_avanzando)

        time.sleep(2)

# cerrar driver
driver.quit()

# si hay datos en la lista, insertar en mongoDB
if lst_data:
    # conexion a mongoDB
    client = pymongo.MongoClient("mongodb+srv://martinleiro9:0Sy5H7XRFtSt26oY@cluster0.x2m2b2x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["db_g"]
    collection = db["gallito"]
    # borrar todos los datos
    collection.delete_many({})
    # insertar datos
    collection.insert_many(lst_data)
