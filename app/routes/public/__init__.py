from flask import Blueprint
from app.models.models import SekolahInfo

public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_sekolah_info():
    info = SekolahInfo.query.first()
    return dict(sekolah_info=info)

# PERBAIKAN: Gunakan titik (.) untuk import modul di folder yang sama
from . import beranda
from . import profil
from . import berita
from . import agenda
from . import galeri
from . import fasilitas
