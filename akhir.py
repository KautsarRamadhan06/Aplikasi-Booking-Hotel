import pandas as pd
import os
import tkinter as tk
import smtplib

from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# Fungsi untuk membersihkan frame
def clear_frame(main):
    for widget in main.winfo_children():
        widget.destroy()

