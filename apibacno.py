from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
import os
import datetime as datetime
import io
import pandas as pd
import time


i=time.time()

#Descarga de un archivo de Sharepoint
site_url = "https://aquanimavdi.sharepoint.com/sites/DDBBCE"
usersp="francisco.alvarez@aquanimaservices.com"
passsp="Aquanima.2023"



ctx = ClientContext(site_url).with_credentials(UserCredential(usersp, passsp))
file_relative_path = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/Informe pedidos.xlsx"
file_relative_path2 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/Informe solicitudes.xlsx"
file_relative_path3 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/BBDD.xlsx"
file_relative_path4 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/informe-SGT.xlsx"
file_relative_path5 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/Contracts Pipeline.xlsx"
file_relative_path6 = "/sites/DDBBCE/Documentos compartidos/SGTBBDD/Informe Sourcing.xlsx"

#response = File.open_binary(ctx, file_relative_path)
#bytes_file_obj= io.BytesIO()
#bytes_file_obj.write(response.content)
#bytes_file_obj.seek(0)
#
#response2= File.open_binary(ctx,file_relative_path2)
#bytes_file_obj1= io.BytesIO()
#bytes_file_obj1.write(response2.content)
#bytes_file_obj1.seek(0)

#response3= File.open_binary(ctx,file_relative_path3)
#bytes_file_obj2= io.BytesIO()
#bytes_file_obj2.write(response3.content)
#bytes_file_obj2.seek(0)

#response4= File.open_binary(ctx,file_relative_path4)
#bytes_file_obj4= io.BytesIO()
#bytes_file_obj4.write(response4.content)
#bytes_file_obj4.seek(0)
#
response5 = File.open_binary(ctx, file_relative_path5)
bytes_file_obj5= io.BytesIO()
bytes_file_obj5.write(response5.content)
bytes_file_obj5.seek(0)

response6 = File.open_binary(ctx, file_relative_path6)
bytes_file_obj6= io.BytesIO()
bytes_file_obj6.write(response6.content)
bytes_file_obj6.seek(0)

#with open('./sgt/Seguimiento de pedidos.xlsx', 'wb') as f:
#    f.write(bytes_file_obj.getvalue())
#
#with open('./sgt/Seguimiento de solicitudes.xlsx', 'wb') as f:
#    f.write(bytes_file_obj1.getvalue())

#with open('./sgt/BBDD.xlsx', 'wb') as f:
#    f.write(bytes_file_obj2.getvalue())

#with open('./sgt/informesgt.xlsx', 'wb') as f:
#    f.write(bytes_file_obj4.getvalue())

with open('./sgt/contratos.xlsx', 'wb') as f:
    f.write(bytes_file_obj5.getvalue())

with open('./sgt/sourcing.xlsx', 'wb') as f:
    f.write(bytes_file_obj6.getvalue())
print("pasando de .xlsx a pkl")
df1= pd.read_excel('./sgt/contratos.xlsx')
df2= pd.read_excel('./sgt/sourcing.xlsx')

df1.to_pickle('./sgt/contratos.pkl')

df2.to_pickle('./sgt/sourcing.pkl')

f=time.time()
tiempo= f-i


print("finalizado: ", tiempo)