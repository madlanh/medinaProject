# Alumni Testimoni CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import AlumniTestimoni
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/alumni')
@login_required
def manage_alumni():
    """List all alumni testimonials."""
    alumni_list = AlumniTestimoni.query.order_by(AlumniTestimoni.tahun_lulus.desc()).all()
    return render_template('admin/manage_alumni.html', alumni_list=alumni_list)


@admin_bp.route('/alumni/create', methods=['GET', 'POST'])
@login_required
def create_alumni():
    """Create new alumni testimonial."""
    if request.method == 'POST':
        try:
            tahun_lulus_str = request.form.get('tahun_lulus')
            new_alumni = AlumniTestimoni(
                nama=request.form['nama'],
                tahun_lulus=int(tahun_lulus_str) if tahun_lulus_str else None,
                testimoni=request.form['testimoni'],
                status_saat_ini=request.form['status_saat_ini'],
                image_url=request.form.get('image_url', ''),
                is_featured='is_featured' in request.form
            )
            db.session.add(new_alumni)
            db.session.commit()
            flash('Alumni testimoni baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_alumni'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan alumni: {e}', 'danger')
    return render_template('admin/edit_alumni.html', title='Tambah Alumni Testimoni', alumni=None)


@admin_bp.route('/alumni/edit/<int:alumni_id>', methods=['GET', 'POST'])
@login_required
def edit_alumni(alumni_id):
    """Edit existing alumni testimonial."""
    alumni = AlumniTestimoni.query.get_or_404(alumni_id)
    
    if request.method == 'POST':
        try:
            tahun_lulus_str = request.form.get('tahun_lulus')
            alumni.nama = request.form['nama']
            alumni.tahun_lulus = int(tahun_lulus_str) if tahun_lulus_str else None
            alumni.testimoni = request.form['testimoni']
            alumni.status_saat_ini = request.form['status_saat_ini']
            alumni.image_url = request.form.get('image_url', '')
            alumni.is_featured = 'is_featured' in request.form
            db.session.commit()
            flash('Data alumni berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_alumni'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui data alumni: {e}', 'danger')

    return render_template('admin/edit_alumni.html', title=f'Edit Alumni: {alumni.nama}', alumni=alumni)


@admin_bp.route('/alumni/delete/<int:alumni_id>', methods=['POST'])
@login_required
def delete_alumni(alumni_id):
    """Delete alumni testimonial."""
    alumni = AlumniTestimoni.query.get_or_404(alumni_id)
    try:
        db.session.delete(alumni)
        db.session.commit()
        flash(f'Alumni "{alumni.nama}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus alumni: {e}', 'danger')
    return redirect(url_for('admin.manage_alumni'))
