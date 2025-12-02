-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 02, 2025 at 04:26 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medinadb`
--

-- --------------------------------------------------------

--
-- Table structure for table `agenda`
--

CREATE TABLE `agenda` (
  `id` int(11) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `tanggal` datetime NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `waktu_display` varchar(50) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agenda`
--

INSERT INTO `agenda` (`id`, `judul`, `tanggal`, `deskripsi`, `lokasi`, `waktu_display`, `image_url`, `created_at`) VALUES
(1, 'Peringatan Hari Guru Nasional', '2025-11-25 00:00:00', 'Upacara dan berbagai perlombaan untuk memperingati Hari Guru.', 'Aula Sekolah', '08.00 - 14.00', '1', '2025-12-01 01:53:56'),
(2, 'Rapat Kerja Komite Sekolah', '2025-11-19 00:00:00', 'Rapat internal komite sekolah untuk evaluasi semester ganjil.', 'Ruang Rapat', '13.00 - 16.00', '2', '2025-12-01 01:53:56'),
(3, 'Lomba Debat Bahasa Inggris', '2025-11-15 00:00:00', 'Pelaksanaan lomba debat antar kelas di aula utama sekolah.', 'Aula Utama', '09.00 - 15.00', '3', '2025-12-01 01:53:56'),
(4, 'Open House & Pendaftaran Gel. 2', '2025-12-10 00:00:00', 'Acara promosi sekolah dan pembukaan pendaftaran gelombang kedua.', 'Seluruh Area Sekolah', '08.00 - 16.00', '4', '2025-12-01 01:53:56'),
(5, 'Studi Tur Museum Geologi', '2025-10-20 00:00:00', 'Kunjungan ke Museum Geologi Bandung untuk kelas IPA.', 'Museum Geologi Bandung', '08.00 - 15.00', '5', '2025-12-01 01:53:56');

-- --------------------------------------------------------

--
-- Table structure for table `alumni_testimoni`
--

CREATE TABLE `alumni_testimoni` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tahun_lulus` int(11) DEFAULT NULL,
  `testimoni` text DEFAULT NULL,
  `status_saat_ini` varchar(200) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `is_featured` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alumni_testimoni`
--

