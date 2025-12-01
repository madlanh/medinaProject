from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import datetime, date
from functools import wraps

app = Flask(__name__)

# =================================================================
#           KONFIGURASI APLIKASI (MODE DUMMY)
# =================================================================

app.config['SECRET_KEY'] = 'kunci_rahasia_anda_yang_sangat_aman_dan_panjang'

# =================================================================
#           DATA DUMMY UNTUK DEVELOPMENT
# =================================================================

# Simulasi database dengan dictionary
dummy_db = {
    'admin_users': [
        {'id': 1, 'username': 'admin', 'password': 'password123'}
    ],
    'berita': [
        {
            'id': 1,
            'judul': 'Juara 1 Lomba Cerdas Cermat Pancasila',
            'tanggal': date(2025, 10, 31),
            'ringkasan': 'SMA Medina berhasil meraih juara 1 dalam Lomba Cerdas Cermat Pancasila tingkat nasional yang diselenggarakan oleh UNY.',
            'konten_lengkap': 'SMA Medina Bandung kembali mengharumkan nama sekolah dengan meraih juara 1 dalam Lomba Cerdas Cermat Pancasila tingkat nasional. Tim yang terdiri dari 3 siswa terbaik berhasil mengalahkan puluhan sekolah dari seluruh Indonesia dalam kompetisi yang berlangsung selama 3 hari di UNY Yogyakarta.'
        },
        {
            'id': 2,
            'judul': 'Peringatan Hari Guru Nasional 2025',
            'tanggal': date(2025, 11, 25),
            'ringkasan': 'SMA Medina mengadakan peringatan Hari Guru Nasional dengan berbagai kegiatan menarik dan penuh makna.',
            'konten_lengkap': 'Dalam rangka memperingati Hari Guru Nasional, SMA Medina mengadakan serangkaian acara yang melibatkan seluruh civitas akademika. Acara dimulai dengan upacara bendera yang khidmat, dilanjutkan dengan pemberian penghargaan kepada guru berprestasi, dan diakhiri dengan pentas seni dari siswa-siswi.'
        },
        {
            'id': 3,
            'judul': 'Program Studi Tur ke Museum Geologi',
            'tanggal': date(2025, 10, 20),
            'ringkasan': 'Siswa kelas X IPA melaksanakan studi tur edukatif ke Museum Geologi Bandung untuk memperdalam pemahaman materi pembelajaran.',
            'konten_lengkap': 'Siswa-siswi kelas X IPA SMA Medina mengikuti kegiatan studi tur ke Museum Geologi Bandung. Kegiatan ini bertujuan untuk memberikan pengalaman belajar langsung dan memperdalam pemahaman siswa tentang geologi Indonesia. Para siswa sangat antusias mengikuti penjelasan dari pemandu museum.'
        }
    ],
    'agenda': [
        {'id': 1, 'judul': 'Peringatan Hari Guru Nasional', 'tanggal': datetime(2025, 11, 25), 'deskripsi': 'Upacara dan berbagai perlombaan untuk memperingati Hari Guru.', 'lokasi': 'Aula Sekolah', 'waktu': '08.00 - 14.00', 'image_num': 1},
        {'id': 2, 'judul': 'Rapat Kerja Komite Sekolah', 'tanggal': datetime(2025, 11, 19), 'deskripsi': 'Rapat internal komite sekolah untuk evaluasi semester ganjil.', 'lokasi': 'Ruang Rapat', 'waktu': '13.00 - 16.00', 'image_num': 2},
        {'id': 3, 'judul': 'Lomba Debat Bahasa Inggris', 'tanggal': datetime(2025, 11, 15), 'deskripsi': 'Pelaksanaan lomba debat antar kelas di aula utama sekolah.', 'lokasi': 'Aula Utama', 'waktu': '09.00 - 15.00', 'image_num': 3},
        {'id': 4, 'judul': 'Open House & Pendaftaran Gel. 2', 'tanggal': datetime(2025, 12, 10), 'deskripsi': 'Acara promosi sekolah dan pembukaan pendaftaran gelombang kedua.', 'lokasi': 'Seluruh Area Sekolah', 'waktu': '08.00 - 16.00', 'image_num': 4},
        {'id': 5, 'judul': 'Studi Tur Museum Geologi', 'tanggal': datetime(2025, 10, 20), 'deskripsi': 'Kunjungan ke Museum Geologi Bandung untuk kelas IPA.', 'lokasi': 'Museum Geologi Bandung', 'waktu': '08.00 - 15.00', 'image_num': 5},
    ],
    'galeri': [
        {'id': 1, 'judul': 'Upacara Hari Kemerdekaan 2025', 'kategori': 'Kegiatan', 'tanggal': date(2025, 8, 17), 'deskripsi': 'Pelaksanaan upacara peringatan HUT RI ke-80', 'image_num': 1},
        {'id': 2, 'judul': 'Lomba Cerdas Cermat', 'kategori': 'Prestasi', 'tanggal': date(2025, 10, 31), 'deskripsi': 'Tim cerdas cermat SMA Medina juara nasional', 'image_num': 2},
        {'id': 3, 'judul': 'Fasilitas Laboratorium Kimia', 'kategori': 'Fasilitas', 'tanggal': date(2025, 9, 1), 'deskripsi': 'Laboratorium kimia dengan peralatan modern', 'image_num': 3},
        {'id': 4, 'judul': 'Perpustakaan Digital', 'kategori': 'Fasilitas', 'tanggal': date(2025, 9, 1), 'deskripsi': 'Perpustakaan dengan koleksi buku dan e-book lengkap', 'image_num': 4},
        {'id': 5, 'judul': 'Pentas Seni Tahun Ajaran 2025', 'kategori': 'Kegiatan', 'tanggal': date(2025, 11, 10), 'deskripsi': 'Penampilan seni dari berbagai ekstrakurikuler', 'image_num': 5},
        {'id': 6, 'judul': 'Kelas Robotika', 'kategori': 'Kegiatan', 'tanggal': date(2025, 10, 15), 'deskripsi': 'Pembelajaran robotika untuk siswa', 'image_num': 6},
    ],
    'ekstrakurikuler': [
        {'id': 1, 'nama': 'Paskibra', 'kategori': 'Baris-Berbaris', 'pembina': 'Bpk. Dedi Supriadi, S.Pd', 'jadwal': 'Rabu & Jumat, 15.30-17.00', 'deskripsi': 'Melatih kedisiplinan dan kepemimpinan melalui kegiatan baris-berbaris', 'image_num': 1},
        {'id': 2, 'nama': 'Pramuka', 'kategori': 'Kepramukaan', 'pembina': 'Ibu Siti Nurhaliza, S.Pd', 'jadwal': 'Sabtu, 14.00-16.00', 'deskripsi': 'Membentuk karakter dan keterampilan survival', 'image_num': 2},
        {'id': 3, 'nama': 'Basket', 'kategori': 'Olahraga', 'pembina': 'Bpk. Ahmad Fauzi, S.Pd', 'jadwal': 'Selasa & Kamis, 15.30-17.30', 'deskripsi': 'Mengembangkan kemampuan bermain basket dan kerjasama tim', 'image_num': 3},
        {'id': 4, 'nama': 'Robotika', 'kategori': 'Sains & Teknologi', 'pembina': 'Bpk. Budi Santoso, M.T', 'jadwal': 'Rabu, 15.00-17.00', 'deskripsi': 'Belajar pemrograman dan membuat robot', 'image_num': 4},
        {'id': 5, 'nama': 'English Club', 'kategori': 'Bahasa', 'pembina': 'Ibu Diana Putri, S.Pd', 'jadwal': 'Kamis, 15.00-16.30', 'deskripsi': 'Meningkatkan kemampuan berbahasa Inggris', 'image_num': 5},
        {'id': 6, 'nama': 'Seni Musik', 'kategori': 'Seni', 'pembina': 'Bpk. Rizky Ananda, S.Sn', 'jadwal': 'Jumat, 15.00-17.00', 'deskripsi': 'Mengembangkan bakat musik vokal dan instrumental', 'image_num': 6},
    ],
    'info_sekolah': {
        'nama': 'SMA Medina Bandung',
        'npsn': '20219345',
        'akreditasi': 'A',
        'alamat': 'Jl. Pendidikan No. 123, Bandung, Jawa Barat',
        'telepon': '(022) 7654321',
        'email': 'info@smamedina.sch.id',
        'website': 'www.smamedina.sch.id',
        'kepala_sekolah': 'Dr. H. Abdullah Rahman, M.Pd',
        'jumlah_siswa': 720,
        'jumlah_guru': 58,
        'jumlah_kelas': 24,
        'tahun_berdiri': 1995
    },
    'laboratorium': [
        {'id': 1, 'nama': 'Laboratorium Fisika', 'deskripsi': 'Dilengkapi dengan peralatan eksperimen fisika modern', 'fasilitas': ['Osiloskop Digital', 'Set Optik Lengkap', 'Alat Mekanika', 'Komputer Analisis'], 'image_num': 1},
        {'id': 2, 'nama': 'Laboratorium Kimia', 'deskripsi': 'Laboratorium dengan standar keamanan tinggi untuk praktikum kimia', 'fasilitas': ['Lemari Asam', 'Peralatan Gelas', 'Bahan Kimia Lengkap', 'Safety Equipment'], 'image_num': 2},
        {'id': 3, 'nama': 'Laboratorium Biologi', 'deskripsi': 'Fasilitas untuk praktikum biologi dan penelitian', 'fasilitas': ['Mikroskop Digital', 'Herbarium', 'Model Anatomi', 'Aquarium'], 'image_num': 3},
        {'id': 4, 'nama': 'Laboratorium Komputer', 'deskripsi': 'Lab komputer dengan 40 unit PC dan koneksi internet cepat', 'fasilitas': ['40 Unit PC', 'Software Lengkap', 'Internet 100 Mbps', 'Proyektor'], 'image_num': 4},
        {'id': 5, 'nama': 'Laboratorium Bahasa', 'deskripsi': 'Ruang multimedia untuk pembelajaran bahasa asing', 'fasilitas': ['Audio System', 'Headset Individual', 'Software Pembelajaran', 'Booth Recording'], 'image_num': 5},
    ],
    'perpustakaan': {
        'jam_buka': {
            'senin_jumat': '07.30 - 16.00',
            'sabtu': '08.00 - 14.00'
        },
        'koleksi': {
            'buku_pelajaran': 3500,
            'buku_fiksi': 1200,
            'buku_referensi': 800,
            'majalah_jurnal': 150,
            'e_book': 5000
        },
        'fasilitas': [
            'Ruang Baca Nyaman (kapasitas 100 orang)',
            'Area Diskusi Kelompok',
            'Komputer Katalog Digital',
            'Wifi Gratis',
            'AC dan Pencahayaan Optimal',
            'CCTV 24 Jam'
        ],
        'layanan': [
            'Peminjaman Buku (maks 3 buku, 1 minggu)',
            'Referensi dan Penelusuran Informasi',
            'Akses E-Book dan Jurnal Online',
            'Layanan Fotokopi',
            'Bimbingan Literasi Informasi'
        ]
    },
    'organisasi': [
        {'jabatan': 'Kepala Sekolah', 'nama': 'Dr. H. Abdullah Rahman, M.Pd', 'level': 1},
        {'jabatan': 'Wakil Kepala Sekolah Kurikulum', 'nama': 'Drs. Bambang Sutrisno, M.Pd', 'level': 2},
        {'jabatan': 'Wakil Kepala Sekolah Kesiswaan', 'nama': 'Ibu Hj. Rina Kusumawati, S.Pd, M.Si', 'level': 2},
        {'jabatan': 'Wakil Kepala Sekolah Humas', 'nama': 'Bpk. Dedi Kurniawan, S.Sos, M.M', 'level': 2},
        {'jabatan': 'Wakil Kepala Sekolah Sarana Prasarana', 'nama': 'Bpk. Ir. Yusuf Hidayat, M.T', 'level': 2},
        {'jabatan': 'Kepala Tata Usaha', 'nama': 'Ibu Susi Susanti, S.E', 'level': 3},
    ],
    'banner': [
        {'id': 1, 'judul': 'Selamat Datang di SMA Medina', 'subjudul': 'Mencetak Generasi Berakhlak, Berprestasi, dan Berwawasan Global', 'image_num': 1, 'aktif': True},
        {'id': 2, 'judul': 'Pendaftaran Siswa Baru 2026', 'subjudul': 'Daftarkan putra-putri Anda di sekolah terbaik', 'image_num': 2, 'aktif': True},
        {'id': 3, 'judul': 'Fasilitas Modern & Lengkap', 'subjudul': 'Laboratorium, Perpustakaan, dan Sarana Olahraga Terbaik', 'image_num': 3, 'aktif': True},
    ],
    'profil_content': {
        'sejarah': '''SMA Medina Bandung didirikan pada tahun 1995 dengan visi menjadi lembaga pendidikan yang unggul dalam mengembangkan potensi siswa secara holistik. Berawal dari sebuah gedung sederhana dengan hanya 3 kelas, kini SMA Medina telah berkembang menjadi salah satu sekolah favorit di kota Bandung.

Dalam perjalanannya selama lebih dari 25 tahun, SMA Medina telah menghasilkan ribuan alumni yang tersebar di berbagai perguruan tinggi ternama di Indonesia dan luar negeri. Prestasi demi prestasi terus diraih, baik di bidang akademik maupun non-akademik.

Dengan motto "Berakhlak, Berprestasi, Berwawasan Global", SMA Medina terus berkomitmen untuk memberikan pendidikan berkualitas yang tidak hanya fokus pada aspek kognitif, tetapi juga pengembangan karakter dan soft skills siswa.''',
        
        'visi': 'Menjadi sekolah menengah atas yang unggul, berkarakter, dan berwawasan global dalam mencetak generasi pemimpin masa depan yang berakhlak mulia.',
        
        'misi': '''1. Menyelenggarakan pendidikan berkualitas dengan standar nasional dan internasional
2. Mengembangkan potensi akademik dan non-akademik siswa secara optimal
3. Membentuk karakter siswa yang berakhlak mulia, disiplin, dan bertanggung jawab
4. Menciptakan lingkungan belajar yang kondusif, inovatif, dan berbasis teknologi
5. Membangun kerjasama dengan berbagai pihak untuk pengembangan sekolah
6. Mempersiapkan siswa untuk bersaing di tingkat nasional dan internasional
7. Mengintegrasikan nilai-nilai keislaman dalam setiap aspek pembelajaran''',
        
        'sambutan': '''Assalamu'alaikum Warahmatullahi Wabarakatuh,

Puji syukur kehadirat Allah SWT atas segala rahmat dan karunia-Nya. Shalawat serta salam semoga tercurah kepada Nabi Muhammad SAW, keluarga, dan para sahabatnya.

Selamat datang di website resmi SMA Medina Bandung. Sebagai Kepala Sekolah, saya merasa bangga dapat memimpin lembaga pendidikan yang telah memiliki reputasi baik dalam mencetak generasi unggul.

SMA Medina tidak hanya fokus pada pencapaian akademik, tetapi juga pada pembentukan karakter dan akhlak mulia siswa. Kami percaya bahwa pendidikan sejati adalah yang mampu menyeimbangkan kecerdasan intelektual, emosional, dan spiritual.

Kepada seluruh siswa, orang tua, dan masyarakat, mari bersama-sama kita wujudkan visi SMA Medina untuk menjadi sekolah yang unggul dan berkarakter. Semoga Allah SWT senantiasa memberkahi setiap langkah kita.

Wassalamu'alaikum Warahmatullahi Wabarakatuh.

Dr. H. Abdullah Rahman, M.Pd
Kepala SMA Medina Bandung'''
    }
}

