import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')


EMAKTAB_LOGIN = os.environ.get('EMAKTAB_LOGIN')
EMAKTAB_PASSWORD = os.environ.get('EMAKTAB_PASSWORD')
