import json
import uuid
import os

class PetManager:
    def __init__(self, filename="pets.json"):
        self.filename = filename
        self.pets = self._load_data()

    def _load_data(self):
        try:
            if not os.path.exists(self.filename):
                return []
                
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Lỗi khi đọc file dữ liệu: {e}")
            return []

    def _save_data(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.pets, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")

    def create_pet(self, pet_info):
        pet_id = str(uuid.uuid4())
        pet_info['id'] = pet_id
        self.pets.append(pet_info)
        self._save_data()
        return pet_id

    def read_pets(self):
        # Đảm bảo dữ liệu luôn mới nhất
        self.pets = self._load_data()
        return self.pets

    def update_pet(self, pet_id, updated_info):
        for pet in self.pets:
            if pet['id'] == pet_id:
                pet.update(updated_info)
                self._save_data()
                return True
        return False

    def delete_pet(self, pet_id):
        initial_len = len(self.pets)
        self.pets = [pet for pet in self.pets if pet['id'] != pet_id]
        if len(self.pets) < initial_len:
            self._save_data()
            return True
        return False

    def get_pet(self, pet_id):
        for pet in self.pets:
            if pet['id'] == pet_id:
                return pet
        return None
