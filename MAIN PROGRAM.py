import tkinter as tk
from login import login_with_session
from hotel import hotel_selection_page, book_hotel, load_hotels
from booking import send_booking_confirmation, save_booking
from akhir import clear_frame

# Program utama
def main():
    window = tk.Tk()
    window.title("Hotel Booking System")
    window.geometry("1000x600")
    window.email = None

    login_with_session(window)

    window.mainloop()

if __name__ == "__main__":
    main()
