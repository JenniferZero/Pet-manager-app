import json
import hashlib
import os


class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self._load_users()
        self._ensure_all_passwords_hashed()

    def _load_users(self):
        try:
            if not os.path.exists(self.filename):
                return []
                
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Lỗi khi đọc file người dùng: {e}")
            return []

    def _save_users(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu người dùng: {e}")

    def _is_password_hashed(self, password):
        # Kiểm tra xem mật khẩu đã được hash chưa
        # SHA-256 tạo ra một chuỗi hex 64 ký tự
        return len(password) == 64 and all(c in "0123456789abcdef" for c in password.lower())

    def _ensure_all_passwords_hashed(self):
        need_save = False
        for user in self.users:
            if not self._is_password_hashed(user["password"]):
                user["password"] = hashlib.sha256(user["password"].encode()).hexdigest()
                need_save = True
                print(f"Đã hash mật khẩu cho người dùng: {user['username']}")
        
        if need_save:
            self._save_users()

    def create_user(self, username, password, role="user"):
        if not username or not password:
            return False, "Tên người dùng và mật khẩu không được để trống."
            
        if any(user["username"] == username for user in self.users):
            return False, "Tên người dùng đã tồn tại."
            
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users.append({"username": username, "password": hashed_password, "role": role})
        self._save_users()
        return True, "Tạo tài khoản thành công."

    def authenticate_user(self, username, password):
        if not username or not password:
            return None
            
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        for user in self.users:
            if user["username"] == username:
                if not self._is_password_hashed(user["password"]):
                    # Trường hợp đặc biệt: mật khẩu chưa hash trong database
                    if user["password"] == password:
                        # Cập nhật thành mật khẩu đã hash
                        user["password"] = hashed_password
                        self._save_users()
                        return user
                elif user["password"] == hashed_password:
                    return user
                    
        return None

    def get_user_role(self, username):
        for user in self.users:
            if user["username"] == username:
                return user.get("role", "user")
        return None

    def check_permission(self, user_role, required_permission):
        permissions = {
            "admin": ["create", "read", "update", "delete", "manage_users", "fetch_data"],
            "user": ["read", "create", "update"]  # Mở rộng quyền cho người dùng thông thường
        }
        return required_permission in permissions.get(user_role, [])
