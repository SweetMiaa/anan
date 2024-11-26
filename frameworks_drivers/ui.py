import tkinter as tk
from tkinter import messagebox
from use_cases.user_management import UserManagement
from use_cases.transaction_management import TransactionManagement


class AnanApp:
    def __init__(self, root, user_management, transaction_management):
        self.root = root
        self.user_management = user_management
        self.transaction_management = transaction_management
        self.current_user = None
        self.root.title("Anan Management")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Anan Management", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)

    def create_user_dashboard(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {self.current_user}!", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="View Balance", command=self.view_balance).pack(pady=5)
        tk.Button(self.root, text="Add Balance with Consent", command=self.add_balance_with_consent).pack(pady=5)
        tk.Button(self.root, text="Consume Anan", command=self.consume_anan).pack(pady=5)
        tk.Button(self.root, text="Transfer Anan", command=self.transfer_anan).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            user = self.user_management.login(username, password)
            self.current_user = user.username
            self.create_user_dashboard()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.user_management.register(username, password)
            messagebox.showinfo("Registration Successful", "You can now log in!")
        except ValueError as e:
            messagebox.showerror("Registration Failed", str(e))

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def view_balance(self):
        user = self.user_management.repository.get_user(self.current_user)
        messagebox.showinfo("Balance", f"Your balance is: {user.balance} anan")

    def add_balance_with_consent(self):
        def confirm_add_balance():
            requestor_username = self.current_user
            target_username = superviser_entry.get()
            target_password = target_password_entry.get()
            amount = int(amount_entry.get())

            try:
                self.transaction_management.add_balance_with_consent(
                    self.current_user, target_username, target_password, amount
                )
                messagebox.showinfo("Success", f"{amount} anan added to {requestor_username}'s account with supervisor's consent.")
                add_balance_window.destroy()
            except ValueError as e:
                messagebox.showerror("Failed", str(e))

        add_balance_window = tk.Toplevel(self.root)
        add_balance_window.title("Add Balance with Consent")

        tk.Label(add_balance_window, text="Supervisor Username:").pack()
        superviser_entry = tk.Entry(add_balance_window)
        superviser_entry.pack()

        tk.Label(add_balance_window, text="Supervisor Password:").pack()
        target_password_entry = tk.Entry(add_balance_window, show="*")
        target_password_entry.pack()

        tk.Label(add_balance_window, text="Amount to Add:").pack()
        amount_entry = tk.Entry(add_balance_window)
        amount_entry.pack()

        tk.Button(add_balance_window, text="Confirm", command=confirm_add_balance).pack()

    def transfer_anan(self):
        def confirm_transfer():
            to_user = recipient_entry.get()
            amount = int(amount_entry.get())
            password = sender_password_entry.get()
            try:
                self.transaction_management.transfer(self.current_user, password, to_user, amount)
                messagebox.showinfo("Success", f"{amount} anan transferred to {to_user}.")
                transfer_window.destroy()
            except ValueError as e:
                messagebox.showerror("Transfer Failed", str(e))

        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transfer Anan")

        tk.Label(transfer_window, text="Recipient Username:").pack()
        recipient_entry = tk.Entry(transfer_window)
        recipient_entry.pack()

        tk.Label(transfer_window, text="Amount:").pack()
        amount_entry = tk.Entry(transfer_window)
        amount_entry.pack()

        tk.Label(transfer_window, text="Your Password:").pack()
        sender_password_entry = tk.Entry(transfer_window, show="*")
        sender_password_entry.pack()

        tk.Button(transfer_window, text="Transfer", command=confirm_transfer).pack()

    def consume_anan(self):
        def confirm_consume():
            amount = int(amount_entry.get())
            password = password_entry.get()

            try:
                self.transaction_management.consume_anan(self.current_user, password, amount)
                messagebox.showinfo("Success", f"{amount} anan has been consumed.")
                consume_window.destroy()
            except ValueError as e:
                messagebox.showerror("Failed", str(e))

        consume_window = tk.Toplevel(self.root)
        consume_window.title("Consume Anan")

        tk.Label(consume_window, text="Enter amount to consume:").pack()
        amount_entry = tk.Entry(consume_window)
        amount_entry.pack()

        tk.Label(consume_window, text="Enter your password:").pack()
        password_entry = tk.Entry(consume_window, show="*")
        password_entry.pack()

        tk.Button(consume_window, text="Confirm", command=confirm_consume).pack()
