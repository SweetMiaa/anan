from tkinter import Tk
from interface_adapters.data_repository import DataRepository
from use_cases.user_management import UserManagement
from use_cases.transaction_management import TransactionManagement
from frameworks_drivers.ui import AnanApp

if __name__ == "__main__":
    repository = DataRepository("data.json")
    user_management = UserManagement(repository)
    transaction_management = TransactionManagement(repository)

    root = Tk()
    app = AnanApp(root, user_management, transaction_management)
    root.mainloop()
