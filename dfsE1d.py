import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import openpyxl as O
import datetime
import os
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from datetime import datetime, timedelta

hoy = datetime.now() -timedelta(days=48)



#3######CHROMEDRIVER
inicioscript= datetime.now()

hoy= datetime.now()

formateada= hoy.strftime("%d-%m-%Y") #fecha que cambiará
today= hoy.strftime("%d-%m-%Y") #fecha real 
diaformateada= int(hoy.strftime("%d"))
diahoy=int(hoy.strftime("%d"))


#direccion de descarga para cambio de nombre:
pathdescarga = "./"

capabilities=DesiredCapabilities().CHROME

prefs = {

    "download.default_directory": "/dev/null",  # Configurar la carpeta de descarga como nula
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": False,
    'profile.default_content_seting_values':    
         {
              'automatic_downloads': 0     
         },
         'profile.content_settings.exceptions':
         {
              'automatic_downloads':0
         }
        }

chromeOptions = Options()
chromeOptions.add_experimental_option("detach", True)
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-popup-blocking")


#chromeOptions.add_argument("--disable-gpu")
#chromeOptions.add_argument("--disable-software-rasterizer")


capabilities.update(chromeOptions.to_capabilities())
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chromeOptions)
####FINCHROMEDRIVER


#df = pd.read_hdf('07082023.h5', key='data')


#ultima_fila = df.iloc[-1,0]
#ultima_fila= str(ultima_fila).split(';')[0]


hoy =  datetime.strptime('13-05-2024', '%d-%m-%Y')



iniciopromedio= datetime.now()

dias_atras = 19
x = 0
while dias_atras != 0:
    x += 1

    inicioiteracion=datetime.now()
    dias_atras = dias_atras - 1
    hoy = hoy - timedelta(days=1)
    print(hoy)
    time.sleep(10)
    fecha_variable= hoy.strftime("%d-%m-%Y")
    print(fecha_variable)
    urlcentinela="https://www.registrodeempresasysociedades.cl/BuscarActuaciones2.aspx"
    driver.get(urlcentinela)

    registroeeud= Select(driver.find_element(By.XPATH, '//*[@id="ddlTipoRegistro"]'))
    registroeeud.select_by_index(1)
    time.sleep(1)
    registroeeud= Select(driver.find_element(By.XPATH, '//*[@id="ddlTipoBusqueda"]'))
    registroeeud.select_by_index(4)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="txtFechaRegistro"]').send_keys(fecha_variable)



    api_key = "352fe691ec16b2b5ff9210c255904496"
    sitekey = "6Ldg2F8UAAAAABeObtL-07JwAW0bYWI_j2rgz21u"
    url = "https://www.registrodeempresasysociedades.cl/BuscarActuaciones2.aspx"

    # Configuración de reCAPTCHA
    data = {
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': sitekey,
        'pageurl': url,
        'json': 1
    }

    # Solicitar la resolución de reCAPTCHA a 2captcha
    response = requests.post('http://2captcha.com/in.php', data=data)
    request_result = response.json()
    if request_result['status'] != 1:
        raise SystemExit(f'Error en la solicitud a 2captcha: {request_result["request"]}')

    # Obtener el ID del captcha resuelto
    captcha_id = request_result['request']

    # Esperar a que se resuelva el captcha (puedes ajustar el tiempo de espera según sea necesario)
    for _ in range(30):  # Intentar durante 30 segundos
        time.sleep(5)  # Esperar 5 segundos entre intentos
        response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1')
        result = response.json()
        if result['status'] == 1:
            token = result['request']

            # Ejecutar un script JavaScript para establecer el valor de g-recaptcha-response
            script = f'document.getElementById("g-recaptcha-response").innerHTML="{token}";'
            driver.execute_script(script)
            time.sleep(3)

            # Hacer clic en el botón de búsqueda
            
            #print(f'Captcha resuelto. Token: {token}')
            driver.find_element(By.XPATH, '//*[@id="btnBuscar"]').click()
            break
    else:
        raise SystemExit('Error: No se pudo resolver el captcha en el tiempo especificado.')
    
    urldia = str(driver.current_url)

    time.sleep(3)




    try:
        

        waitexpandir= W(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tblSociedades_length"]/label/select'))
        )

        expandir= Select(driver.find_element(By.XPATH, '//*[@id="tblSociedades_length"]/label/select'))
        time.sleep(2)
        expandir.select_by_value("-1")
        time.sleep(5)
        html = driver.page_source
        
        soup = BeautifulSoup(html, 'html.parser')

        rows = soup.select('table#tblSociedades tbody tr')

        data = []

        for row in rows:
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            data.append(row_data)


        # Crear un DataFrame con los datos
        df = pd.DataFrame(data, columns=["Fecha", "Descripcion", "Numero", "OtroCampo", "CampoTexto", "OtroCampo2"])
  


       
        df["Numero"] = df["Numero"].str.replace(r'[^0-9K]', '', regex=True)
     
        df= df[df['Fecha'] == fecha_variable]

        archivo_pickle= "./mayo2024.pkl"
        
        if os.path.exists(archivo_pickle):
            df_existente = pd.read_pickle(archivo_pickle)

            # Concatenar el nuevo DataFrame con el existente
            df = pd.concat([df_existente, df], ignore_index=True)


            df.to_pickle(archivo_pickle)
        else:
            df.to_pickle(archivo_pickle)

            
        finiteracion= datetime.now()
        
        tiempototal= finiteracion-inicioiteracion

        tiempo_transcurrido = datetime.now() - iniciopromedio

        tiempo_promedio = tiempo_transcurrido / x   
        

        print(f'Iteración:{dias_atras}\n',
              f'Fecha Actual {fecha_variable}\n',
              f'Tiempo Iteración: {tiempototal}\n',
              f'Promedio por iteración: {tiempo_promedio}\n', 
              'Guardado...\n')


    except Exception as e:
        print("ERROR FATAL\n",f'Iteración: {dias_atras}\n',
              f'Fecha Actual {fecha_variable}\n',
              e)

finiteracion= datetime.now()
    
tiempototal= finiteracion-iniciopromedio
print(f'Tiempo total para todos los {dias_atras} registros: {tiempototal}')



print(df.tail())

 