# Counter untuk ID auto-increment
id_counters = {
    'berita': 4,
    'agenda': 6,
    'galeri': 7,
    'ekstrakurikuler': 7,
    'laboratorium': 6,
    'banner': 4
}

TODAY = date(2025, 11, 19)

prestasi_data = [
    {'nama': 'Juara 1 Lomba Cerdas Cermat Pancasila', 'skala': 'Nasional', 'tanggal': '31 Okt 2025', 'penyelenggara': 'UNY'},
    {'nama': 'Juara 2 FIKSI Nasional 2025', 'skala': 'Nasional', 'tanggal': '30 Okt 2025', 'penyelenggara': 'Kemendikbud'},
    {'nama': 'Medali Emas Olimpiade Fisika Regional', 'skala': 'Regional', 'tanggal': '15 Sep 2025', 'penyelenggara': 'Dinas Pendidikan'},
    {'nama': 'Juara Lomba Debat Bahasa Inggris', 'skala': 'Sekolah', 'tanggal': '20 Ags 2025', 'penyelenggara': 'SMA Medina'},
]

alumni_data = [
    {'nama': 'Budi Santoso (Lulusan 2020)', 'testimoni': 'SMA Medina membentuk saya menjadi pribadi yang disiplin dan inovatif, sangat siap untuk dunia kuliah.', 'status': 'Kuliah Teknik ITB'},
    {'nama': 'Siti Aisyah (Lulusan 2022)', 'testimoni': 'Guru-guru sangat suportif dan membantu saya mendapatkan beasiswa ke Fakultas Kedokteran.', 'status': 'Kuliah Kedokteran UGM'},
]

