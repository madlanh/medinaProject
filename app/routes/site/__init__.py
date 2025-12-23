from flask import Blueprint
from app.models.models import SekolahInfo

# Ganti nama blueprint dan variable
site_bp = Blueprint('site', __name__) # Ganti 'public' jadi 'site'

@site_bp.context_processor
def inject_sekolah_info():
    info = SekolahInfo.query.first()
    return dict(sekolah_info=info)

# Update import di bawahnya (GANTI 'public' JADI 'site')
from app.routes.site import beranda
from app.routes.site import profil
from app.routes.site import berita
from app.routes.site import agenda
from app.routes.site import galeri
from app.routes.site import fasilitas
