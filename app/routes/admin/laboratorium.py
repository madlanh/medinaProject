# Laboratorium CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Laboratorium, LaboratoriumFasilitas
from app.utils.decorators import login_required
from app.routes.admin import admin_bp


@admin_bp.route('/laboratorium')
@login_required
def manage_laboratorium():
    """List all laboratorium."""
    lab_list = Laboratorium.query.all()
    return render_template('admin/manage_laboratorium.html', lab_list=lab_list)


@admin_bp.route('/laboratorium/create', methods=['GET', 'POST'])
@login_required
def create_laboratorium():
    """Create new laboratorium."""
    if request.method == 'POST':
        try:
            new_lab = Laboratorium(
                nama=request.form['nama'],
                deskripsi=request.form['deskripsi'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_lab)
            db.session.flush()  # Get ID
            
            fasilitas_str = request.form['fasilitas']
            fasilitas_list = [f.strip() for f in fasilitas_str.split(',') if f.strip()]
            
            for f_name in fasilitas_list:
                new_fasilitas = LaboratoriumFasilitas(laboratorium_id=new_lab.id, nama_fasilitas=f_name)
                db.session.add(new_fasilitas)
                
            db.session.commit()
            flash('Laboratorium baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_laboratorium'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan laboratorium: {e}', 'danger')
    return render_template('admin/edit_laboratorium.html', title='Tambah Laboratorium', lab=None)


@admin_bp.route('/laboratorium/edit/<int:lab_id>', methods=['GET', 'POST'])
@login_required
def edit_laboratorium(lab_id):
    """Edit existing laboratorium."""
    lab = Laboratorium.query.get_or_404(lab_id)
    
    if request.method == 'POST':
        try:
            lab.nama = request.form['nama']
            lab.deskripsi = request.form['deskripsi']
            lab.image_url = request.form.get('image_num', '1')
            
            # Update facilities: delete all and re-add
            LaboratoriumFasilitas.query.filter_by(laboratorium_id=lab.id).delete()
            
            fasilitas_str = request.form['fasilitas']
            fasilitas_list = [f.strip() for f in fasilitas_str.split(',') if f.strip()]
            
            for f_name in fasilitas_list:
                new_fasilitas = LaboratoriumFasilitas(laboratorium_id=lab.id, nama_fasilitas=f_name)
                db.session.add(new_fasilitas)
                
            db.session.commit()
            flash('Laboratorium berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_laboratorium'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui laboratorium: {e}', 'danger')

    # Prepare facilities string for the form
    current_fasilitas = [f.nama_fasilitas for f in lab.fasilitas]
    lab.fasilitas_str = ", ".join(current_fasilitas)
    
    return render_template('admin/edit_laboratorium.html', title=f'Edit Laboratorium: {lab.nama}', lab=lab)


@admin_bp.route('/laboratorium/delete/<int:lab_id>', methods=['POST'])
@login_required
def delete_laboratorium(lab_id):
    """Delete laboratorium."""
    lab = Laboratorium.query.get_or_404(lab_id)
    try:
        db.session.delete(lab)
        db.session.commit()
        flash(f'Laboratorium "{lab.nama}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus laboratorium: {e}', 'danger')
    return redirect(url_for('admin.manage_laboratorium'))
