# Public Routes Package
# This package contains modular public route handlers

from flask import Blueprint
# HAPUS BARIS INI: from app.models.models import SekolahInfo (Kita pindahkan ke bawah)

# Create main public blueprint
public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_sekolah_info():
    """Inject school info into all public templates."""
    # PINDAHKAN IMPORT KE DALAM FUNGSI INI
    from app.models.models import SekolahInfo
    
    # Gunakan try-except agar tidak error jika tabel belum ada (saat migrasi awal)
    try:
        info = SekolahInfo.query.first()
    except:
        info = None
        
    return dict(sekolah_info=info)

# Import and register all sub-modules
from app.routes.public import beranda
from app.routes.public import profil
from app.routes.public import berita
from app.routes.public import agenda
from app.routes.public import galeri
from app.routes.public import fasilitas
