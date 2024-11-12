
import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, nama, tgl_lahir, email, password, no_telepon):
        self.nama = nama
        self.tgl_lahir = tgl_lahir
        self.email = email
        self.password = password
        self.no_telepon = no_telepon

class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Booking Hotel")
        self.users = {}
        self.current_user = None
        self.create_login_screen()

    def create_login_screen(self):
        # Frame Login
        self.clear_screen()
        tk.Label(self.root, text="Masukkan Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Label(self.root, text="Masukkan Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Registrasi", command=self.create_register_screen).pack()

    def create_register_screen(self):
        # Frame Registrasi
        self.clear_screen()
        tk.Label(self.root, text="Nama:").pack()
        self.nama_entry = tk.Entry(self.root)
        self.nama_entry.pack()

        tk.Label(self.root, text="Tanggal Lahir (YYYY-MM-DD):").pack()
        self.tgl_lahir_entry = tk.Entry(self.root)
        self.tgl_lahir_entry.pack()

        tk.Label(self.root, text="Email:").pack()
        self.reg_email_entry = tk.Entry(self.root)
        self.reg_email_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.pack()

        tk.Label(self.root, text="Nomor Telepon:").pack()
        self.no_telepon_entry = tk.Entry(self.root)
        self.no_telepon_entry.pack()

        tk.Button(self.root, text="Daftar", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Kembali ke Login", command=self.create_login_screen).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def register(self):
        nama = self.nama_entry.get()
        tgl_lahir = self.tgl_lahir_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        no_telepon = self.no_telepon_entry.get()

        if email in self.users:
            messagebox.showerror("Error", "Email sudah terdaftar. Silakan masuk.")
            return

        new_user = User(nama, tgl_lahir, email, password, no_telepon)
        self.users[email] = new_user
        messagebox.showinfo("Sukses", "Registrasi berhasil!")
        self.create_login_screen()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in self.users and self.users[email].password == password:
            self.current_user = self.users[email]
            messagebox.showinfo("Sukses", "Login berhasil!")
            self.create_booking_screen()
        else:
            messagebox.showerror("Error", "Email atau Password salah.")

    def create_booking_screen(self):
        # Frame Booking
        self.clear_screen()
        tk.Label(self.root, text="Pilih Nama Hotel:").pack()
        self.hotel_entry = tk.Entry(self.root)
        self.hotel_entry.pack()

        tk.Label(self.root, text="Tanggal Booking (YYYY-MM-DD):").pack()
        self.tanggal_entry = tk.Entry(self.root)
        self.tanggal_entry.pack()

        tk.Button(self.root, text="Kirim Booking", command=self.send_booking_code).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.create_login_screen).pack()

    def send_booking_code(self):
        hotel = self.hotel_entry.get()
        tanggal = self.tanggal_entry.get()
        email = self.current_user.email

        messagebox.showinfo("Sukses", f"Kode booking untuk hotel '{hotel}' pada tanggal '{tanggal}' telah dikirim ke email {email}.")

# Menjalankan aplikasi
root = tk.Tk()
app = BookingApp(root)
root.mainloop()

