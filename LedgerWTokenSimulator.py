import time
import hashlib
from collections import defaultdict

class Ledger:
    def __init__(self, initial_tokens, num_accounts=5):
        self.tokens = [self.hash_value(i) for i in range(1, initial_tokens + 1)]
        self.fund = 0
        self.total_transferred = 0
        self.total_added = 0
        self.total_transactions = 0
        self.accounts = defaultdict(list)
        self.num_accounts = num_accounts

    def hash_value(self, value):
        return hashlib.sha256(str(value).encode()).hexdigest()

    def transfer_tokens(self, amount):
        for _ in range(amount):
            if self.tokens:
                token = self.tokens.pop(0)
                self.fund += 1
                self.total_transferred += 1
                self.total_transactions += 1
                account_id = self.total_transferred % self.num_accounts
                self.accounts[account_id].append(token)
                print(f"Transferred token {token} to account {account_id}")

    def add_tokens(self, amount):
        for _ in range(amount):
            token = self.hash_value(self.total_added + 1)
            self.tokens.append(token)
            self.total_added += 1
            self.total_transactions += 1
            print(f"Added token {token}")

    def simulate(self):
        three_second_interval = 3
        five_second_interval = 5
        last_three_second_time = time.time()
        last_five_second_time = time.time()

        while self.total_transactions < 500:
            current_time = time.time()

            if current_time - last_three_second_time >= three_second_interval:
                if len(self.tokens) >= 20:
                    remaining_to_500 = 500 - self.total_transactions
                    transfer_amount = min(20, remaining_to_500)
                    self.transfer_tokens(transfer_amount)
                    print(f"{time.strftime('%X')}: Ledger: {len(self.tokens)} tokens, Fund: {self.fund}, Total Transferred: {self.total_transferred}, Total Added: {self.total_added}, Total Transactions: {self.total_transactions}")
                last_three_second_time = current_time

            if self.total_transactions >= 500:
                break

            if current_time - last_five_second_time >= five_second_interval:
                remaining_to_500 = 500 - self.total_transactions
                add_amount = min(60, remaining_to_500)
                self.add_tokens(add_amount)
                print(f"{time.strftime('%X')}: Ledger: {len(self.tokens)} tokens, Fund: {self.fund}, Total Transferred: {self.total_transferred}, Total Added: {self.total_added}, Total Transactions: {self.total_transactions}")
                last_five_second_time = current_time

            if self.total_transactions >= 500:
                break

            time.sleep(1)

        print("Simulation complete. Final state:")
        print(f"Ledger: {len(self.tokens)} tokens, Fund: {self.fund}, Total Transferred: {self.total_transferred}, Total Added: {self.total_added}, Total Transactions: {self.total_transactions}")
        for account, tokens in self.accounts.items():
            print(f"Account {account}: {len(tokens)} tokens")

if __name__ == "__main__":
    ledger = Ledger(100)
    ledger.simulate()