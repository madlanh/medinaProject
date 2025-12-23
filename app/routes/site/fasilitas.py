# Fasilitas Routes (Ekstrakurikuler, Laboratorium, Perpustakaan)
from flask import render_template, request, flash, redirect, url_for
from app.models.models import (
    Ekstrakurikuler, Laboratorium, 
    PerpustakaanInfo, PerpustakaanFasilitas, PerpustakaanLayanan
)
# from app.routes.public import public_bp
from app.routes.site import site_bp as public_bp


@public_bp.route('/ekstrakurikuler')
def ekstrakurikuler():
    """Extracurricular activities page."""
    ekskul_data = Ekstrakurikuler.query.all()
    kategoris = list(set([e.kategori for e in ekskul_data if e.kategori]))
    return render_template('ekstrakurikuler.html', title='Ekstrakurikuler', ekstrakurikuler=ekskul_data, kategoris=kategoris)


@public_bp.route('/ekstrakurikuler/daftar/<int:ekskul_id>', methods=['GET', 'POST'])
def daftar_ekskul(ekskul_id):
    """Extracurricular registration form."""
    ekskul = Ekstrakurikuler.query.get_or_404(ekskul_id)
    
    if request.method == 'POST':
        nama_siswa = request.form.get('nama')
        kelas = request.form.get('kelas')
        
        flash(f'Terima kasih {nama_siswa}! Formulir pendaftaran {ekskul.nama} berhasil dikirim. Pembina akan segera menghubungi Anda.', 'success')
        return redirect(url_for('public.ekstrakurikuler'))
        
    return render_template('daftar_ekskul.html', title=f'Daftar {ekskul.nama}', ekskul=ekskul)


@public_bp.route('/laboratorium')
def laboratorium():
    """Laboratories listing page."""
    lab_data = Laboratorium.query.all()
    return render_template('laboratorium.html', title='Laboratorium', laboratorium=lab_data)


@public_bp.route('/laboratorium/<int:lab_id>')
def laboratorium_detail(lab_id):
    """Laboratory detail page."""
    lab = Laboratorium.query.get_or_404(lab_id)
    return render_template('laboratorium_detail.html', title=lab.nama, lab=lab)


@public_bp.route('/perpustakaan')
def perpustakaan():
    """Library page."""
    perpus_info = PerpustakaanInfo.query.first()
    fasilitas = [f.nama_fasilitas for f in PerpustakaanFasilitas.query.all()]
    layanan = [l.nama_layanan for l in PerpustakaanLayanan.query.all()]
    
    perpus_data = {
        'jam_buka': {
            'senin_jumat': perpus_info.jam_buka_senin_jumat if perpus_info else '',
            'sabtu': perpus_info.jam_buka_sabtu if perpus_info else ''
        },
        'koleksi': {
            'buku_pelajaran': perpus_info.jumlah_buku_pelajaran if perpus_info else 0,
            'buku_fiksi': perpus_info.jumlah_buku_fiksi if perpus_info else 0,
            'buku_referensi': perpus_info.jumlah_buku_referensi if perpus_info else 0,
            'majalah_jurnal': perpus_info.jumlah_majalah_jurnal if perpus_info else 0,
            'e_book': perpus_info.jumlah_ebook if perpus_info else 0
        },
        'fasilitas': fasilitas,
        'layanan': layanan
    }
    
    return render_template('perpustakaan.html', title='Perpustakaan', perpustakaan=perpus_data)
