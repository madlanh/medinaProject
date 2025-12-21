# Public Routes Package
# This package contains modular public route handlers

from flask import Blueprint
from app.models.models import SekolahInfo

# Create main public blueprint
public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_sekolah_info():
    """Inject school info into all public templates."""
    info = SekolahInfo.query.first()
    return dict(sekolah_info=info)

# Import and register all sub-modules
from app.routes.public import beranda
from app.routes.public import profil
from app.routes.public import berita
from app.routes.public import agenda
from app.routes.public import galeri
from app.routes.public import fasilitas
