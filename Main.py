import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import pandas as pd
import os

SESSION_FILE = 'session.txt'

# Fungsi untuk memuat hotel dari file CSV
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

# Fungsi untuk memuat data pengguna dari file CSV
def load_users():
    if os.path.exists('users.csv'):
        return pd.read_csv('users.csv')
    else:
        return pd.DataFrame(columns=['Email', 'Password', 'Phone', 'Birthday'])

# Fungsi untuk menyimpan pengguna ke file CSV
def save_user(email, password, phone, birthday):
    users = load_users()
    if users.empty:
        users = pd.DataFrame(columns=['Email', 'Password', 'Phone', 'Birthday'])

    new_user = pd.DataFrame({'Email': [email], 'Password': [password], 'Phone': [phone], 'Birthday': [birthday]})
    users = pd.concat([users, new_user], ignore_index=True)

    users.to_csv('users.csv', index=False, mode='w', header=True)

# Fungsi untuk memuat riwayat pemesanan
def load_bookings():
    if os.path.exists('bookings.csv'):
        return pd.read_csv('bookings.csv')
    else:
        return pd.DataFrame(columns=['Email', 'Hotel', 'Date', 'Room'])

# Fungsi untuk menyimpan riwayat pemesanan
def save_booking(email, hotel_name, date, room_type):
    bookings = load_bookings()
    new_booking = pd.DataFrame({'Email': [email], 'Hotel': [hotel_name], 'Date': [date], 'Room': [room_type]})
    bookings = pd.concat([bookings, new_booking], ignore_index=True)
    bookings.to_csv('bookings.csv', index=False, mode='w', header=True)

# Fungsi untuk menyimpan sesi pengguna
def save_session(email):
    with open(SESSION_FILE, 'w') as f:
        f.write(email)

# Fungsi untuk memuat sesi pengguna
def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return f.read().strip()
    return None

# Fungsi untuk menghapus sesi pengguna
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# Fungsi logout
def logout(main):
    if messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?"):
        main.email = None
        clear_session()
        login_page(main)

# Halaman Registrasi
def registration_page(main):
    clear_frame(main)
    
    reg_frame = tk.Frame(main)
    reg_frame.pack(pady=50)

    tk.Label(reg_frame, text="Email:", font=("Arial", 14)).pack(pady=10)
    tk.Label(reg_frame, text="Password:", font=("Arial", 14)).pack(pady=10)
    tk.Label(reg_frame, text="Confirm Password:", font=("Arial", 14)).pack(pady=10)
    tk.Label(reg_frame, text="Phone Number:", font=("Arial", 14)).pack(pady=10)
    tk.Label(reg_frame, text="Birthday (yyyy-mm-dd):", font=("Arial", 14)).pack(pady=10)

    email_entry = tk.Entry(reg_frame, font=("Arial", 14))
    password_entry = tk.Entry(reg_frame, font=("Arial", 14), show="*")
    confirm_password_entry = tk.Entry(reg_frame, font=("Arial", 14), show="*")
    phone_entry = tk.Entry(reg_frame, font=("Arial", 14))
    birthday_entry = tk.Entry(reg_frame, font=("Arial", 14))

    email_entry.pack(pady=10)
    password_entry.pack(pady=10)
    confirm_password_entry.pack(pady=10)
    phone_entry.pack(pady=10)
    birthday_entry.pack(pady=10)

    def on_register():
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        phone = phone_entry.get()
        birthday = birthday_entry.get()

        if email == "" or password == "" or confirm_password == "" or phone == "" or birthday == "":
            messagebox.showerror("Error", "Harap lengkapi semua kolom")
        elif password != confirm_password:
            messagebox.showerror("Error", "Password dan konfirmasi password tidak cocok")
        else:
            users = load_users()
            if email in users['Email'].values:
                messagebox.showerror("Error", "Email sudah terdaftar")
            else:
                save_user(email, password, phone, birthday)
                messagebox.showinfo("Success", "Registrasi berhasil, silakan login")
                login_page(main)

    reg_button = tk.Button(reg_frame, text="Register", font=("Arial", 14), command=on_register)
    reg_button.pack(pady=20)

# Fungsi login dengan sesi
def login_with_session(main):
    session_email = load_session()
    if session_email:
        users = load_users()
        user = users[users['Email'] == session_email]
        if not user.empty:
            main.email = session_email
            hotel_selection_page(main)
            return
    login_page(main)

