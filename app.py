from flask import Flask, render_template
from datetime import datetime, date # Diperlukan untuk membandingkan tanggal

app = Flask(__name__)

# --- DUMMY DATA FOR FRONT-END (FE) ---

# Tanggal hari ini (untuk memisahkan agenda)
# NOTE: Silakan ubah tanggal ini untuk menguji kategori agenda (past, today, future)
TODAY = date(2025, 11, 19) 

berita_data = [
    {'id': 1, 'judul': 'Lomba Cerdas Cermat Pancasila', 'tanggal': '31 Okt 2025', 'ringkasan': 'Siswa SMA Medina meraih juara 1 dalam Lomba Cerdas Cermat Skala Nasional di UNY.'},
    {'id': 2, 'judul': 'Juara FIKSI Nasional 25', 'tanggal': '30 Okt 2025', 'ringkasan': 'Tim Kewirausahaan meraih juara 2 kategori Ajuan Kesehatan.'},
    {'id': 3, 'judul': 'Open House & Pendaftaran Gelombang 2', 'tanggal': '10 Okt 2025', 'ringkasan': 'Informasi terkini mengenai acara Open House dan jadwal pendaftaran siswa baru.'},
    {'id': 4, 'judul': 'Seminar Karir Alumni', 'tanggal': '5 Okt 2025', 'ringkasan': 'SMA Medina mengadakan seminar karir tahunan dengan alumni dari berbagai profesi.'},
]

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

# DATA AGENDA DENGAN FORMAT DATETIME
raw_agenda_data = [
    {'id': 1, 'judul': 'Peringatan Hari Guru Nasional', 'tanggal': datetime(2025, 11, 25), 'deskripsi': 'Upacara dan berbagai perlombaan untuk memperingati Hari Guru.', 'image_num': 1}, 
    {'id': 2, 'judul': 'Rapat Kerja Komite Sekolah', 'tanggal': datetime(2025, 11, 19), 'deskripsi': 'Rapat internal komite sekolah untuk evaluasi semester ganjil.', 'image_num': 2}, # Sedang berlangsung (TODAY)
    {'id': 3, 'judul': 'Lomba Debat Bahasa Inggris', 'tanggal': datetime(2025, 11, 15), 'deskripsi': 'Pelaksanaan lomba debat antar kelas di aula utama sekolah.', 'image_num': 3}, # Telah lalu (PAST)
    {'id': 4, 'judul': 'Open House & Pendaftaran Gel. 2', 'tanggal': datetime(2025, 12, 10), 'deskripsi': 'Acara promosi sekolah dan pembukaan pendaftaran gelombang kedua.', 'image_num': 4}, # Akan datang (FUTURE)
    {'id': 5, 'judul': 'Studi Tur Museum Geologi', 'tanggal': datetime(2025, 10, 20), 'deskripsi': 'Kunjungan ke Museum Geologi Bandung untuk kelas IPA.', 'image_num': 5}, # Telah lalu (PAST)
]

# --- FUNGSI PEMBAGI AGENDA (UNTUK ROUTE /agenda) ---
def categorize_agenda(agenda_list):
    past = []
    today = []
    future = []
    
    current_date = TODAY
    
    for item in agenda_list:
        # Konversi objek datetime ke string yang mudah dibaca untuk FE
        item['display_date'] = item['tanggal'].strftime('%d %b %Y')
        item['day'] = item['tanggal'].strftime('%d')
        item['month'] = item['tanggal'].strftime('%b')
        
        # NOTE: Kita membandingkan hanya bagian .date() agar perbandingan akurat
        if item['tanggal'].date() < current_date:
            past.append(item)
        elif item['tanggal'].date() == current_date:
            today.append(item)
        else:
            future.append(item)
            
    return past, today, future

# --- ROUTES DASHBOARD & PROFIL SEKOLAH INTI ---
@app.route('/')
def index():
    berita_beranda = berita_data[:3]
    return render_template('index.html', 
                           berita=berita_beranda,
                           prestasi=prestasi_data, 
                           alumni=alumni_data)

@app.route('/sejarah')
def sejarah():
    return render_template('sejarah.html')

@app.route('/visi-misi')
def visi_misi():
    return render_template('visi-misi.html')

# --- ROUTES PROFIL SEKOLAH EKSPANSI ---
@app.route('/sambutan')
def sambutan():
    return render_template('sambutan.html', title='Sambutan Kepala Sekolah') 

@app.route('/organisasi')
def organisasi():
    return render_template('organisasi.html', title='Struktur Organisasi')

# --- ROUTES BERITA ---
@app.route('/berita-terbaru')
def berita_terbaru():
    return render_template('berita_terbaru.html', title='Berita Terbaru', all_berita=berita_data)

@app.route('/info-sekolah')
def info_sekolah():
    return render_template('info_sekolah.html', title='Info Sekolah')

@app.route('/agenda')
def agenda():
    past, today, future = categorize_agenda(raw_agenda_data)
    
    # Mengirim 3 kategori agenda ke template
    return render_template('agenda.html', 
                           title='Agenda Sekolah',
                           past_agenda=past,
                           today_agenda=today,
                           future_agenda=future)

@app.route('/galeri')
def galeri():
    return render_template('galeri.html', title='Galeri')

# --- ROUTES LAYANAN (SIMPLIFIKASI) ---
@app.route('/ekstrakurikuler')
def ekstrakurikuler():
    return render_template('ekstrakurikuler.html', title='Ekstrakurikuler')

@app.route('/laboratorium')
def laboratorium():
    return render_template('laboratorium.html', title='Laboratorium')

@app.route('/perpustakaan')
def perpustakaan():
    return render_template('perpustakaan.html', title='Perpustakaan')


if __name__ == '__main__':
    app.run(debug=True)