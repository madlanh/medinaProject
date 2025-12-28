from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SekolahInfo(db.Model):
    __tablename__ = 'sekolah_info'
    id = db.Column(db.Integer, primary_key=True, default=1)
    nama = db.Column(db.String(100), nullable=False)
    npsn = db.Column(db.String(20))
    akreditasi = db.Column(db.String(1))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    kepala_sekolah = db.Column(db.String(100))
    jumlah_siswa = db.Column(db.Integer)
    jumlah_guru = db.Column(db.Integer)
    jumlah_kelas = db.Column(db.Integer)
    tahun_berdiri = db.Column(db.Integer)
    sejarah = db.Column(db.Text)
    visi = db.Column(db.Text)
    misi = db.Column(db.Text)
    sambutan_kepsek = db.Column(db.Text)
    foto_kepala_sekolah = db.Column(db.String(255))  # URL foto kepala sekolah
    nama_kepala_sekolah = db.Column(db.String(100))  # Nama lengkap kepala sekolah
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Organisasi(db.Model):
    __tablename__ = 'organisasi'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=99)
    image_url = db.Column(db.String(255))
    jumlah = db.Column(db.Integer, default=0)  # Staff count (for staff level)
    emoji = db.Column(db.String(10), default='👔')  # Icon emoji

class Berita(db.Model):
    __tablename__ = 'berita'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    tanggal = db.Column(db.Date, nullable=False)
    ringkasan = db.Column(db.Text)
    konten_lengkap = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Agenda(db.Model):
    __tablename__ = 'agenda'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False)
    deskripsi = db.Column(db.Text)
    lokasi = db.Column(db.String(100))
    waktu_display = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Galeri(db.Model):
    __tablename__ = 'galeri'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    deskripsi = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100))
    subjudul = db.Column(db.String(200))
    image_url = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link_url = db.Column(db.String(255), nullable=True, default='#')

class Ekstrakurikuler(db.Model):
    __tablename__ = 'ekstrakurikuler'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50))
    pembina = db.Column(db.String(100))
    jadwal = db.Column(db.String(100))
    deskripsi = db.Column(db.Text)
    image_url = db.Column(db.String(255))

class Laboratorium(db.Model):
    __tablename__ = 'laboratorium'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    fasilitas = db.relationship('LaboratoriumFasilitas', backref='laboratorium', lazy=True, cascade="all, delete-orphan")

class LaboratoriumFasilitas(db.Model):
    __tablename__ = 'laboratorium_fasilitas'
    id = db.Column(db.Integer, primary_key=True)
    laboratorium_id = db.Column(db.Integer, db.ForeignKey('laboratorium.id'), nullable=False)
    nama_fasilitas = db.Column(db.String(200), nullable=False)
    def __str__(self):
        return self.nama_fasilitas

class PerpustakaanInfo(db.Model):
    __tablename__ = 'perpustakaan_info'
    id = db.Column(db.Integer, primary_key=True, default=1)
    jam_buka_senin_jumat = db.Column(db.String(50))
    jam_buka_sabtu = db.Column(db.String(50))
    jumlah_buku_pelajaran = db.Column(db.Integer, default=0)
    jumlah_buku_fiksi = db.Column(db.Integer, default=0)
    jumlah_buku_referensi = db.Column(db.Integer, default=0)
    jumlah_majalah_jurnal = db.Column(db.Integer, default=0)
    jumlah_ebook = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PerpustakaanFasilitas(db.Model):
    __tablename__ = 'perpustakaan_fasilitas'
    id = db.Column(db.Integer, primary_key=True)
    nama_fasilitas = db.Column(db.String(200), nullable=False)

class PerpustakaanLayanan(db.Model):
    __tablename__ = 'perpustakaan_layanan'
    id = db.Column(db.Integer, primary_key=True)
    nama_layanan = db.Column(db.String(200), nullable=False)

class Prestasi(db.Model):
    __tablename__ = 'prestasi'
    id = db.Column(db.Integer, primary_key=True)
    nama_prestasi = db.Column(db.String(255), nullable=False)
    skala = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    penyelenggara = db.Column(db.String(100))
    keterangan = db.Column(db.Text)

class AlumniTestimoni(db.Model):
    __tablename__ = 'alumni_testimoni'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    tahun_lulus = db.Column(db.Integer)
    testimoni = db.Column(db.Text)
    status_saat_ini = db.Column(db.String(200))
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
