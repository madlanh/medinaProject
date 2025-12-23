# Berita Routes
from flask import render_template
from app.models.models import Berita
# from app.routes.public import public_bp
from app.routes.site import site_bp as public_bp


@public_bp.route('/berita-terbaru')
def berita_terbaru():
    """List all news."""
    berita_list = Berita.query.order_by(Berita.tanggal.desc()).all()
    return render_template('berita_terbaru.html', title='Berita Terbaru', berita_list=berita_list)


@public_bp.route('/berita/<int:berita_id>')
def berita_detail(berita_id):
    """News detail page."""
    berita = Berita.query.get_or_404(berita_id)
    berita_lain = Berita.query.filter(Berita.id != berita_id).order_by(Berita.tanggal.desc()).limit(5).all()
    return render_template('berita_detail.html', title=berita.judul, berita=berita, berita_lain=berita_lain)
