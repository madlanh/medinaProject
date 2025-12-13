# Info Sekolah CRUD Routes
from flask import render_template, request, flash
from app import db
from app.models.models import SekolahInfo
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/info-sekolah', methods=['GET', 'POST'])
@login_required
def manage_info_sekolah():
    """Manage school information."""
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
        db.session.commit()

    if request.method == 'POST':
        try:
            info.nama = request.form['nama']
            info.npsn = request.form['npsn']
            info.akreditasi = request.form['akreditasi']
            info.alamat = request.form['alamat']
            info.telepon = request.form['telepon']
            info.email = request.form['email']
            info.website = request.form['website']
            info.kepala_sekolah = request.form['kepala_sekolah']
            info.jumlah_siswa = int(request.form['jumlah_siswa'])
            info.jumlah_guru = int(request.form['jumlah_guru'])
            info.jumlah_kelas = int(request.form['jumlah_kelas'])
            info.tahun_berdiri = int(request.form['tahun_berdiri'])
            db.session.commit()
            flash('Info sekolah berhasil diperbarui!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui info sekolah: {e}', 'danger')
    
    return render_template('admin/manage_info_sekolah.html', info=info)
