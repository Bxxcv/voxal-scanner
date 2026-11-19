# VOCXAL — Demo Review Keamanan

VOCXAL menampilkan laporan dari tiga skenario sintetis. Dashboard memperlihatkan
jumlah temuan, sedangkan laporan memuat keparahan dan saran remediasi. Skenario
baseline memperlihatkan kondisi tanpa temuan; itu bukan jaminan keamanan.

## Jalankan

Butuh Python 3.11+ dan browser dengan dukungan JavaScript modules. Tidak ada
paket yang perlu dipasang.

```sh
python backend/server.py
```

Buka `http://localhost:5000`, pilih skenario dari halaman utama atau dashboard,
lalu buka laporan. URL laporan bisa dibagikan dan tidak menyimpan data pengguna.

Server hanya menyajikan file demo yang diizinkan. Endpoint scan lama tidak
tersedia; kode lama di `backend/` tidak digunakan atau disajikan oleh demo.
Gunakan demo untuk edukasi, bukan sebagai penilaian keamanan atas sistem nyata.

## Verifikasi

```sh
python -B -m unittest discover -s tests
node --test tests/scenarios.test.mjs
```

Perintah kedua menggunakan Node.js 18+ dan tidak memerlukan paket tambahan.
