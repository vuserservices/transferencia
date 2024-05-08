from fastapi import FastAPI, Request, HTTPException,Query
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime
from fastapi import Header
import os
from dotenv import load_dotenv, dotenv_values
import json
import time

load_dotenv()
uri = os.getenv("API_MONGO")
scrt= os.getenv("TOKEN_JWT_KEY")
ip_ruta= os.getenv("IP_RUTA")
apisant= os.getenv("API_KEY_SANTANDER")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["bbddruts"]

Collection = db["rutscollection"]
Collectionid = db["idnumbers"]
collection_ip = db["ip_solicitudes"]
limite_solicitudes_diario=5

#3######CHROMEDRIVER
inicioscript= datetime.now()

hoy= datetime.now()

formateada= hoy.strftime("%d-%m-%Y") #fecha que cambiará
today= hoy.strftime("%d-%m-%Y") #fecha real 
diaformateada= int(hoy.strftime("%d"))
diahoy=int(hoy.strftime("%d"))


def validar_api_key(api_key: str) -> bool:
    

    return api_key == apisant


app = FastAPI(
    docs_url=None, 
    redoc_url=None,
)

"""
@app.get("/")
 #el rut que buscará será siempre sin guion ni punto, hay que aplicar un replace antes de procesarlo.
async def root():
   
    
    return {"message":"Homepage"} 

"""
@app.middleware("http")
async def get_client_ip(request: Request, call_next):
    client_ip = request.client.host  #request.headers.get("X-Forwarded-For") or request.headers.get("X-Client-IP") or 
    request.state.client_ip = client_ip
    response = await call_next(request)
    return response


#validador de API FINAL
 
@app.get("/validador_rut/{id_rut}")
def leer_rut(id_rut: str, request: Request, api_key: str = Header(..., description="API")):
    if not validar_api_key(api_key):
        
        raise HTTPException(status_code=401, detail="API-KEY-ERROR")
    
    else:
        latest_record = Collectionid.find_one(sort=[("idnumber", -1)])
        idnumber_updated = latest_record["idnumber"] + 1   


        client_ip = request.state.client_ip
        client_ip = client_ip.split(":")[0]
        # Obtiene la fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Actualiza el contador de solicitudes para la dirección IP y fecha actual
        result = collection_ip.update_one(
            {"ip": client_ip, "fecha": fecha_actual,"rut":id_rut},
            {"$inc": {"solicitudes": 1}},
            upsert=True
        )


        # Buscar el documento en la base de datos
        solicitudes = collection_ip.find_one({"ip": client_ip, "fecha": fecha_actual, "rut": id_rut})

        # Obtener el número de solicitudes del documento encontrado
        if solicitudes:
            solicitud_count = solicitudes.get("solicitudes", 0)
        else:
            solicitud_count = 0

        # Verificar si se ha excedido el límite
        if solicitud_count > limite_solicitudes_diario:
            raise HTTPException(status_code=429, detail="Demasiadas solicitudes desde esta dirección IP hoy")


        if "." in id_rut or "-" in id_rut:
            id_rut = id_rut.replace(".", "").replace("-", "")
            validado="si con rut y punto"
        else:
            id_rut=id_rut
            validado="si"

        if len(id_rut) != 9:
                
            with open("errorjson.json", "r") as file:
                error_content = json.load(file)

            new_record = {
                "valid": "false",  # Reemplaza con el valor correspondiente
                "idnumber": idnumber_updated,
                "date": fecha_actual,
                "idrut": id_rut
            }
            Collectionid.insert_one(new_record)
            
            return JSONResponse(content=error_content)             


        # Verificar que el último dígito sea un número o la letra 'K' en mayúsculas o minúsculas
        if not (id_rut[-1].isdigit() or (id_rut[-1] == 'K' or id_rut[-1] == 'k')):
            with open("errorjson.json", "r") as file:
                error_content = json.load(file)

            new_record = {
                "valid": "false",  # Reemplaza con el valor correspondiente
                "idnumber": idnumber_updated,
                "date": fecha_actual,
                "idrut": id_rut
            }
            Collectionid.insert_one(new_record)
        
            return JSONResponse(content=error_content)             


        #busqueda de rut en mongo
        result= Collection.find_one({'data.estado.rut':id_rut})
        #rescata resultado unico de BBDD collectionid
        idnumber= Collectionid.find_one()

        
        # si el rut existe se trae el ID, le suma 1 y entrega el json encontrado
        if result:
            try:

                data_content = result.get("data", {})
                
                result["_id"] = str(result["_id"])

                payload = {
                    "idnumber": idnumber_updated,
                    "message": id_rut,
                    "detalle": data_content
                }

                token = jwt.encode(payload, scrt, algorithm="HS256")
                response_content = {
                    "token": token
                }
            
                new_record = {
                    "valid": "true",  # Reemplaza con el valor correspondiente
                    "idnumber": idnumber_updated,
                    "date": fecha_actual,
                    "idrut": id_rut
                }
                Collectionid.insert_one(new_record)

                return JSONResponse(content=response_content)
            
            except:

                with open("errorjson.json", "r") as file:
                    error_content = json.load(file)
                new_record = {
                    "valid": "false",  # Reemplaza con el valor correspondiente
                    "idnumber": idnumber_updated,
                    "date": fecha_actual,
                    "idrut": id_rut
                }
                Collectionid.insert_one(new_record)
                
                return JSONResponse(content=error_content)                
        

        else:
            
            with open("errorjson.json", "r") as file:
                error_content = json.load(file)
            new_record = {
                "valid": "false",  # Reemplaza con el valor correspondiente
                "idnumber": idnumber_updated,
                "date": fecha_actual,
                "idrut": id_rut
            }
            Collectionid.insert_one(new_record)
            
            return JSONResponse(content=error_content)

