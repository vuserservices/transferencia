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



df1= pd.read_excel('./sgt/contratos.xlsx')
df2= pd.read_excel('./sgt/sourcing.xlsx')

df1.to_pickle('./sgt/contratos.pkl')

df2.to_pickle('./sgt/sourcing.pkl')
