from typing import List, Tuple

def bytes_to_hex(b: bytes) -> str:
    return b.hex()

def safe_chr(x: int) -> str:
    # Untuk menampilkan karakter printable, selain itu pakai '.'
    return chr(x) if 32 <= x <= 126 else "."

def show_s_window(S: List[int], center: int, radius: int = 3) -> str:
    # Tampilkan sebagian kecil S di sekitar index tertentu
    lo = max(0, center - radius)
    hi = min(255, center + radius)
    parts = []
    for idx in range(lo, hi + 1):
        parts.append(f"{idx:3d}:{S[idx]:3d}")
    return " | ".join(parts)

def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def print_table(headers: List[str], rows: List[List[str]]):
    # hitung lebar kolom
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(r: List[str]) -> str:
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(r))

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt_row(r))



def ksa(key: bytes, show_steps: int = 12, show_s_radius: int = 2) -> List[int]:
    """
    KSA: Inisialisasi S (0..255), lalu aduk berdasarkan key.
    show_steps: jumlah langkah awal yang ditampilkan (agar output tidak panjang)
    """
    if not key:
        raise ValueError("Key tidak boleh kosong.")

    S = list(range(256))
    j = 0
    klen = len(key)

    print_section("KSA (Key Scheduling Algorithm)")
    print(f"Key (string)  : {key.decode('utf-8', errors='replace')}")
    print(f"Key (bytes)   : {list(key)}")
    print(f"Key length    : {klen} byte\n")

    rows = []
    for i in range(256):
        j_old = j
        j = (j + S[i] + key[i % klen]) % 256

        # sebelum swap
        Si_before = S[i]
        Sj_before = S[j]

        # swap
        S[i], S[j] = S[j], S[i]

        if i < show_steps:
            rows.append([
                str(i),
                str(j_old),
                str(key[i % klen]),
                f"(j + S[i] + key) mod 256",
                str(j),
                f"S[i]={Si_before} ↔ S[j]={Sj_before}",
                show_s_window(S, i, show_s_radius)
            ])

    print("Menampilkan beberapa langkah awal KSA (agar tidak 256 baris penuh):\n")
    print_table(
        headers=["i", "j_awal", "key[i%k]", "rumus", "j_akhir", "swap", "S window sekitar i"],
        rows=rows
    )
    print("\nKSA selesai.")
    print("S (10 elemen pertama) :", S[:10])
    print("S (10 elemen terakhir):", S[-10:])

    return S


def prga(S: List[int], nbytes: int, show_steps: int = 12, show_s_radius: int = 2) -> bytes:
    """
    PRGA: menghasilkan keystream sepanjang nbytes.
    show_steps: jumlah byte awal keystream yang ditampilkan.
    """
    i = 0
    j = 0
    out = []

    print_section("PRGA (Pseudo Random Generation Algorithm) - Keystream")
    rows = []

    for t in range(nbytes):
        i_old, j_old = i, j
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        Si_before = S[i]
        Sj_before = S[j]

        # swap
        S[i], S[j] = S[j], S[i]

        idx = (S[i] + S[j]) % 256
        K = S[idx]
        out.append(K)

        if t < show_steps:
            rows.append([
                str(t),
                f"{i_old}→{i}",
                f"{j_old}→{j}",
                f"S[i]={Si_before} ↔ S[j]={Sj_before}",
                f"idx=(S[i]+S[j])%256={idx}",
                str(K),
                f"0x{K:02x}",
                show_s_window(S, i, show_s_radius)
            ])

    print("Menampilkan beberapa byte awal PRGA:\n")
    print_table(
        headers=["t", "i", "j", "swap", "index", "K(dec)", "K(hex)", "S window sekitar i"],
        rows=rows
    )
    print("\nPRGA selesai.")
    return bytes(out)


