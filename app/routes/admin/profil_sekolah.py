# Profil Sekolah CRUD Routes with Photo Upload
"""
Profil Sekolah Management Routes.

Provides endpoints for managing school profile sections including:
- Sejarah (History)
- Visi & Misi (Vision & Mission)
- Sambutan Kepala Sekolah (Principal's Greeting with Photo)
"""
from flask import render_template, request, flash, redirect, url_for, jsonify
from app import db
from app.models.models import SekolahInfo
from app.utils.decorators import login_required
from app.utils.file_upload import save_uploaded_file, delete_file
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
    """
    Edit principal's greeting with photo upload.
    
    Now supports:
    - Foto kepala sekolah (image upload)
    - Nama kepala sekolah
    - Sambutan text
    """
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
        db.session.commit()
        
    if request.method == 'POST':
        try:
            # Handle photo upload
            if 'foto_kepsek' in request.files:
                file = request.files['foto_kepsek']
                if file and file.filename:
                    # Delete old photo if exists
                    if info.foto_kepala_sekolah:
                        delete_file(info.foto_kepala_sekolah)
                    # Save new photo
                    new_url = save_uploaded_file(file, 'kepsek')
                    if new_url:
                        info.foto_kepala_sekolah = new_url
            
            # Update text fields
            info.nama_kepala_sekolah = request.form.get('nama_kepsek', '')
            info.sambutan_kepsek = request.form.get('konten', '')
            
            db.session.commit()
            flash('Sambutan Kepala Sekolah berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_profil_sekolah'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui Sambutan: {e}', 'danger')
            
    return render_template('admin/edit_sambutan.html', 
                          title='Edit Sambutan Kepala Sekolah', 
                          info=info)


# ============================================================================
# REST API ROUTES (JSON)
# ============================================================================

@admin_bp.route('/api/sambutan', methods=['GET'])
@login_required
def api_get_sambutan():
    """
    API: Get sambutan kepala sekolah data.
    
    ---
    tags:
      - Profil Sekolah
    responses:
      200:
        description: Sambutan data
    """
    info = SekolahInfo.query.first()
    if not info:
        return jsonify({
            'success': True,
            'data': {
                'nama_kepala_sekolah': None,
                'foto_kepala_sekolah': None,
                'sambutan_kepsek': None
            }
        })
    
    return jsonify({
        'success': True,
        'data': {
            'nama_kepala_sekolah': info.nama_kepala_sekolah,
            'foto_kepala_sekolah': info.foto_kepala_sekolah,
            'sambutan_kepsek': info.sambutan_kepsek
        }
    })


@admin_bp.route('/api/sambutan', methods=['PUT'])
@login_required
def api_update_sambutan():
    """
    API: Update sambutan kepala sekolah.
    
    ---
    tags:
      - Profil Sekolah
    consumes:
      - multipart/form-data
    parameters:
      - name: foto_kepsek
        in: formData
        type: file
        required: false
      - name: nama_kepsek
        in: formData
        type: string
        required: false
      - name: konten
        in: formData
        type: string
        required: false
    responses:
      200:
        description: Sambutan updated successfully
    """
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
    
    try:
        # Handle photo upload
        if 'foto_kepsek' in request.files:
            file = request.files['foto_kepsek']
            if file and file.filename:
                if info.foto_kepala_sekolah:
                    delete_file(info.foto_kepala_sekolah)
                new_url = save_uploaded_file(file, 'kepsek')
                if new_url:
                    info.foto_kepala_sekolah = new_url
        
        if 'nama_kepsek' in request.form:
            info.nama_kepala_sekolah = request.form['nama_kepsek']
        if 'konten' in request.form:
            info.sambutan_kepsek = request.form['konten']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sambutan berhasil diperbarui',
            'data': {
                'nama_kepala_sekolah': info.nama_kepala_sekolah,
                'foto_kepala_sekolah': info.foto_kepala_sekolah
            }
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
