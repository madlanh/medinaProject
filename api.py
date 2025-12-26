from app import create_app
from flask import jsonify

# Tambahkan ini di bagian paling atas file api.py
import os
import sys

print("--- DEBUGGING INFO ---")
try:
    print("Isi folder 'app':", os.listdir('app'))
    
    # Cek apakah ada folder 'routes' atau 'Routes'
    routes_folder = [f for f in os.listdir('app') if f.lower() == 'routes']
    if routes_folder:
        actual_name = routes_folder[0]
        print(f"Nama folder routes yang ditemukan: '{actual_name}'")
        
        # Cek isi dalam folder routes tersebut
        print(f"Isi folder 'app/{actual_name}':", os.listdir(f'app/{actual_name}'))
    else:
        print("Folder routes TIDAK DITEMUKAN di dalam 'app'")
except Exception as e:
    print("Error saat debugging:", e)
print("--- END DEBUGGING ---")
# ... kode api.py kamu yang asli di bawah ini ...

app = create_app()

@app.route('/test-supabase')
def test_supabase():
    try:
        from app.utils.file_upload import get_supabase_client
        supabase = get_supabase_client()
        
        if not supabase:
            return jsonify({"status": "error", "pesan": "Gagal inisialisasi Client Supabase. Cek Config/Env Vars."})

        # Tes 1: Cek apakah bisa melihat Bucket
        buckets = supabase.storage.list_buckets()
        bucket_list = [b.name for b in buckets]
        
        return jsonify({
            "status": "sukses",
            "pesan": "Koneksi Berhasil!",
            "bucket_ditemukan": bucket_list,
            "target_bucket_di_config": app.config.get('SUPABASE_BUCKET'),
            "apakah_bucket_target_ada": app.config.get('SUPABASE_BUCKET') in bucket_list
        })
    except Exception as e:
        return jsonify({"status": "error", "pesan": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
