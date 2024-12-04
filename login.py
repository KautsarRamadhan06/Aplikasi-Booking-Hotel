import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from akhir import clear_frame,load_users,save_session
from hotel import hotel_selection_page

def login_with_session(main):
    from akhir import load_session
    session_email = load_session()
    if session_email:
        users = load_users()
        user = users[users['Email'] == session_email]
        if not user.empty:
            main.email = session_email
            hotel_selection_page(main)
            return
    login_page(main)
    
def login_page(main):
    # Bersihkan frame utama
    clear_frame(main)

    # Canvas untuk background
    canvas = tk.Canvas(main, width=1000, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Muat gambar JPG untuk background
    try:
        # Pastikan file "login awal.png" ada
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
    login_frame.place(relx=0.7, rely=0.3, relwidth=0.15, relheight=0.3)  # Posisikan di tengah

    # Email field with label
    email_frame = tk.Frame(login_frame, bg="white", width=300, height=100)
    email_frame.pack(pady=10, anchor="s")
    tk.Label(email_frame, text="Email:", font=("Arial", 14), bg="white").pack(anchor="w")
    email_entry = tk.Entry(email_frame, font=("Arial", 14))
    email_entry.pack(anchor="w")

    # Password field with label
    password_frame = tk.Frame(login_frame, bg="white")
    password_frame.pack(pady=10, anchor="s")
    tk.Label(password_frame, text="Password:", font=("Arial", 14), bg="white").pack(anchor="w")
    password_entry = tk.Entry(password_frame, font=("Arial", 14), show="*")
    password_entry.pack(anchor="w")

    # Fungsi login
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

    # Tombol Login
    login_button = tk.Button(login_frame, text="Login", font=("Arial", 14), command=on_login, bg="green", fg="white")
    login_button.pack(pady=20)

    # Tombol Registrasi
    register_button = tk.Button(
        login_frame, 
        text="Don't have an account? Register", 
        font=("Arial", 12), 
        bg="green", 
        fg="white", 
        command=lambda: login_page(main)
    )
    register_button.pack(pady=10)