# =================================================================
#           HELPER FUNCTIONS
# =================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login untuk mengakses halaman ini.', 'warning')
            return redirect(url_for('admin_login_or_dashboard', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def categorize_agenda(agenda_list):
    past = []
    today = []
    future = []
    current_date = TODAY
    for item in agenda_list:
        item['display_date'] = item['tanggal'].strftime('%d %b %Y')
        item['day'] = item['tanggal'].strftime('%d')
        item['month'] = item['tanggal'].strftime('%b')
        if item['tanggal'].date() < current_date:
            past.append(item)
        elif item['tanggal'].date() == current_date:
            today.append(item)
        else:
            future.append(item)
    return past, today, future

# =================================================================
#           ROUTES PUBLIK
# =================================================================

@app.route('/')
def index():
    berita_beranda = sorted(dummy_db['berita'], key=lambda x: x['tanggal'], reverse=True)[:3]
    banner_aktif = [b for b in dummy_db['banner'] if b.get('aktif', False)]
    return render_template('index.html', 
                           berita=berita_beranda,
                           prestasi=prestasi_data, 
                           alumni=alumni_data,
                           banners=banner_aktif)

@app.route('/sejarah')
def sejarah():
    return render_template('sejarah.html')

@app.route('/visi-misi')
def visi_misi():
    return render_template('visi-misi.html')

@app.route('/sambutan')
def sambutan():
    return render_template('sambutan.html', title='Sambutan Kepala Sekolah')

@app.route('/organisasi')
def organisasi():
    org_data = dummy_db['organisasi']
    return render_template('organisasi.html', title='Struktur Organisasi', organisasi=org_data)

@app.route('/berita-terbaru')
def berita_terbaru():
    all_berita = sorted(dummy_db['berita'], key=lambda x: x['tanggal'], reverse=True)
    return render_template('berita_terbaru.html', title='Berita Terbaru', all_berita=all_berita)

@app.route('/info-sekolah')
def info_sekolah():
    info = dummy_db['info_sekolah']
    return render_template('info_sekolah.html', title='Info Sekolah', info=info)

@app.route('/agenda')
def agenda():
    past, today, future = categorize_agenda(dummy_db['agenda'].copy())
    return render_template('agenda.html', 
                           title='Agenda Sekolah',
                           past_agenda=past,
                           today_agenda=today,
                           future_agenda=future)

@app.route('/galeri')
def galeri():
    galeri_data = sorted(dummy_db['galeri'], key=lambda x: x['tanggal'], reverse=True)
    kategoris = list(set([g['kategori'] for g in galeri_data]))
    return render_template('galeri.html', title='Galeri', galeri=galeri_data, kategoris=kategoris)

@app.route('/ekstrakurikuler')
def ekstrakurikuler():
    ekskul_data = dummy_db['ekstrakurikuler']
    kategoris = list(set([e['kategori'] for e in ekskul_data]))
    return render_template('ekstrakurikuler.html', title='Ekstrakurikuler', ekstrakurikuler=ekskul_data, kategoris=kategoris)

@app.route('/laboratorium')
def laboratorium():
    lab_data = dummy_db['laboratorium']
    return render_template('laboratorium.html', title='Laboratorium', laboratorium=lab_data)

@app.route('/perpustakaan')
def perpustakaan():
    perpus_data = dummy_db['perpustakaan']
    return render_template('perpustakaan.html', title='Perpustakaan', perpustakaan=perpus_data)

# =================================================================
#           ROUTES ADMIN
# =================================================================

@app.route('/admin', methods=['GET', 'POST'])
def admin_login_or_dashboard():
    if 'user_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = next((u for u in dummy_db['admin_users'] if u['username'] == username), None)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login berhasil!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Username atau password salah.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    stats = {
        'total_berita': len(dummy_db['berita']),
        'total_agenda': len(dummy_db['agenda']),
        'total_galeri': len(dummy_db['galeri']),
        'total_ekstrakurikuler': len(dummy_db['ekstrakurikuler'])
    }
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/admin/logout')
@login_required
def admin_logout():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('admin_login_or_dashboard'))

