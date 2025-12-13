# Admin Routes Package
# This package contains modular admin route handlers

from flask import Blueprint
from app import db
from app.models.models import (
    Berita, Agenda, Galeri, Ekstrakurikuler, Laboratorium, 
    Banner, Prestasi, AlumniTestimoni
)
from app.utils.decorators import login_required
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
from app.routes.admin import berita
from app.routes.admin import agenda
from app.routes.admin import galeri
from app.routes.admin import ekstrakurikuler
from app.routes.admin import laboratorium
from app.routes.admin import banner
from app.routes.admin import info_sekolah
from app.routes.admin import perpustakaan
from app.routes.admin import profil_sekolah
from app.routes.admin import organisasi
from app.routes.admin import prestasi
from app.routes.admin import alumni
