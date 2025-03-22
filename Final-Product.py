import csv
import hashlib
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
USER_FILE = "users.csv"
TRANS = "transaction.csv"

class User:
    #do not forget this has dunder scores
    def __init__(self, username, user_id, password, balance):
        self.username = username
        self.user_id = user_id
        self.password = password
        self.__balance = float(balance)

    @property
    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount
        with open(USER_FILE, "r") as f:
            user = list(csv.reader(f))
        for row in user:
            if row and row[1] == self.user_id:
                row[7] = float(self.__balance)
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(user)
        with open(TRANS, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    self.username,
                    self.user_id,
                    None,
                    None,
                    "Deposit",
                    amount,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                ]
            )
        return self.__balance

    def withdraw(self, amount):
        self.__balance = float(self.__balance)
        if amount > self.__balance:
            return "Insufficient funds"
        self.__balance -= amount
        with open(USER_FILE, "r") as f:
            user = list(csv.reader(f))
        for row in user:
            if row and row[1] == self.user_id:
                row[7] = float(self.__balance)
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(user)
        with open(TRANS, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    self.username,
                    self.user_id,
                    None,
                    None,
                    "Withdraw",
                    amount,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                ]
            )
        return self.__balance

    def updated_balance(self):
        with open(USER_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[1] == self.user_id:
                    self.__balance = float(row[7])

def generate_user_id():
    return os.urandom(4).hex()

def pwd(self):
    return self.__password

def verify(user_id, password):
    with open(USER_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == user_id:
                return (
                    hashlib.sha256((password + row[3]).encode()).hexdigest() == row[2]
                )
    return False

def transfer(sender_id, sender_password, receiver_id, amount):
    users = []
    sender_found = False
    receiver_found = False
    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            if row and row[1] == sender_id:
                if verify(sender_id, sender_password):
                    sender_found = True
                    sender_name = row[0]
                    sender_balance = float(row[7])
                    if sender_balance < amount:
                        return "❌ Insufficient funds."
                    sender_new_balance = sender_balance - amount
                    row[7] = float(sender_new_balance)
                else:
                    return "❌ Incorrect password."

            if row and row[1] == receiver_id:
                receiver_found = True
                receiver_name = row[0]
                row[7] = str(float(row[7]) + amount)
            users.append(row)
    if not sender_found:
        return "❌ Sender account not found."
    if not receiver_found:
        return "❌ Receiver account not found."
    with open(USER_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(users)
    with open(TRANS, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                sender_name,
                sender_id,
                receiver_name,
                receiver_id,
                "Transfer",
                amount,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
            ]
        )
    return "✅ Transfer successful."

def file_exists():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Username",
                    "User_id",
                    "Password",
                    "Salt",
                    "Sex",
                    "DOB",
                    "Current_Status",
                    "Balance",
                ]
            )
    if not os.path.exists(TRANS):
        with open(TRANS, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Sender_name",
                    "Sender_id",
                    "Receiver_name",
                    "Receiver_id",
                    "Transaction_type",
                    "Amount($)",
                    "Date",
                ]
            )

def is_valid_password(password):
    return password.isdigit() and len(password) == 4

def check_pwd(password):
    if password.isdigit() and len(password) == 4:
        return True

def view_trans_history(user_id):
    with open(TRANS, "r") as f:
        reader = csv.reader(f)
        transactions = [
            row for row in reader if row and (row[1] == user_id or row[2] == user_id)
        ]
    return transactions

def hash_password(password, salt):
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed

def register_user(username, password, sex, dob, current_status, balance):
    file_exists()
    with open(USER_FILE, "r", newline="") as f:
        reader = csv.reader(f)
    user_id = generate_user_id()
    salt = os.urandom(16).hex()
    hashed_password = hash_password(password, salt)
    with open(USER_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                username,
                user_id,
                hashed_password,
                salt,
                sex,
                dob,
                current_status,
                balance,
            ]
        )
    return f"User registered successfully! Your User ID: {user_id} 🫰 🫰"