# =================================================================
#           CRUD BERITA
# =================================================================

@app.route('/admin/berita')
@login_required
def manage_berita():
    berita_list = sorted(dummy_db['berita'], key=lambda x: x['tanggal'], reverse=True)
    return render_template('admin/manage_berita.html', berita_list=berita_list)

@app.route('/admin/berita/create', methods=['GET', 'POST'])
@login_required
def create_berita():
    if request.method == 'POST':
        try:
            new_berita = {
                'id': id_counters['berita'],
                'judul': request.form['judul'],
                'tanggal': datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                'ringkasan': request.form['ringkasan'],
                'konten_lengkap': request.form['konten_lengkap']
            }
            dummy_db['berita'].append(new_berita)
            id_counters['berita'] += 1
            flash('Berita baru berhasil dibuat!', 'success')
            return redirect(url_for('manage_berita'))
        except Exception as e:
            flash(f'Gagal membuat berita: {e}', 'danger')
    return render_template('admin/edit_berita.html', title='Buat Berita Baru', berita=None)

@app.route('/admin/berita/edit/<int:berita_id>', methods=['GET', 'POST'])
@login_required
def edit_berita(berita_id):
    berita = next((b for b in dummy_db['berita'] if b['id'] == berita_id), None)
    if not berita:
        flash('Berita tidak ditemukan.', 'danger')
        return redirect(url_for('manage_berita'))
    
    if request.method == 'POST':
        try:
            berita['judul'] = request.form['judul']
            berita['tanggal'] = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            berita['ringkasan'] = request.form['ringkasan']
            berita['konten_lengkap'] = request.form['konten_lengkap']
            flash('Berita berhasil diperbarui!', 'success')
            return redirect(url_for('manage_berita'))
        except Exception as e:
            flash(f'Gagal memperbarui berita: {e}', 'danger')

    return render_template('admin/edit_berita.html', title=f'Edit Berita: {berita["judul"]}', berita=berita)

