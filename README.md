# Selenium Automation with ChromeDriver

## Kebutuhan Sistem

- **Python**: Pastikan Python versi 3.7 atau lebih baru telah terinstall.
- **pip**: Manajer paket Python (pip) harus terinstall.
- **Google Chrome**: Pastikan Google Chrome terinstall pada sistem Anda.
- **ChromeDriver**: ChromeDriver versi yang kompatibel dengan versi Google Chrome Anda. Unduh dari [situs resmi ChromeDriver](https://sites.google.com/chromium.org/driver/) atau [situs resmi ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/).

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

2. **Run Positive Test**:
   ```bash
   python test_positive.py

3. **Tun Negative Test**:
   ```bash
   python test_negative.py

Pastikan file `requirements.txt` berisi semua dependensi Python yang diperlukan, seperti `selenium`.

Untuk melihat log atau report hasil dari test silahkan buka `log.txt` 

# Penjelasan Test Case

## Test Case Positive (test_positive.py)

Test case ini dirancang untuk memverifikasi alur kerja yang normal dan positif. Dalam skenario ini, pengguna melakukan login dengan kredensial yang valid, menambahkan produk ke dalam keranjang, dan menyelesaikan proses checkout.

1. Login Positive: Pengguna masuk ke aplikasi menggunakan kredensial yang valid (standard_user dan secret_sauce).
2. Verifikasi Homepage: Setelah login, halaman utama (homepage) yang memuat daftar produk diverifikasi untuk memastikan telah dimuat dengan benar.
3. Menambahkan Produk ke Keranjang: Pengguna menambahkan 6 produk ke dalam keranjang belanja. Setiap harga produk dijumlahkan untuk mendapatkan total harga.
4. Checkout: Pengguna melanjutkan ke proses checkout, mengisi informasi pribadi seperti nama dan kode pos, dan memastikan bahwa subtotal yang dihitung sesuai dengan subtotal yang ditampilkan.
5. Verifikasi Checkout Berhasil: Sistem memverifikasi bahwa proses checkout berhasil dengan menampilkan pesan "THANK YOU FOR YOUR ORDER".
   
## Test Case Negative (test_negative.py)

Test case ini dirancang untuk menguji skenario negatif, seperti penggunaan kredensial yang salah atau bug yang diketahui pada aplikasi.

1. Login Negative: Pengguna mencoba login dengan kredensial yang salah. Sistem memverifikasi bahwa login gagal dan menampilkan pesan kesalahan yang sesuai.
2. Reload Browser: Setelah percobaan login yang gagal, halaman browser di-refresh untuk mengatur ulang form login.
3. Login dengan problem_user: Pengguna mencoba login kembali menggunakan kredensial problem_user, yang dikenal memiliki bug pada aplikasi.
4. Verifikasi Login Berhasil: Setelah login berhasil, diverifikasi apakah halaman utama telah dimuat dengan benar.
5. Menambahkan Produk ke Keranjang: Pengguna menambahkan 6 produk ke dalam keranjang belanja.
6. Checkout: Pengguna melanjutkan ke proses checkout dan mengisi informasi pribadi.
7. Verifikasi Kesalahan pada Checkout: Diverifikasi bahwa terjadi kesalahan pada saat pengisian data checkout, di mana input field first-name berubah mengikuti nilai dari last-name.
8. Verifikasi Item Total Tidak Sesuai: Diverifikasi bahwa subtotal yang ditampilkan tidak sesuai dengan subtotal yang diharapkan, yang mencerminkan bug pada aplikasi.
9. Verifikasi Checkout Berhasil: Meskipun terdapat ketidaksesuaian pada subtotal, proses checkout tetap diverifikasi berhasil.
