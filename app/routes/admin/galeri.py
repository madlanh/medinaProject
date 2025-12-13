# Galeri CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Galeri
from app.utils.decorators import login_required
from datetime import datetime
from app.routes.admin import admin_bp


@admin_bp.route('/galeri')
@login_required
def manage_galeri():
    """List all galeri."""
    galeri_list = Galeri.query.order_by(Galeri.tanggal.desc()).all()
    return render_template('admin/manage_galeri.html', galeri_list=galeri_list)


@admin_bp.route('/galeri/create', methods=['GET', 'POST'])
@login_required
def create_galeri():
    """Create new galeri item."""
    if request.method == 'POST':
        try:
            new_galeri = Galeri(
                judul=request.form['judul'],
                kategori=request.form['kategori'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                deskripsi=request.form['deskripsi'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_galeri)
            db.session.commit()
            flash('Foto galeri baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_galeri'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan foto: {e}', 'danger')
    return render_template('admin/edit_galeri.html', title='Tambah Foto Galeri', galeri=None)


@admin_bp.route('/galeri/edit/<int:galeri_id>', methods=['GET', 'POST'])
@login_required
def edit_galeri(galeri_id):
    """Edit existing galeri item."""
    galeri = Galeri.query.get_or_404(galeri_id)
    
    if request.method == 'POST':
        try:
            galeri.judul = request.form['judul']
            galeri.kategori = request.form['kategori']
            galeri.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            galeri.deskripsi = request.form['deskripsi']
            galeri.image_url = request.form.get('image_num', '1')
            db.session.commit()
            flash('Foto galeri berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_galeri'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui foto: {e}', 'danger')

    return render_template('admin/edit_galeri.html', title=f'Edit Galeri: {galeri.judul}', galeri=galeri)


@admin_bp.route('/galeri/delete/<int:galeri_id>', methods=['POST'])
@login_required
def delete_galeri(galeri_id):
    """Delete galeri item."""
    galeri = Galeri.query.get_or_404(galeri_id)
    try:
        db.session.delete(galeri)
        db.session.commit()
        flash(f'Foto "{galeri.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus foto: {e}', 'danger')
    return redirect(url_for('admin.manage_galeri'))
