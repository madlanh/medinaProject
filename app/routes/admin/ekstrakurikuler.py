# Ekstrakurikuler CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Ekstrakurikuler
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/ekstrakurikuler')
@login_required
def manage_ekstrakurikuler():
    """List all ekstrakurikuler."""
    ekskul_list = Ekstrakurikuler.query.all()
    return render_template('admin/manage_ekstrakurikuler.html', ekskul_list=ekskul_list)


@admin_bp.route('/ekstrakurikuler/create', methods=['GET', 'POST'])
@login_required
def create_ekstrakurikuler():
    """Create new ekstrakurikuler."""
    if request.method == 'POST':
        try:
            new_ekskul = Ekstrakurikuler(
                nama=request.form['nama'],
                kategori=request.form['kategori'],
                pembina=request.form['pembina'],
                jadwal=request.form['jadwal'],
                deskripsi=request.form['deskripsi'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_ekskul)
            db.session.commit()
            flash('Ekstrakurikuler baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_ekstrakurikuler'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan ekstrakurikuler: {e}', 'danger')
    return render_template('admin/edit_ekstrakurikuler.html', title='Tambah Ekstrakurikuler', ekskul=None)


@admin_bp.route('/ekstrakurikuler/edit/<int:ekskul_id>', methods=['GET', 'POST'])
@login_required
def edit_ekstrakurikuler(ekskul_id):
    """Edit existing ekstrakurikuler."""
    ekskul = Ekstrakurikuler.query.get_or_404(ekskul_id)
    
    if request.method == 'POST':
        try:
            ekskul.nama = request.form['nama']
            ekskul.kategori = request.form['kategori']
            ekskul.pembina = request.form['pembina']
            ekskul.jadwal = request.form['jadwal']
            ekskul.deskripsi = request.form['deskripsi']
            ekskul.image_url = request.form.get('image_num', '1')
            db.session.commit()
            flash('Ekstrakurikuler berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_ekstrakurikuler'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui ekstrakurikuler: {e}', 'danger')

    return render_template('admin/edit_ekstrakurikuler.html', title=f'Edit Ekstrakurikuler: {ekskul.nama}', ekskul=ekskul)


@admin_bp.route('/ekstrakurikuler/delete/<int:ekskul_id>', methods=['POST'])
@login_required
def delete_ekstrakurikuler(ekskul_id):
    """Delete ekstrakurikuler."""
    ekskul = Ekstrakurikuler.query.get_or_404(ekskul_id)
    try:
        db.session.delete(ekskul)
        db.session.commit()
        flash(f'Ekstrakurikuler "{ekskul.nama}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus ekstrakurikuler: {e}', 'danger')
    return redirect(url_for('admin.manage_ekstrakurikuler'))