@app.route('/admin/berita/delete/<int:berita_id>', methods=['POST'])
@login_required
def delete_berita(berita_id):
    berita = next((b for b in dummy_db['berita'] if b['id'] == berita_id), None)
    if berita:
        dummy_db['berita'].remove(berita)
        flash(f'Berita "{berita["judul"]}" berhasil dihapus.', 'success')
    else:
        flash('Berita tidak ditemukan.', 'danger')
    return redirect(url_for('manage_berita'))

# =================================================================
#           CRUD AGENDA
# =================================================================

@app.route('/admin/agenda')
@login_required
def manage_agenda():
    agenda_list = sorted(dummy_db['agenda'], key=lambda x: x['tanggal'], reverse=True)
    return render_template('admin/manage_agenda.html', agenda_list=agenda_list)

@app.route('/admin/agenda/create', methods=['GET', 'POST'])
@login_required
def create_agenda():
    if request.method == 'POST':
        try:
            new_agenda = {
                'id': id_counters['agenda'],
                'judul': request.form['judul'],
                'tanggal': datetime.strptime(request.form['tanggal'], '%Y-%m-%d'),
                'deskripsi': request.form['deskripsi'],
                'lokasi': request.form['lokasi'],
                'waktu': request.form['waktu'],
                'image_num': int(request.form.get('image_num', 1))
            }
            dummy_db['agenda'].append(new_agenda)
            id_counters['agenda'] += 1
            flash('Agenda baru berhasil dibuat!', 'success')
            return redirect(url_for('manage_agenda'))
        except Exception as e:
            flash(f'Gagal membuat agenda: {e}', 'danger')
    return render_template('admin/edit_agenda.html', title='Buat Agenda Baru', agenda=None)

@app.route('/admin/agenda/edit/<int:agenda_id>', methods=['GET', 'POST'])
@login_required
def edit_agenda(agenda_id):
    agenda = next((a for a in dummy_db['agenda'] if a['id'] == agenda_id), None)
    if not agenda:
        flash('Agenda tidak ditemukan.', 'danger')
        return redirect(url_for('manage_agenda'))
    
    if request.method == 'POST':
        try:
            agenda['judul'] = request.form['judul']
            agenda['tanggal'] = datetime.strptime(request.form['tanggal'], '%Y-%m-%d')
            agenda['deskripsi'] = request.form['deskripsi']
            agenda['lokasi'] = request.form['lokasi']
            agenda['waktu'] = request.form['waktu']
            agenda['image_num'] = int(request.form.get('image_num', 1))
            flash('Agenda berhasil diperbarui!', 'success')
            return redirect(url_for('manage_agenda'))
        except Exception as e:
            flash(f'Gagal memperbarui agenda: {e}', 'danger')

    return render_template('admin/edit_agenda.html', title=f'Edit Agenda: {agenda["judul"]}', agenda=agenda)

@app.route('/admin/agenda/delete/<int:agenda_id>', methods=['POST'])
@login_required
def delete_agenda(agenda_id):
    agenda = next((a for a in dummy_db['agenda'] if a['id'] == agenda_id), None)
    if agenda:
        dummy_db['agenda'].remove(agenda)
        flash(f'Agenda "{agenda["judul"]}" berhasil dihapus.', 'success')
    else:
        flash('Agenda tidak ditemukan.', 'danger')
    return redirect(url_for('manage_agenda'))

# =================================================================
#           CRUD GALERI
# =================================================================

@app.route('/admin/galeri')
@login_required
def manage_galeri():
    galeri_list = sorted(dummy_db['galeri'], key=lambda x: x['tanggal'], reverse=True)
    return render_template('admin/manage_galeri.html', galeri_list=galeri_list)

@app.route('/admin/galeri/create', methods=['GET', 'POST'])
@login_required
def create_galeri():
    if request.method == 'POST':
        try:
            new_galeri = {
                'id': id_counters['galeri'],
                'judul': request.form['judul'],
                'kategori': request.form['kategori'],
                'tanggal': datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date(),
                'deskripsi': request.form['deskripsi'],
                'image_num': int(request.form.get('image_num', 1))
            }
            dummy_db['galeri'].append(new_galeri)
            id_counters['galeri'] += 1
            flash('Foto galeri baru berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_galeri'))
        except Exception as e:
            flash(f'Gagal menambahkan foto: {e}', 'danger')
    return render_template('admin/edit_galeri.html', title='Tambah Foto Galeri', galeri=None)

