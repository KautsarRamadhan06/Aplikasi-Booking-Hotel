import tkinter as tk
from tkinter import ttk, messagebox
from hotel import hotel_selection_page
import os
import csv
import re
from PIL import Image, ImageTk  # Untuk background image

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def load_users():
    import pandas as pd
    if not os.path.exists('users.csv'):
        return pd.DataFrame(columns=['Email', 'Password', 'Phone', 'Birthday'])
    return pd.read_csv('users.csv')

def save_session(email):
    with open('session.txt', 'w') as file:
        file.write(email)

def login_page(main):
    clear_frame(main)  # Pastikan frame utama dibersihkan terlebih dahulu

    # Canvas untuk background
    canvas = tk.Canvas(main, width=1000, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Muat gambar JPG untuk background
    try:
        bg_image_path = "login1.png"  # Sesuaikan path jika gambar ada di folder lain
        if not os.path.exists(bg_image_path):
            raise FileNotFoundError(f"File '{bg_image_path}' tidak ditemukan.")

        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Resize sesuai jendela
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Simpan referensi ke gambar di objek `main`
        main.bg_photo = bg_photo  # Simpan referensi agar gambar tidak hilang
        canvas.create_image(0, 0, image=main.bg_photo, anchor="nw")

    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
        return

    # Frame untuk elemen login
    login_frame = tk.Frame(main, bg="white", bd=5)
    login_frame.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.4)  # Posisikan frame login

    # Email field with label
    tk.Label(login_frame, text="Email:", font=("Arial", 14), bg="white").pack(anchor="w", padx=10, pady=5)
    email_entry = tk.Entry(login_frame, font=("Arial", 14))
    email_entry.pack(fill="x", padx=10)

    # Password field with label
    tk.Label(login_frame, text="Password:", font=("Arial", 14), bg="white").pack(anchor="w", padx=10, pady=5)
    password_entry = tk.Entry(login_frame, font=("Arial", 14), show="*")
    password_entry.pack(fill="x", padx=10)

    # Fungsi login
    def on_login():
        email = email_entry.get()
        password = password_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "Harap masukkan email dan password")
        else:
             users = load_users()  # Assuming this function is implemented to load user data
        user = users[users['Email'] == email]
        if user.empty:
            messagebox.showerror("Error", "Email belum terdaftar")
        elif user.iloc[0]['Password'] != password:
            messagebox.showerror("Error", "Password salah")
        else:
            main.email = email  # Simpan email pengguna
            save_session(email)  # Simpan sesi login pengguna
            clear_frame(main)  # Bersihkan frame utama
            hotel_selection_page(main, priceSingle=0, priceDouble=0, room_type=None, payment_method=None)

    # Tombol Login
    login_button = tk.Button(login_frame, text="Login", font=("Arial", 14), command=on_login, bg="green", fg="white")
    login_button.pack(pady=10)

    # Tombol Registrasi
    register_button = tk.Button(
        login_frame, 
        text="Don't have an account? Register", 
        font=("Arial", 12), 
        bg="green", 
        fg="white", 
        command=lambda: registration_page(main)
    )
    register_button.pack(pady=5)

def registration_page(main):
    clear_frame(main)

    # Buat frame utama untuk registrasi
    reg_frame = ttk.Frame(main, padding="20")
    reg_frame.pack(pady=50)

    # Judul
    ttk.Label(reg_frame, text="Registration Page", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Kolom Email
    ttk.Label(reg_frame, text="Email:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
    email_entry = ttk.Entry(reg_frame, font=("Arial", 14), width=30)
    email_entry.grid(row=1, column=1, pady=5)

    # Kolom Password
    ttk.Label(reg_frame, text="Password:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=5)
    password_entry = ttk.Entry(reg_frame, font=("Arial", 14), width=30, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    # Kolom Konfirmasi Password
    ttk.Label(reg_frame, text="Confirm Password:", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=5)
    confirm_password_entry = ttk.Entry(reg_frame, font=("Arial", 14), width=30, show="*")
    confirm_password_entry.grid(row=3, column=1, pady=5)

    # Kolom Nomor Telepon
    ttk.Label(reg_frame, text="Phone Number:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", pady=5)
    phone_entry = ttk.Entry(reg_frame, font=("Arial", 14), width=30)
    phone_entry.grid(row=4, column=1, pady=5)

    # Kolom Tanggal Lahir
    ttk.Label(reg_frame, text="Birthday (yyyy-mm-dd):", font=("Arial", 14)).grid(row=5, column=0, sticky="w", pady=5)
    birthday_entry = ttk.Entry(reg_frame, font=("Arial", 14), width=30)
    birthday_entry.grid(row=5, column=1, pady=5)

    # Fungsi validasi tanggal lahir
    def validate_birthday():
        birthday = birthday_entry.get()
        if re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", birthday):
            messagebox.showinfo("Valid", "Tanggal lahir valid!")
        else:
            messagebox.showerror("Invalid", "Format tanggal lahir harus yyyy-mm-dd.")

    # Fungsi untuk registrasi
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
        elif not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", birthday):
            messagebox.showerror("Error", "Format tanggal lahir harus yyyy-mm-dd.")
        else:
            file_exists = os.path.isfile('users.csv')
            with open('users.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Email', 'Password', 'Phone', 'Birthday'])
                writer.writerow([email, password, phone, birthday])

            messagebox.showinfo("Success", "Registrasi berhasil")
            login_page(main)  # Panggil kembali halaman login

    # Tombol validasi tanggal lahir
    ttk.Button(reg_frame, text="Validate Birthday", command=validate_birthday).grid(row=6, column=0, pady=10, sticky="w")

    # Tombol registrasi
    ttk.Button(reg_frame, text="Register", command=on_register).grid(row=6, column=1, pady=10, sticky="e")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hotel Booking System")
    root.geometry("1000x600")
    login_page(root)
    root.mainloop()
