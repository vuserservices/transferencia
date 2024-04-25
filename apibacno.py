from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
import os
import datetime as datetime
import io
import pandas as pd

#Descarga de un archivo de Sharepoint
site_url = "https://santandernet.sharepoint.com/sites/QABIAquanimaChile"
ctx = ClientContext(site_url).with_credentials(UserCredential("N921437@corp.santander.cl", "Informatica.2024.."))
file_relative_path = "/sites/DDBBCE/Documentos compartidos/General/Libro.xlsx"
response = File.open_binary(ctx, file_relative_path)
content = response.content

content_stream = io.BytesIO(content)

# Lee el contenido en un DataFrame de pandas
df = pd.read_csv(content_stream)

df.head()
