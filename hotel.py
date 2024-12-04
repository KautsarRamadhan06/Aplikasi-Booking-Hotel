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
    
def hotel_selection_page(main):
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


def book_hotel(hotels, index, main):
    from akhir import clear_frame
    clear_frame(main)
    
    hotel_name = hotels.iloc[index]['Nama Hotel']
    address = hotels.iloc[index]['Alamat']
    rating = hotels.iloc[index]['Rating']
    phone = hotels.iloc[index]['Nomor Telepon']
    priceSingle = hotels.iloc[index]['Single']
    priceDouble = hotels.iloc[index]['Double']

    booking_date = tk.StringVar()
    room_type = tk.StringVar()
    payment_method = tk.StringVar()

    tk.Label(main, text=f"Hotel: {hotel_name}", font=("Arial", 20)).pack(pady=10)
    tk.Label(main, text=f"Alamat: {address}", font=("Arial", 14)).pack(pady=5)
    tk.Label(main, text=f"Rating: {rating}", font=("Arial", 14)).pack(pady=5)
    tk.Label(main, text=f"Telepon: {phone}", font=("Arial", 14)).pack(pady=5)

    def select_date():
        date_window = tk.Toplevel(main)
        date_window.title("Pilih Tanggal")
        calendar = Calendar(date_window, selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False)
        calendar.pack(pady=20)

        def confirm_date():
            booking_date.set(calendar.get_date())
            date_window.destroy()

        confirm_button = tk.Button(date_window, text="Pilih", command=confirm_date)
        confirm_button.pack(pady=10)

    select_date_button = tk.Button(main, text="Pilih Tanggal Booking", command=select_date)
    select_date_button.pack(pady=20)

    tk.Label(main, text="Tipe Kamar:", font=("Arial", 14)).pack(pady=10)
    room_type.set("Single")
    tk.Radiobutton(main, text=f"Single (Rp {priceSingle})", variable=room_type, value="Single", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text=f"Double (Rp {priceDouble})", variable=room_type, value="Double", font=("Arial", 12)).pack()
    
    tk.Label(main, text="Pilih Metode Pembayaran:", font=("Arial", 14)).pack(pady=10)
    payment_method.set("Transfer Bank")
    tk.Radiobutton(main, text="Transfer Bank", variable=payment_method, value="Transfer Bank", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text="Kartu Kredit", variable=payment_method, value="Kartu Kredit", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text="Bayar di Tempat", variable=payment_method, value="Bayar di Tempat", font=("Arial", 12)).pack()

    def on_book():
        selected_date = booking_date.get()
        selected_payment = payment_method.get()
        if not selected_date:
            messagebox.showerror("Error", "Harap pilih tanggal booking!")
            return

        # Validasi tanggal
        try:
            datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Format tanggal salah!")
            return
        
        # Logika tambahan untuk metode pembayaran
        if selected_payment == "Transfer Bank":
            messagebox.showinfo("Instruksi", "Silakan transfer ke rekening berikut:\n\nBank: BNI\nNo. Rekening: 1814241787\nAtas Nama: Hotel Booking")
        elif selected_payment == "Kartu Kredit":
            messagebox.showinfo("Instruksi", "Pembayaran melalui kartu kredit akan diproses secara otomatis.")
        else:
            messagebox.showinfo("Instruksi", "Silakan selesaikan pembayaran di lokasi.")

        # Simpan data booking
        save_booking(main.email, hotel_name, selected_date, room_type.get(),selected_payment)
        
        # Kirim email konfirmasi
        price = priceSingle if room_type.get() == "Single" else priceDouble
        email_sent = send_booking_confirmation(
            main.email, hotel_name, selected_date, room_type.get(), price, selected_payment
        )

        if email_sent:
            messagebox.showinfo("Sukses", f"Pemesanan berhasil! Email konfirmasi dikirim ke {main.email}.")
            thank_you_page(main)
        else:
            messagebox.showerror("Error", "Gagal mengirim email konfirmasi.")
            hotel_selection_page(main)

    book_button = tk.Button(main, text="Booking", font=("Arial", 14), bg="green", fg="white", command=on_book)
    book_button.pack(pady=20)

    back_button = tk.Button(main, text="Kembali", font=("Arial", 14), command=lambda: hotel_selection_page(main))
    back_button.pack(pady=10)

def thank_you_page(main):
    from akhir import clear_frame
    from login import login_page
    clear_frame(main)  # Bersihkan frame sebelumnya

    # Buat label terima kasih
    tk.Label(main, text="Terima Kasih!", font=("Arial", 24, "bold"), fg="green").pack(pady=20)
    tk.Label(main, text="Pemesanan Anda telah berhasil.", font=("Arial", 16)).pack(pady=10)
    tk.Label(main, text="Email konfirmasi telah dikirim.", font=("Arial", 14)).pack(pady=5)
        
    # Tombol untuk kembali ke halaman awal
    tk.Button(main, text="Kembali ke Halaman Utama", font=("Arial", 14), command=lambda: login_page(main)).pack(pady=20)   

