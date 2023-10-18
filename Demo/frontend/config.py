import os
from pathlib import Path

BACKEND_URL = 'http://127.0.0.1:8000'
USER_ICON_URL = "https://cdn-icons-png.flaticon.com/128/9970/9970541.png"
BOT_ICON_URL = "https://noticon-static.tammolo.com/dgggcrkxq/image/upload/v1672321451/noticon/wg8oczvevrvjtbvkiskk.png"
PDF_LIST = os.listdir(str(Path(__file__).resolve().parent.parent) + "\pdf") #os.listdir(Path(__file__).resolve().parent)

if __name__ == "__main__":
    print(PDF_LIST)
