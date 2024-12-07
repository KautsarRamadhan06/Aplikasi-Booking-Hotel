import smtplib
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image, ImageTk

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
    
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def show_booking_form(main, booking_date, hotel_name, address, rating, phone, priceSingle, priceDouble):
    from akhir import clear_frame
    from hotel import hotel_selection_page
    
     # Load background image
    canvas = tk.Canvas(main, width=1920, height=1080)
    canvas.pack(fill=tk.BOTH, expand=True)

    try:
        bg_image = Image.open("py.png")  # Pastikan file "py.png" ada
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        main.bg_photo = bg_photo
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image 'py.png' not found.")
        return

    # Inisialisasi room_type dan payment_method sebagai StringVar
    room_type_var = tk.StringVar(value="Single")  # Default value "Single"
    payment_method_var = tk.StringVar(value="Transfer Bank") 

    clear_frame(main)

    tk.Label(main, text=f"Hotel: {hotel_name}", font=("Arial", 20)).pack(pady=10)
    tk.Label(main, text=f"Alamat: {address}", font=("Arial", 14)).pack(pady=5)
    tk.Label(main, text=f"Rating: {rating}", font=("Arial", 14)).pack(pady=5)
    tk.Label(main, text=f"Telepon: {phone}", font=("Arial", 14)).pack(pady=5)

    tk.Label(main, text="Tipe Kamar:", font=("Arial", 14)).pack(pady=10)
    tk.Radiobutton(main, text=f"Single (Rp {priceSingle})", variable=room_type_var, value="Single", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text=f"Double (Rp {priceDouble})", variable=room_type_var, value="Double", font=("Arial", 12)).pack()
    
    tk.Label(main, text="Pilih Metode Pembayaran:", font=("Arial", 14)).pack(pady=10)
    tk.Radiobutton(main, text="Transfer Bank", variable=payment_method_var, value="Transfer Bank", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text="Kartu Kredit", variable=payment_method_var, value="Kartu Kredit", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text="Bayar di Tempat", variable=payment_method_var, value="Bayar di Tempat", font=("Arial", 12)).pack()

    tk.Button(main, text="Booking", font=("Arial", 14), bg="green", fg="white", command=lambda: on_book(main, booking_date, room_type_var, payment_method_var, hotel_name, priceSingle, priceDouble)).pack(pady=20)
    tk.Button(main, text="Kembali", font=("Arial", 14), command=lambda: hotel_selection_page(main, priceSingle, priceDouble,room_type=None,payment_method=None)).pack(pady=10)

def on_book(main, booking_date, room_type_var, payment_method_var, hotel_name, priceSingle, priceDouble):
    from akhir import thank_you_page
    from hotel import hotel_selection_page

    # if not booking_date.get():
    #     messagebox.showerror("Error", "Harap pilih tanggal booking!")
    #     return

    try:
        datetime.strptime(booking_date.get(), '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Format tanggal salah!")
        return

    selected_payment = payment_method_var.get()
    price = priceSingle if room_type_var.get() == "Single" else priceDouble

    # Simpan booking
    save_booking(main.email, hotel_name, booking_date.get(), room_type_var.get(), selected_payment)

    # Kirim email konfirmasi
    email_sent = send_booking_confirmation(main.email, hotel_name, booking_date.get(), room_type_var.get(), price, selected_payment)
    if email_sent:
        messagebox.showinfo("Sukses", f"Pemesanan berhasil! Email konfirmasi dikirim ke {main.email}.")
        thank_you_page(main)
    else:
        messagebox.showerror("Error", "Gagal mengirim email konfirmasi.")
        hotel_selection_page(main)
