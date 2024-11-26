from entities.transaction import Transaction


class TransactionManagement:
    def __init__(self, repository):
        self.repository = repository

    def add_balance_with_consent(self, requestor_username: str, supervisor_username: str, supervisor_password: str, amount: int):
        requestor = self.repository.get_user(requestor_username)
        supervisor = self.repository.get_user(supervisor_username)

        if requestor.username == supervisor.username:
            raise ValueError("Must be another person")

        if supervisor.password != supervisor_password:
            raise ValueError("Supervisor authentication failed!")
        if not requestor:
            raise ValueError("Requestor not found!")
        if not supervisor:
            raise ValueError("Supervisor not found!")
        requestor.balance += amount
        self.repository.save_user(requestor)

    def transfer(self, from_user: str, password: str, to_user: str, amount: int):
        sender = self.repository.get_user(from_user)
        receiver = self.repository.get_user(to_user)

        if not sender or sender.password != password:
            raise ValueError("Sender authentication failed!")
        if not receiver:
            raise ValueError("Receiver not found!")
        if sender.balance < amount:
            raise ValueError("Insufficient balance!")

        sender.balance -= amount
        receiver.balance += amount

        transaction = Transaction(from_user, to_user, amount, "Transfer")
        sender.add_transaction(transaction)
        receiver.add_transaction(transaction)

        self.repository.save_user(sender)
        self.repository.save_user(receiver)

    def consume_anan(self, username: str, password: str, amount: int, description: str = "Consumption"):
        user = self.repository.get_user(username)

        if not user or user.password != password:
            raise ValueError("Authentication failed!")

        if user.balance < amount:
            raise ValueError("Insufficient balance!")

        user.balance -= amount

        self.repository.save_user(user)

