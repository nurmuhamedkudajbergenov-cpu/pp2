class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        self.balance -= amount
        return self.balance

B, W = map(int, input().split())
acc = Account("User", B)
print(acc.withdraw(W))