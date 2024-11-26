from entities.user import User


class UserManagement:
    def __init__(self, repository):
        self.repository = repository

    def register(self, username: str, password: str, is_admin: bool = False):
        if self.repository.get_user(username):
            raise ValueError("User already exists!")
        new_user = User(username, password, is_admin)
        self.repository.save_user(new_user)

    def login(self, username: str, password: str):
        user = self.repository.get_user(username)
        if user and user.password == password:
            return user
        raise ValueError("Invalid credentials!")

    def update_password(self, username: str, old_password: str, new_password: str):
        user = self.login(username, old_password)
        user.update_password(new_password)
        self.repository.save_user(user)
