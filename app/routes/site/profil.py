# Profil Sekolah Routes (Sejarah, Visi-Misi, Sambutan, Organisasi, Info)
from flask import render_template
from app.models.models import SekolahInfo, Organisasi
# from app.routes.public import public_bp
from app.routes.site import site_bp as public_bp

@public_bp.route('/sejarah')
def sejarah():
    """School history page."""
    info = SekolahInfo.query.first()
    return render_template('sejarah.html', info=info)


@public_bp.route('/visi-misi')
def visi_misi():
    """Vision and mission page."""
    info = SekolahInfo.query.first()
    return render_template('visi-misi.html', info=info)


@public_bp.route('/sambutan')
def sambutan():
    """Principal's greeting page."""
    info = SekolahInfo.query.first()
    return render_template('sambutan.html', title='Sambutan Kepala Sekolah', info=info)


@public_bp.route('/organisasi')
def organisasi():
    """Organization structure page."""
    org_data = Organisasi.query.order_by(Organisasi.level).all()
    return render_template('organisasi.html', title='Struktur Organisasi', organisasi=org_data)


@public_bp.route('/info-sekolah')
def info_sekolah():
    """School information page."""
    info = SekolahInfo.query.first()
    return render_template('info_sekolah.html', title='Info Sekolah', info=info)
