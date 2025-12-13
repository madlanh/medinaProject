# Banner CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Banner
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/banner')
@login_required
def manage_banner():
    """List all banners."""
    banner_list = Banner.query.all()
    return render_template('admin/manage_banner.html', banner_list=banner_list)


@admin_bp.route('/banner/create', methods=['GET', 'POST'])
@login_required
def create_banner():
    """Create new banner."""
    if request.method == 'POST':
        try:
            new_banner = Banner(
                judul=request.form['judul'],
                subjudul=request.form['subjudul'],
                image_url=request.form.get('image_num', '1'),
                is_active='aktif' in request.form
            )
            db.session.add(new_banner)
            db.session.commit()
            flash('Banner baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_banner'))
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
            banner.judul = request.form['judul']
            banner.subjudul = request.form['subjudul']
            banner.image_url = request.form.get('image_num', '1')
            banner.is_active = 'aktif' in request.form
            db.session.commit()
            flash('Banner berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_banner'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui banner: {e}', 'danger')

    return render_template('admin/edit_banner.html', title=f'Edit Banner: {banner.judul}', banner=banner)


@admin_bp.route('/banner/delete/<int:banner_id>', methods=['POST'])
@login_required
def delete_banner(banner_id):
    """Delete banner."""
    banner = Banner.query.get_or_404(banner_id)
    try:
        db.session.delete(banner)
        db.session.commit()
        flash(f'Banner "{banner.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus banner: {e}', 'danger')
    return redirect(url_for('admin.manage_banner'))