def xor_encrypt(plaintext: bytes, keystream: bytes, show_steps: int = 24) -> bytes:
    """
    XOR plaintext dengan keystream => ciphertext.
    show_steps: jumlah byte awal yang ditampilkan pada tabel XOR.
    """
    if len(plaintext) != len(keystream):
        raise ValueError("Plaintext dan keystream harus sama panjang.")

    ciphertext = bytes([p ^ k for p, k in zip(plaintext, keystream)])

    print_section("XOR (Plaintext ⊕ Keystream = Ciphertext)")
    rows = []
    n = len(plaintext)

    for t in range(min(show_steps, n)):
        p = plaintext[t]
        k = keystream[t]
        c = ciphertext[t]
        rows.append([
            str(t),
            f"{p:3d} ('{safe_chr(p)}')",
            f"{k:3d} (0x{k:02x})",
            f"{c:3d} (0x{c:02x})",
        ])

    print_table(
        headers=["t", "P[t] (dec/char)", "K[t] (dec/hex)", "C[t] (dec/hex)"],
        rows=rows
    )

    if n > show_steps:
        print(f"\n... (dipotong, total {n} byte)")

    return ciphertext


def rc4_encrypt(key: bytes, plaintext: bytes,
                ksa_steps: int = 12, prga_steps: int = 12, xor_steps: int = 24) -> Tuple[bytes, bytes]:
    """
    Enkripsi RC4:
    1) KSA => S
    2) PRGA => keystream
    3) XOR => ciphertext
    """
    S = ksa(key, show_steps=ksa_steps)
    keystream = prga(S, len(plaintext), show_steps=prga_steps)
    ciphertext = xor_encrypt(plaintext, keystream, show_steps=xor_steps)

    print_section("RINGKASAN ENKRIPSI")
    print("Plaintext (utf-8) :", plaintext.decode("utf-8", errors="replace"))
    print("Plaintext (hex)   :", bytes_to_hex(plaintext))
    print("Keystream (hex)   :", bytes_to_hex(keystream))
    print("Ciphertext (hex)  :", bytes_to_hex(ciphertext))

    return ciphertext, keystream


def rc4_decrypt(key: bytes, ciphertext: bytes,
                ksa_steps: int = 12, prga_steps: int = 12, xor_steps: int = 24) -> bytes:
    """
    Dekripsi RC4 identik:
    ciphertext XOR keystream => plaintext
    (keystream harus sama => ulang KSA+PRGA dengan key yang sama)
    """
    S = ksa(key, show_steps=ksa_steps)
    keystream = prga(S, len(ciphertext), show_steps=prga_steps)
    plaintext = xor_encrypt(ciphertext, keystream, show_steps=xor_steps)

    print_section("RINGKASAN DEKRIPSI")
    print("Ciphertext (hex)  :", bytes_to_hex(ciphertext))
    print("Keystream (hex)   :", bytes_to_hex(keystream))
    print("Recovered (utf-8) :", plaintext.decode("utf-8", errors="replace"))
    print("Recovered (hex)   :", bytes_to_hex(plaintext))

    return plaintext


def main():
    print_section("DEMO RC4 ENKRIPSI & DEKRIPSI - STEP BY STEP")

    key_str = "kunci-rahasia"
    plaintext_str = "Halo RC4! Ini demo step-by-step."

    key = key_str.encode("utf-8")
    plaintext = plaintext_str.encode("utf-8")

    # Atur jumlah langkah yang ingin ditampilkan agar cocok untuk presentasi
    KSA_STEPS = 10     # tampilkan 10 langkah awal KSA
    PRGA_STEPS = 12    # tampilkan 12 byte awal PRGA
    XOR_STEPS = 24     # tampilkan 24 byte awal XOR

    print("Key      :", key_str)
    print("Plaintext:", plaintext_str)

    # ENKRIPSI
    ciphertext, _ = rc4_encrypt(
        key, plaintext,
        ksa_steps=KSA_STEPS,
        prga_steps=PRGA_STEPS,
        xor_steps=XOR_STEPS
    )

    # DEKRIPSI
    recovered = rc4_decrypt(
        key, ciphertext,
        ksa_steps=KSA_STEPS,
        prga_steps=PRGA_STEPS,
        xor_steps=XOR_STEPS
    )

    assert recovered == plaintext, "Dekripsi gagal: plaintext tidak kembali sama!"
    print("\n✅ Validasi OK: recovered == plaintext")


if __name__ == "__main__":
    main()