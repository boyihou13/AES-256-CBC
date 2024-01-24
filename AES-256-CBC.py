import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as assymetric_padding
from cryptography.hazmat.backends import default_backend
import os
from PIL import Image, ImageTk
import base64
import io


def encrypt_or_decrypt():
    try:
        # 從文件中讀取金鑰
        with open(key_filename.get(), 'rb') as f:
            key = f.read()

        # 從輸入框讀取密碼，用 SHA-256 生成雜湊，然後取雜湊的前8位和後8位作為 IV
        password = password_input.get().encode()
        hash_value = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_value.update(password)
        hashed_password = hash_value.finalize()
        iv = hashed_password[:8] + hashed_password[-8:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        # 從文件中讀取要加密或解密的數據
        with open(input_filename.get(), 'rb') as f:
            input_data = f.read()

        if v.get() == 'encrypt':
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(input_data) + padder.finalize()
            output_data = encryptor.update(padded_data) + encryptor.finalize()
        else:
            decryptor = cipher.decryptor()
            output_data = decryptor.update(input_data) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            output_data = unpadder.update(output_data) + unpadder.finalize()

        # 將輸出數據保存到文件
        with open(output_filename.get(), 'wb') as f:
            f.write(output_data)

        messagebox.showinfo("信息", "操作成功!")
    except Exception as e:
        messagebox.showerror("錯誤", f"操作失敗，原因：{str(e)}")

def select_file(var):
    filename = filedialog.askopenfilename()
    var.set(filename)

def select_output_file(var):
    filename = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[('All Files', '*.*'), ('Text Files', '*.txt'), ('PDF Files', '*.pdf'), ('PNG Files', '*.png'), ('JPG Files', '*.jpg'), ('MP4 Files', '*.mp4'), ('WAV Files', '*.wav'), ('Zip Files', '*.zip')])
    var.set(filename)

window = tk.Tk()
window.title("AES-256-CBC 文件加密/解密")
window.geometry('400x700')  # Set window size
window.configure(bg='white')  # Set background color

icon_data = "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"
icon_image = Image.open(io.BytesIO(base64.b64decode(icon_data)))
icon_photo = ImageTk.PhotoImage(icon_image)
window.tk.call('wm', 'iconphoto', window._w, icon_photo)


input_filename = tk.StringVar()
output_filename = tk.StringVar()
key_filename = tk.StringVar()
password_input = tk.StringVar()
v = tk.StringVar(value="")

style = ('Helvetica', 16, 'bold')
style01 = ('Helvetica', 20, 'bold')

tk.Label(window, text="AES-256-CBC", bg='white', font=style01).pack(pady=5)
tk.Label(window, text="", bg='white').pack(pady=1)

tk.Label(window, text="輸入文件:", bg='white', font=style).pack(pady=1)
tk.Entry(window, textvariable=input_filename, font=style).pack(pady=1)
# 選擇文件
tk.Button(window, text="選擇文件", command=lambda: select_file(input_filename), font=style).pack(pady=1)
tk.Label(window, text="", bg='white').pack(pady=1)

tk.Label(window, text="輸出文件:", bg='white', font=style).pack(pady=1)
tk.Entry(window, textvariable=output_filename, font=style).pack(pady=1)
tk.Button(window, text="選擇文件", command=lambda: select_output_file(output_filename), font=style).pack(pady=1)
tk.Label(window, text="", bg='white').pack(pady=1)

tk.Label(window, text="金鑰文件:", bg='white', font=style).pack(pady=1)
tk.Entry(window, textvariable=key_filename, font=style).pack(pady=1)
tk.Button(window, text="選擇文件", command=lambda: select_file(key_filename), font=style).pack(pady=1)
tk.Label(window, text="", bg='white').pack(pady=1)

tk.Label(window, text="輸入密碼:", bg='white', font=style).pack(pady=1)
tk.Entry(window, textvariable=password_input, show="*", font=style).pack(pady=1)
tk.Label(window, text="", bg='white').pack(pady=1)

tk.Radiobutton(window, text="加密", variable=v, value='encrypt', bg='white', font=style).pack(pady=1)
tk.Radiobutton(window, text="解密", variable=v, value='decrypt', bg='white', font=style).pack(pady=1)

tk.Button(window, text="提交", command=encrypt_or_decrypt, font=style).pack(pady=1)

window.mainloop()

