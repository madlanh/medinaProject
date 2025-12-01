from app import create_app, db
from app.models.models import (
    User, SekolahInfo, Organisasi, Berita, Agenda, Galeri, 
    Ekstrakurikuler, Laboratorium, LaboratoriumFasilitas, 
    Banner, PerpustakaanInfo, PerpustakaanFasilitas, PerpustakaanLayanan,
    Prestasi, AlumniTestimoni
)
from datetime import datetime, date
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        db.create_all()
        
        # 1. Create Admin User
        # 1. Create Admin User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # In a real app, hash this password!
            admin = User(username='admin', password_hash=generate_password_hash('password123'))
            db.session.add(admin)
            print("Admin user created.")
        else:
            # Update password if user exists (to ensure hashing)
            admin.password_hash = generate_password_hash('password123')
            db.session.commit()
            print("Admin user password updated.")

        # 2. Sekolah Info
        if not SekolahInfo.query.first():
            info = SekolahInfo(
                nama='SMA Medina Bandung',
                npsn='20219345',
                akreditasi='A',
                alamat='Jl. Pendidikan No. 123, Bandung, Jawa Barat',
                telepon='(022) 7654321',
                email='info@smamedina.sch.id',
                website='www.smamedina.sch.id',
                kepala_sekolah='Dr. H. Abdullah Rahman, M.Pd',
                jumlah_siswa=720,
                jumlah_guru=58,
                jumlah_kelas=24,
                tahun_berdiri=1995,
                sejarah="SMA Medina Bandung didirikan pada tahun 1995 dengan visi menjadi lembaga pendidikan yang unggul dalam mengembangkan potensi siswa secara holistik. Berawal dari sebuah gedung sederhana dengan hanya 3 kelas, kini SMA Medina telah berkembang menjadi salah satu sekolah favorit di kota Bandung.\n\nDalam perjalanannya selama lebih dari 25 tahun, SMA Medina telah menghasilkan ribuan alumni yang tersebar di berbagai perguruan tinggi ternama di Indonesia dan luar negeri. Prestasi demi prestasi terus diraih, baik di bidang akademik maupun non-akademik.\n\nDengan motto \"Berakhlak, Berprestasi, Berwawasan Global\", SMA Medina terus berkomitmen untuk memberikan pendidikan berkualitas yang tidak hanya fokus pada aspek kognitif, tetapi juga pengembangan karakter dan soft skills siswa.",
                visi='Menjadi sekolah menengah atas yang unggul, berkarakter, dan berwawasan global dalam mencetak generasi pemimpin masa depan yang berakhlak mulia.',
                misi="1. Menyelenggarakan pendidikan berkualitas dengan standar nasional dan internasional\n2. Mengembangkan potensi akademik dan non-akademik siswa secara optimal\n3. Membentuk karakter siswa yang berakhlak mulia, disiplin, dan bertanggung jawab\n4. Menciptakan lingkungan belajar yang kondusif, inovatif, dan berbasis teknologi\n5. Membangun kerjasama dengan berbagai pihak untuk pengembangan sekolah\n6. Mempersiapkan siswa untuk bersaing di tingkat nasional dan internasional\n7. Mengintegrasikan nilai-nilai keislaman dalam setiap aspek pembelajaran",
                sambutan_kepsek="Assalamu'alaikum Warahmatullahi Wabarakatuh,\n\nPuji syukur kehadirat Allah SWT atas segala rahmat dan karunia-Nya. Shalawat serta salam semoga tercurah kepada Nabi Muhammad SAW, keluarga, dan para sahabatnya.\n\nSelamat datang di website resmi SMA Medina Bandung. Sebagai Kepala Sekolah, saya merasa bangga dapat memimpin lembaga pendidikan yang telah memiliki reputasi baik dalam mencetak generasi unggul.\n\nSMA Medina tidak hanya fokus pada pencapaian akademik, tetapi juga pada pembentukan karakter dan akhlak mulia siswa. Kami percaya bahwa pendidikan sejati adalah yang mampu menyeimbangkan kecerdasan intelektual, emosional, dan spiritual.\n\nKepada seluruh siswa, orang tua, dan masyarakat, mari bersama-sama kita wujudkan visi SMA Medina untuk menjadi sekolah yang unggul dan berkarakter. Semoga Allah SWT senantiasa memberkahi setiap langkah kita.\n\nWassalamu'alaikum Warahmatullahi Wabarakatuh.\n\nDr. H. Abdullah Rahman, M.Pd\nKepala SMA Medina Bandung"
            )
            db.session.add(info)
            print("Sekolah Info created.")

        # 3. Organisasi
        if Organisasi.query.count() == 0:
            orgs = [
                {'jabatan': 'Kepala Sekolah', 'nama': 'Dr. H. Abdullah Rahman, M.Pd', 'level': 1},
                {'jabatan': 'Wakil Kepala Sekolah Kurikulum', 'nama': 'Drs. Bambang Sutrisno, M.Pd', 'level': 2},
                {'jabatan': 'Wakil Kepala Sekolah Kesiswaan', 'nama': 'Ibu Hj. Rina Kusumawati, S.Pd, M.Si', 'level': 2},
                {'jabatan': 'Wakil Kepala Sekolah Humas', 'nama': 'Bpk. Dedi Kurniawan, S.Sos, M.M', 'level': 2},
                {'jabatan': 'Wakil Kepala Sekolah Sarana Prasarana', 'nama': 'Bpk. Ir. Yusuf Hidayat, M.T', 'level': 2},
                {'jabatan': 'Kepala Tata Usaha', 'nama': 'Ibu Susi Susanti, S.E', 'level': 3},
            ]
            for o in orgs:
                db.session.add(Organisasi(**o))
            print("Organisasi created.")

        # 4. Berita
        if Berita.query.count() == 0:
            beritas = [
                {
                    'judul': 'Juara 1 Lomba Cerdas Cermat Pancasila',
                    'tanggal': date(2025, 10, 31),
                    'ringkasan': 'SMA Medina berhasil meraih juara 1 dalam Lomba Cerdas Cermat Pancasila tingkat nasional yang diselenggarakan oleh UNY.',
                    'konten_lengkap': 'SMA Medina Bandung kembali mengharumkan nama sekolah dengan meraih juara 1 dalam Lomba Cerdas Cermat Pancasila tingkat nasional. Tim yang terdiri dari 3 siswa terbaik berhasil mengalahkan puluhan sekolah dari seluruh Indonesia dalam kompetisi yang berlangsung selama 3 hari di UNY Yogyakarta.'
                },
                {
                    'judul': 'Peringatan Hari Guru Nasional 2025',
                    'tanggal': date(2025, 11, 25),
                    'ringkasan': 'SMA Medina mengadakan peringatan Hari Guru Nasional dengan berbagai kegiatan menarik dan penuh makna.',
                    'konten_lengkap': 'Dalam rangka memperingati Hari Guru Nasional, SMA Medina mengadakan serangkaian acara yang melibatkan seluruh civitas akademika. Acara dimulai dengan upacara bendera yang khidmat, dilanjutkan dengan pemberian penghargaan kepada guru berprestasi, dan diakhiri dengan pentas seni dari siswa-siswi.'
                },
                {
                    'judul': 'Program Studi Tur ke Museum Geologi',
                    'tanggal': date(2025, 10, 20),
                    'ringkasan': 'Siswa kelas X IPA melaksanakan studi tur edukatif ke Museum Geologi Bandung untuk memperdalam pemahaman materi pembelajaran.',
                    'konten_lengkap': 'Siswa-siswi kelas X IPA SMA Medina mengikuti kegiatan studi tur ke Museum Geologi Bandung. Kegiatan ini bertujuan untuk memberikan pengalaman belajar langsung dan memperdalam pemahaman siswa tentang geologi Indonesia. Para siswa sangat antusias mengikuti penjelasan dari pemandu museum.'
                }
            ]
            for b in beritas:
                db.session.add(Berita(**b))
            print("Berita created.")

        # 5. Agenda
        if Agenda.query.count() == 0:
            agendas = [
                {'judul': 'Peringatan Hari Guru Nasional', 'tanggal': datetime(2025, 11, 25), 'deskripsi': 'Upacara dan berbagai perlombaan untuk memperingati Hari Guru.', 'lokasi': 'Aula Sekolah', 'waktu_display': '08.00 - 14.00', 'image_url': '1'},
                {'judul': 'Rapat Kerja Komite Sekolah', 'tanggal': datetime(2025, 11, 19), 'deskripsi': 'Rapat internal komite sekolah untuk evaluasi semester ganjil.', 'lokasi': 'Ruang Rapat', 'waktu_display': '13.00 - 16.00', 'image_url': '2'},
                {'judul': 'Lomba Debat Bahasa Inggris', 'tanggal': datetime(2025, 11, 15), 'deskripsi': 'Pelaksanaan lomba debat antar kelas di aula utama sekolah.', 'lokasi': 'Aula Utama', 'waktu_display': '09.00 - 15.00', 'image_url': '3'},
                {'judul': 'Open House & Pendaftaran Gel. 2', 'tanggal': datetime(2025, 12, 10), 'deskripsi': 'Acara promosi sekolah dan pembukaan pendaftaran gelombang kedua.', 'lokasi': 'Seluruh Area Sekolah', 'waktu_display': '08.00 - 16.00', 'image_url': '4'},
                {'judul': 'Studi Tur Museum Geologi', 'tanggal': datetime(2025, 10, 20), 'deskripsi': 'Kunjungan ke Museum Geologi Bandung untuk kelas IPA.', 'lokasi': 'Museum Geologi Bandung', 'waktu_display': '08.00 - 15.00', 'image_url': '5'},
            ]
            for a in agendas:
                db.session.add(Agenda(**a))
            print("Agenda created.")

        # 6. Galeri
        if Galeri.query.count() == 0:
            galeris = [
                {'judul': 'Upacara Hari Kemerdekaan 2025', 'kategori': 'Kegiatan', 'tanggal': date(2025, 8, 17), 'deskripsi': 'Pelaksanaan upacara peringatan HUT RI ke-80', 'image_url': '1'},
                {'judul': 'Lomba Cerdas Cermat', 'kategori': 'Prestasi', 'tanggal': date(2025, 10, 31), 'deskripsi': 'Tim cerdas cermat SMA Medina juara nasional', 'image_url': '2'},
                {'judul': 'Fasilitas Laboratorium Kimia', 'kategori': 'Fasilitas', 'tanggal': date(2025, 9, 1), 'deskripsi': 'Laboratorium kimia dengan peralatan modern', 'image_url': '3'},
                {'judul': 'Perpustakaan Digital', 'kategori': 'Fasilitas', 'tanggal': date(2025, 9, 1), 'deskripsi': 'Perpustakaan dengan koleksi buku dan e-book lengkap', 'image_url': '4'},
                {'judul': 'Pentas Seni Tahun Ajaran 2025', 'kategori': 'Kegiatan', 'tanggal': date(2025, 11, 10), 'deskripsi': 'Penampilan seni dari berbagai ekstrakurikuler', 'image_url': '5'},
                {'judul': 'Kelas Robotika', 'kategori': 'Kegiatan', 'tanggal': date(2025, 10, 15), 'deskripsi': 'Pembelajaran robotika untuk siswa', 'image_url': '6'},
            ]
            for g in galeris:
                db.session.add(Galeri(**g))
            print("Galeri created.")

        # 7. Ekstrakurikuler
        if Ekstrakurikuler.query.count() == 0:
            ekskuls = [
                {'nama': 'Paskibra', 'kategori': 'Baris-Berbaris', 'pembina': 'Bpk. Dedi Supriadi, S.Pd', 'jadwal': 'Rabu & Jumat, 15.30-17.00', 'deskripsi': 'Melatih kedisiplinan dan kepemimpinan melalui kegiatan baris-berbaris', 'image_url': '1'},
                {'nama': 'Pramuka', 'kategori': 'Kepramukaan', 'pembina': 'Ibu Siti Nurhaliza, S.Pd', 'jadwal': 'Sabtu, 14.00-16.00', 'deskripsi': 'Membentuk karakter dan keterampilan survival', 'image_url': '2'},
                {'nama': 'Basket', 'kategori': 'Olahraga', 'pembina': 'Bpk. Ahmad Fauzi, S.Pd', 'jadwal': 'Selasa & Kamis, 15.30-17.30', 'deskripsi': 'Mengembangkan kemampuan bermain basket dan kerjasama tim', 'image_url': '3'},
                {'nama': 'Robotika', 'kategori': 'Sains & Teknologi', 'pembina': 'Bpk. Budi Santoso, M.T', 'jadwal': 'Rabu, 15.00-17.00', 'deskripsi': 'Belajar pemrograman dan membuat robot', 'image_url': '4'},
                {'nama': 'English Club', 'kategori': 'Bahasa', 'pembina': 'Ibu Diana Putri, S.Pd', 'jadwal': 'Kamis, 15.00-16.30', 'deskripsi': 'Meningkatkan kemampuan berbahasa Inggris', 'image_url': '5'},
                {'nama': 'Seni Musik', 'kategori': 'Seni', 'pembina': 'Bpk. Rizky Ananda, S.Sn', 'jadwal': 'Jumat, 15.00-17.00', 'deskripsi': 'Mengembangkan bakat musik vokal dan instrumental', 'image_url': '6'},
            ]
            for e in ekskuls:
                db.session.add(Ekstrakurikuler(**e))
            print("Ekstrakurikuler created.")

        # 8. Banner
        if Banner.query.count() == 0:
            banners = [
                {'judul': 'Selamat Datang di SMA Medina', 'subjudul': 'Mencetak Generasi Berakhlak, Berprestasi, dan Berwawasan Global', 'image_url': '1', 'is_active': True},
                {'judul': 'Pendaftaran Siswa Baru 2026', 'subjudul': 'Daftarkan putra-putri Anda di sekolah terbaik', 'image_url': '2', 'is_active': True},
                {'judul': 'Fasilitas Modern & Lengkap', 'subjudul': 'Laboratorium, Perpustakaan, dan Sarana Olahraga Terbaik', 'image_url': '3', 'is_active': True},
            ]
            for b in banners:
                db.session.add(Banner(**b))
            print("Banner created.")

        # 9. Laboratorium
        if Laboratorium.query.count() == 0:
            labs = [
                {'nama': 'Laboratorium Fisika', 'deskripsi': 'Dilengkapi dengan peralatan eksperimen fisika modern', 'fasilitas': ['Osiloskop Digital', 'Set Optik Lengkap', 'Alat Mekanika', 'Komputer Analisis'], 'image_url': '1'},
                {'nama': 'Laboratorium Kimia', 'deskripsi': 'Laboratorium dengan standar keamanan tinggi untuk praktikum kimia', 'fasilitas': ['Lemari Asam', 'Peralatan Gelas', 'Bahan Kimia Lengkap', 'Safety Equipment'], 'image_url': '2'},
                {'nama': 'Laboratorium Biologi', 'deskripsi': 'Fasilitas untuk praktikum biologi dan penelitian', 'fasilitas': ['Mikroskop Digital', 'Herbarium', 'Model Anatomi', 'Aquarium'], 'image_url': '3'},
                {'nama': 'Laboratorium Komputer', 'deskripsi': 'Lab komputer dengan 40 unit PC dan koneksi internet cepat', 'fasilitas': ['40 Unit PC', 'Software Lengkap', 'Internet 100 Mbps', 'Proyektor'], 'image_url': '4'},
                {'nama': 'Laboratorium Bahasa', 'deskripsi': 'Ruang multimedia untuk pembelajaran bahasa asing', 'fasilitas': ['Audio System', 'Headset Individual', 'Software Pembelajaran', 'Booth Recording'], 'image_url': '5'},
            ]
            for l_data in labs:
                fasilitas = l_data.pop('fasilitas')
                lab = Laboratorium(**l_data)
                db.session.add(lab)
                db.session.flush()
                for f in fasilitas:
                    db.session.add(LaboratoriumFasilitas(laboratorium_id=lab.id, nama_fasilitas=f))
            print("Laboratorium created.")

        # 10. Perpustakaan
        if not PerpustakaanInfo.query.first():
            perpus = PerpustakaanInfo(
                jam_buka_senin_jumat='07.30 - 16.00',
                jam_buka_sabtu='08.00 - 14.00',
                jumlah_buku_pelajaran=3500,
                jumlah_buku_fiksi=1200,
                jumlah_buku_referensi=800,
                jumlah_majalah_jurnal=150,
                jumlah_ebook=5000
            )
            db.session.add(perpus)
            
            fasilitas = [
                'Ruang Baca Nyaman (kapasitas 100 orang)', 'Area Diskusi Kelompok', 
                'Komputer Katalog Digital', 'Wifi Gratis', 'AC dan Pencahayaan Optimal', 'CCTV 24 Jam'
            ]
            for f in fasilitas:
                db.session.add(PerpustakaanFasilitas(nama_fasilitas=f))

            layanan = [
                'Peminjaman Buku (maks 3 buku, 1 minggu)', 'Referensi dan Penelusuran Informasi',
                'Akses E-Book dan Jurnal Online', 'Layanan Fotokopi', 'Bimbingan Literasi Informasi'
            ]
            for l in layanan:
                db.session.add(PerpustakaanLayanan(nama_layanan=l))
            print("Perpustakaan created.")

        # 11. Prestasi
        if Prestasi.query.count() == 0:
            prestasis = [
                {'nama_prestasi': 'Juara 1 Lomba Cerdas Cermat Pancasila', 'skala': 'Nasional', 'tanggal': date(2025, 10, 31), 'penyelenggara': 'UNY'},
                {'nama_prestasi': 'Juara 2 FIKSI Nasional 2025', 'skala': 'Nasional', 'tanggal': date(2025, 10, 30), 'penyelenggara': 'Kemendikbud'},
                {'nama_prestasi': 'Medali Emas Olimpiade Fisika Regional', 'skala': 'Regional', 'tanggal': date(2025, 9, 15), 'penyelenggara': 'Dinas Pendidikan'},
                {'nama_prestasi': 'Juara Lomba Debat Bahasa Inggris', 'skala': 'Sekolah', 'tanggal': date(2025, 8, 20), 'penyelenggara': 'SMA Medina'},
            ]
            for p in prestasis:
                db.session.add(Prestasi(**p))
            print("Prestasi created.")

        # 12. Alumni
        if AlumniTestimoni.query.count() == 0:
            alumnis = [
                {'nama': 'Budi Santoso', 'tahun_lulus': 2020, 'testimoni': 'SMA Medina membentuk saya menjadi pribadi yang disiplin dan inovatif, sangat siap untuk dunia kuliah.', 'status_saat_ini': 'Kuliah Teknik ITB'},
                {'nama': 'Siti Aisyah', 'tahun_lulus': 2022, 'testimoni': 'Guru-guru sangat suportif dan membantu saya mendapatkan beasiswa ke Fakultas Kedokteran.', 'status_saat_ini': 'Kuliah Kedokteran UGM'},
            ]
            for al in alumnis:
                db.session.add(AlumniTestimoni(**al))
            print("Alumni created.")

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
