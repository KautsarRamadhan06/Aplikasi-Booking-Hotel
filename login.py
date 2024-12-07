import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from akhir import clear_frame,load_users,save_session
from hotel import hotel_selection_page

def login_with_session(main, priceSingle, priceDouble, room_type, payment_method):
    print(f"Price Single: {priceSingle}")
    print(f"Price Double: {priceDouble}")
    print(f"Room Type: {room_type}")
    print(f"Payment Method: {payment_method}")
    
    from akhir import load_session
    session_email = load_session()
    if session_email:
        users = load_users()
        user = users[users['Email'] == session_email]
        if not user.empty:
            main.email = session_email  # Ganti main dengan window
            hotel_selection_page(main, priceSingle, priceDouble, room_type, payment_method)  # Ganti main dengan window
            return
    login_page(main)  # Ganti main dengan window


import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk  # Make sure Pillow is installed (`pip install Pillow`)

# Assuming load_users and save_session are defined elsewhere in your code
# from your_users_module import load_users, save_session
from hotel import hotel_selection_page

def login_page(main):
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
            users = load_users()  # Assuming this function is implemented to load user data
            user = users[users['Email'] == email]
            if user.empty:
                messagebox.showerror("Error", "Email belum terdaftar")
            elif user.iloc[0]['Password'] != password:
                messagebox.showerror("Error", "Password salah")
            else:
                main.email = email
                save_session(email)  # Assuming this function saves the session
                hotel_selection_page(main,priceSingle=0, priceDouble=0, room_type=None,payment_method=None)  # Redirect to hotel selection page

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
        command=lambda: registration_page(main)  # Assuming registration_page is defined elsewhere
    )
    register_button.pack(pady=10)

    
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def registration_page(main):
    clear_frame(main)

    reg_frame = tk.Frame(main)
    reg_frame.pack(pady=50)

    tk.Label(reg_frame, text="Registration Page", font=("Arial", 16)).pack(pady=10)

    email_frame = tk.Frame(reg_frame)
    email_frame.pack(pady=10, anchor="w")
    tk.Label(email_frame, text="Email:", font=("Arial", 14)).pack(anchor="w")
    email_entry = tk.Entry(email_frame, font=("Arial", 14))
    email_entry.pack(anchor="w")

    password_frame = tk.Frame(reg_frame)
    password_frame.pack(pady=10, anchor="w")
    tk.Label(password_frame, text="Password:", font=("Arial", 14)).pack(anchor="w")
    password_entry = tk.Entry(password_frame, font=("Arial", 14), show="*")
    password_entry.pack(anchor="w")

    confirm_password_frame = tk.Frame(reg_frame)
    confirm_password_frame.pack(pady=10, anchor="w")
    tk.Label(confirm_password_frame, text="Confirm Password:", font=("Arial", 14)).pack(anchor="w")
    confirm_password_entry = tk.Entry(confirm_password_frame, font=("Arial", 14), show="*")
    confirm_password_entry.pack(anchor="w")

    phone_frame = tk.Frame(reg_frame)
    phone_frame.pack(pady=10, anchor="w")
    tk.Label(phone_frame, text="Phone Number:", font=("Arial", 14)).pack(anchor="w")
    phone_entry = tk.Entry(phone_frame, font=("Arial", 14))
    phone_entry.pack(anchor="w")

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
            messagebox.showinfo("Success", "Registrasi berhasil")
            
        clear_frame(main)
        # Kembali ke halaman login
        login_page(main)


    reg_button = tk.Button(reg_frame, text="Register", font=("Arial", 14), command=on_register)
    reg_button.pack(pady=20)
    
# root = tk.Tk()
# root.geometry("400x500")
# main = tk.Frame(root)
# main.pack(fill="both", expand=True)

# registration_page(main)
# root.mainloop()