"""
            try:

                url = f"http://{ip_ruta}/consulta_rut/{id_rut}"

                response = requests.get(url)

                if response.status_code == 200:

                    json_response = response.json()
                    payload = {
                    "idnumber": idnumberupdated,
                    "message": id_rut,
                    "detalle": data_content
                    }

                    token = jwt.encode(payload, scrt, algorithm="HS256")

                    response_content = {
                        "token": token
                    }

                    return JSONResponse(content=response_content)

                else:
                    with open("errorjson.json", "r") as file:
                        error_content = json.load(file)
                    

                    return JSONResponse(content=error_content)
            except:
                    
                    with open("errorjson.json", "r") as file:
                        error_content = json.load(file)
                    
                    return JSONResponse(content=error_content)
            
"""


"""


@app.get("/iteracion/") #este envía rut a rut al bot qeue stará en la VDI, falta configurar el host y puerto para ahcer el request
async def iteracion(
    webdia: str = Query(..., alias="webdia"),
    ParamBusqueda1: str = Query(..., alias="ParamBusqueda1"),
    codigo: str = Query(..., alias="codigo")
):
    print(webdia)

    print(ParamBusqueda1)
    print(codigo) 

    completo = f"{webdia}&ParamBusqueda1={ParamBusqueda1}&codigo={codigo}"
    driver.get(completo)

    # Resto de tu lógica aquí

    x = 0

    try:
        print("inicio")
        
        time.sleep(2)
        expandir= Select(driver.find_element(By.XPATH, '//*[@id="tblSociedades_length"]/label/select'))
        time.sleep(2)
        expandir.select_by_value("-1")
        print("etapa1")
        time.sleep(5)
        html = driver.page_source
        
        soup = BeautifulSoup(html, 'html.parser')

        rows = soup.select('table#tblSociedades tbody tr')

        data = []
        print("iteracion rows")
        for row in rows:
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            data.append(row_data)

        print("iteracion rows fin")
        # Crear un DataFrame con los datos
        df = pd.DataFrame(data, columns=["Fecha", "Descripcion", "Numero", "OtroCampo", "CampoTexto", "OtroCampo2"])
  

        df= df.drop(["Descripcion", "OtroCampo", "CampoTexto", "OtroCampo2"], axis=1)
        print("creada la tabla",df)
       
        df["Numero"] = df["Numero"].str.replace(r'[^0-9K]', '', regex=True)
     

        print("drop de columnas")
        df= df[df['Fecha'] == formateada]
       
        #url_base = "http://localhost:8000/cargamasiva/" #cambiar esto cuando sepa cual es la url
        
        inicioiteracion= datetime.now()
        
        for i in df["Numero"]:
            print(i, x)
            
            #url = f"{url_base}{i}"
            #response = requests.get(url)
            x += 1
            #time.sleep(180)

        
        finiteracion= datetime.now()
        tiempototal= finiteracion-inicioiteracion
        estadoiteracion="Proceso exitoso"

    except Exception as e:
        print(e)
        estadoiteracion="proceso falló"
        inicioiteracion="error"
        finiteracion="error"
        tiempototal="no se peude calcular"
        

    # ultimo_rut = df['Número'].astype(int).values[0]

    return {"message":"Proceso completado",
            "CantidadProcesada": x,
            "TimestampInicio": inicioiteracion,
            "TimestampFinal":finiteracion,
            "tiempototalproceso": tiempototal,
            "status":estadoiteracion
            
            }


"""     
       




   

""" 
#####prueba

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

#JWT
SECRET_KEY = "99a609f0f76f340642ba535e215056db1ea7f476db10109ebbd977e6cc23054g"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#autenteicacion
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# Aquí se obtiene el token que durará 30 min
@app.post("/token")
async def login_for_access_token(username: str, password: str, grant_type: str = "password"):
    # Verificar credenciales (ejemplo básico, personaliza según tus necesidades)
    if username != "testuser" or password != "testpassword":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token y devolverlo
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected route", "current_user": current_user}

# Configuración de seguridad para la documentación
app.openapi = {
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        },
        "security": [{"bearerAuth": []}],
    },
    "info": {
        "title": "Your API",
        "version": "1.0.0",
    },
    "openapi": "3.0.0",
}

# Configuración de rutas para documentación
@app.get("/docs", include_in_schema=False)
async def get_docs():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# Ruta para acceder a la documentación protegida
@app.get("/protected/docs")
async def get_protected_docs(token: str = Depends(get_current_user)):
    return app.openapi()

"""




   
   


