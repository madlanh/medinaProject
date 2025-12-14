# Galeri Routes
from flask import render_template
from app.models.models import Galeri
from app.routes.public import public_bp


@public_bp.route('/galeri')
def galeri():
    """Photo gallery page."""
    galeri_data = Galeri.query.order_by(Galeri.tanggal.desc()).all()
    kategoris = list(set([g.kategori for g in galeri_data if g.kategori]))
    return render_template('galeri.html', title='Galeri', galeri=galeri_data, kategoris=kategoris)
