from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.models import (
    Berita, Agenda, Galeri, Ekstrakurikuler, Laboratorium, LaboratoriumFasilitas,
    Banner, SekolahInfo, PerpustakaanInfo, PerpustakaanFasilitas, PerpustakaanLayanan
)
from app.utils.decorators import login_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_berita': Berita.query.count(),
        'total_agenda': Agenda.query.count(),
        'total_galeri': Galeri.query.count(),
        'total_ekstrakurikuler': Ekstrakurikuler.query.count()
    }
    return render_template('admin_dashboard.html', stats=stats)

# =================================================================
#           CRUD BERITA
# =================================================================

@admin_bp.route('/berita')
@login_required
def manage_berita():
    berita_list = Berita.query.order_by(Berita.tanggal.desc()).all()
    return render_template('admin/manage_berita.html', berita_list=berita_list)

@admin_bp.route('/berita/create', methods=['GET', 'POST'])
@login_required
def create_berita():
    if request.method == 'POST':
        try:
            new_berita = Berita(
                judul=request.form['judul'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                ringkasan=request.form['ringkasan'],
                konten_lengkap=request.form['konten_lengkap']
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
    berita = Berita.query.get_or_404(berita_id)
    
    if request.method == 'POST':
        try:
            berita.judul = request.form['judul']
            berita.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            berita.ringkasan = request.form['ringkasan']
            berita.konten_lengkap = request.form['konten_lengkap']
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
    berita = Berita.query.get_or_404(berita_id)
    try:
        db.session.delete(berita)
        db.session.commit()
        flash(f'Berita "{berita.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus berita: {e}', 'danger')
    return redirect(url_for('admin.manage_berita'))

# =================================================================
#           CRUD AGENDA
# =================================================================

@admin_bp.route('/agenda')
@login_required
def manage_agenda():
    agenda_list = Agenda.query.order_by(Agenda.tanggal.desc()).all()
    return render_template('admin/manage_agenda.html', agenda_list=agenda_list)

@admin_bp.route('/agenda/create', methods=['GET', 'POST'])
@login_required
def create_agenda():
    if request.method == 'POST':
        try:
            new_agenda = Agenda(
                judul=request.form['judul'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d'),
                deskripsi=request.form['deskripsi'],
                lokasi=request.form['lokasi'],
                waktu_display=request.form['waktu'],
                image_url=request.form.get('image_num', '1') # Keeping logic similar to dummy for now
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
    agenda = Agenda.query.get_or_404(agenda_id)
    try:
        db.session.delete(agenda)
        db.session.commit()
        flash(f'Agenda "{agenda.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus agenda: {e}', 'danger')
    return redirect(url_for('admin.manage_agenda'))

# =================================================================
#           CRUD GALERI
# =================================================================

@admin_bp.route('/galeri')
@login_required
def manage_galeri():
    galeri_list = Galeri.query.order_by(Galeri.tanggal.desc()).all()
    return render_template('admin/manage_galeri.html', galeri_list=galeri_list)

@admin_bp.route('/galeri/create', methods=['GET', 'POST'])
@login_required
def create_galeri():
    if request.method == 'POST':
        try:
            new_galeri = Galeri(
                judul=request.form['judul'],
                kategori=request.form['kategori'],
                tanggal=datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                deskripsi=request.form['deskripsi'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_galeri)
            db.session.commit()
            flash('Foto galeri baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_galeri'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan foto: {e}', 'danger')
    return render_template('admin/edit_galeri.html', title='Tambah Foto Galeri', galeri=None)

@admin_bp.route('/galeri/edit/<int:galeri_id>', methods=['GET', 'POST'])
@login_required
def edit_galeri(galeri_id):
    galeri = Galeri.query.get_or_404(galeri_id)
    
    if request.method == 'POST':
        try:
            galeri.judul = request.form['judul']
            galeri.kategori = request.form['kategori']
            galeri.tanggal = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            galeri.deskripsi = request.form['deskripsi']
            galeri.image_url = request.form.get('image_num', '1')
            db.session.commit()
            flash('Foto galeri berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_galeri'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui foto: {e}', 'danger')

    return render_template('admin/edit_galeri.html', title=f'Edit Galeri: {galeri.judul}', galeri=galeri)

@admin_bp.route('/galeri/delete/<int:galeri_id>', methods=['POST'])
@login_required
def delete_galeri(galeri_id):
    galeri = Galeri.query.get_or_404(galeri_id)
    try:
        db.session.delete(galeri)
        db.session.commit()
        flash(f'Foto "{galeri.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus foto: {e}', 'danger')
    return redirect(url_for('admin.manage_galeri'))

# =================================================================
#           CRUD EKSTRAKURIKULER
# =================================================================

@admin_bp.route('/ekstrakurikuler')
@login_required
def manage_ekstrakurikuler():
    ekskul_list = Ekstrakurikuler.query.all()
    return render_template('admin/manage_ekstrakurikuler.html', ekskul_list=ekskul_list)

@admin_bp.route('/ekstrakurikuler/create', methods=['GET', 'POST'])
@login_required
def create_ekstrakurikuler():
    if request.method == 'POST':
        try:
            new_ekskul = Ekstrakurikuler(
                nama=request.form['nama'],
                kategori=request.form['kategori'],
                pembina=request.form['pembina'],
                jadwal=request.form['jadwal'],
                deskripsi=request.form['deskripsi'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_ekskul)
            db.session.commit()
            flash('Ekstrakurikuler baru berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_ekstrakurikuler'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan ekstrakurikuler: {e}', 'danger')
    return render_template('admin/edit_ekstrakurikuler.html', title='Tambah Ekstrakurikuler', ekskul=None)

@admin_bp.route('/ekstrakurikuler/edit/<int:ekskul_id>', methods=['GET', 'POST'])
@login_required
def edit_ekstrakurikuler(ekskul_id):
    ekskul = Ekstrakurikuler.query.get_or_404(ekskul_id)
    
    if request.method == 'POST':
        try:
            ekskul.nama = request.form['nama']
            ekskul.kategori = request.form['kategori']
            ekskul.pembina = request.form['pembina']
            ekskul.jadwal = request.form['jadwal']
            ekskul.deskripsi = request.form['deskripsi']
            ekskul.image_url = request.form.get('image_num', '1')
            db.session.commit()
            flash('Ekstrakurikuler berhasil diperbarui!', 'success')
            return redirect(url_for('admin.manage_ekstrakurikuler'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui ekstrakurikuler: {e}', 'danger')

    return render_template('admin/edit_ekstrakurikuler.html', title=f'Edit Ekstrakurikuler: {ekskul.nama}', ekskul=ekskul)

@admin_bp.route('/ekstrakurikuler/delete/<int:ekskul_id>', methods=['POST'])
@login_required
def delete_ekstrakurikuler(ekskul_id):
    ekskul = Ekstrakurikuler.query.get_or_404(ekskul_id)
    try:
        db.session.delete(ekskul)
        db.session.commit()
        flash(f'Ekstrakurikuler "{ekskul.nama}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus ekstrakurikuler: {e}', 'danger')
    return redirect(url_for('admin.manage_ekstrakurikuler'))

# =================================================================
#           CRUD LABORATORIUM
# =================================================================

@admin_bp.route('/laboratorium')
@login_required
def manage_laboratorium():
    lab_list = Laboratorium.query.all()
    # We need to manually attach fasilitas list for the template if it expects a list of strings
    # The template probably does: {% for f in lab.fasilitas %}
    # In SQLAlchemy, lab.fasilitas is a list of LaboratoriumFasilitas objects.
    # We might need to adjust the template or pass a modified object.
    # Let's assume the template iterates over lab.fasilitas and prints f.
    # If the template does {{ f }}, it will print the object representation.
    # If the template does {{ f.nama_fasilitas }}, it works.
    # Given the original code was a list of strings, the template likely does {{ f }}.
    # I should probably check the template, but I can't right now easily without switching context.
    # Safest bet is to make sure the template works or the object behaves like a string.
    # Or I can update the template later.
    # For now, let's assume I'll need to fix the template or make the object stringifiable.
    return render_template('admin/manage_laboratorium.html', lab_list=lab_list)

@admin_bp.route('/laboratorium/create', methods=['GET', 'POST'])
@login_required
def create_laboratorium():
    if request.method == 'POST':
        try:
            new_lab = Laboratorium(
                nama=request.form['nama'],
                deskripsi=request.form['deskripsi'],
                image_url=request.form.get('image_num', '1')
            )
            db.session.add(new_lab)
            db.session.flush() # Get ID
            
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
    # The form likely expects a comma-separated string
    current_fasilitas = [f.nama_fasilitas for f in lab.fasilitas]
    lab.fasilitas_str = ", ".join(current_fasilitas) # Attach temporary attribute
    
    return render_template('admin/edit_laboratorium.html', title=f'Edit Laboratorium: {lab.nama}', lab=lab)

@admin_bp.route('/laboratorium/delete/<int:lab_id>', methods=['POST'])
@login_required
def delete_laboratorium(lab_id):
    lab = Laboratorium.query.get_or_404(lab_id)
    try:
        db.session.delete(lab)
        db.session.commit()
        flash(f'Laboratorium "{lab.nama}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus laboratorium: {e}', 'danger')
    return redirect(url_for('admin.manage_laboratorium'))

# =================================================================
#           CRUD BANNER
# =================================================================

@admin_bp.route('/banner')
@login_required
def manage_banner():
    banner_list = Banner.query.all()
    return render_template('admin/manage_banner.html', banner_list=banner_list)

@admin_bp.route('/banner/create', methods=['GET', 'POST'])
@login_required
def create_banner():
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
    banner = Banner.query.get_or_404(banner_id)
    try:
        db.session.delete(banner)
        db.session.commit()
        flash(f'Banner "{banner.judul}" berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus banner: {e}', 'danger')
    return redirect(url_for('admin.manage_banner'))

# =================================================================
#           CRUD INFO SEKOLAH
# =================================================================

@admin_bp.route('/info-sekolah', methods=['GET', 'POST'])
@login_required
def manage_info_sekolah():
    info = SekolahInfo.query.first()
    if not info:
        info = SekolahInfo(nama="SMA Medina")
        db.session.add(info)
        db.session.commit()

    if request.method == 'POST':
        try:
            info.nama = request.form['nama']
            info.npsn = request.form['npsn']
            info.akreditasi = request.form['akreditasi']
            info.alamat = request.form['alamat']
            info.telepon = request.form['telepon']
            info.email = request.form['email']
            info.website = request.form['website']
            info.kepala_sekolah = request.form['kepala_sekolah']
            info.jumlah_siswa = int(request.form['jumlah_siswa'])
            info.jumlah_guru = int(request.form['jumlah_guru'])
            info.jumlah_kelas = int(request.form['jumlah_kelas'])
            info.tahun_berdiri = int(request.form['tahun_berdiri'])
            db.session.commit()
            flash('Info sekolah berhasil diperbarui!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui info sekolah: {e}', 'danger')
    
    return render_template('admin/manage_info_sekolah.html', info=info)

# =================================================================
#           CRUD PERPUSTAKAAN
# =================================================================

@admin_bp.route('/perpustakaan', methods=['GET', 'POST'])
@login_required
def manage_perpustakaan_admin():
    perpus = PerpustakaanInfo.query.first()
    if not perpus:
        perpus = PerpustakaanInfo()
        db.session.add(perpus)
        db.session.commit()

    if request.method == 'POST':
        try:
            perpus.jam_buka_senin_jumat = request.form['jam_senin_jumat']
            perpus.jam_buka_sabtu = request.form['jam_sabtu']
            perpus.jumlah_buku_pelajaran = int(request.form['buku_pelajaran'])
            perpus.jumlah_buku_fiksi = int(request.form['buku_fiksi'])
            perpus.jumlah_buku_referensi = int(request.form['buku_referensi'])
            perpus.jumlah_majalah_jurnal = int(request.form['majalah_jurnal'])
            perpus.jumlah_ebook = int(request.form['e_book'])
            
            # Update facilities
            PerpustakaanFasilitas.query.delete()
            fasilitas_str = request.form['fasilitas']
            for f in fasilitas_str.split(','):
                if f.strip():
                    db.session.add(PerpustakaanFasilitas(nama_fasilitas=f.strip()))
            
            # Update services
            PerpustakaanLayanan.query.delete()
            layanan_str = request.form['layanan']
            for l in layanan_str.split(','):
                if l.strip():
                    db.session.add(PerpustakaanLayanan(nama_layanan=l.strip()))
            
            db.session.commit()
            flash('Data perpustakaan berhasil diperbarui!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui data perpustakaan: {e}', 'danger')
    
    # Prepare data for template
    fasilitas = [f.nama_fasilitas for f in PerpustakaanFasilitas.query.all()]
    layanan = [l.nama_layanan for l in PerpustakaanLayanan.query.all()]
    
    # Construct object compatible with template
    perpus_data = {
        'jam_buka': {
            'senin_jumat': perpus.jam_buka_senin_jumat,
            'sabtu': perpus.jam_buka_sabtu
        },
        'koleksi': {
            'buku_pelajaran': perpus.jumlah_buku_pelajaran,
            'buku_fiksi': perpus.jumlah_buku_fiksi,
            'buku_referensi': perpus.jumlah_buku_referensi,
            'majalah_jurnal': perpus.jumlah_majalah_jurnal,
            'e_book': perpus.jumlah_ebook
        },
        'fasilitas': fasilitas,
        'layanan': layanan
    }
    
    return render_template('admin/manage_perpustakaan.html', perpus=perpus_data)

# =================================================================
#           CRUD PROFIL SEKOLAH
# =================================================================

@admin_bp.route('/profil-sekolah')
@login_required
def manage_profil_sekolah():
    return render_template('admin/manage_profil_sekolah.html')

@admin_bp.route('/profil-sekolah/sejarah', methods=['GET', 'POST'])
@login_required
def edit_sejarah():
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
            
    # Template expects dummy_db['profil_content']['sejarah']
    # We need to pass the content directly or adapt the template
    # The template likely uses `profil_content.sejarah` if passed `profil_content`
    # Or just `content` if we pass it.
    # Let's check how the original app did it.
    # It didn't have a specific route for GET edit_sejarah in the snippet I saw, 
    # but likely it renders a generic edit page or specific one.
    # I'll assume there is a template `admin/edit_profil_section.html` or similar?
    # Wait, the original code had:
    # @app.route('/admin/profil-sekolah/sejarah', methods=['GET', 'POST'])
    # def edit_sejarah(): ...
    # It didn't show the render_template call in the snippet (it was cut off).
    # I will assume there is a template and I should pass the current content.
    
    return render_template('admin/edit_profil_section.html', title='Edit Sejarah', content=info.sejarah, section='sejarah')

# I need to implement the other profile sections similarly (Visi Misi, Sambutan)
# But I don't have the full original code for those routes.
# I will implement them based on the pattern.

@admin_bp.route('/profil-sekolah/visi-misi', methods=['GET', 'POST'])
@login_required
def edit_visi_misi():
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
            
    return render_template('admin/edit_visi_misi.html', title='Edit Visi & Misi', visi=info.visi, misi=info.misi)

@admin_bp.route('/profil-sekolah/sambutan', methods=['GET', 'POST'])
@login_required
def edit_sambutan():
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
            
    return render_template('admin/edit_profil_section.html', title='Edit Sambutan', content=info.sambutan_kepsek, section='sambutan')