INSERT INTO `alumni_testimoni` (`id`, `nama`, `tahun_lulus`, `testimoni`, `status_saat_ini`, `image_url`, `is_featured`) VALUES
(1, 'Budi Santoso', 2020, 'SMA Medina membentuk saya menjadi pribadi yang disiplin dan inovatif, sangat siap untuk dunia kuliah.', 'Kuliah Teknik ITB', NULL, 0),
(2, 'Siti Aisyah', 2022, 'Guru-guru sangat suportif dan membantu saya mendapatkan beasiswa ke Fakultas Kedokteran.', 'Kuliah Kedokteran UGM', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `banner`
--

CREATE TABLE `banner` (
  `id` int(11) NOT NULL,
  `judul` varchar(100) DEFAULT NULL,
  `subjudul` varchar(200) DEFAULT NULL,
  `image_url` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `display_order` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `banner`
--

INSERT INTO `banner` (`id`, `judul`, `subjudul`, `image_url`, `is_active`, `display_order`, `created_at`) VALUES
(1, 'Selamat Datang di SMA Medina', 'Mencetak Generasi Berakhlak, Berprestasi, dan Berwawasan Global', '1', 1, 0, '2025-12-01 01:53:56'),
(2, 'Pendaftaran Siswa Baru 2026', 'Daftarkan putra-putri Anda di sekolah terbaik', '2', 1, 0, '2025-12-01 01:53:56'),
(3, 'Fasilitas Modern & Lengkap', 'Laboratorium, Perpustakaan, dan Sarana Olahraga Terbaik', '3', 1, 0, '2025-12-01 01:53:56');

-- --------------------------------------------------------

--
-- Table structure for table `berita`
--

CREATE TABLE `berita` (
  `id` int(11) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `tanggal` date NOT NULL,
  `ringkasan` text DEFAULT NULL,
  `konten_lengkap` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `berita`
--

INSERT INTO `berita` (`id`, `judul`, `slug`, `tanggal`, `ringkasan`, `konten_lengkap`, `image_url`, `created_at`, `updated_at`) VALUES
(1, 'Juara 1 Lomba Cerdas Cermat Pancasila', NULL, '2025-10-31', 'SMA Medina berhasil meraih juara 1 dalam Lomba Cerdas Cermat Pancasila tingkat nasional yang diselenggarakan oleh UNY.', 'SMA Medina Bandung kembali mengharumkan nama sekolah dengan meraih juara 1 dalam Lomba Cerdas Cermat Pancasila tingkat nasional. Tim yang terdiri dari 3 siswa terbaik berhasil mengalahkan puluhan sekolah dari seluruh Indonesia dalam kompetisi yang berlangsung selama 3 hari di UNY Yogyakarta.', NULL, '2025-12-01 01:53:56', '2025-12-01 01:53:56'),
(2, 'Peringatan Hari Guru Nasional 2025', NULL, '2025-11-25', 'SMA Medina mengadakan peringatan Hari Guru Nasional dengan berbagai kegiatan menarik dan penuh makna.', 'Dalam rangka memperingati Hari Guru Nasional, SMA Medina mengadakan serangkaian acara yang melibatkan seluruh civitas akademika. Acara dimulai dengan upacara bendera yang khidmat, dilanjutkan dengan pemberian penghargaan kepada guru berprestasi, dan diakhiri dengan pentas seni dari siswa-siswi.', NULL, '2025-12-01 01:53:56', '2025-12-01 01:53:56'),
(3, 'Program Studi Tur ke Museum Geologi', NULL, '2025-10-20', 'Siswa kelas X IPA melaksanakan studi tur edukatif ke Museum Geologi Bandung untuk memperdalam pemahaman materi pembelajaran.', 'Siswa-siswi kelas X IPA SMA Medina mengikuti kegiatan studi tur ke Museum Geologi Bandung. Kegiatan ini bertujuan untuk memberikan pengalaman belajar langsung dan memperdalam pemahaman siswa tentang geologi Indonesia. Para siswa sangat antusias mengikuti penjelasan dari pemandu museum.', NULL, '2025-12-01 01:53:56', '2025-12-01 01:53:56');

-- --------------------------------------------------------

--
-- Table structure for table `ekstrakurikuler`
--

CREATE TABLE `ekstrakurikuler` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `kategori` varchar(50) DEFAULT NULL,
  `pembina` varchar(100) DEFAULT NULL,
  `jadwal` varchar(100) DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ekstrakurikuler`
--

INSERT INTO `ekstrakurikuler` (`id`, `nama`, `kategori`, `pembina`, `jadwal`, `deskripsi`, `image_url`) VALUES
(1, 'Paskibra', 'Baris-Berbaris', 'Bpk. Dedi Supriadi, S.Pd', 'Rabu & Jumat, 15.30-17.00', 'Melatih kedisiplinan dan kepemimpinan melalui kegiatan baris-berbaris', '1'),
(2, 'Pramuka', 'Kepramukaan', 'Ibu Siti Nurhaliza, S.Pd', 'Sabtu, 14.00-16.00', 'Membentuk karakter dan keterampilan survival', '2'),
(3, 'Basket', 'Olahraga', 'Bpk. Ahmad Fauzi, S.Pd', 'Selasa & Kamis, 15.30-17.30', 'Mengembangkan kemampuan bermain basket dan kerjasama tim', '3'),
(4, 'Robotika', 'Sains & Teknologi', 'Bpk. Budi Santoso, M.T', 'Rabu, 15.00-17.00', 'Belajar pemrograman dan membuat robot', '4'),
(5, 'English Club', 'Bahasa', 'Ibu Diana Putri, S.Pd', 'Kamis, 15.00-16.30', 'Meningkatkan kemampuan berbahasa Inggris', '5'),
(6, 'Seni Musik', 'Seni', 'Bpk. Rizky Ananda, S.Sn', 'Jumat, 15.00-17.00', 'Mengembangkan bakat musik vokal dan instrumental', '6');

-- --------------------------------------------------------

--
-- Table structure for table `galeri`
--

CREATE TABLE `galeri` (
  `id` int(11) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `kategori` varchar(50) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `galeri`
--

INSERT INTO `galeri` (`id`, `judul`, `kategori`, `tanggal`, `deskripsi`, `image_url`, `created_at`) VALUES
(1, 'Upacara Hari Kemerdekaan 2025', 'Kegiatan', '2025-08-17', 'Pelaksanaan upacara peringatan HUT RI ke-80', '1', '2025-12-01 01:53:56'),
(2, 'Lomba Cerdas Cermat', 'Prestasi', '2025-10-31', 'Tim cerdas cermat SMA Medina juara nasional', '2', '2025-12-01 01:53:56'),
(3, 'Fasilitas Laboratorium Kimia', 'Fasilitas', '2025-09-01', 'Laboratorium kimia dengan peralatan modern', '3', '2025-12-01 01:53:56'),
(4, 'Perpustakaan Digital', 'Fasilitas', '2025-09-01', 'Perpustakaan dengan koleksi buku dan e-book lengkap', '4', '2025-12-01 01:53:56'),
(5, 'Pentas Seni Tahun Ajaran 2025', 'Kegiatan', '2025-11-10', 'Penampilan seni dari berbagai ekstrakurikuler', '5', '2025-12-01 01:53:56'),
(6, 'Kelas Robotika', 'Kegiatan', '2025-10-15', 'Pembelajaran robotika untuk siswa', '6', '2025-12-01 01:53:56');

-- --------------------------------------------------------

--
-- Table structure for table `laboratorium`
--

CREATE TABLE `laboratorium` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `laboratorium`
--

INSERT INTO `laboratorium` (`id`, `nama`, `deskripsi`, `image_url`) VALUES
(1, 'Laboratorium Fisika', 'Dilengkapi dengan peralatan eksperimen fisika modern', '1'),
(2, 'Laboratorium Kimia', 'Laboratorium dengan standar keamanan tinggi untuk praktikum kimia', '2'),
(3, 'Laboratorium Biologi', 'Fasilitas untuk praktikum biologi dan penelitian', '3'),
(4, 'Laboratorium Komputer', 'Lab komputer dengan 40 unit PC dan koneksi internet cepat', '4'),
(5, 'Laboratorium Bahasa', 'Ruang multimedia untuk pembelajaran bahasa asing', '5'),
(6, 'lab mulmet', 'keren', '1');

-- --------------------------------------------------------

--
-- Table structure for table `laboratorium_fasilitas`
--

CREATE TABLE `laboratorium_fasilitas` (
  `id` int(11) NOT NULL,
  `laboratorium_id` int(11) NOT NULL,
  `nama_fasilitas` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `laboratorium_fasilitas`
--

INSERT INTO `laboratorium_fasilitas` (`id`, `laboratorium_id`, `nama_fasilitas`) VALUES
(1, 1, 'Osiloskop Digital'),
(2, 1, 'Set Optik Lengkap'),
(3, 1, 'Alat Mekanika'),
(4, 1, 'Komputer Analisis'),
(5, 2, 'Lemari Asam'),
(6, 2, 'Peralatan Gelas'),
(7, 2, 'Bahan Kimia Lengkap'),
(8, 2, 'Safety Equipment'),
(9, 3, 'Mikroskop Digital'),
(10, 3, 'Herbarium'),
(11, 3, 'Model Anatomi'),
(12, 3, 'Aquarium'),
(13, 4, '40 Unit PC'),
(14, 4, 'Software Lengkap'),
(15, 4, 'Internet 100 Mbps'),
(16, 4, 'Proyektor'),
(17, 5, 'Audio System'),
(18, 5, 'Headset Individual'),
(19, 5, 'Software Pembelajaran'),
(20, 5, 'Booth Recording'),
(21, 6, 'pc geming');

-- --------------------------------------------------------

--
-- Table structure for table `organisasi`
--

CREATE TABLE `organisasi` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jabatan` varchar(100) NOT NULL,
  `level` int(11) DEFAULT 99,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `organisasi`
--

INSERT INTO `organisasi` (`id`, `nama`, `jabatan`, `level`, `image_url`) VALUES
(1, 'Dr. H. Abdullah Rahman, M.Pd', 'Kepala Sekolah', 1, NULL),
(2, 'Drs. Bambang Sutrisno, M.Pd', 'Wakil Kepala Sekolah Kurikulum', 2, NULL),
(3, 'Ibu Hj. Rina Kusumawati, S.Pd, M.Si', 'Wakil Kepala Sekolah Kesiswaan', 2, NULL),
(4, 'Bpk. Dedi Kurniawan, S.Sos, M.M', 'Wakil Kepala Sekolah Humas', 2, NULL),
(5, 'Bpk. Ir. Yusuf Hidayat, M.T', 'Wakil Kepala Sekolah Sarana Prasarana', 2, NULL),
(6, 'Ibu Susi Susanti, S.E', 'Kepala Tata Usaha', 3, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `perpustakaan_fasilitas`
--

CREATE TABLE `perpustakaan_fasilitas` (
  `id` int(11) NOT NULL,
  `nama_fasilitas` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `perpustakaan_fasilitas`
--

INSERT INTO `perpustakaan_fasilitas` (`id`, `nama_fasilitas`) VALUES
(1, 'Ruang Baca Nyaman (kapasitas 100 orang)'),
(2, 'Area Diskusi Kelompok'),
(3, 'Komputer Katalog Digital'),
(4, 'Wifi Gratis'),
(5, 'AC dan Pencahayaan Optimal'),
(6, 'CCTV 24 Jam');

-- --------------------------------------------------------

--
-- Table structure for table `perpustakaan_info`
--

CREATE TABLE `perpustakaan_info` (
  `id` int(11) NOT NULL DEFAULT 1,
  `jam_buka_senin_jumat` varchar(50) DEFAULT NULL,
  `jam_buka_sabtu` varchar(50) DEFAULT NULL,
  `jumlah_buku_pelajaran` int(11) DEFAULT 0,
  `jumlah_buku_fiksi` int(11) DEFAULT 0,
  `jumlah_buku_referensi` int(11) DEFAULT 0,
  `jumlah_majalah_jurnal` int(11) DEFAULT 0,
  `jumlah_ebook` int(11) DEFAULT 0,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `perpustakaan_info`
--

INSERT INTO `perpustakaan_info` (`id`, `jam_buka_senin_jumat`, `jam_buka_sabtu`, `jumlah_buku_pelajaran`, `jumlah_buku_fiksi`, `jumlah_buku_referensi`, `jumlah_majalah_jurnal`, `jumlah_ebook`, `updated_at`) VALUES
(1, '07.30 - 16.00', '08.00 - 14.00', 3500, 1200, 800, 150, 5000, '2025-12-01 01:53:56');

-- --------------------------------------------------------

--
-- Table structure for table `perpustakaan_layanan`
--

CREATE TABLE `perpustakaan_layanan` (
  `id` int(11) NOT NULL,
  `nama_layanan` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `perpustakaan_layanan`
--

INSERT INTO `perpustakaan_layanan` (`id`, `nama_layanan`) VALUES
(1, 'Peminjaman Buku (maks 3 buku, 1 minggu)'),
(2, 'Referensi dan Penelusuran Informasi'),
(3, 'Akses E-Book dan Jurnal Online'),
(4, 'Layanan Fotokopi'),
(5, 'Bimbingan Literasi Informasi');

-- --------------------------------------------------------

--
-- Table structure for table `prestasi`
--

CREATE TABLE `prestasi` (
  `id` int(11) NOT NULL,
  `nama_prestasi` varchar(255) NOT NULL,
  `skala` varchar(50) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `penyelenggara` varchar(100) DEFAULT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prestasi`
--

INSERT INTO `prestasi` (`id`, `nama_prestasi`, `skala`, `tanggal`, `penyelenggara`, `keterangan`) VALUES
(1, 'Juara 1 Lomba Cerdas Cermat Pancasila', 'Nasional', '2025-10-31', 'UNY', NULL),
(2, 'Juara 2 FIKSI Nasional 2025', 'Nasional', '2025-10-30', 'Kemendikbud', NULL),
(3, 'Medali Emas Olimpiade Fisika Regional', 'Regional', '2025-09-15', 'Dinas Pendidikan', NULL),
(4, 'Juara Lomba Debat Bahasa Inggris', 'Sekolah', '2025-08-20', 'SMA Medina', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sekolah_info`
--

CREATE TABLE `sekolah_info` (
  `id` int(11) NOT NULL DEFAULT 1,
  `nama` varchar(100) NOT NULL,
  `npsn` varchar(20) DEFAULT NULL,
  `akreditasi` char(1) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `telepon` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `website` varchar(100) DEFAULT NULL,
  `kepala_sekolah` varchar(100) DEFAULT NULL,
  `jumlah_siswa` int(11) DEFAULT NULL,
  `jumlah_guru` int(11) DEFAULT NULL,
  `jumlah_kelas` int(11) DEFAULT NULL,
  `tahun_berdiri` int(11) DEFAULT NULL,
  `sejarah` text DEFAULT NULL,
  `visi` text DEFAULT NULL,
  `misi` text DEFAULT NULL,
  `sambutan_kepsek` text DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sekolah_info`
--

INSERT INTO `sekolah_info` (`id`, `nama`, `npsn`, `akreditasi`, `alamat`, `telepon`, `email`, `website`, `kepala_sekolah`, `jumlah_siswa`, `jumlah_guru`, `jumlah_kelas`, `tahun_berdiri`, `sejarah`, `visi`, `misi`, `sambutan_kepsek`, `updated_at`) VALUES
(1, 'SMA Medina Bandung', '20219345', 'A', 'Jl. Pendidikan No. 123, Bandung, Jawa Barat', '(022) 7654321', 'info@smamedina.sch.id', 'www.smamedina.sch.id', 'Dr. H. Abdullah Rahman, M.Pd', 720, 58, 24, 1995, 'SMA Medina Bandung didirikan pada tahun 1995 dengan visi menjadi lembaga pendidikan yang unggul dalam mengembangkan potensi siswa secara holistik. Berawal dari sebuah gedung sederhana dengan hanya 3 kelas, kini SMA Medina telah berkembang menjadi salah satu sekolah favorit di kota Bandung.\n\nDalam perjalanannya selama lebih dari 25 tahun, SMA Medina telah menghasilkan ribuan alumni yang tersebar di berbagai perguruan tinggi ternama di Indonesia dan luar negeri. Prestasi demi prestasi terus diraih, baik di bidang akademik maupun non-akademik.\n\nDengan motto \"Berakhlak, Berprestasi, Berwawasan Global\", SMA Medina terus berkomitmen untuk memberikan pendidikan berkualitas yang tidak hanya fokus pada aspek kognitif, tetapi juga pengembangan karakter dan soft skills siswa.', 'Menjadi sekolah menengah atas yang unggul, berkarakter, dan berwawasan global dalam mencetak generasi pemimpin masa depan yang berakhlak mulia.', '1. Menyelenggarakan pendidikan berkualitas dengan standar nasional dan internasional\n2. Mengembangkan potensi akademik dan non-akademik siswa secara optimal\n3. Membentuk karakter siswa yang berakhlak mulia, disiplin, dan bertanggung jawab\n4. Menciptakan lingkungan belajar yang kondusif, inovatif, dan berbasis teknologi\n5. Membangun kerjasama dengan berbagai pihak untuk pengembangan sekolah\n6. Mempersiapkan siswa untuk bersaing di tingkat nasional dan internasional\n7. Mengintegrasikan nilai-nilai keislaman dalam setiap aspek pembelajaran', 'Assalamu\'alaikum Warahmatullahi Wabarakatuh,\n\nPuji syukur kehadirat Allah SWT atas segala rahmat dan karunia-Nya. Shalawat serta salam semoga tercurah kepada Nabi Muhammad SAW, keluarga, dan para sahabatnya.\n\nSelamat datang di website resmi SMA Medina Bandung. Sebagai Kepala Sekolah, saya merasa bangga dapat memimpin lembaga pendidikan yang telah memiliki reputasi baik dalam mencetak generasi unggul.\n\nSMA Medina tidak hanya fokus pada pencapaian akademik, tetapi juga pada pembentukan karakter dan akhlak mulia siswa. Kami percaya bahwa pendidikan sejati adalah yang mampu menyeimbangkan kecerdasan intelektual, emosional, dan spiritual.\n\nKepada seluruh siswa, orang tua, dan masyarakat, mari bersama-sama kita wujudkan visi SMA Medina untuk menjadi sekolah yang unggul dan berkarakter. Semoga Allah SWT senantiasa memberkahi setiap langkah kita.\n\nWassalamu\'alaikum Warahmatullahi Wabarakatuh.\n\nDr. H. Abdullah Rahman, M.Pd\nKepala SMA Medina Bandung', '2025-12-01 01:53:56');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `created_at`) VALUES
(1, 'admin', 'scrypt:32768:8:1$9EzKoDvtA6rTYYnj$e808bb4ff1c611e25ed6fa542e8c6b979368c8f072a7ce208f6c734af461e2c768acbed5784f9008bcad023ef8fcd4985bd8a1637c4cda82ea1b7c39b44d250c', '2025-12-01 01:53:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agenda`
--
ALTER TABLE `agenda`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `alumni_testimoni`
--
ALTER TABLE `alumni_testimoni`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `banner`
--
ALTER TABLE `banner`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `berita`
--
ALTER TABLE `berita`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `ekstrakurikuler`
--
ALTER TABLE `ekstrakurikuler`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `galeri`
--
ALTER TABLE `galeri`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `laboratorium`
--
ALTER TABLE `laboratorium`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `laboratorium_fasilitas`
--
ALTER TABLE `laboratorium_fasilitas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `laboratorium_id` (`laboratorium_id`);

--
-- Indexes for table `organisasi`
--
ALTER TABLE `organisasi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `perpustakaan_fasilitas`
--
ALTER TABLE `perpustakaan_fasilitas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `perpustakaan_info`
--
ALTER TABLE `perpustakaan_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `perpustakaan_layanan`
--
ALTER TABLE `perpustakaan_layanan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prestasi`
--
ALTER TABLE `prestasi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sekolah_info`
--
ALTER TABLE `sekolah_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agenda`
--
ALTER TABLE `agenda`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `alumni_testimoni`
--
ALTER TABLE `alumni_testimoni`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `banner`
--
ALTER TABLE `banner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `berita`
--
ALTER TABLE `berita`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ekstrakurikuler`
--
ALTER TABLE `ekstrakurikuler`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `galeri`
--
ALTER TABLE `galeri`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `laboratorium`
--
ALTER TABLE `laboratorium`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `laboratorium_fasilitas`
--
ALTER TABLE `laboratorium_fasilitas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `organisasi`
--
ALTER TABLE `organisasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `perpustakaan_fasilitas`
--
ALTER TABLE `perpustakaan_fasilitas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `perpustakaan_layanan`
--
ALTER TABLE `perpustakaan_layanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `prestasi`
--
ALTER TABLE `prestasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `laboratorium_fasilitas`
--
ALTER TABLE `laboratorium_fasilitas`
  ADD CONSTRAINT `laboratorium_fasilitas_ibfk_1` FOREIGN KEY (`laboratorium_id`) REFERENCES `laboratorium` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
