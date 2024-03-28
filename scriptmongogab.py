
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time



usermg='userviewer'
passmg= 'aquanima123'
uri= f"mongodb+srv://{usermg}:{passmg}@cluster1.xed1v1a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client["bbddruts"]
collection = db["rutscollection"]


print("Ingrese Rut a Continuacion:")
rut=input()

result = collection.find_one({"data.estado.rut": rut})


# re si se encontró el documento
if result:
    # Accede a los campos "Content1" y "Content2" si están presentes en el documento
    content1 = result.get("content1")
    content2 = result.get("content2")
    
    # Haz lo que necesites con content1 y content2
    print(content1, content2)

else:
    print("Documento no encontrado")

"""
for i, row in df.iterrows():
    if i % 1000 == 0:  # Imprimir y guardar cada 1000 registros
        elapsed_time = time.time() - start_time
        print(f"Registros procesados: {i}, Tiempo transcurrido: {elapsed_time} segundos")
        df.to_pickle('./basemongo.pkl')  # Guardar el DataFrame como pickle
    # Buscar el valor de la columna "Numero" en MongoDB
    numero = row['Numero']
    result = collection.find_one({"data.estado.rut": numero})

"""