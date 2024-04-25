import pandas as pd
import json
import xlsxwriter
import concurrent.futures
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
import os
import time
import io
from io import BytesIO



#Descarga de un archivo de Sharepoint
site_url = "https://aquanimavdi.sharepoint.com/sites/DDBBCE"
ctx = ClientContext(site_url).with_credentials(UserCredential("francisco.alvarez@aquanimaservices.com", "Aquanima.2023"))
file_relative_path = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/Informe pedidos.xls"

file_relative_path2 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/Informe solicitudes.zip"
file_relative_path3 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/BBDD.xlsx"
file_relative_path4 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/informe-SGT.xlsx"

"""
response = File.open_binary(ctx, file_relative_path)

bytes_file_obj= io.BytesIO()#nuevo
bytes_file_obj.write(response.content)#nuevo
bytes_file_obj.seek(0)#nuevo

response2= File.open_binary(ctx,file_relative_path2)
bytes_file_obj1= io.BytesIO()
bytes_file_obj1.write(response2.content)
bytes_file_obj1.seek(0)


response3= File.open_binary(ctx,file_relative_path3)
bytes_file_obj2= io.BytesIO()
bytes_file_obj2.write(response3.content)
bytes_file_obj2.seek(0)
"""
response4= File.open_binary(ctx,file_relative_path4)
bytes_file_obj4= io.BytesIO()
bytes_file_obj4.write(response4.content)
bytes_file_obj4.seek(0)

#with open('./sgt/Seguimiento de pedidos.xls', 'wb') as f:
#    f.write(bytes_file_obj.getvalue())
#

#with open('./sgt/archivo.zip', 'wb') as f:
#    f.write(bytes_file_obj1.getvalue())

#with open('./sgt/BBDD1.xlsx', 'wb') as f:
#    f.write(bytes_file_obj2.getvalue())

with open('./sgt/INFORME_SGT.xlsx', 'wb') as f:
    f.write(bytes_file_obj4.getvalue())