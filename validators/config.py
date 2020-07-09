"""
Файл настроек для валидаторов входа и выхода
"""

import os
import pandas as pd

ALLOWED_EXTENSIONS = {
    ".XLSX": pd.read_excel,
    ".XLSM": pd.read_excel,
    ".XLSB": pd.read_excel,
    ".XLTX": pd.read_excel,
    ".XLS": pd.read_excel,
    ".CSV": pd.read_csv
}
ALLOWED_MIMETYPES = {
    "application/vnd.ms-excel": True
}
# Список недопустимых строк
trash_content = ["", " "]
MAX_FILE_SIZE = 1024 * 1024 * 30 + 1
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "upload")



