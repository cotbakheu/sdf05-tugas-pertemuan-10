# Tugas 3 Kelompok — Pengujian Pricing

## 1. Struktur Proyek

sdf05-tugas-pertemuan-10/
├── src/
│   └── pricing.py
├── tests/
│   └── test_pricing.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md

## 2. Cara Menjalankan

1. Pasang alat: pip install uv
2. Pasang kebutuhan: uv sync
3. Jalankan tes: uv run pytest tests/ -v
4. Jalankan program: uv run python -m src.pricing

## Pertanyaan Analisis

### 1. Mengapa unit testing penting dalam pengembangan program ini?

Unit testing penting untuk memastikan setiap fungsi pada program perhitungan belanja berjalan sesuai dengan kebutuhan. Program ini memiliki beberapa fungsi utama, yaitu `calculate_subtotal()`, `apply_member_discount()`, `add_tax()`, `calculate_total()`, dan `write_receipt()`.

Dengan unit testing, setiap fungsi dapat diuji secara terpisah untuk memastikan hasil perhitungan benar, aturan bisnis diterapkan sesuai ketentuan, dan kesalahan dapat ditemukan lebih awal sebelum memengaruhi keseluruhan program.

Pengujian juga membantu memastikan bahwa perubahan kode tidak merusak fungsionalitas yang sebelumnya sudah berjalan dengan benar.

### 2. Apakah unit test yang dibuat sudah mencakup berbagai kemungkinan input?

Unit test yang tersedia telah mencakup beberapa kondisi penting, antara lain:

- Input valid dengan harga dan jumlah barang yang berbeda.
- Harga barang sebesar nol.
- Harga barang negatif.
- Jumlah barang nol atau negatif.
- Penggunaan diskon untuk member dan non-member.
- Perhitungan pajak sebesar 11%.
- Perhitungan total pembayaran dengan dan tanpa status member.
- Penulisan struk, termasuk kondisi ketika daftar baris kosong dan ketika file struk sudah memiliki isi sebelumnya.

Pengujian tersebut menunjukkan bahwa program tidak hanya diuji menggunakan input normal, tetapi juga menggunakan beberapa input yang tidak valid dan kondisi khusus.

Meskipun demikian, cakupan pengujian masih dapat ditingkatkan, misalnya dengan menguji input berupa tipe data yang tidak sesuai, nilai pecahan, serta kondisi kegagalan ketika program tidak memiliki izin untuk menulis file.

### 3. Bagaimana cara memastikan hasil perhitungan total pembayaran sudah benar?

Kebenaran perhitungan dapat diperiksa dengan membandingkan hasil aktual program dengan hasil yang diperoleh dari perhitungan manual.

Program menerapkan diskon member sebesar 10% dan pajak sebesar 11%. Berdasarkan implementasi tersebut, urutan perhitungan adalah menghitung subtotal, menerapkan diskon jika pelanggan merupakan member, kemudian menambahkan pajak.

Contoh perhitungan untuk pelanggan non-member:

- Harga barang: Rp100.000
- Jumlah barang: 1
- Subtotal: Rp100.000
- Diskon: Rp0
- Pajak: 11% × Rp100.000 = Rp11.000
- Total pembayaran: Rp111.000

Contoh perhitungan untuk pelanggan member:

- Harga barang: Rp100.000
- Jumlah barang: 1
- Subtotal: Rp100.000
- Diskon: 10% × Rp100.000 = Rp10.000
- Subtotal setelah diskon: Rp90.000
- Pajak: 11% × Rp90.000 = Rp9.900
- Total pembayaran: Rp99.900

Hasil tersebut sesuai dengan ekspektasi yang digunakan pada unit test `test_calculate_total_for_member()` dan `test_calculate_total_for_non_member()`.

Dengan demikian, pengujian membantu memverifikasi bahwa diskon diterapkan sebelum pajak dan hasil akhirnya sesuai dengan aturan perhitungan yang diimplementasikan.

### 4. Apa perbedaan antara unit testing dan mutation testing?

Unit testing merupakan pengujian yang memeriksa apakah program menghasilkan keluaran yang sesuai dengan ekspektasi untuk input tertentu.

Sementara itu, mutation testing merupakan teknik untuk mengevaluasi efektivitas unit test dengan cara membuat perubahan kecil yang disengaja pada kode program, yang disebut mutant.

Contohnya, operator perkalian pada perhitungan subtotal dapat diubah menjadi operator penjumlahan. Jika unit test gagal setelah perubahan tersebut, berarti pengujian mampu mendeteksi kesalahan pada logika perhitungan.

Sebaliknya, jika mutant masih lolos dari seluruh pengujian, terdapat kemungkinan bahwa unit test belum cukup kuat untuk mendeteksi perubahan tersebut.

Oleh karena itu, unit testing digunakan untuk memeriksa perilaku program, sedangkan mutation testing membantu menilai kemampuan pengujian dalam mendeteksi kesalahan pada implementasi program.

### 5. Apa yang dapat dilakukan untuk meningkatkan kualitas pengujian?

Kualitas pengujian dapat ditingkatkan melalui beberapa langkah berikut:

1. Menambahkan pengujian untuk berbagai nilai batas, seperti harga nol, jumlah barang satu, dan nilai input yang sangat besar.
2. Menambahkan pengujian untuk tipe data yang tidak sesuai dengan kebutuhan fungsi.
3. Menguji perilaku program ketika terjadi kegagalan penulisan file struk.
4. Memastikan setiap fungsi memiliki pengujian yang mencakup kondisi normal dan kondisi kesalahan.
5. Menggunakan mutation testing untuk mengidentifikasi perubahan kode yang belum dapat dideteksi oleh unit test.
6. Menambahkan pengujian berdasarkan hasil evaluasi mutation testing agar pengujian menjadi lebih efektif.

Selain itu, fungsi `apply_member_discount()` dan `add_tax()` dapat dipertimbangkan untuk diberikan validasi input apabila persyaratan program mengharuskan nilai subtotal atau nominal pajak tidak boleh negatif.

Dengan langkah-langkah tersebut, pengujian diharapkan dapat memberikan keyakinan yang lebih baik terhadap ketepatan perhitungan dan keandalan program.
