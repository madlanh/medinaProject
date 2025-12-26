# Banner CRUD Routes with REST API
"""
Banner Management CRUD Routes.

Provides endpoints for managing hero banners on the homepage.
Includes file upload, toggle active status, and display order management.
"""
from flask import render_template, request, flash, redirect, url_for, jsonify
from app import db
from app.models.models import Banner
from app.utils.decorators import login_required
from app.utils.file_upload import save_uploaded_file, delete_file
from app.routes.admin import admin_bp


# ============================================================================
# WEB ROUTES (HTML)
# ============================================================================

@admin_bp.route('/banner')
@login_required
def manage_banner():
    """List all banners."""
    banners = Banner.query.order_by(Banner.display_order, Banner.id.desc()).all()
    return render_template('admin/manage_banner.html', banners=banners)


@admin_bp.route('/banner/create', methods=['GET', 'POST'])
@login_required
def create_banner():
    """Create new banner with image upload."""
    if request.method == 'POST':
        try:
            # Handle file upload
            image_url = None
            
            # PERBAIKAN: Menggunakan 'image_file' sesuai name di HTML
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file and file.filename:
                    image_url = save_uploaded_file(file, 'banners')
            
            # Fallback check jika nama input di API masih 'gambar'
            elif 'gambar' in request.files:
                file = request.files['gambar']
                if file and file.filename:
                    image_url = save_uploaded_file(file, 'banners')
            
            if not image_url:
                flash('Gambar wajib diupload!', 'danger')
                return render_template('admin/edit_banner.html', title='Tambah Banner', banner=None)
            
            # Get max display_order for auto numbering
            max_order = db.session.query(db.func.max(Banner.display_order)).scalar() or 0
            
            new_banner = Banner(
                judul=request.form.get('judul', ''),
                subjudul=request.form.get('subjudul', ''),
                image_url=image_url,
                is_active=request.form.get('is_active') == 'on',
                display_order=max_order + 1
            )
            db.session.add(new_banner)
            db.session.commit()
            flash('Banner baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_banner'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan banner: {e}', 'danger')
    
    return render_template('admin/edit_banner.html', title='Tambah Banner', banner=None)


@admin_bp.route('/banner/edit/<int:banner_id>', methods=['GET', 'POST'])
@login_required
def edit_banner(banner_id):
    """Edit existing banner."""
    banner = Banner.query.get_or_404(banner_id)
    
    if request.method == 'POST':
        try:
            # Handle file upload (optional for edit)
            # PERBAIKAN: Cek 'image_file' dulu
            file = request.files.get('image_file') or request.files.get('gambar')
            
            if file and file.filename:
                # Delete old image
                if banner.image_url:
                    delete_file(banner.image_url)
                # Save new image
                new_url = save_uploaded_file(file, 'banners')
                if new_url:
                    banner.image_url = new_url
            
            banner.judul = request.form.get('judul', '')
            banner.subjudul = request.form.get('subjudul', '')
            banner.is_active = request.form.get('is_active') == 'on'
            banner.display_order = int(request.form.get('display_order', 0))
            
            db.session.commit()
            flash('Banner berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_banner'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui banner: {e}', 'danger')
    
    return render_template('admin/edit_banner.html', title=f'Edit Banner', banner=banner)


@admin_bp.route('/banner/delete/<int:banner_id>', methods=['POST'])
@login_required
def delete_banner(banner_id):
    """Delete banner and its image file."""
    banner = Banner.query.get_or_404(banner_id)
    try:
        # Delete image file
        if banner.image_url:
            delete_file(banner.image_url)
        
        db.session.delete(banner)
        db.session.commit()
        flash(f'Banner "{banner.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus banner: {e}', 'danger')
    return redirect(url_for('admin.manage_banner'))


@admin_bp.route('/banner/toggle/<int:banner_id>', methods=['POST'])
@login_required
def toggle_banner(banner_id):
    """Toggle banner active status."""
    banner = Banner.query.get_or_404(banner_id)
    try:
        banner.is_active = not banner.is_active
        db.session.commit()
        status = 'aktif' if banner.is_active else 'nonaktif'
        flash(f'Banner "{banner.judul}" sekarang {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal mengubah status banner: {e}', 'danger')
    return redirect(url_for('admin.manage_banner'))


# ============================================================================
# REST API ROUTES (JSON)
# ============================================================================

@admin_bp.route('/api/banners', methods=['GET'])
@login_required
def api_list_banners():
    """API: Get all banners."""
    banners = Banner.query.order_by(Banner.display_order).all()
    return jsonify({
        'success': True,
        'data': [{
            'id': b.id,
            'judul': b.judul,
            'subjudul': b.subjudul,
            'image_url': b.image_url,
            'is_active': b.is_active,
            'display_order': b.display_order
        } for b in banners]
    })


@admin_bp.route('/api/banners', methods=['POST'])
@login_required
def api_create_banner():
    """API: Create new banner."""
    try:
        # Handle file upload
        image_url = None
        # Support both names for API flexibility
        file = request.files.get('gambar') or request.files.get('image_file')
        
        if file and file.filename:
            image_url = save_uploaded_file(file, 'banners')
        
        if not image_url:
            return jsonify({'success': False, 'error': 'Gambar wajib diupload'}), 400
        
        max_order = db.session.query(db.func.max(Banner.display_order)).scalar() or 0
        
        new_banner = Banner(
            judul=request.form.get('judul', ''),
            subjudul=request.form.get('subjudul', ''),
            image_url=image_url,
            is_active=request.form.get('is_active', 'true').lower() == 'true',
            display_order=max_order + 1
        )
        db.session.add(new_banner)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Banner berhasil ditambahkan',
            'data': {
                'id': new_banner.id,
                'judul': new_banner.judul,
                'image_url': new_banner.image_url,
                'display_order': new_banner.display_order
            }
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/api/banners/<int:banner_id>', methods=['GET'])
@login_required
def api_get_banner(banner_id):
    """API: Get single banner by ID."""
    banner = Banner.query.get_or_404(banner_id)
    return jsonify({
        'success': True,
        'data': {
            'id': banner.id,
            'judul': banner.judul,
            'subjudul': banner.subjudul,
            'image_url': banner.image_url,
            'is_active': banner.is_active,
            'display_order': banner.display_order
        }
    })


@admin_bp.route('/api/banners/<int:banner_id>', methods=['PUT'])
@login_required
def api_update_banner(banner_id):
    """API: Update existing banner."""
    banner = Banner.query.get_or_404(banner_id)
    
    try:
        # Handle file upload (optional)
        file = request.files.get('gambar') or request.files.get('image_file')
        
        if file and file.filename:
            if banner.image_url:
                delete_file(banner.image_url)
            new_url = save_uploaded_file(file, 'banners')
            if new_url:
                banner.image_url = new_url
        
        if 'judul' in request.form:
            banner.judul = request.form['judul']
        if 'subjudul' in request.form:
            banner.subjudul = request.form['subjudul']
        if 'is_active' in request.form:
            banner.is_active = request.form['is_active'].lower() == 'true'
        if 'display_order' in request.form:
            banner.display_order = int(request.form['display_order'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Banner berhasil diperbarui',
            'data': {
                'id': banner.id,
                'judul': banner.judul,
                'image_url': banner.image_url
            }
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/api/banners/<int:banner_id>', methods=['DELETE'])
@login_required
def api_delete_banner(banner_id):
    """API: Delete banner."""
    banner = Banner.query.get_or_404(banner_id)
    
    try:
        if banner.image_url:
            delete_file(banner.image_url)
        
        db.session.delete(banner)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Banner "{banner.judul}" berhasil dihapus'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/api/banners/<int:banner_id>/toggle', methods=['POST'])
@login_required
def api_toggle_banner(banner_id):
    """API: Toggle banner active status."""
    banner = Banner.query.get_or_404(banner_id)
    
    try:
        banner.is_active = not banner.is_active
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Banner sekarang {"aktif" if banner.is_active else "nonaktif"}',
            'data': {'is_active': banner.is_active}
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
