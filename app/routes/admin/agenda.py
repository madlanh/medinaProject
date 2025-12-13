# Agenda CRUD Routes
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.models import Agenda
from app.utils.decorators import login_required
from datetime import datetime
from app.routes.admin import admin_bp


@admin_bp.route('/agenda')
@login_required
def manage_agenda():
    """List all agenda."""
    agenda_list = Agenda.query.order_by(Agenda.tanggal.desc()).all()
    return render_template('admin/manage_agenda.html', agenda_list=agenda_list)


@admin_bp.route('/agenda/create', methods=['GET', 'POST'])
@login_required
def create_agenda():
    """Create new agenda."""
    if request.method == 'POST':
        try:
            new_agenda = Agenda(
                judul=request.form['judul'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d'),
                deskripsi=request.form['deskripsi'],
                lokasi=request.form['lokasi'],
                waktu_display=request.form['waktu'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_agenda)
            db.session.commit()
            flash('Agenda baru berhasil dibuat!', 'success')
            return redirect(url_for('admin.manage_agenda'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal membuat agenda: {e}', 'danger')
    return render_template('admin/edit_agenda.html', title='Buat Agenda Baru', agenda=None)


@admin_bp.route('/agenda/edit/<int:agenda_id>', methods=['GET', 'POST'])
@login_required
def edit_agenda(agenda_id):
    """Edit existing agenda."""
    agenda = Agenda.query.get_or_404(agenda_id)
    
    if request.method == 'POST':
        try:
            agenda.judul = request.form['judul']
            agenda.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d')
            agenda.deskripsi = request.form['deskripsi']
            agenda.lokasi = request.form['lokasi']
            agenda.waktu_display = request.form['waktu']
            agenda.image_url = request.form.get('image_num', '1')
            db.session.commit()
            flash('Agenda berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_agenda'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui agenda: {e}', 'danger')

    return render_template('admin/edit_agenda.html', title=f'Edit Agenda: {agenda.judul}', agenda=agenda)


@admin_bp.route('/agenda/delete/<int:agenda_id>', methods=['POST'])
@login_required
def delete_agenda(agenda_id):
    """Delete agenda."""
    agenda = Agenda.query.get_or_404(agenda_id)
    try:
        db.session.delete(agenda)
        db.session.commit()
        flash(f'Agenda "{agenda.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus agenda: {e}', 'danger')
    return redirect(url_for('admin.manage_agenda'))