@app.route('/admin/galeri/edit/<int:galeri_id>', methods=['GET', 'POST'])
@login_required
def edit_galeri(galeri_id):
    galeri = next((g for g in dummy_db['galeri'] if g['id'] == galeri_id), None)
    if not galeri:
        flash('Foto galeri tidak ditemukan.', 'danger')
        return redirect(url_for('manage_galeri'))
    
    if request.method == 'POST':
        try:
            galeri['judul'] = request.form['judul']
            galeri['kategori'] = request.form['kategori']
            galeri['tanggal'] = datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
            galeri['deskripsi'] = request.form['deskripsi']
            galeri['image_num'] = int(request.form.get('image_num', 1))
            flash('Foto galeri berhasil diperbarui!', 'success')
            return redirect(url_for('manage_galeri'))
        except Exception as e:
            flash(f'Gagal memperbarui foto: {e}', 'danger')

    return render_template('admin/edit_galeri.html', title=f'Edit Galeri: {galeri["judul"]}', galeri=galeri)

@app.route('/admin/galeri/delete/<int:galeri_id>', methods=['POST'])
@login_required
def delete_galeri(galeri_id):
    galeri = next((g for g in dummy_db['galeri'] if g['id'] == galeri_id), None)
    if galeri:
        dummy_db['galeri'].remove(galeri)
        flash(f'Foto "{galeri["judul"]}" berhasil dihapus.', 'success')
    else:
        flash('Foto tidak ditemukan.', 'danger')
    return redirect(url_for('manage_galeri'))

# =================================================================
#           CRUD EKSTRAKURIKULER
# =================================================================

@app.route('/admin/ekstrakurikuler')
@login_required
def manage_ekstrakurikuler():
    ekskul_list = dummy_db['ekstrakurikuler']
    return render_template('admin/manage_ekstrakurikuler.html', ekskul_list=ekskul_list)

@app.route('/admin/ekstrakurikuler/create', methods=['GET', 'POST'])
@login_required
def create_ekstrakurikuler():
    if request.method == 'POST':
        try:
            new_ekskul = {
                'id': id_counters['ekstrakurikuler'],
                'nama': request.form['nama'],
                'kategori': request.form['kategori'],
                'pembina': request.form['pembina'],
                'jadwal': request.form['jadwal'],
                'deskripsi': request.form['deskripsi'],
                'image_num': int(request.form.get('image_num', 1))
            }
            dummy_db['ekstrakurikuler'].append(new_ekskul)
            id_counters['ekstrakurikuler'] += 1
            flash('Ekstrakurikuler baru berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_ekstrakurikuler'))
        except Exception as e:
            flash(f'Gagal menambahkan ekstrakurikuler: {e}', 'danger')
    return render_template('admin/edit_ekstrakurikuler.html', title='Tambah Ekstrakurikuler', ekskul=None)

@app.route('/admin/ekstrakurikuler/edit/<int:ekskul_id>', methods=['GET', 'POST'])
@login_required
def edit_ekstrakurikuler(ekskul_id):
    ekskul = next((e for e in dummy_db['ekstrakurikuler'] if e['id'] == ekskul_id), None)
    if not ekskul:
        flash('Ekstrakurikuler tidak ditemukan.', 'danger')
        return redirect(url_for('manage_ekstrakurikuler'))
    
    if request.method == 'POST':
        try:
            ekskul['nama'] = request.form['nama']
            ekskul['kategori'] = request.form['kategori']
            ekskul['pembina'] = request.form['pembina']
            ekskul['jadwal'] = request.form['jadwal']
            ekskul['deskripsi'] = request.form['deskripsi']
            ekskul['image_num'] = int(request.form.get('image_num', 1))
            flash('Ekstrakurikuler berhasil diperbarui!', 'success')
            return redirect(url_for('manage_ekstrakurikuler'))
        except Exception as e:
            flash(f'Gagal memperbarui ekstrakurikuler: {e}', 'danger')

    return render_template('admin/edit_ekstrakurikuler.html', title=f'Edit Ekstrakurikuler: {ekskul["nama"]}', ekskul=ekskul)

@app.route('/admin/ekstrakurikuler/delete/<int:ekskul_id>', methods=['POST'])
@login_required
def delete_ekstrakurikuler(ekskul_id):
    ekskul = next((e for e in dummy_db['ekstrakurikuler'] if e['id'] == ekskul_id), None)
    if ekskul:
        dummy_db['ekstrakurikuler'].remove(ekskul)
        flash(f'Ekstrakurikuler "{ekskul["nama"]}" berhasil dihapus.', 'success')
    else:
        flash('Ekstrakurikuler tidak ditemukan.', 'danger')
    return redirect(url_for('manage_ekstrakurikuler'))

# =================================================================
#           CRUD LABORATORIUM
# =================================================================

@app.route('/admin/laboratorium')
@login_required
def manage_laboratorium():
    lab_list = dummy_db['laboratorium']
    return render_template('admin/manage_laboratorium.html', lab_list=lab_list)

@app.route('/admin/laboratorium/create', methods=['GET', 'POST'])
@login_required
def create_laboratorium():
    if request.method == 'POST':
        try:
            fasilitas_str = request.form['fasilitas']
            fasilitas_list = [f.strip() for f in fasilitas_str.split(',') if f.strip()]
            
            new_lab = {
                'id': id_counters['laboratorium'],
                'nama': request.form['nama'],
                'deskripsi': request.form['deskripsi'],
                'fasilitas': fasilitas_list,
                'image_num': int(request.form.get('image_num', 1))
            }
            dummy_db['laboratorium'].append(new_lab)
            id_counters['laboratorium'] += 1
            flash('Laboratorium baru berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_laboratorium'))
        except Exception as e:
            flash(f'Gagal menambahkan laboratorium: {e}', 'danger')
    return render_template('admin/edit_laboratorium.html', title='Tambah Laboratorium', lab=None)

