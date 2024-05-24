from package import *
from screeninfo import get_monitors

def show_binary_image_pulang(binary_data):
    # Konversi data biner ke objek image
    image_data = BytesIO(binary_data)
    image = Image.open(image_data)

    # Perbesar gambar (misalnya, menjadi 2 kali ukuran aslinya)
    width, height = image.size
    new_width = width * 3
    new_height = height * 3
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Buat jendela pop-up untuk menampilkan gambar
    root = tk.Tk()
    tk_image = ImageTk.PhotoImage(image)
    tk.Label(root, image=tk_image).pack()

    monitors = get_monitors()
    if len(monitors) > 1:
        # Mengatur ukuran dan posisi jendela sesuai dengan ukuran gambar yang di-resize dan monitor kedua
        root.geometry(f"{new_width}x{new_height}+{monitors[1].x}+{monitors[1].y}")
    else:
        # Jika hanya ada satu monitor, tampilkan di tengah
        root.geometry(f"{new_width}x{new_height}+0+0")
    
    # Atur timer untuk menutup jendela setelah 1000 milidetik (1 detik)
    root.after(1500, root.destroy)

    # Jalankan loop utama tkinter
    root.mainloop()

def get_binary_data_from_database_pulang():
    # ... kode untuk mengambil data biner dari database ...
    cur = conn.cursor()
    cur.execute("SELECT foto_absen FROM data_absen_pulang ORDER BY id DESC LIMIT 1")
    binary_data_pulang = cur.fetchone()[0]
    
    return binary_data_pulang