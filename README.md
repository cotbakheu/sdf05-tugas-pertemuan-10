# Tugas 3 Kelompok — Pengujian Pricing

## 1. Struktur Proyek

```text
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
```

## 2. Cara Menjalankan

1. Pasang alat: pip install uv
2. Pasang kebutuhan: uv sync
3. Jalankan tes: uv run pytest tests/ -v
4. Jalankan program: uv run python -m src.pricing

## 3. Pengujian Mutasi

Pengujian mutasi dilakukan dengan mengubah implementasi `src/pricing.py` secara sengaja untuk memastikan unit test dapat mendeteksi kerusakan pada aturan bisnis. Setiap mutasi diuji pada salinan kode di folder sementara, jadi kode asli tetap aman.

### Hasil pengujian mutasi

| Kerusakan buatan                                                                                                        | Test yang gagal                                                                                                                                                                                        | Kesimpulan daya deteksi                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Menghapus penerapan diskon member sehingga fungsi `apply_member_discount()` selalu mengembalikan subtotal tanpa diskon. | `test_apply_member_discount_applies_ten_percent`; `test_calculate_total_for_member`. **2 test gagal.**                                                                                                 | Unit test mampu mendeteksi hilangnya diskon, baik melalui pengujian fungsi diskon secara langsung maupun perhitungan total belanja member. |
| Mengubah tarif pajak dari 11% menjadi 12% dengan mengubah `TAX_RATE = 0.11` menjadi `TAX_RATE = 0.12`.                  | `test_add_tax_applies_eleven_percent`; `test_calculate_total_for_member`; `test_calculate_total_for_non_member`; `test_calculate_total_defaults_to_non_member`. **4 test gagal.**                      | Unit test mampu mendeteksi perubahan tarif pajak pada fungsi pajak dan perhitungan total belanja untuk member maupun non-member.           |
| Menghapus validasi kuantitas `quantity <= 0` pada fungsi `calculate_subtotal()`.                                        | `test_calculate_subtotal_zero_quantity_raises_value_error`; `test_calculate_subtotal_negative_quantity_raises_value_error`; `test_calculate_total_zero_quantity_raises_value_error`. **3 test gagal.** | Unit test mampu mendeteksi hilangnya validasi kuantitas nol dan negatif, baik pada perhitungan subtotal maupun total belanja.              |

### Ringkasan

| Mutasi                       | Test gagal | Test lulus | Status     |
| ---------------------------- | ---------: | ---------: | ---------- |
| Menghapus diskon             |          2 |         17 | Terdeteksi |
| Mengubah tarif pajak         |          4 |         15 | Terdeteksi |
| Menghapus validasi kuantitas |          3 |         16 | Terdeteksi |

### Cara mengulang pengujian

```bash
uv sync --locked
uv run python scripts/check_mutations.py
```

Script menguji kode yang benar, lalu tiga mutasi satu per satu, dan terakhir kode yang benar lagi. Hasilnya disimpan di folder `bukti/`.

Log hasil pengujian:

- [Kode benar sebelum mutasi](bukti/00-implementasi-benar.txt)
- [Tanpa diskon](bukti/01-tanpa-diskon.txt)
- [Pajak 12%](bukti/02-pajak-12-persen.txt)
- [Tanpa validasi kuantitas](bukti/03-tanpa-validasi-kuantitas.txt)
- [Kode benar setelah mutasi](bukti/04-implementasi-benar-setelah-mutasi.txt)

Ketiga mutasi berhasil terdeteksi (3/3). Artinya, test sudah bisa mendeteksi tiga kerusakan yang dicoba, tetapi belum tentu semua jenis kesalahan.

## 4. Bukti Pengujian pada Implementasi yang Benar

Pengujian dilakukan pada 14 Oktober 2026 dengan Python 3.12.15 dan pytest 9.1.1. Setelah pengujian mutasi, kode asli tetap sama dan seluruh 19 test lulus.

Kode asli juga diuji langsung dengan:

```bash
uv run pytest -v
```

Hasil:

```text
============================== 19 passed in 0.02s ==============================
```

[Hasil lengkap pengujian](bukti/05-pytest-proyek.txt).
