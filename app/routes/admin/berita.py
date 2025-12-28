# Berita CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Berita
from app.utils.decorators import login_required
from app.utils.file_upload import save_uploaded_file, delete_file
from datetime import datetime
from app.routes.admin import admin_bp


@admin_bp.route('/berita')
@login_required
def manage_berita():
    """List all berita."""
    berita_list = Berita.query.order_by(Berita.tanggal.desc()).all()
    return render_template('admin/manage_berita.html', berita_list=berita_list)


@admin_bp.route('/berita/create', methods=['GET', 'POST'])
@login_required
def create_berita():
    """Create new berita."""
    if request.method == 'POST':
        try:
            image_url = None
            file = request.files.get('gambar')
            
            if file and file.filename:
                image_url = save_uploaded_file(file, 'berita')
            
            new_berita = Berita(
                judul=request.form['judul'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                ringkasan=request.form['ringkasan'],
                konten_lengkap=request.form['konten_lengkap'],
                image_url=image_url
            )
            db.session.add(new_berita)
            db.session.commit()
            flash('Berita baru berhasil dibuat!', 'success')
            return redirect(url_for('admin.manage_berita'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal membuat berita: {e}', 'danger')
    return render_template('admin/edit_berita.html', title='Buat Berita Baru', berita=None)


@admin_bp.route('/berita/edit/<int:berita_id>', methods=['GET', 'POST'])
@login_required
def edit_berita(berita_id):
    """Edit existing berita."""
    berita = Berita.query.get_or_404(berita_id)
    
    if request.method == 'POST':
        try:
            berita.judul = request.form['judul']
            berita.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            berita.ringkasan = request.form['ringkasan']
            berita.konten_lengkap = request.form['konten_lengkap']
            file = request.files.get('gambar')
            if file and file.filename:
                if berita.image_url:
                    delete_file(berita.image_url)
                new_url = save_uploaded_file(file, 'berita')
                if new_url:
                    berita.image_url = new_url
            db.session.commit()
            flash('Berita berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_berita'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui berita: {e}', 'danger')

    return render_template('admin/edit_berita.html', title=f'Edit Berita: {berita.judul}', berita=berita)


@admin_bp.route('/berita/delete/<int:berita_id>', methods=['POST'])
@login_required
def delete_berita(berita_id):
    """Delete berita."""
    berita = Berita.query.get_or_404(berita_id)
    try:
        db.session.delete(berita)
        db.session.commit()
        flash(f'Berita "{berita.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus berita: {e}', 'danger')
    return redirect(url_for('admin.manage_berita'))
