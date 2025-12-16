# Galeri CRUD Routes with REST API
"""
Galeri Management CRUD Routes.

Provides endpoints for managing gallery photos with actual file upload.
Replaces the dummy image_num system with real file handling.
"""
from flask import render_template, request, flash, redirect, url_for, jsonify
from app import db
from app.models.models import Galeri
from app.utils.decorators import login_required
from app.utils.file_upload import save_uploaded_file, delete_file
from datetime import datetime
from app.routes.admin import admin_bp


# ============================================================================
# WEB ROUTES (HTML)
# ============================================================================

@admin_bp.route('/galeri')
@login_required
def manage_galeri():
    """List all galeri."""
    galeri_list = Galeri.query.order_by(Galeri.tanggal.desc()).all()
    return render_template('admin/manage_galeri.html', galeri_list=galeri_list)


@admin_bp.route('/galeri/create', methods=['GET', 'POST'])
@login_required
def create_galeri():
    """
    Create new galeri item with actual file upload.
    
    Handles image upload and saves to static/images/galeri/
    """
    if request.method == 'POST':
        try:
            # Handle file upload
            image_url = None
            if 'foto' in request.files:
                file = request.files['foto']
                if file and file.filename:
                    image_url = save_uploaded_file(file, 'galeri')
            
            if not image_url:
                flash('Gambar wajib diupload!', 'danger')
                return render_template('admin/edit_galeri.html', title='Tambah Foto Galeri', galeri=None)
            
            new_galeri = Galeri(
                judul=request.form['judul'],
                kategori=request.form['kategori'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                deskripsi=request.form['deskripsi'],
                image_url=image_url
            )
            db.session.add(new_galeri)
            db.session.commit()
            flash('Foto galeri baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_galeri'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan foto: {e}', 'danger')
    return render_template('admin/edit_galeri.html', title='Tambah Foto Galeri', galeri=None)


@admin_bp.route('/galeri/edit/<int:galeri_id>', methods=['GET', 'POST'])
@login_required
def edit_galeri(galeri_id):
    """
    Edit existing galeri item.
    
    Handles optional image upload - keeps old image if no new upload.
    """
    galeri = Galeri.query.get_or_404(galeri_id)
    
    if request.method == 'POST':
        try:
            # Handle file upload (optional for edit)
            if 'foto' in request.files:
                file = request.files['foto']
                if file and file.filename:
                    # Delete old image
                    if galeri.image_url:
                        delete_file(galeri.image_url)
                    # Save new image
                    new_url = save_uploaded_file(file, 'galeri')
                    if new_url:
                        galeri.image_url = new_url
            
            galeri.judul = request.form['judul']
            galeri.kategori = request.form['kategori']
            galeri.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            galeri.deskripsi = request.form['deskripsi']
            db.session.commit()
            flash('Foto galeri berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_galeri'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui foto: {e}', 'danger')

    return render_template('admin/edit_galeri.html', title=f'Edit Galeri: {galeri.judul}', galeri=galeri)


@admin_bp.route('/galeri/delete/<int:galeri_id>', methods=['POST'])
@login_required
def delete_galeri(galeri_id):
    """
    Delete galeri item and its image file.
    """
    galeri = Galeri.query.get_or_404(galeri_id)
    try:
        # Delete image file
        if galeri.image_url:
            delete_file(galeri.image_url)
        
        db.session.delete(galeri)
        db.session.commit()
        flash(f'Foto "{galeri.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus foto: {e}', 'danger')
    return redirect(url_for('admin.manage_galeri'))


# ============================================================================
# REST API ROUTES (JSON)
# ============================================================================

@admin_bp.route('/api/galeri', methods=['GET'])
@login_required
def api_list_galeri():
    """
    API: Get all galeri items.
    
    ---
    tags:
      - Galeri
    responses:
      200:
        description: List of all gallery photos
    """
    galeri_list = Galeri.query.order_by(Galeri.tanggal.desc()).all()
    return jsonify({
        'success': True,
        'data': [{
            'id': g.id,
            'judul': g.judul,
            'kategori': g.kategori,
            'tanggal': g.tanggal.strftime('%Y-%m-%d') if g.tanggal else None,
            'deskripsi': g.deskripsi,
            'image_url': g.image_url
        } for g in galeri_list]
    })


@admin_bp.route('/api/galeri', methods=['POST'])
@login_required
def api_create_galeri():
    """
    API: Create new galeri item.
    
    ---
    tags:
      - Galeri
    consumes:
      - multipart/form-data
    parameters:
      - name: foto
        in: formData
        type: file
        required: true
      - name: judul
        in: formData
        type: string
        required: true
      - name: kategori
        in: formData
        type: string
        required: true
      - name: tanggal
        in: formData
        type: string
        format: date
        required: true
      - name: deskripsi
        in: formData
        type: string
        required: false
    responses:
      201:
        description: Galeri created successfully
      400:
        description: Bad request
    """
    try:
        # Handle file upload
        image_url = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename:
                image_url = save_uploaded_file(file, 'galeri')
        
        if not image_url:
            return jsonify({'success': False, 'error': 'Gambar wajib diupload'}), 400
        
        new_galeri = Galeri(
            judul=request.form['judul'],
            kategori=request.form.get('kategori', 'Lainnya'),
            tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
            deskripsi=request.form.get('deskripsi', ''),
            image_url=image_url
        )
        db.session.add(new_galeri)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Foto galeri berhasil ditambahkan',
            'data': {
                'id': new_galeri.id,
                'judul': new_galeri.judul,
                'image_url': new_galeri.image_url
            }
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/api/galeri/<int:galeri_id>', methods=['GET'])
@login_required
def api_get_galeri(galeri_id):
    """
    API: Get single galeri by ID.
    
    ---
    tags:
      - Galeri
    parameters:
      - name: galeri_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Galeri data
      404:
        description: Galeri not found
    """
    galeri = Galeri.query.get_or_404(galeri_id)
    return jsonify({
        'success': True,
        'data': {
            'id': galeri.id,
            'judul': galeri.judul,
            'kategori': galeri.kategori,
            'tanggal': galeri.tanggal.strftime('%Y-%m-%d') if galeri.tanggal else None,
            'deskripsi': galeri.deskripsi,
            'image_url': galeri.image_url
        }
    })


@admin_bp.route('/api/galeri/<int:galeri_id>', methods=['PUT'])
@login_required
def api_update_galeri(galeri_id):
    """
    API: Update existing galeri.
    
    ---
    tags:
      - Galeri
    consumes:
      - multipart/form-data
    parameters:
      - name: galeri_id
        in: path
        type: integer
        required: true
      - name: foto
        in: formData
        type: file
        required: false
      - name: judul
        in: formData
        type: string
      - name: kategori
        in: formData
        type: string
      - name: tanggal
        in: formData
        type: string
        format: date
      - name: deskripsi
        in: formData
        type: string
    responses:
      200:
        description: Galeri updated successfully
      404:
        description: Galeri not found
    """
    galeri = Galeri.query.get_or_404(galeri_id)
    
    try:
        # Handle file upload (optional)
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename:
                if galeri.image_url:
                    delete_file(galeri.image_url)
                new_url = save_uploaded_file(file, 'galeri')
                if new_url:
                    galeri.image_url = new_url
        
        if 'judul' in request.form:
            galeri.judul = request.form['judul']
        if 'kategori' in request.form:
            galeri.kategori = request.form['kategori']
        if 'tanggal' in request.form:
            galeri.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
        if 'deskripsi' in request.form:
            galeri.deskripsi = request.form['deskripsi']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Foto galeri berhasil diperbarui',
            'data': {
                'id': galeri.id,
                'judul': galeri.judul,
                'image_url': galeri.image_url
            }
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/api/galeri/<int:galeri_id>', methods=['DELETE'])
@login_required
def api_delete_galeri(galeri_id):
    """
    API: Delete galeri.
    
    ---
    tags:
      - Galeri
    parameters:
      - name: galeri_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Galeri deleted successfully
      404:
        description: Galeri not found
    """
    galeri = Galeri.query.get_or_404(galeri_id)
    
    try:
        if galeri.image_url:
            delete_file(galeri.image_url)
        
        db.session.delete(galeri)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Foto "{galeri.judul}" berhasil dihapus'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
