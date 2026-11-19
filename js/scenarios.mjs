export const scenarios = [
    {
        id: 'catalog',
        title: 'Katalog produk',
        description: 'Contoh review aplikasi katalog dengan dua temuan pada pengolahan input.',
        findings: [
            {
                title: 'Query database dirangkai dari input',
                severity: 'Tinggi',
                remediation: 'Gunakan parameterized query untuk setiap nilai input dan batasi hak akun database.',
            },
            {
                title: 'Komentar ditampilkan sebagai HTML',
                severity: 'Sedang',
                remediation: 'Render komentar sebagai teks. Jika markup diperlukan, sanitasi dengan daftar elemen yang diizinkan.',
            },
        ],
    },
    {
        id: 'portal',
        title: 'Portal internal',
        description: 'Contoh review portal karyawan dengan satu temuan pada kontrol akses.',
        findings: [
            {
                title: 'Hak akses dokumen tidak diperiksa per objek',
                severity: 'Tinggi',
                remediation: 'Periksa izin pengguna di server untuk setiap dokumen sebelum mengembalikan isinya.',
            },
        ],
    },
    {
        id: 'baseline',
        title: 'Baseline tanpa temuan',
        description: 'Skenario untuk melihat format laporan saat data contoh tidak memiliki temuan.',
        findings: [],
    },
];

export function getReport(id) {
    return scenarios.find(scenario => scenario.id === id);
}
