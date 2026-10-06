import smtplib
import os
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Mengambil data kredensial secara aman dari GitHub Secrets
EMAIL_PENGIRIM = os.environ.get("EMAIL_PENGIRIM")
PASSWORD_APLIKASI = os.environ.get("PASSWORD_APLIKASI")

# --- DATA IDENTITAS PELAMAR ---
NAMA_PENGIRIM = "Abdul Mughni Sukma Sadani"
POSISI_YANG_DILAMAR = "Operator Produksi"
FILE_CV = "CV_Anda.pdf"  # *Pastikan nama file ini sama dengan file CV yang Anda upload di GitHub*

# Subjek email resmi sesuai standar HRD
SUBJEK_EMAIL = f"Lamaran Pekerjaan: {POSISI_YANG_DILAMAR} - {NAMA_PENGIRIM}"

# --- TEKS EMAIL RESMI & PROFESIONAL ---
BODY_EMAIL = f"""Dengan hormat,

Bapak/Ibu Pimpinan HRD
PT Armada Footwear Indonesia
Di Tempat

Sesuai dengan informasi lowongan pekerjaan yang saya dapatkan, saya mengetahui bahwa PT Armada Footwear Indonesia sedang membuka lowongan kerja untuk posisi {POSISI_YANG_DILAMAR}. Oleh karena itu, melalui email ini saya bermaksud untuk mengajukan diri guna mengisi posisi tersebut.

Berikut adalah ringkasan data diri singkat saya:

Nama: {NAMA_PENGIRIM}
Tempat, Tanggal Lahir: Tegal, 11 Oktober 2001
Jenis Kelamin: Laki-laki
Pendidikan Terakhir: SMK
Alamat: Jln. Jaya Sumita, RT 07 RW 02, Desa Lebeteng, Kec. Tarub, Kab. Tegal
No. HP / WhatsApp: 0895383240554

Sebagai bahan pertimbangan Bapak/Ibu, saya lampirkan Daftar Riwayat Hidup (CV) beserta berkas pendukung lainnya pada lampiran (attachment) email ini. Saya memiliki motivasi kerja yang tinggi serta siap untuk memberikan kontribusi terbaik bagi perusahaan.

Besar harapan saya untuk diberikan kesempatan mengikuti tahapan tes maupun wawancara, agar saya dapat menjelaskan mengenai potensi dan kualifikasi diri saya secara lebih mendalam.

Atas perhatian serta kesempatan yang Bapak/Ibu berikan, saya mengucapkan terima kasih.

Hormat saya,

{NAMA_PENGIRIM}
"""

def kirim_email():
    # Validasi apakah file daftar email tujuan ada
    if not os.path.exists("daftar_email.txt"):
        print("Error: File 'daftar_email.txt' tidak ditemukan di repositori!")
        return

    with open("daftar_email.txt", "r") as f:
        daftar_hrd = [line.strip() for line in f if line.strip()]

    if not daftar_hrd:
        print("Daftar email HRD di file 'daftar_email.txt' masih kosong.")
        return

    # PERBAIKAN UTAMA: Mengubah "://gmail.com" menjadi server SMTP resmi Gmail yang valid
    print("Menghubungkan ke server SMTP Gmail...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_PENGIRIM, PASSWORD_APLIKASI)
        print("Login berhasil! Memulai proses pengiriman...\n")
    except Exception as e:
        print(f"Gagal login ke server Gmail: {e}")
        print("Periksa kembali isi GitHub Secrets EMAIL_PENGIRIM dan PASSWORD_APLIKASI Anda.")
        return

    # Proses pengiriman email massal berjadwal
    for index, email_tujuan in enumerate(daftar_hrd):
        print(f"[{index + 1}/{len(daftar_hrd)}] Sedang mengirim ke: {email_tujuan}...")
        
        msg = MIMEMultipart()
        msg["From"] = f"{NAMA_PENGIRIM} <{EMAIL_PENGIRIM}>"
        msg["To"] = email_tujuan
        msg["Subject"] = SUBJEK_EMAIL
        msg.attach(MIMEText(BODY_EMAIL, "plain"))

        # Memasukkan lampiran file CV
        try:
            with open(FILE_CV, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(FILE_CV)}")
                msg.attach(part)
        except Exception as e:
            print(f"❌ Gagal membaca atau melampirkan file '{FILE_CV}': {e}")
            print("Pengiriman dibatalkan untuk alamat ini, lanjut ke antrean berikutnya.")
            continue

        # Proses kirim lewat server
        try:
            server.sendmail(EMAIL_PENGIRIM, email_tujuan, msg.as_string())
            print(f"✅ Sukses terkirim ke {email_tujuan}")
        except Exception as e:
            print(f"❌ Gagal mengirim ke {email_tujuan}: {e}")

        # Memberikan jeda waktu acak 10-25 detik agar tidak dianggap spam/bot oleh Google
        if email_tujuan != daftar_hrd[-1]:
            waktu_tunggu = random.randint(10, 25)
            print(f"Menunggu {waktu_tunggu} detik sebelum memproses email berikutnya...\n")
            time.sleep(waktu_tunggu)

    server.quit()
    print("\n[SELESAI] Semua email dalam daftar telah diproses.")

if __name__ == "__main__":
    kirim_email()
