from app import create_app, db

app = create_app()

with app.app_context():
    print("Membuat tabel di Supabase...")
    db.create_all()
    print("Selesai! Tabel berhasil dibuat.")