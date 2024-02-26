import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
ip = str(os.getenv('ip'))
DATABASE = str(os.getenv('DATABASE'))