@app.route('/admin/laboratorium/edit/<int:lab_id>', methods=['GET', 'POST'])
@login_required
def edit_laboratorium(lab_id):
    lab = next((l for l in dummy_db['laboratorium'] if l['id'] == lab_id), None)
    if not lab:
        flash('Laboratorium tidak ditemukan.', 'danger')
        return redirect(url_for('manage_laboratorium'))
    
    if request.method == 'POST':
        try:
            fasilitas_str = request.form['fasilitas']
            fasilitas_list = [f.strip() for f in fasilitas_str.split(',') if f.strip()]
            
            lab['nama'] = request.form['nama']
            lab['deskripsi'] = request.form['deskripsi']
            lab['fasilitas'] = fasilitas_list
            lab['image_num'] = int(request.form.get('image_num', 1))
            flash('Laboratorium berhasil diperbarui!', 'success')
            return redirect(url_for('manage_laboratorium'))
        except Exception as e:
            flash(f'Gagal memperbarui laboratorium: {e}', 'danger')

    return render_template('admin/edit_laboratorium.html', title=f'Edit Laboratorium: {lab["nama"]}', lab=lab)

@app.route('/admin/laboratorium/delete/<int:lab_id>', methods=['POST'])
@login_required
def delete_laboratorium(lab_id):
    lab = next((l for l in dummy_db['laboratorium'] if l['id'] == lab_id), None)
    if lab:
        dummy_db['laboratorium'].remove(lab)
        flash(f'Laboratorium "{lab["nama"]}" berhasil dihapus.', 'success')
    else:
        flash('Laboratorium tidak ditemukan.', 'danger')
    return redirect(url_for('manage_laboratorium'))

# =================================================================
#           CRUD BANNER
# =================================================================

@app.route('/admin/banner')
@login_required
def manage_banner():
    banner_list = dummy_db['banner']
    return render_template('admin/manage_banner.html', banner_list=banner_list)

@app.route('/admin/banner/create', methods=['GET', 'POST'])
@login_required
def create_banner():
    if request.method == 'POST':
        try:
            new_banner = {
                'id': id_counters['banner'],
                'judul': request.form['judul'],
                'subjudul': request.form['subjudul'],
                'image_num': int(request.form.get('image_num', 1)),
                'aktif': 'aktif' in request.form
            }
            dummy_db['banner'].append(new_banner)
            id_counters['banner'] += 1
            flash('Banner baru berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_banner'))
        except Exception as e:
            flash(f'Gagal menambahkan banner: {e}', 'danger')
    return render_template('admin/edit_banner.html', title='Tambah Banner', banner=None)

@app.route('/admin/banner/edit/<int:banner_id>', methods=['GET', 'POST'])
@login_required
def edit_banner(banner_id):
    banner = next((b for b in dummy_db['banner'] if b['id'] == banner_id), None)
    if not banner:
        flash('Banner tidak ditemukan.', 'danger')
        return redirect(url_for('manage_banner'))
    
    if request.method == 'POST':
        try:
            banner['judul'] = request.form['judul']
            banner['subjudul'] = request.form['subjudul']
            banner['image_num'] = int(request.form.get('image_num', 1))
            banner['aktif'] = 'aktif' in request.form
            flash('Banner berhasil diperbarui!', 'success')
            return redirect(url_for('manage_banner'))
        except Exception as e:
            flash(f'Gagal memperbarui banner: {e}', 'danger')

    return render_template('admin/edit_banner.html', title=f'Edit Banner: {banner["judul"]}', banner=banner)

@app.route('/admin/banner/delete/<int:banner_id>', methods=['POST'])
@login_required
def delete_banner(banner_id):
    banner = next((b for b in dummy_db['banner'] if b['id'] == banner_id), None)
    if banner:
        dummy_db['banner'].remove(banner)
        flash(f'Banner "{banner["judul"]}" berhasil dihapus.', 'success')
    else:
        flash('Banner tidak ditemukan.', 'danger')
    return redirect(url_for('manage_banner'))

# =================================================================
#           CRUD INFO SEKOLAH
# =================================================================

@app.route('/admin/info-sekolah', methods=['GET', 'POST'])
@login_required
def manage_info_sekolah():
    if request.method == 'POST':
        try:
            dummy_db['info_sekolah']['nama'] = request.form['nama']
            dummy_db['info_sekolah']['npsn'] = request.form['npsn']
            dummy_db['info_sekolah']['akreditasi'] = request.form['akreditasi']
            dummy_db['info_sekolah']['alamat'] = request.form['alamat']
            dummy_db['info_sekolah']['telepon'] = request.form['telepon']
            dummy_db['info_sekolah']['email'] = request.form['email']
            dummy_db['info_sekolah']['website'] = request.form['website']
            dummy_db['info_sekolah']['kepala_sekolah'] = request.form['kepala_sekolah']
            dummy_db['info_sekolah']['jumlah_siswa'] = int(request.form['jumlah_siswa'])
            dummy_db['info_sekolah']['jumlah_guru'] = int(request.form['jumlah_guru'])
            dummy_db['info_sekolah']['jumlah_kelas'] = int(request.form['jumlah_kelas'])
            dummy_db['info_sekolah']['tahun_berdiri'] = int(request.form['tahun_berdiri'])
            flash('Info sekolah berhasil diperbarui!', 'success')
        except Exception as e:
            flash(f'Gagal memperbarui info sekolah: {e}', 'danger')
    
    return render_template('admin/manage_info_sekolah.html', info=dummy_db['info_sekolah'])

