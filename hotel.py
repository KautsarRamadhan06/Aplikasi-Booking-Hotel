import tkinter as tk
import pandas as pd
import os
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from booking import save_booking, send_booking_confirmation
from PIL import Image, ImageTk

SESSION_FILE = 'session.txt'

# Halaman Pemilihan Hotel
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
    
def hotel_selection_page(main,priceSingle, priceDouble, room_type, payment_method):
   
    # Implementasi halaman pemilihan hotel
    frame = tk.Frame(main)
    frame.pack(fill="both", expand=True)
    tk.Label(frame, text="Welcome to the Hotel Booking Page!", font=("Arial", 20)).pack(pady=20)

    # Contoh tombol untuk logika lebih lanjut
    tk.Button(frame, text="Choose Room", command=lambda: print("Room Selection")).pack(pady=10)

    from akhir import clear_frame
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

    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.config(bg="white", activebackground="white", troughcolor="white")  # Ganti warna
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
            command=lambda i=index: book_hotel(hotels, i, main,priceSingle, priceDouble, room_type, payment_method),
            bg="#f0f0f0",
            fg="#333333"
        )
        hotel_button.pack(pady=5)
        
# Tambahkan tombol Logout di bagian bawah
    logout_button = tk.Button(main,text="Logout",font=("Arial", 14),bg="red",fg="white",command=lambda: logout(main))
    logout_button.place(x=1000, y=750, width=100, height=40)
    
    
from tkinter import messagebox
import pandas as pd

# Fungsi logout
def logout(main):
    from login import login_page
    if messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?"):
        main.email = None
        clear_session()  
        login_page(main)# Fungsi untuk membersihkan sesi pengguna
        # Navigasi ke halaman login

# Fungsi untuk menampilkan daftar hotel
def display_hotel_list(main, hotel_list_frame):
    hotels = load_hotels()  # Fungsi untuk memuat data hotel
    if hotels is None or hotels.empty:
        messagebox.showerror("Error", "Tidak ada hotel yang tersedia.")
        return
    
    # Hapus elemen yang ada di frame (jika perlu refresh)
    for widget in hotel_list_frame.winfo_children():
        widget.destroy()

    # Tambahkan daftar hotel
    for index, row in hotels.iterrows():
        hotel_info = f"{row['Nama Hotel']} - Rating: {row['Rating']} - {row['Alamat']}"
        hotel_button = tk.Button(
            hotel_list_frame,
            text=hotel_info,
            font=("Arial", 12),
            command=lambda i=index: book_hotel(hotels, i, main),  # Fungsi untuk memesan hotel
            bg="#f0f0f0",
            fg="#333333"
        )
        hotel_button.pack(pady=5)
    
# Fungsi untuk menghapus sesi pengguna
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


def book_hotel(hotels, index, main, priceSingle, priceDouble, room_type, payment_method):
    from akhir import clear_frame
    from booking import show_booking_form
    clear_frame(main)

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

    # Informasi hotel
    hotel_name = hotels.iloc[index]['Nama Hotel']
    address = hotels.iloc[index]['Alamat']
    rating = hotels.iloc[index]['Rating']
    phone = hotels.iloc[index]['Nomor Telepon']
    priceSingle = hotels.iloc[index]['Single']
    priceDouble = hotels.iloc[index]['Double']

    # Frame utama untuk semua elemen
    main_frame = tk.Frame(main, bg="white")
    main_frame.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.5, relheight=0.7)

    # Informasi hotel di dalam frame utama
    tk.Label(
        main_frame,
        text=f"Hotel: {hotel_name}",
        font=("Arial", 24, "bold"),
        bg="white",
        fg="#333333"
    ).pack(pady=10)

    tk.Label(
        main_frame,
        text=f"Alamat: {address}",
        font=("Arial", 16),
        bg="white",
        fg="#555555"
    ).pack(pady=5)

    tk.Label(
        main_frame,
        text=f"Rating: {rating}",
        font=("Arial", 16),
        bg="white",
        fg="#555555"
    ).pack(pady=5)

    tk.Label(
        main_frame,
        text=f"Telepon: {phone}",
        font=("Arial", 16),
        bg="white",
        fg="#555555"
    ).pack(pady=5)

    # Pemilihan tanggal booking
    tk.Label(main_frame, text="Pilih Tanggal Booking:", font=("Arial", 16), bg="white").pack(pady=10)
    booking_date = tk.StringVar()
    calendar = Calendar(main_frame, selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False)
    calendar.pack(pady=10)
    # Tombol untuk konfirmasi dan kembali
    tk.Button(
        main_frame,
        text="Pilih",
        font=("Arial", 14),
        bg="green",
        fg="white",
        # Callback untuk memanggil show_booking_form saat tombol diklik
        command=lambda: show_booking_form(
            main, booking_date, hotel_name, address, rating, phone, priceSingle, priceDouble
        )
    ).pack(pady=10)

    tk.Button(
        main_frame,
        text="Kembali",
        font=("Arial", 14),
        bg="red",
        fg="white",
        # Callback untuk kembali ke halaman pemilihan hotel
        command=lambda: hotel_selection_page(main,priceSingle, priceDouble, room_type,payment_method)
    ).pack(pady=10)

def confirm_date(calendar, booking_date):
    from booking import show_booking_form
    # Ambil tanggal dari kalender dan simpan ke booking_date
    booking_date.set(calendar.get_date())
    messagebox.showinfo("Konfirmasi", f"Tanggal yang dipilih: {booking_date.get()}")
