import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def save_booking(email, hotel_name, selected_date,room_type,selected_payment):
    """
    Simulate saving the booking to a database or file.
    Args:
        email (str): Email pengguna yang melakukan booking.
        hotel_name (str): Nama hotel yang dipesan.
        selected_date (str): Tanggal booking dalam format 'YYYY-MM-DD'.
    """
    # Simulasi penyimpanan data booking
    try:
        with open("bookings.csv", "a") as file:
            file.write(f"{email},{hotel_name},{selected_date},{room_type},{selected_payment}\n")
        print(f"Booking berhasil disimpan untuk {email}.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan booking: {e}")


def send_booking_confirmation(to_email, hotel_name, booking_date, room_type, price, payment_method):
    try:
        # Konfigurasi email pengirim (gunakan email dan password aplikasi)
        sender_email = "kautsarbudianto06@gmail.com"
        sender_password = "bfbq sipb wwar otvc"  # Gunakan app password untuk keamanan

        # Buat objek pesan
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = to_email
        message['Subject'] = f"Konfirmasi Booking Hotel {hotel_name}"

        # Buat isi email
        body = f"""
        Konfirmasi Booking Hotel

        Terima kasih telah melakukan booking:

        Detail Booking:
        - Hotel: {hotel_name}
        - Tanggal: {booking_date}
        - Tipe Kamar: {room_type}
        - Harga : {price}
        - Metode Pembayaran: {payment_method}
        
        Jika Anda memilih Transfer Bank:
        Silakan transfer ke rekening berikut:
        
        - Bank: BNI
        - No. Rekening: 1814241787
        - Atas Nama: Hotel Booking

        Terima kasih!
        """

        # Tambahkan body ke email
        message.attach(MIMEText(body, 'plain'))

        # Buat koneksi SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Aktifkan keamanan TLS
            server.login(sender_email, sender_password)
            
            # Kirim email
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
        return False
    
