import random
import time

class MarketMaking:
    def __init__(self, difficulty, balance=500):
        self.difficulty = difficulty
        self.balance = balance

        if self.difficulty == "easy" or self.difficulty == "medium":
            self.n = 3
        elif self.difficulty == "hard":
            self.n = 4
        else:
            raise ValueError("Invalid input. Please set difficulty as 'easy', 'medium', or 'hard'.")

        print(f"Initial balance: {self.balance}")

        print("")
        print("-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print("")

    def generate_cards(self):
        self.lower = random.randint(0, 10)
        self.upper = random.randint(15, 25)

        print(f"Asset value: {self.lower} - {self.upper}")

        self.cards = []
        for i in range(self.n):
            card = random.randint(self.lower, self.upper)
            if card < self.upper and self.difficulty == "medium":
                card += 0 if random.random() < 0.5 else 0.5
            elif card < self.upper and self.difficulty == "hard":
                card += round(random.random(), 1)

            self.cards.append(card)
        return self.cards

    def generate_question(self, chance=0.3):
        res = ""
        shown = 0
        for i in range(self.n):
            if random.random() < chance and shown < 2:
                res += str(self.cards[i]) + "   "
                shown += 1
            else:
                res += "?   "
        print(res)

        middle = random.randint(self.n * self.lower + 1, self.n * self.upper - 1)
        self.ask = middle + 1
        self.bid = middle - 1

        print(f"Bid: {self.bid}, Ask: {self.ask}")

    def get_response(self):
        start = time.time()
        correct = True

        while True:
            try:
                quantity = float(input("Quantity: "))
                if quantity < 0:
                    print("Invalid input. Please enter a positive number.")
                    continue
                side = input("Side: ")
                if side == "buy" or side == "sell":
                    break;
                print("Invalid input. Please enter either 'buy' or 'sell'.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        if side == "buy":
            if quantity * self.ask > self.balance:
                print(f"Buy limit exceeded, -50 penalty")
                self.balance -= 50
            else:
                actual = sum(self.cards)
                difference = quantity * actual - quantity * self.ask
                self.balance += difference
                print(f"Actual: {self.cards}")
                while True:
                    try:
                        balance = float(input("Balance: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                if (balance != self.balance):
                    print(f"Incorrect balance calculation, -50 penalty")
                    self.balance -= 50
                    correct = False
                print(f"PnL: {difference}, Balance: {self.balance}")
        elif side == "sell":
            if quantity * (self.upper - self.bid) > self.balance:
                print(f"Sell limit exceeded, -50 penalty")
                self.balance -= 50
            else:
                actual = sum(self.cards)
                difference = quantity * self.bid - quantity * actual
                self.balance += difference
                print(f"Actual: {self.cards}")
                while True:
                    try:
                        balance = float(input("Balance: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                if (balance != self.balance):
                    print(f"Incorrect balance calculation, -50 penalty")
                    self.balance -= 50
                    correct = False
                print(f"PnL: {difference}, Balance: {self.balance}")

        end = time.time()
        time_taken = end - start
        print(f"Time taken: {time_taken:.2f} seconds")

        print("")
        print("-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print("")

        return time_taken, correct

    def play(self, rounds=None):
        if rounds == None:
            if self.difficulty == "easy":
                rounds = 3
            elif self.difficulty == "medium":
                rounds = 5
            else:
                rounds = 10

        total_time = 0
        correct_response = 0
        for i in range(rounds):
            self.generate_cards()
            self.generate_question()
            time_taken, correct = self.get_response()
            total_time += time_taken
            correct_response += correct

        average_time = total_time / rounds
        print(f"Average time taken: {average_time:.2f} seconds")
        print(f"Correct Responses: {correct_response} / {rounds}")

        with open('stats.txt', 'a') as file:
            file.write(f"Game difficulty: {self.difficulty}\n")
            file.write(f"Average time taken: {average_time:.2f} seconds\n")
            file.write(f"Correct Responses: {correct_response} / {rounds}\n\n")



if __name__ == "__main__":
    marketmaking = MarketMaking("hard")
    marketmaking.play()
