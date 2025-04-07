from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE = os.getenv("DATABASE")
REGISTER_AVAILABLE = os.getenv("REGISTER_AVAILABLE")
CONNECTION = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "db_name": os.getenv("DB_NAME")
}
if REGISTER_AVAILABLE == "False":
    REGISTER_AVAILABLE = False
else:
    REGISTER_AVAILABLE = True