import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci_rahasia_anda_yang_sangat_aman_dan_panjang'
    
    # DB_USER = os.environ.get('DB_USERNAME') or 'postgres.fmovjkhibadscwtmuous'
    # DB_PASS = os.environ.get('DB_PASSWORD') or 'smamediaBdg20'
    # DB_HOST = os.environ.get('DB_HOST') or 'aws-1-ap-southeast-1.pooler.supabase.com'
    # DB_PORT = os.environ.get('DB_PORT') or '5432'
    # DB_NAME = os.environ.get('DB_NAME') or 'postgres'

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://postgres.fmovjkhibadscwtmuous:smamediaBdg20@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    SUPABASE_BUCKET = 'images'
