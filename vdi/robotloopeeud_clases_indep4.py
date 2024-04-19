import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import fitz
import re
import re
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
from BotEIRL import EIRL
from BotLTDA import LTDA
from BotSPA_Mod import SPA_Mod
from BotEIRL_Disoluciuon import EIRL_DIS
from BotSPA1 import SPA
import certifi
###PROXY#########

class rpadiarioe1d:


    def __init__(self):

        pass

    def ejecutar(self):

        def conectar_a_instancia_existente():
            try:
                # Intenta conectar a una instancia existente si hay una
                driver = webdriver.Chrome(options=chromeOptions)
                print("Conectado a una instancia existente.")
                return driver
            except Exception as e:
                print(f"No se pudo conectar a la instancia existente. Creando una nueva. Error: {str(e)}")
                return None

        def resolver_captcha():
            api_key = "352fe691ec16b2b5ff9210c255904496"
            sitekey = "6Ldg2F8UAAAAABeObtL-07JwAW0bYWI_j2rgz21u"
            url = "https://www.registrodeempresasysociedades.cl/VerificarCertificados.aspx"

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
                    driver.find_element(By.XPATH, '//*[@id="boxer_content_lnkValidarCVE"]').click()
                    break
            else:
                raise SystemExit('Error: No se pudo resolver el captcha en el tiempo especificado.')



        borrararchivos= os.listdir('./descargas/')
        try:
            for archivos in borrararchivos:
                os.remove('./descargas/'+archivos)

            print("Archivos borrados...")
        except:
            print("no hay archivos por borrar")
            pass





        df= pd.read_pickle('./robot4.pkl')

        df = df.drop_duplicates(subset=['Numero'], keep='first')
        df = df[(df["status"] != "Cargado") & (df["status"] != "Error") & (df["status"] != "existe")]
        df=df.reset_index(drop=True)

        uri = "mongodb+srv://vuserservices-v1:admin123@cluster0.zoxch51.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        db = client["bbddruts"]
        collection = db["rutscollection"]





        def carga_json(ruta_json):
            try:
            # Cargar datos desde el archivo JSON
                with open(ruta_json, 'r', encoding='utf-8') as file:
                    try:
                        file_data = json.load(file)
                    except json.JSONDecodeError as json_error:
                        print(f"Error al decodificar JSON: {json_error}")
                        raise  

                if isinstance(file_data, dict):
                    # Obtén el valor de 'rut' del documento
                    rut = file_data.get("data", {}).get("estado", {}).get("rut", None)

                    if rut:
                        # Intenta encontrar el documento existente por el valor de 'rut'
                        existing_document = collection.find_one({"data.estado.rut": rut})

                        # Si existe, actualiza el documento
                        if existing_document:
                            collection.update_one({"data.estado.rut": rut}, {"$set": file_data})
                            print(f"Documento con rut {rut} actualizado correctamente.")
                        else:
                            # Si no existe, inserta uno nuevo
                            collection.insert_one(file_data)
                            print(f"Nuevo documento con rut {rut} insertado correctamente.")
                        
                        df.loc[index, "status"] = "Cargado"
                        df.to_pickle(ruta_pickle)

                else:
                    print(f"El archivo {ruta_json} no contiene un objeto de datos válido.")

            except Exception as e:
                print(f"Hubo un error: {e}")
                df.loc[index, "status"] = "Error"
                df.to_pickle(ruta_pickle)
        



        #3######CHROMEDRIVER


        #direccion de descarga para cambio de nombre:
        pathdescarga = "./"

        capabilities=DesiredCapabilities().CHROME

        prefs = {
            "download.default_directory": "C:\\Users\\Administrator\\Desktop\\indep4\\descargas",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "pdfjs.disabled": True,
            'profile.default_content_setting_values':
            {
                'automatic_downloads': 1,
                'zoom_factor': 0.8  # Establecer el nivel de zoom al 80%
            },
            'profile.content_settings.exceptions':
            {
                'automatic_downloads': 1
            },
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}]
        }

        chromeOptions = Options()
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
        chromeOptions.add_argument("--disable-web-security")  # Puede ser necesario desactivar la seguridad web
        chromeOptions.add_experimental_option("detach", True)
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.add_argument("start-maximized")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--disable-popup-blocking")

        # Intenta conectar a una instancia existente



        #chromeOptions.add_argument("--disable-gpu")
        #chromeOptions.add_argument("--disable-software-rasterizer")


        driver = conectar_a_instancia_existente()

        fecha_actual = datetime.now().strftime("%d-%m-%Y")

        if driver is None:
            print("Creando una nueva instancia de chromedriver.")
            driver = webdriver.Chrome(options=chromeOptions)


        #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)
        ####FINCHROMEDRIVER

        ruta_pickle= './robot4.pkl'
        x=0

        driver.get('https://www.registrodeempresasysociedades.cl/VerificarCertificados.aspx')
        time.sleep(1)

        
        try:
            print("empezando el try")
            open("./bloquear/bloqueo.txt", "w").close()
            print("creado el bloqueo")
            for index, row in df.iterrows():
                print("empezanod iteracion")

                driver.get('https://www.registrodeempresasysociedades.cl/VerificarCertificados.aspx')


                cve=row["OtroCampo2"]
                rut=row["Numero"]
                print(cve)
                print(rut)

                existing_document = collection.find_one({"data.estado.rut": rut})
                """
                if existing_document:
                    collection.delete_many({"data.estado.rut": rut})
                else:
                    pass
                """
                existing_document = collection.find_one({"data.estado.rut": rut})
                if existing_document:
                    print("ya Existe el RUT")
                    df.loc[index, "status"] ="existe"
                    df.to_pickle(ruta_pickle)
                    


                else:


                    waitbusqueda= W(driver,10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="boxer_content_txtCve"]'))
                    )
                    print('wait a que esté el campo habilitado')
                    driver.find_element(By.XPATH, '//*[@id="boxer_content_txtCve"]').send_keys(cve)
                    iframe = driver.find_element(By.ID, "athenaChatWindow")

                    # Ocultar el elemento de chat utilizando JavaScript
                    driver.execute_script("arguments[0].style.visibility='hidden';", iframe)

                    resolver_captcha()
                    time.sleep(1)

                    url = driver.current_url
                    response = requests.get(url)

                    with open('./descargas/pdfactual.pdf', 'wb') as f:
                        f.write(response.content)
                            
                    while True:
                        archivos = os.listdir('./descargas')
                        if archivos:

                            break
                        else:
                            time.sleep(5)
                            print("Esperando a que se descargue el archivo...")
                    
                    time.sleep(1)

                    
                    archivos= os.listdir('./descargas')[0]
                    print(f'descargado: {archivos}')

                    intentos=0
                    intentos_maximos=5
                    nombrearchivo=archivos

                    while intentos < intentos_maximos:
                        try:
                            doc = fitz.open('./descargas/' + nombrearchivo)
                            salida = open('./descargas/' + nombrearchivo + ".txt", "wb")
                            break  # Sale del bucle si la apertura es exitosa
                        except Exception as e:
                            print(f"Error al abrir el archivo: {e}")
                            intentos += 1
                            time.sleep(5)

                            if intentos == intentos_maximos:
                                os.remove('./descargas/'+archivos)
                                url = driver.current_url
                                response = requests.get(url)
                                time.sleep(1)

                                with open('./descargas/pdfactual.pdf', 'wb') as f:
                                    f.write(response.content)

                    


                    for pagina in doc:
                        text=pagina.get_text().encode("utf8")
                        salida.write(text)
                        salida.write(b'\n------\n')

                    doc.close()
                    salida.close()

                    # Leer el contenido del archivo de texto
                    with open('./descargas/'+nombrearchivo+'.txt', 'r', encoding='utf-8') as file:
                        content = file.read()
                    time.sleep(1)
                    os.remove('./descargas/'+nombrearchivo+".txt")
                    print(f"se elimina {nombrearchivo}")
                    # Limpiar el texto completo
                    content = re.sub(r'\s+', ' ', content).strip()
                    content = re.sub(r'Página\s+\d+\s+de.*?------', '', content, flags=re.DOTALL)
                    content = re.sub(r'\s\s', ' ', content, flags=re.DOTALL)


                    
                    match_EIRL=None
                    match_SPA=None
                    match_LTDA=None
                    Search_PJ = re.search(r'DE (SOCIEDAD POR ACCIONES|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA) (.*?)(SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|(?:.*?LIMITADA))', content, re.DOTALL)
                    try:
                        Search_PJ=Search_PJ.group(3)


                        if "EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA" in Search_PJ :
                            match_EIRL=re.search(r'EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA',Search_PJ, re.DOTALL)

                        elif "SpA" in Search_PJ :

                            match_SPA=re.search(r'SpA',Search_PJ, re.DOTALL)

                        elif  ("SOCIEDAD DE RESPONSABILIDAD LIMITADA" in Search_PJ)  or ("LIMITADA" in Search_PJ) and (match_EIRL==None):   

                            match_LTDA = re.search(r'(\bSOCIEDAD DE RESPONSABILIDAD LIMITADA\b|(\b(?!EMPRESA INDIVIDUAL DE RESPONSABILIDAD)LIMITADA\b))', Search_PJ, re.DOTALL)

                        else:
                            pass

                        print(f'Match SearchPJ:{Search_PJ}')
                        print(f'Match EIRL:{match_EIRL}')
                        print(f'Match SPA:{match_SPA}')
                        print(f'Match LTDA:{match_LTDA}\n')
                        

                        estado_empresav2= re.search(r'(.*?)DE', content, re.DOTALL).group(1)
                        
                        print(f"Este es el CVE que se procesará: {cve}")
                        
                        if match_EIRL is not None and estado_empresav2 != "DISOLUCIÓN":
                            try:
                                print(match_EIRL)
                                print("Comienza EIRL")
                                eirl_instance = EIRL()  
                                eirl_instance.ejecutar()
                                print("ok EIRL")
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                nombrejson= os.listdir('./jsons')[0]
                                ruta_json = './jsons/'+nombrejson
                                carga_json(ruta_json)
                                os.remove('./jsons/'+nombrejson)
                                print("creadooo")
                            except:
                                df.loc[index, "status"] ="Error"
                                df.to_pickle(ruta_pickle)
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                print("errorrr")
                                pass
                        else:
                            pass


                        if match_EIRL is not None and estado_empresav2 == "DISOLUCIÓN":
                            try:
                                print(match_EIRL)
                                print("Comienza EIRL")
                                eirl_instance = EIRL_DIS()  
                                eirl_instance.ejecutar()
                                print("ok EIRL")
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                nombrejson= os.listdir('./jsons')[0]
                                ruta_json = './jsons/'+nombrejson
                                carga_json(ruta_json)
                                os.remove('./jsons/'+nombrejson)
                                print("creaado")
                            except:
                                df.loc[index, "status"] ="Error"
                                df.to_pickle(ruta_pickle)
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                print("huboi error")
                                pass
                        else:
                            pass


                        if match_SPA is not None and estado_empresav2!="MODIFICACIÓN":
                            try:
                                print(match_SPA)
                                print("Comienza SPA")
                                spa_instance = SPA()  
                                spa_instance.ejecutar()
                                print("ok SPA")
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                nombrejson= os.listdir('./jsons')[0]
                                ruta_json = './jsons/'+nombrejson
                                carga_json(ruta_json)
                                os.remove('./jsons/'+nombrejson)
                            except:
                                df.loc[index, "status"] ="Error"
                                df.to_pickle(ruta_pickle)
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                print("huboi error")

                                pass
                        else:
                            pass


                        if match_SPA is not None and estado_empresav2 =="MODIFICACIÓN":
                            try:
                                print(match_SPA)
                                print("Comienza SPA_Mod")
                                spa_mod_instance = SPA_Mod()  
                                spa_mod_instance.ejecutar()
                                print("ok SPA")
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                nombrejson= os.listdir('./jsons')[0]
                                ruta_json = './jsons/'+nombrejson
                                carga_json(ruta_json)
                                os.remove('./jsons/'+nombrejson)
                            except:
                                df.loc[index, "status"] ="Error"
                                df.to_pickle(ruta_pickle)
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                print("huboi error")

                                pass
                        else:
                            pass


                        if match_LTDA:
                            try:
                                print(match_LTDA)

                                print("Comienza LTDA")
                                ltda_instance = LTDA()  
                                ltda_instance.ejecutar()
                                print("ok LTDA")
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                nombrejson= os.listdir('./jsons')[0]
                                ruta_json = './jsons/'+nombrejson
                                carga_json(ruta_json)
                                os.remove('./jsons/'+nombrejson)                    
                            except:
                                df.loc[index, "status"] ="Error"
                                df.to_pickle(ruta_pickle)
                                os.remove('./descargas/'+archivos)
                                os.remove('./descargas/'+archivos+".txt")
                                print("huboi error")

                                pass                

                        else:
                            pass

                    except:

                        df.loc[index, "status"] = "Error"   
                        df.to_pickle(ruta_pickle)
                        print("errorrr aqui")
            driver.quit()
            os.remove("./bloquear/bloqueo.txt")
            ruta_archivo_original = os.path.join('./', 'robot4.pkl')
            ruta_archivo_nuevo = os.path.join('./listos/', f'{fecha_actual}.pkl')
            os.rename(ruta_archivo_original, ruta_archivo_nuevo)

        except  Exception as e:
            print("removiendobloqueo:::::::::::")
            os.remove("./bloquear/bloqueo.txt")
            driver.quit()

            print(e)
            
            pass


if __name__ == "__main__":
    rpadiarioe1d_instance = rpadiarioe1d()
    rpadiarioe1d_instance.ejecutar()



