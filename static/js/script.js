document.addEventListener('DOMContentLoaded', () => {
    // Interaktivitas untuk tombol "Jelajahi Lebih Lanjut" di Beranda
    const exploreBtn = document.getElementById('exploreBtn');
    if (exploreBtn) {
        exploreBtn.addEventListener('click', () => {
            alert('Terima kasih telah menjelajahi website kami! Mari kita lihat sejarah sekolah.');
            // Anda bisa mengarahkan ke halaman lain, contoh:
            window.location.href = '/sejarah';
        });
    }

    // Interaktivitas untuk form kontak (sederhana, tanpa backend sesungguhnya)
    const contactForm = document.getElementById('contactForm');
    const formStatus = document.getElementById('formStatus');

    if (contactForm) {
        contactForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Mencegah form untuk refresh halaman

            // Simulasi pengiriman data
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;

            console.log('Mengirim pesan:', { name, email, subject, message });

            // Menampilkan status pengiriman (misalnya, berhasil atau gagal)
            formStatus.style.display = 'block';
            formStatus.textContent = 'Pesan Anda berhasil terkirim! Kami akan segera menghubungi Anda.';
            formStatus.classList.remove('error');
            formStatus.classList.add('success');

            // Reset form setelah beberapa detik
            setTimeout(() => {
                contactForm.reset();
                formStatus.style.display = 'none';
            }, 3000);

            // Dalam aplikasi nyata, Anda akan mengirim data ini ke server Node.js
            // menggunakan fetch API atau XMLHttpRequest.
            /*
            fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, subject, message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    formStatus.textContent = 'Pesan Anda berhasil terkirim!';
                    formStatus.classList.remove('error');
                    formStatus.classList.add('success');
                    contactForm.reset();
                } else {
                    formStatus.textContent = 'Terjadi kesalahan saat mengirim pesan.';
                    formStatus.classList.remove('success');
                    formStatus.classList.add('error');
                }
                formStatus.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                formStatus.textContent = 'Terjadi kesalahan jaringan.';
                formStatus.classList.remove('success');
                formStatus.classList.add('error');
                formStatus.style.display = 'block';
            });
            */
        });
    }

    // Menandai navigasi aktif
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('header nav ul li a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else if (currentPath === '/' && link.getAttribute('href') === '/') {
            // Pastikan beranda aktif saat di root path
            link.classList.add('active');
        }
    });

    // Contoh interaktivitas lain: Mengubah warna latar belakang header saat scroll
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) { // Jika sudah scroll lebih dari 50px
                header.style.backgroundColor = '#1a242f'; // Warna lebih gelap
                header.style.transition = 'background-color 0.3s ease';
            } else {
                header.style.backgroundColor = '#2c3e50'; // Kembali ke warna awal
            }
        });
    }
});