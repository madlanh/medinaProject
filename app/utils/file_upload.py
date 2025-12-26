import os
import uuid
import time
from werkzeug.utils import secure_filename
from supabase import create_client
from flask import current_app

# Allowed extensions check (Sama seperti sebelumnya)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024

def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_supabase_client():
    """Helper untuk koneksi ke Supabase"""
    url = current_app.config.get('SUPABASE_URL')
    key = current_app.config.get('SUPABASE_KEY')
    if not url or not key:
        current_app.logger.error("Supabase URL or KEY not found in config")
        return None
    return create_client(url, key)

def save_uploaded_file(file, category: str = 'general') -> str:
    """
    Mengupload file ke Supabase Storage.
    Menggantikan fungsi save lokal yang lama tanpa mengubah nama fungsi.
    """
    if not file or not allowed_file(file.filename):
        return None

    # Cek ukuran file (baca pointer)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0) # Reset pointer ke awal agar bisa dibaca lagi saat upload
    
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB")

    try:
        # 1. Buat nama file unik
        original_filename = secure_filename(file.filename)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}_{original_filename}"
        
        # Path di dalam bucket (contoh: banners/foto.jpg)
        # Kita gunakan 'category' sebagai nama folder di Supabase
        file_path = f"{category}/{filename}"

        # 2. Inisialisasi Supabase
        supabase = get_supabase_client()
        if not supabase:
            return None

        bucket_name = current_app.config.get('SUPABASE_BUCKET', 'images')
        
        # 3. Baca file binary dan Upload
        file_content = file.read()
        
        res = supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )

        # 4. Ambil URL Publik
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        
        return public_url

    except Exception as e:
        current_app.logger.error(f"🔥 Error Upload ke Supabase: {e}")
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
        
        # Kita perlu mengambil path file dari URL lengkap
        # URL Supabase biasanya: https://xyz.supabase.co/.../public/images/banners/foto.jpg
        # Kita butuh bagian: banners/foto.jpg
        
        if bucket_name in file_url:
            # Split URL berdasarkan nama bucket
            file_path = file_url.split(f"/{bucket_name}/")[-1]
            
            # Hapus file
            supabase.storage.from_(bucket_name).remove(file_path)
            return True
            
    except Exception as e:
        current_app.logger.error(f"Error deleting from Supabase: {e}")
        return False
