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



def generate_tree(height):
    for i in range(height):
        print(' ' * (height - i - 1) + '*' * (2 * i + 1))

# define the height of the tree
height = 10
generate_tree(height)