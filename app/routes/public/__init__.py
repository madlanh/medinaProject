# Public Routes Package
# This package contains modular public route handlers

from flask import Blueprint
from .models.models import SekolahInfo

# Create main public blueprint
public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_sekolah_info():
    """Inject school info into all public templates."""
    info = SekolahInfo.query.first()
    return dict(sekolah_info=info)

# Import and register all sub-modules
from .routes.public import beranda
from .routes.public import profil
from .routes.public import berita
from .routes.public import agenda
from .routes.public import galeri
from .routes.public import fasilitas
