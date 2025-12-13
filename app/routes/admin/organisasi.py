# Organisasi CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Organisasi
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/organisasi')
@login_required
def manage_organisasi():
    """List all organization members."""
    org_list = Organisasi.query.order_by(Organisasi.level.asc()).all()
    return render_template('admin/manage_organisasi.html', org_list=org_list)


@admin_bp.route('/organisasi/create', methods=['GET', 'POST'])
@login_required
def create_organisasi():
    """Create new organization member."""
    if request.method == 'POST':
        try:
            new_org = Organisasi(
                nama=request.form['nama'],
                jabatan=request.form['jabatan'],
                level=int(request.form['level']),
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_org)
            db.session.commit()
            flash('Anggota organisasi baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_organisasi'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan anggota organisasi: {e}', 'danger')
    return render_template('admin/edit_organisasi.html', title='Tambah Anggota Organisasi', org=None)


@admin_bp.route('/organisasi/edit/<int:org_id>', methods=['GET', 'POST'])
@login_required
def edit_organisasi_member(org_id):
    """Edit existing organization member."""
    org = Organisasi.query.get_or_404(org_id)
    
    if request.method == 'POST':
        try:
            org.nama = request.form['nama']
            org.jabatan = request.form['jabatan']
            org.level = int(request.form['level'])
            org.image_url = request.form.get('image_num', '1')
            db.session.commit()
            flash('Data anggota organisasi berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_organisasi'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui data anggota: {e}', 'danger')

    return render_template('admin/edit_organisasi.html', title=f'Edit Anggota: {org.nama}', org=org)


@admin_bp.route('/organisasi/delete/<int:org_id>', methods=['POST'])
@login_required
def delete_organisasi(org_id):
    """Delete organization member."""
    org = Organisasi.query.get_or_404(org_id)
    try:
        db.session.delete(org)
        db.session.commit()
        flash(f'Anggota "{org.nama}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus anggota: {e}', 'danger')
    return redirect(url_for('admin.manage_organisasi'))
