# 🏫 Medina Project

Website profil sekolah berbasis Flask dengan database MySQL.

---

## 📋 Requirements

- **Python** 3.8+
- **MySQL** 5.7+ atau MariaDB 10.3+
- **Git** (optional, untuk clone repository)

---

## 🚀 Instalasi Local Development

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd medinaProject
```

---

### Step 2: Setup Virtual Environment

#### 🪟 Windows (PowerShell / CMD)

```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
.\venv\Scripts\activate
```

#### 🍎 macOS / Linux

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Setup Database MySQL

1. **Buat database baru** di MySQL:

```sql
CREATE DATABASE medinadb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **Import schema** (jika menggunakan file SQL):

```bash
mysql -u root -p medinadb < medinadb.sql
```

---

### Step 5: Konfigurasi Environment

Buat file `.env` di root folder project:

```env
SECRET_KEY=kunci_rahasia_anda_yang_sangat_aman_dan_panjang
DB_USERNAME=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=medinadb
```

> **⚠️ Catatan:** Sesuaikan `DB_PORT` dengan port MySQL Anda (default: `3306`, XAMPP: `3306`, MAMP: `8889`).

---

### Step 6: Database Migration

Jika ada perubahan struktur database dari `models.py`, jalankan script migrasi:

```bash
python migrate_org.py
```

Script ini akan menambahkan kolom baru pada tabel `organisasi`:
- `jumlah` (INT) - Jumlah staff
- `emoji` (VARCHAR) - Icon emoji

---

### Step 7: (Optional) Seed Data Awal

Untuk mengisi data sample:

```bash
python seed.py
```

---

### Step 8: Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: **http://127.0.0.1:5000**

---

## 🔐 Admin Access

| Field    | Value                              |
|----------|------------------------------------|
| URL      | http://127.0.0.1:5000/auth/login   |
| Username | `admin`                            |
| Password | `password123`                      |

**Admin Dashboard:** http://127.0.0.1:5000/admin/dashboard

---

## 📁 Struktur Project

```
medinaProject/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   └── utils/          # Helper utilities
├── static/             # CSS, JS, Images
├── templates/          # HTML templates
├── app.py              # Entry point
├── config.py           # Konfigurasi app
├── migrate_org.py      # Script migrasi database
├── seed.py             # Script seed data
├── requirements.txt    # Python dependencies
└── medinadb.sql        # Database schema
```

---

## 🛠️ Troubleshooting

### Error: MySQL Connection Refused

- Pastikan MySQL server sudah berjalan
- Cek port MySQL di `.env` sesuai dengan konfigurasi server Anda

### Error: ModuleNotFoundError

```bash
# Pastikan virtual environment aktif, lalu install ulang
pip install -r requirements.txt
```

### Error: Table Doesn't Exist

```bash
# Import ulang schema database
mysql -u root -p medinadb < medinadb.sql

# Lalu jalankan migrasi
python migrate_org.py
```

---

## 📝 License

© 2024 Medina Project. All rights reserved.
