import smtplib
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Mengambil data rahasia secara aman dari GitHub Secrets atau Environment Variables
EMAIL_PENGIRIM = os.environ.get("EMAIL_PENGIRIM")
PASSWORD_APLIKASI = os.environ.get("PASSWORD_APLIKASI")

# --- LENGKAPI IDENTITAS ANDA DI SINI ---
NAMA_PENGIRIM = "Abdul Mughni Sukma Sadani"
POSISI_YANG_DILAMAR = "Operator Produksi"
FILE_CV = "CV_Anda.pdf"  # Pastikan nama file CV Anda di folder sama dengan nama ini

SUBJEK_EMAIL = f"{POSISI_YANG_DILAMAR} - {NAMA_PENGIRIM}"

BODY_EMAIL = f"""Dengan hormat,

Bapak/Ibu Pimpinan HRD
PT Armada Footwear Indonesia
Di Tempat

Sesuai dengan informasi lowongan kerja yang saya terima bahwa PT Armada Footwear Indonesia sedang membutuhkan karyawan untuk posisi {POSISI_YANG_DILAMAR}, maka dengan ini saya bermaksud mengajukan diri untuk mengisi posisi tersebut.

Berikut adalah data singkat mengenai diri saya:

Nama: {NAMA_PENGIRIM}
Tempat, tanggal lahir: Tegal, 11 Oktober 2001
Jenis kelamin: Laki-laki
Pendidikan terakhir: SMK
Alamat: Jln. Jaya Sumita, RT 07 RW 02, Desa Lebeteng, Kecamatan Tarub, Kabupaten Tegal
No. HP/WhatsApp: 0895383240554

Sebagai bahan pertimbangan Bapak/Ibu, saya lampirkan daftar riwayat hidup (CV) beserta dokumen pendukung lainnya dalam bentuk attachment pada email ini.

Besar harapan saya untuk diberikan kesempatan menghadiri sesi tes dan wawancara agar dapat menjelaskan potensi diri saya secara lebih mendalam. Atas perhatian Bapak/Ibu, saya mengucapkan terima kasih.

Hormat saya,

{NAMA_PENGIRIM}
"""

def kirim_email():
    if not os.path.exists("daftar_email.txt"):
        print("Error: File 'daftar_email.txt' tidak ditemukan!")
        return

    with open("daftar_email.txt", "r") as f:
        daftar_hrd = [line.strip() for line in f if line.strip()]

    if not daftar_hrd:
        print("Daftar email HRD kosong.")
        return

    # PERBAIKAN: Menggunakan host SMTP Gmail yang benar
    print("Menghubungkan ke server SMTP Gmail...")
    try:
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()
        server.login(EMAIL_PENGIRIM, PASSWORD_APLIKASI)
        print("Login berhasil!")
    except Exception as e:
        print(f"Gagal login ke server: {e}")
        return

    for email_tujuan in daftar_hrd:
        print(f"Sedang mengirim email ke: {email_tujuan}...")
        msg = MIMEMultipart()
        msg["From"] = f"{NAMA_PENGIRIM} <{EMAIL_PENGIRIM}>"
        msg["To"] = email_tujuan
        msg["Subject"] = SUBJEK_EMAIL
        msg.attach(MIMEText(BODY_EMAIL, "plain"))

        try:
            with open(FILE_CV, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(FILE_CV)}")
                msg.attach(part)
        except Exception as e:
            print(f"Gagal melampirkan file CV: {e}")
            # Menggunakan continue agar jika 1 file gagal, pengiriman ke email berikutnya tetap berjalan
            continue

        try:
            server.sendmail(EMAIL_PENGIRIM, email_tujuan, msg.as_string())
            print(f"Sukses terkirim ke {email_tujuan} ✅")
        except Exception as e:
            print(f"Gagal mengirim ke {email_tujuan} ❌: {e}")

        time.sleep(5) 

    server.quit()
    print("\nSemua proses pengiriman selesai.")

if __name__ == "__main__":
    kirim_email()
