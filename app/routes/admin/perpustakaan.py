# Perpustakaan CRUD Routes
from flask import render_template, request, flash
from app import db
from app.models.models import PerpustakaanInfo, PerpustakaanFasilitas, PerpustakaanLayanan
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/perpustakaan', methods=['GET', 'POST'])
@login_required
def manage_perpustakaan_admin():
    """Manage library information."""
    perpus = PerpustakaanInfo.query.first()
    if not perpus:
        perpus = PerpustakaanInfo()
        db.session.add(perpus)
        db.session.commit()

    if request.method == 'POST':
        try:
            perpus.jam_buka_senin_jumat = request.form['jam_senin_jumat']
            perpus.jam_buka_sabtu = request.form['jam_sabtu']
            perpus.jumlah_buku_pelajaran = int(request.form['buku_pelajaran'])
            perpus.jumlah_buku_fiksi = int(request.form['buku_fiksi'])
            perpus.jumlah_buku_referensi = int(request.form['buku_referensi'])
            perpus.jumlah_majalah_jurnal = int(request.form['majalah_jurnal'])
            perpus.jumlah_ebook = int(request.form['e_book'])
            
            # Update facilities
            PerpustakaanFasilitas.query.delete()
            fasilitas_str = request.form['fasilitas']
            for f in fasilitas_str.split(','):
                if f.strip():
                    db.session.add(PerpustakaanFasilitas(nama_fasilitas=f.strip()))
            
            # Update services
            PerpustakaanLayanan.query.delete()
            layanan_str = request.form['layanan']
            for l in layanan_str.split(','):
                if l.strip():
                    db.session.add(PerpustakaanLayanan(nama_layanan=l.strip()))
            
            db.session.commit()
            flash('Data perpustakaan berhasil diperbarui!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui data perpustakaan: {e}', 'danger')
    
    # Prepare data for template
    fasilitas = [f.nama_fasilitas for f in PerpustakaanFasilitas.query.all()]
    layanan = [l.nama_layanan for l in PerpustakaanLayanan.query.all()]
    
    # Construct object compatible with template
    perpus_data = {
        'jam_buka': {
            'senin_jumat': perpus.jam_buka_senin_jumat,
            'sabtu': perpus.jam_buka_sabtu
        },
        'koleksi': {
            'buku_pelajaran': perpus.jumlah_buku_pelajaran,
            'buku_fiksi': perpus.jumlah_buku_fiksi,
            'buku_referensi': perpus.jumlah_buku_referensi,
            'majalah_jurnal': perpus.jumlah_majalah_jurnal,
            'e_book': perpus.jumlah_ebook
        },
        'fasilitas': fasilitas,
        'layanan': layanan
    }
    
    return render_template('admin/manage_perpustakaan.html', perpus=perpus_data)
