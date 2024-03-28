
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import time




usermg='userviewer'
passmg= 'aquanima123'
uri= f"mongodb+srv://{usermg}:{passmg}@cluster1.xed1v1a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client["bbddruts"]
collection = db["rutscollection"]



for i, row in df.iterrows():
    print(i)

    numero = row['Numero']
    result = collection.find_one({"data.estado.rut": numero})
    
    if result:
    content1 = result.get("content1")
    content2 = result.get("content2")
    
    content_final= content1, content2

    else:
        print("Documento no encontrado")

    #trabajar con content_final de aqui abajo


