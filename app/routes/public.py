from flask import Blueprint, render_template
from app.models.models import Berita, Banner, Prestasi, AlumniTestimoni, SekolahInfo, Organisasi, Agenda, Galeri, Ekstrakurikuler, Laboratorium, PerpustakaanInfo
from app.utils.helpers import categorize_agenda

public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_sekolah_info():
    info = SekolahInfo.query.first()
    return dict(sekolah_info=info)

@public_bp.route('/')
def index():
    berita_beranda = Berita.query.order_by(Berita.tanggal.desc()).limit(3).all()
    banner_aktif = Banner.query.filter_by(is_active=True).order_by(Banner.display_order).all()
    prestasi_data = Prestasi.query.all() # Limit if needed
    alumni_data = AlumniTestimoni.query.all() # Limit if needed
    
    return render_template('index.html', 
                           berita=berita_beranda,
                           prestasi=prestasi_data, 
                           alumni=alumni_data,
                           banners=banner_aktif)

@public_bp.route('/sejarah')
def sejarah():
    info = SekolahInfo.query.first()
    return render_template('sejarah.html', info=info)

@public_bp.route('/visi-misi')
def visi_misi():
    info = SekolahInfo.query.first()
    return render_template('visi-misi.html', info=info)

@public_bp.route('/sambutan')
def sambutan():
    info = SekolahInfo.query.first()
    return render_template('sambutan.html', title='Sambutan Kepala Sekolah', info=info)

@public_bp.route('/organisasi')
def organisasi():
    org_data = Organisasi.query.order_by(Organisasi.level).all()
    return render_template('organisasi.html', title='Struktur Organisasi', organisasi=org_data)

@public_bp.route('/berita-terbaru')
def berita_terbaru():
    berita_list = Berita.query.order_by(Berita.tanggal.desc()).all()
    return render_template('berita_terbaru.html', title='Berita Terbaru', berita_list=berita_list)

@public_bp.route('/info-sekolah')
def info_sekolah():
    info = SekolahInfo.query.first()
    return render_template('info_sekolah.html', title='Info Sekolah', info=info)

@public_bp.route('/agenda')
def agenda():
    agenda_list = Agenda.query.order_by(Agenda.tanggal.desc()).all()
    return render_template('agenda.html', 
                           title='Agenda Sekolah',
                           agenda_list=agenda_list)

@public_bp.route('/galeri')
def galeri():
    galeri_data = Galeri.query.order_by(Galeri.tanggal.desc()).all()
    kategoris = list(set([g.kategori for g in galeri_data if g.kategori]))
    return render_template('galeri.html', title='Galeri', galeri=galeri_data, kategoris=kategoris)

@public_bp.route('/ekstrakurikuler')
def ekstrakurikuler():
    ekskul_data = Ekstrakurikuler.query.all()
    kategoris = list(set([e.kategori for e in ekskul_data if e.kategori]))
    return render_template('ekstrakurikuler.html', title='Ekstrakurikuler', ekstrakurikuler=ekskul_data, kategoris=kategoris)

@public_bp.route('/laboratorium')
def laboratorium():
    lab_data = Laboratorium.query.all()
    return render_template('laboratorium.html', title='Laboratorium', laboratorium=lab_data)

@public_bp.route('/perpustakaan')
def perpustakaan():
    perpus_info = PerpustakaanInfo.query.first()
    # We might need to fetch facilities and services separately if they are in different tables
    # But based on the template, it expects a single object with lists.
    # The SQL model separated them. I need to adjust how I pass data to the template or update the template.
    # For now, I'll pass the info object and fetch the lists.
    # Wait, the original dummy_db had nested dicts.
    # My SQL model has PerpustakaanInfo, PerpustakaanFasilitas, PerpustakaanLayanan.
    # I should construct a dictionary or object that matches what the template expects.
    
    from app.models.models import PerpustakaanFasilitas, PerpustakaanLayanan
    fasilitas = [f.nama_fasilitas for f in PerpustakaanFasilitas.query.all()]
    layanan = [l.nama_layanan for l in PerpustakaanLayanan.query.all()]
    
    # Construct a compatible object/dict
    perpus_data = {
        'jam_buka': {
            'senin_jumat': perpus_info.jam_buka_senin_jumat if perpus_info else '',
            'sabtu': perpus_info.jam_buka_sabtu if perpus_info else ''
        },
        'koleksi': {
            'buku_pelajaran': perpus_info.jumlah_buku_pelajaran if perpus_info else 0,
            'buku_fiksi': perpus_info.jumlah_buku_fiksi if perpus_info else 0,
            'buku_referensi': perpus_info.jumlah_buku_referensi if perpus_info else 0,
            'majalah_jurnal': perpus_info.jumlah_majalah_jurnal if perpus_info else 0,
            'e_book': perpus_info.jumlah_ebook if perpus_info else 0
        },
        'fasilitas': fasilitas,
        'layanan': layanan
    }
    
    return render_template('perpustakaan.html', title='Perpustakaan', perpustakaan=perpus_data)
