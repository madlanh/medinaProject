# Admin Routes Package
# This package contains modular admin route handlers

from flask import Blueprint
from app import db
from .models.models import (
    Berita, Agenda, Galeri, Ekstrakurikuler, Laboratorium, 
    Banner, Prestasi, AlumniTestimoni
)
from .utils.decorators import login_required
from flask import render_template

# Create main admin blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin Dashboard with statistics."""
    stats = {
        'total_berita': Berita.query.count(),
        'total_agenda': Agenda.query.count(),
        'total_galeri': Galeri.query.count(),
        'total_ekstrakurikuler': Ekstrakurikuler.query.count(),
        'total_prestasi': Prestasi.query.count(),
        'total_alumni': AlumniTestimoni.query.count()
    }
    return render_template('admin_dashboard.html', stats=stats)

# Import and register all sub-modules
from .routes.admin import berita
from .routes.admin import agenda
from .routes.admin import galeri
from .routes.admin import ekstrakurikuler
from .routes.admin import laboratorium
from .routes.admin import banner
from .routes.admin import info_sekolah
from .routes.admin import perpustakaan
from .routes.admin import profil_sekolah
from .routes.admin import organisasi
from .routes.admin import prestasi
from .routes.admin import alumni
from .routes.admin import api_docs
