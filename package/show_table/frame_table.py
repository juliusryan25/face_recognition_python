from package import *

def show_dataframe(conn):
    # Membuat jendela utama
    root = tk.Tk()
    root.title("Rekap Kehadiran Karyawan")

    # Membuat frame untuk Treeview
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Membuat Treeview
    tree = ttk.Treeview(frame, columns=('No', 'Nama Karyawan', 'Jam Masuk'), show='headings')

    # Menentukan judul untuk setiap kolom
    tree.heading('No', text='No')
    tree.heading('Nama Karyawan', text='Nama Karyawan')
    tree.heading('Jam Masuk', text='Jam Masuk')

    # Mengambil data kehadiran dari database
    attendance_data = fetch_data(conn)

    # Menambahkan data ke dalam Treeview
    for index, employee in enumerate(attendance_data, start=1):
        jam_masuk = employee[1].strftime("%H:%M")
        tree.insert('', 'end', values=(index, employee[0], jam_masuk))

    # Mengatur ukuran kolom
    tree.column('No', width=40, anchor='center')
    tree.column('Nama Karyawan', width=120)
    tree.column('Jam Masuk', width=100)

    # Menempatkan Treeview ke dalam frame
    tree.pack()

    # Menjalankan aplikasi
    root.mainloop()