import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci_rahasia_anda_yang_sangat_aman_dan_panjang'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.environ.get('DB_USERNAME', 'root')}:"
        f"{os.environ.get('DB_PASSWORD', '')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '3306')}/"
        f"{os.environ.get('DB_NAME', 'medinadb')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
