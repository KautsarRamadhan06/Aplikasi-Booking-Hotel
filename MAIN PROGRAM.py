import tkinter as tk
from login import login_page
from hotel import hotel_selection_page
from akhir import clear_frame

# Program utama
def main_program():
    main= tk.Tk()
    main.title("Hotel Booking System")
    main.geometry("1000x600")
    main.email = None  # Tambahkan properti `email` pada objek `window` untuk menyimpan email pengguna.

    # Panggil halaman login dengan parameter default (sesuai implementasi `login_with_session`).
    login_page(main)

    # Jalankan loop utama aplikasi
    main.mainloop()

if __name__ == "__main__":
    main_program()
