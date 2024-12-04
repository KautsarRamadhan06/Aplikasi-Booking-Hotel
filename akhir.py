import pandas as pd
import os
import tkinter as tk
import smtplib
from hotel import book_hotel
from PIL import Image, ImageTk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# def load_hotels():
#     try:
#         if os.path.exists('daftar_hotel_solo.csv'):
#             hotels = pd.read_csv('daftar_hotel_solo.csv', on_bad_lines='skip')
#             hotels.columns = hotels.columns.str.strip()
#             return hotels
#         else:
#             messagebox.showerror("Error", "File CSV 'daftar_hotel_solo.csv' tidak ditemukan.")
#             return None
#     except FileNotFoundError:
#         messagebox.showerror("Error", "File CSV 'daftar_hotel_solo.csv' tidak ditemukan.")
#         return None

# Fungsi untuk clear frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Fungsi untuk load daftar pengguna
def load_users():
    if os.path.exists('users.csv'):
        return pd.read_csv('users.csv')
    else:
        return pd.DataFrame(columns=['Email', 'Password', 'Phone', 'Birthday'])

def save_user(email, password, phone, birthday):
    users = load_users()
    users = users.append({'Email': email, 'Password': password, 'Phone': phone, 'Birthday': birthday}, ignore_index=True)
    users.to_csv('users.csv', index=False)

# Fungsi untuk load session
def load_session():
    if os.path.exists('session.txt'):
        with open('session.txt', 'r') as f:
            return f.read().strip()
    return None

def save_session(email):
    with open('session.txt', 'w') as f:
        f.write(email)

def clear_session():
    if os.path.exists('session.txt'):
        os.remove('session.txt')

# Fungsi untuk load daftar hotel
def load_hotels():
    try:
        if os.path.exists('daftar_hotel_solo.csv'):
            hotels = pd.read_csv('daftar_hotel_solo.csv', on_bad_lines='skip')
            hotels.columns = hotels.columns.str.strip()
            return hotels
        else:
            messagebox.showerror("Error", "File CSV 'daftar_hotel_solo.csv' tidak ditemukan.")
            return None
    except FileNotFoundError:
        messagebox.showerror("Error", "File CSV 'daftar_hotel_solo.csv' tidak ditemukan.")
        return None
    
def load_bookings():
    if os.path.exists('bookings.csv'):
        return pd.read_csv('bookings.csv')
    else:
        return pd.DataFrame(columns=['Email', 'Hotel', 'Date', 'Room'])
    
def save_booking(email, hotel_name, date, room_type, payment_method):
    bookings = load_bookings()
    new_booking = pd.DataFrame({'Email': [email], 'Hotel': [hotel_name], 'Date': [date], 'Room': [room_type],'Payment': [payment_method]})
    bookings = pd.concat([bookings, new_booking], ignore_index=True)
    bookings.to_csv('bookings.csv', index=False, mode='w', header=True)
    
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

def hotel_selection_page(main):
    from logout import logout
    clear_frame(main)

    # Load background image
    try:
        bg_image = Image.open("pilih hotel.png")
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image 'pilih hotel.png' not found.")
        return

    # Background label
    background_label = tk.Label(main, image=bg_photo)
    background_label.image = bg_photo  # Simpan referensi agar tidak terhapus garbage collector
    background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Frame utama
    main_frame = tk.Frame(main, bg="white", bd=5)
    main_frame.place(relx=0.55, rely=0.5, anchor="center", relwidth=0.35, relheight=0.4)

    # Canvas untuk daftar hotel
    canvas = tk.Canvas(main_frame, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar vertikal
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Konfigurasi canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    

    # Frame di dalam canvas untuk konten hotel
    hotel_list_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=hotel_list_frame, anchor="nw")

    # Header
    tk.Label(hotel_list_frame, text="Pilih Hotel", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
    
    hotels = load_hotels()
    if hotels is None or hotels.empty:
        messagebox.showerror("Error", "Tidak ada hotel yang tersedia.")
        return
    
    for index, row in hotels.iterrows():
        hotel_info = f"{row['Nama Hotel']} - Rating: {row['Rating']} - {row['Alamat']}"
        hotel_button = tk.Button(
            hotel_list_frame,
            text=hotel_info,
            font=("Arial", 12),
            command=lambda i=index: book_hotel(hotels, i, main),
            bg="#f0f0f0",
            fg="#333333"
        )
        hotel_button.pack(pady=5)
    
     # Tambahkan tombol Logout di bagian bawah
    logout_button = tk.Button(
        hotel_list_frame,
        text="Logout",
        font=("Arial", 14),
        bg="red",
        fg="white",
        command=lambda: logout(main)
    )
    logout_button.pack(pady=20)
    
# Fungsi untuk membersihkan frame
def clear_frame(main):
    for widget in main.winfo_children():
        widget.destroy()

