# Profil Sekolah CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import SekolahInfo
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/profil-sekolah')
@login_required
def manage_profil_sekolah():
    """Manage school profile sections."""
    return render_template('admin/manage_profil_sekolah.html')


@admin_bp.route('/profil-sekolah/sejarah', methods=['GET', 'POST'])
@login_required
def edit_sejarah():
    """Edit school history."""
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
        db.session.commit()
        
    if request.method == 'POST':
        try:
            info.sejarah = request.form['konten']
            db.session.commit()
            flash('Konten Sejarah berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_profil_sekolah'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui Sejarah: {e}', 'danger')
    
    return render_template('admin/edit_profil_content.html', 
                          title='Edit Sejarah', 
                          konten=info.sejarah, 
                          section='sejarah')


@admin_bp.route('/profil-sekolah/visi-misi', methods=['GET', 'POST'])
@login_required
def edit_visi_misi():
    """Edit vision and mission."""
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
        db.session.commit()
        
    if request.method == 'POST':
        try:
            info.visi = request.form['visi']
            info.misi = request.form['misi']
            db.session.commit()
            flash('Visi & Misi berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_profil_sekolah'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui Visi & Misi: {e}', 'danger')
            
    return render_template('admin/edit_visi_misi.html', 
                          title='Edit Visi & Misi', 
                          visi=info.visi, 
                          misi=info.misi)


@admin_bp.route('/profil-sekolah/sambutan', methods=['GET', 'POST'])
@login_required
def edit_sambutan():
    """Edit principal's greeting."""
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
        db.session.commit()
        
    if request.method == 'POST':
        try:
            info.sambutan_kepsek = request.form['konten']
            db.session.commit()
            flash('Sambutan Kepala Sekolah berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_profil_sekolah'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui Sambutan: {e}', 'danger')
            
    return render_template('admin/edit_profil_content.html', 
                          title='Edit Sambutan', 
                          konten=info.sambutan_kepsek, 
                          section='sambutan')