def login_user(username, user_id, password):
    file_exists()
    with open(USER_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == username and row[1] == user_id:
                stored_hash = row[2]
                salt = row[3]
                attempts = 1
                while attempts < 3:
                    if hash_password(password, salt) == stored_hash:
                        print("login successful!!")
                        return User(row[0], row[1], row[2], row[7])
                    else:
                        print("❌ Invalid password. Password must be 4 digits.")
                        password = input("Enter password: ")
                        attempts += 1
                print("❌ Too many invalid attempts. Exiting...")
                return None
        print("❌Invalid username or user_id")
        return None

def check_dob():
    while True:
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        try:
            return datetime.strptime(
                dob, "%Y-%m-%d"
            ).date()  # user .date() because we want only YYYY-MM-DD
        except ValueError:
            print("Invalid date of birth. Please try again.")

def show_all_transaction(user_id):
    df = pd.read_csv(TRANS)
    df["Date"] = pd.to_datetime(df["Date"])
    today = pd.to_datetime("today")

    while True:
        print("Choose time range to display transactions:")
        print("1. Last 1 week")
        print("2. Last 1 month")
        print("3. Last 3 months")
        print("4. Last 6 months")
        choice = input("Enter choice (1-4): ")

        if choice == "1":
            start_date = today - timedelta(weeks=1)
            period_name = "Last 1 week"
            break
        elif choice == "2":
            start_date = today - timedelta(days=30)
            period_name = "Last 1 month"
            break
        elif choice == "3":
            start_date = today - timedelta(days=90)
            period_name = "Last 3 months"
            break
        elif choice == "4":
            start_date = today - timedelta(days=180)
            period_name = "Last 6 months"
            break
        else:
            print("Invalid choice. Please choose options between 1 and 4.")

    filtered_df = df[
        (df["Date"] >= start_date)
        & (
            (df["Sender_id"].astype(str) == user_id)
            | (df["Receiver_id"].astype(str) == user_id)
        )
    ]
    filtered_df["Transaction_Category"] = filtered_df["Transaction_type"]
    filtered_df.loc[
        filtered_df["Sender_id"].astype(str) == user_id, "Transaction_Category"
    ] = "Transfer Out"
    filtered_df.loc[
        filtered_df["Receiver_id"].astype(str) == user_id, "Transaction_Category"
    ] = "Transfer In"
    filtered_df.loc[
        filtered_df["Transaction_type"] == "Withdraw", "Transaction_Category"
    ] = "Withdraw"
    filtered_df.loc[
        filtered_df["Transaction_type"] == "Deposit", "Transaction_Category"
    ] = "Deposit"
    groupby_df = filtered_df.groupby("Transaction_Category")["Amount($)"].sum()

    print(f"\nTotal amounts for {period_name}:")
    for category, amount in groupby_df.items():
        print(f"{category}: ${amount}")

    plt.figure(figsize=(7, 7))
    plt.pie(
        groupby_df,
        labels=groupby_df.index,
        autopct="%1.1f%%",
        startangle=140,
        textprops=dict(color="black"),
    )

    plt.title(f"Transaction Breakdown for {period_name}")
    plt.show()

#correct this one
def trans_data():
    df = pd.read_csv(TRANS)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    today = pd.to_datetime("today").date()
    start_date = today - timedelta(days=7)

    while True:
        user_id = input("Enter user ID to view transaction history: ")
        if user_id not in df["Receiver_id"].astype(str).values and user_id not in df["Sender_id"].astype(str).values:
            print("User ID not in transaction history or Invalid")
        else:
            break

    while True: 
        print("Choose option to display your data in last 1 week: ")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer in")
        print("4. Transfer out")
        print("5. All transaction as pie chart")
        trans_opt = input("Enter your choices(1-4): ")
        if trans_opt == "1":
            filtered_df = df[(df["Date"] >= start_date) & (df["Transaction_type"] == "Deposit") & (df["Sender_id"].astype(str) == user_id)]
            Trans_category = "Deposit"
            break
        elif trans_opt == "2":
            filtered_df = df[(df["Date"] >= start_date) & (df["Transaction_type"] == "Withdraw") & (df["Sender_id"].astype(str) == user_id)]
            Trans_category = "Withdraw"
            break
        elif trans_opt == "3":
            filtered_df = df[(df["Date"] >= start_date) & (df["Receiver_id"].astype(str) == user_id)]
            Trans_category = "Transfer In"
            break
        elif trans_opt == "4":
            filtered_df = df[(df["Date"] >= start_date) & (df["Sender_id"].astype(str) == user_id)]
            Trans_category = "Transfer Out"
            break
        elif trans_opt == "5":
            show_all_transaction(user_id)
            break
        else:
            print("Invalid option. Please enter number in range(1-4).")

        if filtered_df.empty:
            print("No transactions found in the last 7 days.")
            return

        daily_totals = filtered_df.groupby(["Date"])["Amount($)"].sum()
        date_range = pd.date_range(start=start_date, end=today).date
        daily_totals = daily_totals.reindex(date_range, fill_value=0)

        plt.figure(figsize=(10, 5))
        bars = daily_totals.plot(kind="bar", color="skyblue", edgecolor="black")
        plt.xlabel("Date")
        plt.ylabel("Total Amount ($)")
        plt.title(f"{Trans_category} Transactions (Last 7 Days) for User ID {user_id}")
        plt.xticks(rotation=0)
        for bar in bars.patches:
            plt.text(bar.get_x() + bar.get_width() / 2, 
                    bar.get_height(), 
                    f"${bar.get_height():.2f}", 
                    ha="center", va="bottom", fontsize=10)
        plt.show()

def show_data_user():
    df = pd.read_csv(USER_FILE)
    counter = df["Current_Status"].value_counts()
    print(counter)
    # to count
    plt.figure(figsize=(6, 6))  # Set figure size (width=6, height=6 inches)
    plt.pie(counter, labels=counter.index, autopct="%1.1f%%", startangle=90)
    plt.title("User Status Distribution")  # Set title
    plt.show()

def view_inc_exsp():
    df = pd.read_csv(TRANS)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    today = datetime.today().date()
    start_date = today - timedelta(days=6)  # Last 7 days including today

    while True:
        user_id = input("Enter user ID to view transaction history: ")
        if user_id not in df["Sender_id"].astype(str).values and user_id not in df["Receiver_id"].astype(str).values:
            print("User ID not found in transaction history. Try again.")
        else:
            break

    filtered_df = df[(df["Date"] >= start_date) & 
                     ((df["Sender_id"].astype(str) == user_id) | (df["Receiver_id"].astype(str) == user_id))]

    filtered_df["Transaction_Category"] = "Spent"  # Default to Spent
    filtered_df.loc[filtered_df["Receiver_id"].astype(str) == user_id, "Transaction_Category"] = "Income"
    filtered_df.loc[(filtered_df["Transaction_type"] == "Withdraw") & 
                    (filtered_df["Sender_id"].astype(str) == user_id), "Transaction_Category"] = "Spent"
    filtered_df.loc[(filtered_df["Transaction_type"] == "Deposit") & 
                    (filtered_df["Receiver_id"].astype(str) == user_id), "Transaction_Category"] = "Income"

    grouped_df = filtered_df.groupby(["Date", "Transaction_Category"])["Amount($)"].sum().unstack(fill_value=0)
    print(grouped_df)

    date_range = [start_date + timedelta(days=i) for i in range(7)]
    grouped_df = grouped_df.reindex(date_range, fill_value=0)

    grouped_df.plot(kind='bar', color=['green', 'red'])
    plt.title(f"Income vs Expense for User {user_id} (Last 7 Days)")
    plt.xlabel("Date")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)
    plt.show()
