````md
# RC4 Stream Cipher (From Scratch)\

Implementasi algoritma **RC4 (Stream Cipher)** dari nol (**from scratch**) menggunakan Python, tanpa memakai library enkripsi instan seperti `cryptography`, `pycrypto`, dll.

Program menampilkan langkah-langkah utama RC4 secara **step-by-step** (tabel KSA, PRGA, dan XOR) agar mudah dipresentasikan / direkam layar.

---

## Isi Repo
- `rc4_presentasi.py` : program utama (KSA + PRGA + XOR) dengan output tabel presentasi
- (opsional) `rc4_demo.py` : versi verbose sederhana (kalau kamu juga mau simpan)

---

## Requirements
- Python 3.8+ (disarankan Python 3.10+)

Tidak ada dependency tambahan.

---

## Cara Menjalankan

1) Clone repo:
```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
````

2. Jalankan program:

```bash
python rc4_presentasi.py
```

> Jika di komputermu `python` mengarah ke Python 2, gunakan:

```bash
python3 rc4_presentasi.py
```

---

## Input yang Dipakai (Key & Plaintext)

Di file `rc4_presentasi.py`, input berada pada bagian `main()`:

```python
key_str = "kunci-rahasia"
plaintext_str = "Halo RC4! Ini demo step-by-step."
```

### Penjelasan Key (Kunci)

* RC4 adalah **kriptografi simetris**, artinya **kunci yang sama** dipakai untuk enkripsi dan dekripsi.
* Pada demo ini, `key_str` adalah kunci dalam bentuk **string**, lalu dikonversi menjadi **byte** dengan UTF-8:

  ```python
  key = key_str.encode("utf-8")
  ```
* Panjang kunci pada implementasi ini bersifat **variabel** (selama tidak kosong). RC4 akan memakai `key[i % key_length]` pada tahap KSA.

> Catatan keamanan (untuk laporan): ini hanya demo edukasi. Pada penggunaan nyata, kunci harus dibangkitkan secara acak (CSPRNG/KDF) dan dibagikan lewat kanal aman.

---

## Apa yang Ditampilkan Program

Program akan menampilkan:

1. **KSA (Key Scheduling Algorithm)**

   * Inisialisasi array S = 0..255
   * Perhitungan indeks `j`
   * Proses swap `S[i]` dan `S[j]`
   * Ditampilkan beberapa langkah awal agar output tidak terlalu panjang

2. **PRGA (Pseudo Random Generation Algorithm)**

   * Menghasilkan byte keystream K[t]
   * Ditampilkan beberapa byte awal keystream

3. **XOR**

   * Menampilkan tabel per-byte: `C[t] = P[t] XOR K[t]`

4. **Ringkasan**

   * Plaintext (utf-8 + hex)
   * Keystream (hex)
   * Ciphertext (hex)
   * Hasil dekripsi (recovered plaintext)

---

## Mengatur Jumlah Langkah yang Ditampilkan (Untuk Presentasi)

Di `main()` kamu bisa atur:

```python
KSA_STEPS = 10
PRGA_STEPS = 12
XOR_STEPS = 24
```

* Naikkan jika ingin lebih detail saat presentasi
* Turunkan jika ingin lebih singkat

---

## Contoh Output (Singkat)

* Tabel KSA langkah awal
* Tabel PRGA byte awal (keystream)
* Tabel XOR byte awal
* Ringkasan ciphertext (hex) dan recovered plaintext

---

## Lisensi

Untuk tugas kuliah / edukasi.

```

---

## Bagian “Key” sebaiknya ditulis seperti apa?
Pakai format di README tadi, intinya harus ada:

- **key_str itu apa** (kunci simetris)
- **bagaimana jadi bytes** (UTF-8 encode)
- **bagaimana dipakai di KSA** (`key[i % keylen]`)
- catatan: demo edukasi vs produksi (opsional tapi bagus)

Kalau kamu mau versi yang lebih “dosen friendly”, ini paragraf yang bisa kamu tempel:

**“Key pada RC4 bersifat simetris (satu kunci untuk enkripsi dan dekripsi). Pada program ini kunci diinput sebagai string `key_str`, kemudian diubah menjadi deret byte UTF-8 (`encode('utf-8')`). Pada tahap KSA, byte kunci digunakan secara berulang menggunakan indeks `i % key_length` untuk mempengaruhi nilai `j` dan proses swap pada array state S.”**

```
