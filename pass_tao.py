import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tạo Mật Khẩu Ngẫu Nhiên")
        
        self.passwords_file = 'passwords.json'
        self.saved_passwords = self.load_passwords()
        
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack()
        
        app_frame = tk.Frame(main_frame)
        app_frame.pack(pady=5, fill='x')
        
        tk.Label(app_frame, text="Tên ứng dụng:").pack(side='left')
        self.app_entry = tk.Entry(app_frame)
        self.app_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        self.password_var = tk.StringVar()
        self.password_label = tk.Label(main_frame, textvariable=self.password_var, 
                                     font=('Courier', 14), relief='sunken', width=20)
        self.password_label.pack(pady=10)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=5)

        generate_btn = tk.Button(btn_frame, text="Tạo Mật Khẩu", 
                               command=self.generate_password)
        generate_btn.pack(side='left', padx=5)
        
        copy_btn = tk.Button(btn_frame, text="Copy", command=self.copy_password)
        copy_btn.pack(side='left', padx=5)
        
        save_btn = tk.Button(btn_frame, text="Lưu", command=self.save_password)
        save_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Xóa", command=self.delete_password)
        delete_btn.pack(side='left', padx=5)
        
        self.tree = ttk.Treeview(main_frame, columns=('App', 'Password'), show='headings')
        self.tree.heading('App', text='Ứng dụng')
        self.tree.heading('Password', text='Mật khẩu')
        self.tree.pack(pady=10, fill='both', expand=True)
        self.update_treeview()
        self.tree.bind('<Double-1>', self.load_selected_password)
        
    def generate_password(self):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        length = random.randint(8, 12)
        
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
            
        random.shuffle(password)
        self.password_var.set(''.join(password))
        
    def copy_password(self):
        if self.password_var.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password_var.get())
            messagebox.showinfo("Thông báo", "Đã copy mật khẩu!")
        else:
            messagebox.showwarning("Cảnh báo", "Chưa có mật khẩu để copy!")
            
    def load_passwords(self):
        if os.path.exists(self.passwords_file):
            try:
                with open(self.passwords_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
        
    def save_password(self):
        app_name = self.app_entry.get().strip()
        password = self.password_var.get()
        
        if not app_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên ứng dụng!")
            return
        if not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo mật khẩu trước!")
            return
            
        self.saved_passwords[app_name] = password
        
        with open(self.passwords_file, 'w') as f:
            json.dump(self.saved_passwords, f)
            
        self.update_treeview()
        messagebox.showinfo("Thông báo", "Đã lưu mật khẩu!")

    def delete_password(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn mật khẩu cần xóa!")
            return
            
        app = self.tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa mật khẩu cho {app}?"):
            del self.saved_passwords[app]
            
            with open(self.passwords_file, 'w') as f:
                json.dump(self.saved_passwords, f)
                
            self.update_treeview()
            self.app_entry.delete(0, tk.END)
            self.password_var.set('')
            messagebox.showinfo("Thông báo", "Đã xóa mật khẩu!")
        
    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for app, password in self.saved_passwords.items():
            self.tree.insert('', 'end', values=(app, password))
            
    def load_selected_password(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        app, password = self.tree.item(selected_item[0])['values']
        self.app_entry.delete(0, tk.END)
        self.app_entry.insert(0, app)
        self.password_var.set(password)

if __name__ == '__main__':
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
