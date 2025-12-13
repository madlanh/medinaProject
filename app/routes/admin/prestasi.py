# Prestasi CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Prestasi
from app.utils.decorators import login_required
from datetime import datetime
from app.routes.admin import admin_bp


@admin_bp.route('/prestasi')
@login_required
def manage_prestasi():
    """List all prestasi."""
    prestasi_list = Prestasi.query.order_by(Prestasi.tanggal.desc()).all()
    return render_template('admin/manage_prestasi.html', prestasi_list=prestasi_list)


@admin_bp.route('/prestasi/create', methods=['GET', 'POST'])
@login_required
def create_prestasi():
    """Create new prestasi."""
    if request.method == 'POST':
        try:
            tanggal_str = request.form.get('tanggal')
            tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date() if tanggal_str else None
            
            new_prestasi = Prestasi(
                nama_prestasi=request.form['nama_prestasi'],
                skala=request.form['skala'],
                tanggal=tanggal,
                penyelenggara=request.form['penyelenggara'],
                keterangan=request.form.get('keterangan', '')
            )
            db.session.add(new_prestasi)
            db.session.commit()
            flash('Prestasi baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_prestasi'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan prestasi: {e}', 'danger')
    return render_template('admin/edit_prestasi.html', title='Tambah Prestasi', prestasi=None)


@admin_bp.route('/prestasi/edit/<int:prestasi_id>', methods=['GET', 'POST'])
@login_required
def edit_prestasi(prestasi_id):
    """Edit existing prestasi."""
    prestasi = Prestasi.query.get_or_404(prestasi_id)
    
    if request.method == 'POST':
        try:
            tanggal_str = request.form.get('tanggal')
            prestasi.nama_prestasi = request.form['nama_prestasi']
            prestasi.skala = request.form['skala']
            prestasi.tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date() if tanggal_str else None
            prestasi.penyelenggara = request.form['penyelenggara']
            prestasi.keterangan = request.form.get('keterangan', '')
            db.session.commit()
            flash('Prestasi berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_prestasi'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui prestasi: {e}', 'danger')

    return render_template('admin/edit_prestasi.html', title=f'Edit Prestasi: {prestasi.nama_prestasi}', prestasi=prestasi)


@admin_bp.route('/prestasi/delete/<int:prestasi_id>', methods=['POST'])
@login_required
def delete_prestasi(prestasi_id):
    """Delete prestasi."""
    prestasi = Prestasi.query.get_or_404(prestasi_id)
    try:
        db.session.delete(prestasi)
        db.session.commit()
        flash(f'Prestasi "{prestasi.nama_prestasi}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus prestasi: {e}', 'danger')
    return redirect(url_for('admin.manage_prestasi'))