#another one 
if __name__ == "__main__":
    while True:
        print("\n1. Register\n2. Login\n3. Analyze Transaction\n4. User Data\n5. View total Income and Expense this weeks\n6. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            username = input("Enter Username: ")
            password = input("Enter password(4 Digits): ")
            while not check_pwd(password):
                print("❌ Invalid password. Password must be 4 digits.")
                password = input("Enter password: ")
            while True:
                sex = input("Enter gender (M/F): ").strip().upper()
                if sex in ["M", "F"]:
                    break
                print("❌ Invalid input. Please enter M or F !!!")
            dob = check_dob()
            status = ["1.Student", "2.Employee", "3.Merchant", "4.Others"]
            print(status)
            current_status = int(input("Enter the your current status (1-4): "))
            try:
                current_status = status[int(current_status) - 1]
                print(f"Your current status is: {current_status}")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number between 1 and 4.")
                current_status = int(input("Enter the your current status : "))
            while True:
                balance_input = input("Enter your first deposit amount: ").strip()
                if not balance_input.isnumeric():
                    print("❌ Warning: Only number allow !!")
                    continue
                balance = float(balance_input)
                if balance < 0:
                    print("❌ Balance cannot be negative.Please enter again.")
                else:
                    break
            result = register_user(
                username, password, sex, dob, current_status, balance
            )
            print(result)
        elif choice == "2":
            username = input("Enter username: ")
            user_id = input("Enter user ID: ")
            password = input("Enter password: ")
            user = login_user(username, user_id, password)
            if user is not None:
                while True:
                    print(  
                        "\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer\n5. View Transaction\n6. Log Out"
                    )
                    option = input("Choose an option: ")
                    if option == "1":
                        while True:
                            try:
                                amount = float(input("Enter amount you want to deposit: "))
                                user.deposit(amount)
                                break
                            except ValueError as e:
                                print(f"{e}")
                    elif option == "2":
                        while True:
                            try:
                                amount = float(input("Enter amount you want to withdraw: "))
                                user.withdraw(amount)
                                break
                            except ValueError as e:
                                print(f"{e}")
                    elif option == "3":
                        print(f"Your current balance is: {user.get_balance}")
                    elif option == "4":
                        while True:
                            try:
                                receiver_id = input("Enter receiver ID: ")
                                amount = float(input("Enter amount you want to transfer: "))
                                transfer(user_id, password, receiver_id, amount)
                                user.updated_balance()
                                break
                            except ValueError as e:
                                print(f"{e}")
                    elif option == "5":
                        transactions = view_trans_history(user_id)
                        for i in transactions:
                            print(i)
                    elif option == "6":
                        print("Logging out...")
                        break
                    else:
                        print("❌ Invalid choice. Try again.")
                        continue
        elif choice == "3":
            trans_data()
        elif choice == "4":	
            show_data_user()
        elif choice == "5":
            view_inc_exsp()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.") 