# =================================================================
#           CRUD PERPUSTAKAAN
# =================================================================

@app.route('/admin/perpustakaan', methods=['GET', 'POST'])
@login_required
def manage_perpustakaan_admin():
    if request.method == 'POST':
        try:
            dummy_db['perpustakaan']['jam_buka']['senin_jumat'] = request.form['jam_senin_jumat']
            dummy_db['perpustakaan']['jam_buka']['sabtu'] = request.form['jam_sabtu']
            dummy_db['perpustakaan']['koleksi']['buku_pelajaran'] = int(request.form['buku_pelajaran'])
            dummy_db['perpustakaan']['koleksi']['buku_fiksi'] = int(request.form['buku_fiksi'])
            dummy_db['perpustakaan']['koleksi']['buku_referensi'] = int(request.form['buku_referensi'])
            dummy_db['perpustakaan']['koleksi']['majalah_jurnal'] = int(request.form['majalah_jurnal'])
            dummy_db['perpustakaan']['koleksi']['e_book'] = int(request.form['e_book'])
            
            fasilitas_str = request.form['fasilitas']
            dummy_db['perpustakaan']['fasilitas'] = [f.strip() for f in fasilitas_str.split(',') if f.strip()]
            
            layanan_str = request.form['layanan']
            dummy_db['perpustakaan']['layanan'] = [l.strip() for l in layanan_str.split(',') if l.strip()]
            
            flash('Data perpustakaan berhasil diperbarui!', 'success')
        except Exception as e:
            flash(f'Gagal memperbarui data perpustakaan: {e}', 'danger')
    
    return render_template('admin/manage_perpustakaan.html', perpus=dummy_db['perpustakaan'])

# =================================================================
#           CRUD PROFIL SEKOLAH
# =================================================================

@app.route('/admin/profil-sekolah')
@login_required
def manage_profil_sekolah():
    return render_template('admin/manage_profil_sekolah.html')

@app.route('/admin/profil-sekolah/sejarah', methods=['GET', 'POST'])
@login_required
def edit_sejarah():
    if request.method == 'POST':
        try:
            sejarah_content = request.form['konten']
            if 'profil_content' not in dummy_db:
                dummy_db['profil_content'] = {}
            dummy_db['profil_content']['sejarah'] = sejarah_content
            flash('Konten Sejarah berhasil diperbarui!', 'success')
            return redirect(url_for('manage_profil_sekolah'))
        except Exception as e:
            flash(f'Gagal memperbarui Sejarah: {e}', 'danger')
    
    sejarah = dummy_db.get('profil_content', {}).get('sejarah', '')
    return render_template('admin/edit_profil_content.html', 
                         title='Edit Sejarah Sekolah',
                         content_type='sejarah',
                         konten=sejarah)

@app.route('/admin/profil-sekolah/visi-misi', methods=['GET', 'POST'])
@login_required
def edit_visi_misi():
    if request.method == 'POST':
        try:
            visi = request.form['visi']
            misi = request.form['misi']
            if 'profil_content' not in dummy_db:
                dummy_db['profil_content'] = {}
            dummy_db['profil_content']['visi'] = visi
            dummy_db['profil_content']['misi'] = misi
            flash('Visi & Misi berhasil diperbarui!', 'success')
            return redirect(url_for('manage_profil_sekolah'))
        except Exception as e:
            flash(f'Gagal memperbarui Visi & Misi: {e}', 'danger')
    
    visi = dummy_db.get('profil_content', {}).get('visi', '')
    misi = dummy_db.get('profil_content', {}).get('misi', '')
    return render_template('admin/edit_visi_misi.html', 
                         title='Edit Visi & Misi',
                         visi=visi,
                         misi=misi)

@app.route('/admin/profil-sekolah/sambutan', methods=['GET', 'POST'])
@login_required
def edit_sambutan():
    if request.method == 'POST':
        try:
            sambutan = request.form['konten']
            if 'profil_content' not in dummy_db:
                dummy_db['profil_content'] = {}
            dummy_db['profil_content']['sambutan'] = sambutan
            flash('Sambutan Kepala Sekolah berhasil diperbarui!', 'success')
            return redirect(url_for('manage_profil_sekolah'))
        except Exception as e:
            flash(f'Gagal memperbarui Sambutan: {e}', 'danger')
    
    sambutan = dummy_db.get('profil_content', {}).get('sambutan', '')
    return render_template('admin/edit_profil_content.html', 
                         title='Edit Sambutan Kepala Sekolah',
                         content_type='sambutan',
                         konten=sambutan)

@app.route('/admin/profil-sekolah/organisasi', methods=['GET', 'POST'])
@login_required
def edit_organisasi():
    if request.method == 'POST':
        try:
            for i, org in enumerate(dummy_db['organisasi']):
                nama_key = f'nama_{i}'
                jabatan_key = f'jabatan_{i}'
                if nama_key in request.form:
                    org['nama'] = request.form[nama_key]
                    org['jabatan'] = request.form[jabatan_key]
            
            flash('Struktur Organisasi berhasil diperbarui!', 'success')
            return redirect(url_for('manage_profil_sekolah'))
        except Exception as e:
            flash(f'Gagal memperbarui Struktur Organisasi: {e}', 'danger')
    
    return render_template('admin/edit_organisasi.html', 
                         title='Edit Struktur Organisasi',
                         organisasi=dummy_db['organisasi'])

# =================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("MODE DUMMY DATA - Tidak Perlu Database")
    print("="*60)
    print("Login Admin:")
    print("  Username: admin")
    print("  Password: password123")
    print("="*60 + "\n")
    app.run(debug=True)