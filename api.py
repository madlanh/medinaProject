from app import create_app

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

if __name__ == '__main__':
    app.run(debug=True)
