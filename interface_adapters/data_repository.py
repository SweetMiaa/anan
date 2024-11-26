import json
from entities.user import User

class DataRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read_data(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"Warning: {self.file_path} is corrupted. Resetting data.")
            return {}

    def _write_data(self, data):
        temp_file_path = self.file_path + ".tmp"
        with open(temp_file_path, "w") as f:
            json.dump(data, f, indent=4)
        import os
        os.replace(temp_file_path, self.file_path)

    def get_user(self, username: str):
        data = self._read_data()
        if username in data:
            return User.from_dict(data[username])
        return None

    def save_user(self, user: User):
        # 调用 to_dict 方法序列化 User 对象
        data = self._read_data()
        data[user.username] = user.to_dict()
        self._write_data(data)
