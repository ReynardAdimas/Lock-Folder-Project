import tkinter as tk
from tkinter import messagebox, filedialog
from auth import init_config, verify_password
from locker import (
    add_folder, remove_folder,
    lock_all, unlock_all,
    get_folders
)

# ===== INIT CONFIG =====
init_config()

# ===== GUI =====
root = tk.Tk()
root.title("Folder Lock App")
root.geometry("450x350")

# ===== LOGIN =====
login_frame = tk.Frame(root)
login_frame.pack(pady=60)

tk.Label(login_frame, text="Masukkan Password").pack()
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)

def login():
    if verify_password(password_entry.get()):
        login_frame.pack_forget()
        dashboard.pack()
        refresh_list()
    else:
        messagebox.showerror("Error", "Password salah!")

tk.Button(login_frame, text="Login", command=login).pack(pady=10)

# ===== DASHBOARD =====
dashboard = tk.Frame(root)

listbox = tk.Listbox(dashboard, width=60)
listbox.pack(pady=10)

def refresh_list():
    listbox.delete(0, tk.END)
    for folder in get_folders():
        listbox.insert(tk.END, folder)

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        add_folder(folder)
        refresh_list()

def delete_folder():
    selected = listbox.curselection()
    if selected:
        remove_folder(listbox.get(selected[0]))
        refresh_list()

tk.Button(dashboard, text="Tambah Folder", command=choose_folder).pack(pady=3)
tk.Button(dashboard, text="Hapus Folder", command=delete_folder).pack(pady=3)
tk.Button(dashboard, text="Lock Semua Folder", command=lock_all).pack(pady=3)
tk.Button(dashboard, text="Unlock Semua Folder", command=unlock_all).pack(pady=3)

# ===== AUTO LOCK ON CLOSE =====
def on_close():
    lock_all()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

