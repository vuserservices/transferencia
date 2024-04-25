import pandas as pd
from datetime import datetime
inicio=datetime.now()
df=pd.read_excel('./contracts.xlsx',sheet_name="Repository")
df2=pd.read_excel('./sourcing.xlsx',sheet_name="SOURCING EXECUTION")

df2['ID_prefiltrado'] = df2['Associated CW'].str.extract(r'(CW\d{6,7})')
filtro=["In Progress", "On Hold"]

df=df[df['Status'].isin(filtro)]


df.insert(1, 'columna1', df['Contract Id'].isin(df2['ID_prefiltrado']).map({True: 'Si', False: 'No'}))
df.insert(2, 'Columna2',  "vacio2")

df=df[df['columna1']=="No"]
print(df)

fin=datetime.now()
print(f"tiempo total: {fin-inicio}")