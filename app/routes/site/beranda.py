# Beranda (Homepage) Route
from flask import render_template
from app.models.models import Berita, Banner, Prestasi, AlumniTestimoni
# from app.routes.public import public_bp
from app.routes.site import site_bp as public_bp


@public_bp.route('/')
def index():
    """Homepage with banners, berita, prestasi, and alumni."""
    berita_beranda = Berita.query.order_by(Berita.tanggal.desc()).limit(3).all()
    banner_aktif = Banner.query.filter_by(is_active=True).order_by(Banner.display_order).all()
    prestasi_data = Prestasi.query.all()
    alumni_data = AlumniTestimoni.query.all()
    
    return render_template('index.html', 
                           berita=berita_beranda,
                           prestasi=prestasi_data, 
                           alumni=alumni_data,
                           banners=banner_aktif)
