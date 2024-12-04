import tkinter as tk
from tkinter import messagebox
from akhir import load_users, save_user, load_session, save_session, clear_session
from hotel import hotel_selection_page
from akhir import clear_frame


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
    from PIL import Image,ImageTk
    clear_frame(main)

    # Canvas untuk background
    canvas = tk.Canvas(main, width=1000, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Muat gambar JPG untuk background
    try:
        bg_image = Image.open("login awal.png")  # Pastikan file "background.jpg" ada di folder proyek
        # Ganti bagian resize
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Ubah ukuran sesuai jendela
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    except FileNotFoundError:
        messagebox.showerror("Error", "File login awal.png tidak ditemukan.")
        return
    
    # Frame untuk elemen login
    login_frame = tk.Frame(main, bg="white", bd=5)
    login_frame.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.4)  # Posisikan di tengah

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
    register_button = tk.Button(login_frame, text="Don't have an account? Register", font=("Arial", 12), bg="green", fg="white", command=lambda: registration_page(main))
    register_button.pack(pady=10)
    

# Halaman Registrasi
def registration_page(main):
    clear_frame(main)

    # Main registration frame
    reg_frame = tk.Frame(main)
    reg_frame.pack(pady=50)

    # Email field with label
    email_frame = tk.Frame(reg_frame)
    email_frame.pack(pady=10, anchor="w")
    tk.Label(email_frame, text="Email:", font=("Arial", 14)).pack(anchor="w")
    email_entry = tk.Entry(email_frame, font=("Arial", 14))
    email_entry.pack(anchor="w")

    # Password field with label
    password_frame = tk.Frame(reg_frame)
    password_frame.pack(pady=10, anchor="w")
    tk.Label(password_frame, text="Password:", font=("Arial", 14)).pack(anchor="w")
    password_entry = tk.Entry(password_frame, font=("Arial", 14), show="*")
    password_entry.pack(anchor="w")

    # Confirm Password field with label
    confirm_password_frame = tk.Frame(reg_frame)
    confirm_password_frame.pack(pady=10, anchor="w")
    tk.Label(confirm_password_frame, text="Confirm Password:", font=("Arial", 14)).pack(anchor="w")
    confirm_password_entry = tk.Entry(confirm_password_frame, font=("Arial", 14), show="*")
    confirm_password_entry.pack(anchor="w")

    # Phone Number field with label
    phone_frame = tk.Frame(reg_frame)
    phone_frame.pack(pady=10, anchor="w")
    tk.Label(phone_frame, text="Phone Number:", font=("Arial", 14)).pack(anchor="w")
    phone_entry = tk.Entry(phone_frame, font=("Arial", 14))
    phone_entry.pack(anchor="w")

    # Birthday field with label
    birthday_frame = tk.Frame(reg_frame)
    birthday_frame.pack(pady=10, anchor="w")
    tk.Label(birthday_frame, text="Birthday (yyyy-mm-dd):", font=("Arial", 14)).pack(anchor="w")
    birthday_entry = tk.Entry(birthday_frame, font=("Arial", 14))
    birthday_entry.pack(anchor="w")

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
    
    back_button = tk.Button(main, text="Kembali", font=("Arial", 14), command=lambda: login_page(main))
    back_button.pack(pady=10)

# Fungsi logout
def logout(main):
    if messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?"):
        main.email = None
        clear_session()
        login_page(main)
