import smtplib
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Mengambil data rahasia secara aman dari GitHub Secrets
EMAIL_PENGIRIM = os.environ.get("EMAIL_PENGIRIM")
PASSWORD_APLIKASI = os.environ.get("PASSWORD_APLIKASI")

# --- LENGKAPI IDENTITAS ANDA DI SINI ---
NAMA_PENGIRIM = "Abdul Mughni Sukma Sadani"
POSISI_YANG_DILAMAR = "Operator Produksi"
FILE_CV = "CV_Anda.pdf"

SUBJEK_EMAIL = f"Operator produksi_Abdul Mughni Sukma Sadani"

BODY_EMAIL = f"""Dengan hormat,
Bapak/Ibu Pimpinan HRD 
Di 
PT Armada Footwear Indonesia 

 Sesuai dengan informasi yang saya terima, bahwa PT Armada Footwer Indonesia. sedang membutuhkan beberapa lowongan Pekerjaan Operator Produksi, Maka saya yang bertanda tangan dibawah ini.

Nama : Abdul Mughni Sukma Sadani
Tempat, tanggal lahir : Tegal, 11 Oktober 2001
Jenis kelamin : Laki-laki
Pendidikan terakhir : SMK
Alamat : Jln. Jaya Sumita, RT 07 RW 02, Desa Lebeteng, Kecamatan Tarub, Kabupaten Tegal
No Hp/Wa : 0895383240554

Bermaksud untuk mengisi lowongan pekerjaan tersebut. Bersama ini saya lampirkan satu lembar daftar riwayat hidup dan data pendukung lainnya sebagai bahan pertimbangan dalam bentuk attachment.

Bila dikehendaki, saya bersedia memenuhi panggilan untuk dites dan diwawancarai. Atas perhatian Bapak/Ibu saya mengucapkan terima kasih.

Hormat saya,

(Abdul Mughni Sukma Sadani)

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
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(FILE_CV)}")
                msg.attach(part)
        except Exception as e:
            print(f"Gagal melampirkan file CV: {e}")
            break

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
