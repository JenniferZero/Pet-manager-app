import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pet_manager import PetManager
from user_manager import UserManager
from data_fetcher import DataFetcher


class PetApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Ứng Dụng Quản Lý Thú Cưng")

        self.pet_manager = PetManager()

        self.user_manager = UserManager()

        self.data_fetcher = DataFetcher(self.pet_manager)

        self.current_user = None

        self.show_login_screen()



    def show_login_screen(self):

        self.clear_window()

        login_frame = ttk.LabelFrame(self.root, text="Đăng Nhập")

        login_frame.pack(padx=20, pady=20)



        ttk.Label(login_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.username_entry = ttk.Entry(login_frame)

        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



        ttk.Label(login_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.password_entry = ttk.Entry(login_frame, show="*")

        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



        login_button = ttk.Button(login_frame, text="Đăng Nhập", command=self.login)

        login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)



        register_button = ttk.Button(self.root, text="Đăng Ký", command=self.show_register_screen)

        register_button.pack(pady=5)



    def show_register_screen(self):

        self.clear_window()

        register_frame = ttk.LabelFrame(self.root, text="Đăng Ký")

        register_frame.pack(padx=20, pady=20)



        ttk.Label(register_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.reg_username_entry = ttk.Entry(register_frame)

        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



        ttk.Label(register_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.reg_password_entry = ttk.Entry(register_frame, show="*")

        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



        register_button = ttk.Button(register_frame, text="Đăng Ký", command=self.register)

        register_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)



        back_button = ttk.Button(self.root, text="Quay lại đăng nhập", command=self.show_login_screen)

        back_button.pack(pady=5)



    def login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()

        user = self.user_manager.authenticate_user(username, password)

        if user:

            self.current_user = user

            self.show_main_window()

        else:

            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")



    def register(self):

        username = self.reg_username_entry.get()

        password = self.reg_password_entry.get()

        success, message = self.user_manager.create_user(username, password)

        if success:

            messagebox.showinfo("Thành công", message)

            self.show_login_screen()

        else:

            messagebox.showerror("Lỗi", message)



    def clear_window(self):

        for widget in self.root.winfo_children():

            widget.destroy()

    def show_main_window(self):
        self.clear_window()
        if self.current_user and 'username' in self.current_user:
            self.root.title("Quản Lý Thú Cưng - Đã đăng nhập: {}".format(self.current_user['username']))
        else:
            self.root.title("Quản Lý Thú Cưng")



        # Menu Bar

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label="Thoát", command=self.root.quit)

        menubar.add_cascade(label="Tệp", menu=file_menu)
        
        data_menu = tk.Menu(menubar, tearoff=0)
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'fetch_data'):
            data_menu.add_command(label="Thu thập dữ liệu", command=self.fetch_data_dialog)
        menubar.add_cascade(label="Dữ liệu", menu=data_menu)


        admin_menu = tk.Menu(menubar, tearoff=0)
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'manage_users'):
            admin_menu.add_command(label="Quản lý người dùng", command=self.show_user_management)
        menubar.add_cascade(label="Quản trị", menu=admin_menu)



        self.root.config(menu=menubar)



        # Main Frame

        main_frame = ttk.Frame(self.root, padding=10)

        main_frame.pack(expand=True, fill="both")



        # Pet List

        ttk.Label(main_frame, text="Danh sách thú cưng:").pack(pady=5)

        self.pet_list = tk.Listbox(main_frame, height=15, width=50)

        self.pet_list.pack(pady=5, padx=10, fill="both", expand=True)

        self.pet_list.bind('<<ListboxSelect>>', self.show_pet_details)



        # CRUD Buttons Frame

        crud_frame = ttk.Frame(main_frame)

        crud_frame.pack(pady=5)



        ttk.Button(crud_frame, text="Thêm mới", command=self.add_pet_dialog).pack(side="left", padx=5)

        ttk.Button(crud_frame, text="Sửa", command=self.edit_selected_pet).pack(side="left", padx=5)

        ttk.Button(crud_frame, text="Xóa", command=self.delete_selected_pet).pack(side="left", padx=5)



        # Details Frame

        details_frame = ttk.LabelFrame(main_frame, text="Chi tiết thú cưng")

        details_frame.pack(pady=10, padx=10, fill="x")



        self.details_labels = {}

        labels = ["Tên:", "Giống:", "Tuổi:", "Giới tính:"]

        for i, label_text in enumerate(labels):

            ttk.Label(details_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=2)

            detail_label = ttk.Label(details_frame, text="")

            detail_label.grid(row=i, column=1, sticky="w", padx=5, pady=2)

            self.details_labels[label_text.replace(":", "")] = detail_label



        self.update_pet_list()



    def update_pet_list(self):

        self.pet_list.delete(0, tk.END)

        pets = self.pet_manager.read_pets()

        for pet in pets:

            self.pet_list.insert(tk.END, f"{pet.get('name', 'Không tên')} ({pet.get('breed', 'Không rõ')}) - ID: {pet['id']}")

    def show_pet_details(self, event):

        selected_index = self.pet_list.curselection()

        if selected_index:

            selected_pet_index = selected_index[0]

            pets = self.pet_manager.read_pets()

            if 0 <= selected_pet_index < len(pets):

                selected_pet = pets[selected_pet_index]

                self.details_labels['Tên'].config(text=selected_pet.get('name', ''))

                self.details_labels['Giống'].config(text=selected_pet.get('breed', ''))

                self.details_labels['Tuổi'].config(text=selected_pet.get('age', ''))

                self.details_labels['Giới tính'].config(text=selected_pet.get('gender', ''))

            else:

                self.clear_pet_details()

        else:

            self.clear_pet_details()



    def clear_pet_details(self):

        for label in self.details_labels.values():

            label.config(text="")

    def add_pet_dialog(self):
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'create'):
            add_window = tk.Toplevel(self.root)
            add_window.title("Thêm Thú Cưng Mới")



            labels = ["Tên:", "Giống:", "Tuổi:", "Giới tính:"]

            entries = {}

            for i, label_text in enumerate(labels):

                ttk.Label(add_window, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")

                entry = ttk.Entry(add_window)

                entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

                entries[label_text.replace(":", "")] = entry



            def save_pet():

                pet_info = {key: entry.get() for key, entry in entries.items()}

                self.pet_manager.create_pet(pet_info)

                self.update_pet_list()

                add_window.destroy()



            save_button = ttk.Button(add_window, text="Lưu", command=save_pet)

            save_button.grid(row=len(labels), column=0, columnspan=2, padx=5, pady=10)

        else:

            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện hành động này.")

    def edit_selected_pet(self):
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'update'):
            selected_index = self.pet_list.curselection()

            if selected_index:

                selected_pet_index = selected_index[0]

                pets = self.pet_manager.read_pets()

                if 0 <= selected_pet_index < len(pets):

                    selected_pet = pets[selected_pet_index]

                    self.show_edit_pet_dialog(selected_pet)

                else:

                    messagebox.showerror("Lỗi", "Không tìm thấy thú cưng để sửa.")

            else:

                messagebox.showinfo("Thông báo", "Vui lòng chọn một thú cưng để sửa.")

        else:

            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện hành động này.")



    def show_edit_pet_dialog(self, pet):

        edit_window = tk.Toplevel(self.root)

        edit_window.title("Sửa Thông Tin Thú Cưng")



        labels = ["Tên:", "Giống:", "Tuổi:", "Giới tính:"]

        entries = {}

        for i, label_text in enumerate(labels):

            ttk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(edit_window)

            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

            entries[label_text.replace(":", "")] = entry

            entry.insert(0, pet.get(label_text.replace(":", ""), ''))



        def update_pet():

            updated_info = {key: entry.get() for key, entry in entries.items()}

            if self.pet_manager.update_pet(pet['id'], updated_info):

                self.update_pet_list()

                self.show_pet_details(None) # Cập nhật chi tiết sau khi sửa

                edit_window.destroy()

            else:

                messagebox.showerror("Lỗi", "Không thể cập nhật thông tin thú cưng.")



        update_button = ttk.Button(edit_window, text="Cập nhật", command=update_pet)

        update_button.grid(row=len(labels), column=0, columnspan=2, padx=5, pady=10)

    def delete_selected_pet(self):
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'delete'):
            selected_index = self.pet_list.curselection()

            if selected_index:

                selected_pet_index = selected_index[0]

                pets = self.pet_manager.read_pets()

                if 0 <= selected_pet_index < len(pets):

                    pet_id_to_delete = pets[selected_pet_index]['id']

                    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa thú cưng này?"):

                        if self.pet_manager.delete_pet(pet_id_to_delete):

                            messagebox.showinfo("Thông báo", "Đã xóa thú cưng thành công.")

                            self.update_pet_list()

                            self.clear_pet_details()

                        else:

                            messagebox.showerror("Lỗi", "Không tìm thấy thú cưng để xóa.")

                else:

                    messagebox.showerror("Lỗi", "Không tìm thấy thú cưng để xóa.")

            else:

                messagebox.showinfo("Thông báo", "Vui lòng chọn một thú cưng để xóa.")

        else:

            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện hành động này.")

    def fetch_data_dialog(self):
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'fetch_data'):
            fetch_window = tk.Toplevel(self.root)
            fetch_window.title("Thu thập dữ liệu")



            ttk.Label(fetch_window, text="Chọn nguồn dữ liệu:").pack(pady=5)



            def fetch_from_web_input():

                url = simpledialog.askstring("Nhập URL", "Nhập URL trang web:")

                if url:

                    if self.data_fetcher.fetch_pet_data_from_web(url):

                        self.update_pet_list()



            def fetch_from_api_input():

                api_url = simpledialog.askstring("Nhập URL API", "Nhập URL API:")

                if api_url:

                    if self.data_fetcher.fetch_pet_data_from_api(api_url):

                        self.update_pet_list()



            ttk.Button(fetch_window, text="Từ trang web", command=fetch_from_web_input).pack(pady=5)

            ttk.Button(fetch_window, text="Từ API", command=fetch_from_api_input).pack(pady=5)

        else:

            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện hành động này.")

    def show_user_management(self):
        if self.current_user and 'role' in self.current_user and self.user_manager.check_permission(self.current_user['role'], 'manage_users'):
            manage_window = tk.Toplevel(self.root)
            manage_window.title("Quản lý người dùng")



            # Hiển thị danh sách người dùng (đơn giản hóa)

            users = self.user_manager._load_users()

            user_list_label = ttk.Label(manage_window, text="Danh sách người dùng:")

            user_list_label.pack(pady=5)

            user_list_text = tk.Text(manage_window, height=10, width=40)

            user_list_text.pack(padx=10, pady=5)

            for user in users:

                user_list_text.insert(tk.END, f"Tên: {user['username']}, Vai trò: {user['role']}\n")

            user_list_text.config(state=tk.DISABLED)



            # Chức năng tạo người dùng mới (đơn giản hóa)

            create_user_frame = ttk.LabelFrame(manage_window, text="Tạo người dùng mới")

            create_user_frame.pack(padx=10, pady=10)



            ttk.Label(create_user_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

            new_username_entry = ttk.Entry(create_user_frame)

            new_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



            ttk.Label(create_user_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

            new_password_entry = ttk.Entry(create_user_frame, show="*")

            new_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



            ttk.Label(create_user_frame, text="Vai trò:").grid(row=2, column=0, padx=5, pady=5, sticky="w")

            role_combo = ttk.Combobox(create_user_frame, values=["user", "admin"])

            role_combo.set("user")

            role_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")



            def create_new_user():

                username = new_username_entry.get()

                password = new_password_entry.get()

                role = role_combo.get()

                success, message = self.user_manager.create_user(username, password, role)

                messagebox.showinfo("Thông báo", message)

                self.show_user_management() # Refresh user list



            create_button = ttk.Button(create_user_frame, text="Tạo", command=create_new_user)

            create_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)



        else:

            messagebox.showerror("Lỗi", "Bạn không có quyền truy cập chức năng này.")



if __name__ == "__main__":

    root = tk.Tk()

    app = PetApp(root)

    root.mainloop()
