import os
import uuid
import time
from werkzeug.utils import secure_filename
from supabase import create_client
from flask import current_app

# Ekstensi yang diperbolehkan
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_supabase_client():
    """Helper untuk koneksi ke Supabase"""
    url = current_app.config.get('SUPABASE_URL')
    key = current_app.config.get('SUPABASE_KEY')
    
    # Debugging: Cek apakah config terbaca
    if not url or not key:
        print("❌ ERROR: SUPABASE_URL atau SUPABASE_KEY belum diset di Config/Environment!")
        return None
    return create_client(url, key)

def save_uploaded_file(file, category: str = 'general') -> str:
    """
    Fungsi Upload ke Supabase Storage.
    Menggantikan fungsi save lokal yang lama.
    """
    if not file or not allowed_file(file.filename):
        print(f"❌ File tidak valid atau ekstensi salah: {file.filename}")
        return None

    # Cek ukuran file
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    if size > MAX_FILE_SIZE:
        print("❌ File terlalu besar (>5MB)")
        return None

    try:
        # 1. Buat nama file unik
        original_filename = secure_filename(file.filename)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}_{original_filename}"
        
        # Path di dalam bucket (contoh: banners/foto.jpg)
        file_path = f"{category}/{filename}"

        # 2. Koneksi ke Supabase
        supabase = get_supabase_client()
        if not supabase:
            return None

        bucket_name = current_app.config.get('SUPABASE_BUCKET', 'images')
        
        # 3. Baca file dan Upload
        file_content = file.read()
        
        # Eksekusi Upload
        res = supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )

        # 4. Ambil URL Publik agar bisa disimpan di database
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        
        print(f"✅ Sukses Upload ke Supabase: {public_url}")
        return public_url

    except Exception as e:
        print(f"🔥 Error Upload ke Supabase: {e}")
        return None

def delete_file(file_url: str) -> bool:
    """
    Menghapus file dari Supabase Storage.
    """
    if not file_url:
        return False
        
    try:
        supabase = get_supabase_client()
        if not supabase: 
            return False
            
        bucket_name = current_app.config.get('SUPABASE_BUCKET', 'images')
        
        if bucket_name in file_url:
            # Ambil path file dari URL
            file_path = file_url.split(f"/{bucket_name}/")[-1]
            supabase.storage.from_(bucket_name).remove(file_path)
            return True
            
    except Exception as e:
        print(f"Error deleting from Supabase: {e}")
        return False