# Halaman Login
def login_page(main):
    clear_frame(main)
    
    login_frame = tk.Frame(main)
    login_frame.pack(pady=50)

    tk.Label(login_frame, text="Email:", font=("Arial", 14)).pack(pady=10)
    tk.Label(login_frame, text="Password:", font=("Arial", 14)).pack(pady=10)

    email_entry = tk.Entry(login_frame, font=("Arial", 14))
    password_entry = tk.Entry(login_frame, font=("Arial", 14), show="*")

    email_entry.pack(pady=10)
    password_entry.pack(pady=10)

    def on_login():
        email = email_entry.get()
        password = password_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "Harap masukkan email dan password")
        else:
            users = load_users()
            user = users[users['Email'] == email]
            if user.empty:
                messagebox.showerror("Error", "Email belum terdaftar")
            elif user.iloc[0]['Password'] != password:
                messagebox.showerror("Error", "Password salah")
            else:
                main.email = email
                save_session(email)
                hotel_selection_page(main)

    login_button = tk.Button(login_frame, text="Login", font=("Arial", 14), command=on_login)
    login_button.pack(pady=20)

    register_button = tk.Button(login_frame, text="Don't have an account? Register", font=("Arial", 12), command=lambda: registration_page(main))
    register_button.pack(pady=10)

# Halaman Pemilihan Hotel
def hotel_selection_page(main):
    clear_frame(main)
    
    hotels = load_hotels()
    if hotels is None or hotels.empty:
        messagebox.showerror("Error", "Tidak ada hotel yang tersedia.")
        return

    hotel_frame = tk.Frame(main)
    hotel_frame.pack(pady=50)

    tk.Label(hotel_frame, text="Pilih Hotel", font=("Arial", 20)).pack(pady=10)

    for index, row in hotels.iterrows():
        hotel_info = f"{row['Nama Hotel']} - Rating: {row['Rating']} - {row['Alamat']}"
        hotel_button = tk.Button(
            hotel_frame,
            text=hotel_info,
            font=("Arial", 12),
            width=50,
            command=lambda i=index: book_hotel(hotels, i, main)
        )
        hotel_button.pack(pady=5)

    logout_button = tk.Button(hotel_frame, text="Logout", font=("Arial", 14), bg="red", fg="white", command=lambda: logout(main))
    logout_button.pack(pady=20)

# Halaman Pemesanan
def book_hotel(hotels, index, main):
    clear_frame(main)
    
    hotel_name = hotels.iloc[index]['Nama Hotel']
    address = hotels.iloc[index]['Alamat']
    rating = hotels.iloc[index]['Rating']
    phone = hotels.iloc[index]['Nomor Telepon']

    booking_date = tk.StringVar()
    room_type = tk.StringVar()

    def select_date():
        date_window = tk.Toplevel(main)
        date_window.title("Select Booking Date")
        calendar = Calendar(date_window, selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False)
        calendar.pack(pady=20)

        def confirm_date():
            booking_date.set(calendar.get_date())
            date_window.destroy()

        confirm_button = tk.Button(date_window, text="Confirm Date", command=confirm_date)
        confirm_button.pack(pady=10)

    select_date_button = tk.Button(main, text="Select Booking Date", command=select_date)
    select_date_button.pack(pady=20)

    tk.Label(main, text="Room Type:", font=("Arial", 14)).pack(pady=10)
    room_type.set("Single")
    tk.Radiobutton(main, text="Single", variable=room_type, value="Single", font=("Arial", 12)).pack()
    tk.Radiobutton(main, text="Double", variable=room_type, value="Double", font=("Arial", 12)).pack()

    def on_book():
        if booking_date.get() == "":
            messagebox.showerror("Error", "Harap pilih tanggal pemesanan")
        else:
            save_booking(main.email, hotel_name, booking_date.get(), room_type.get())
            messagebox.showinfo("Success", f"Pemesanan untuk {hotel_name} berhasil!")
            hotel_selection_page(main)

    book_button = tk.Button(main, text="Book Now", font=("Arial", 14), command=on_book)
    book_button.pack(pady=20)

# Fungsi untuk membersihkan frame
def clear_frame(main):
    for widget in main.winfo_children():
        widget.destroy()

# Program utama
def main():
    window = tk.Tk()
    window.title("Hotel Booking System")
    window.geometry("600x600")
    window.email = None

    login_with_session(window)

    window.mainloop()

if __name__ == "__main__":
    main()
